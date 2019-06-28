#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
import base64
import hashlib
from threading import Thread
import threading 
import sys
import operator
import logging
import logging.handlers
#接收连接池
g_conn_pool = []  
#控制端地址
k_conn_pool =()
#线程池
thread_list =[]

#日志配置
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)

#handler = logging.FileHandler("log.txt",encoding='utf-8')
# 添加TimedRotatingFileHandler
# 定义一个1天换一次log文件的handler
# 保留3个旧log文件
handler = logging.handlers.TimedRotatingFileHandler(filename="log.log",when='D',interval=1,backupCount=3,encoding='utf-8')



handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger.addHandler(handler)
logger.addHandler(console)

def get_headers(data):
    """
    将请求头格式化成字典
    :param data:
    :return:
    """
    header_dict = {}
    data = str(data, encoding='utf-8')
 
    header, body = data.split('\r\n\r\n', 1)
    header_list = header.split('\r\n')
    for i in range(0, len(header_list)):
        if i == 0:
            if len(header_list[i].split(' ')) == 3:
                header_dict['method'], header_dict['url'], header_dict['protocol'] = header_list[i].split(' ')
        else:
            k, v = header_list[i].split(':', 1)
            header_dict[k] = v.strip()
    return header_dict
 
 
def send_msg(conn,address, msg_bytes):
    """
    WebSocket服务端向客户端发送消息
    :param conn: 客户端连接到服务器端的socket对象,即： conn,address = socket.accept()
    :param msg_bytes: 向客户端发送的字节
    :return:
    """
    import struct
    global g_conn_pool,k_conn_pool
    token = b"\x81"
    length = len(msg_bytes)
    if length < 126:
        token += struct.pack("B", length)
    elif length <= 0xFFFF:
        token += struct.pack("!BH", 126, length)
    else:
        token += struct.pack("!BQ", 127, length)
 
    msg = token + msg_bytes
    #logger.info(k_conn_pool,address)

    #判断是否为控制端传递信息，是的话分发给所有连接
    if(operator.eq(k_conn_pool,address)):
        logger.info("======================传递参数")
        logger.info(len(g_conn_pool))
        #定义一个空数组，用于保存还存活的连接
        cur_g_conn_pool=[]
        for i in range(len(g_conn_pool)):
            
            
            try:
                #向连接池中的所有传递信息（包括控制端和接收端）
                g_conn_pool[i].send(msg)
            except Exception as e:
                logger.debug(repr(e))
                logger.info("{}:已断开连接".format(g_conn_pool[i].getpeername()))
                #打印当前存活线程
                thread_log(thread_list)
                
            else:
                #保存存活的连接
                cur_g_conn_pool.append(g_conn_pool[i])
                logger.info("{}成功向{}传递 ==>{} ".format(address,g_conn_pool[i].getpeername(), msg_bytes.decode("UTF-8","ignore")))
        #更新接收连接池
        g_conn_pool=cur_g_conn_pool
        logger.info("======================传递参数结束")        
    #给自身回传信息
    conn.send(msg)
    return True


#等待接收客户
def wait_client(sock):
    global g_conn_pool
    # 新开一个线程，用于接收新连接
    while True:
        conn, address = sock.accept()
        data = conn.recv(1024)
        headers = get_headers(data)
        response_tpl = "HTTP/1.1 101 Switching Protocols\r\n" \
                   "Upgrade:websocket\r\n" \
                   "Connection:Upgrade\r\n" \
                   "Sec-WebSocket-Accept:%s\r\n" \
                   "WebSocket-Location:ws://%s%s\r\n\r\n"
 
        value = headers['Sec-WebSocket-Key'] + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        ac = base64.b64encode(hashlib.sha1(value.encode('utf-8')).digest())
        response_str = response_tpl % (ac.decode('utf-8'), headers['Host'], headers['url'])
        conn.send(bytes(response_str, encoding='utf-8'))
        #将新连接添加到连接池
        g_conn_pool.append(conn)
        #新建线程处理连接
        newthread_(conn,address)

#消息处理
def accept_client(conn, address):
    global k_conn_pool,thread_list
    
    
 
    while True:
        try:
            info = conn.recv(8096)
        except Exception as e:
            info = None
        if not info:
            logger.info('info没接收到信息，退出监听循环')
            break
        #logger.info("info ==> ",info)
        payload_len = info[1] & 127
        if payload_len == 126:
            extend_payload_len = info[2:4]
            mask = info[4:8]
            decoded = info[8:]
        elif payload_len == 127:
            extend_payload_len = info[2:10]
            mask = info[10:14]
            decoded = info[14:]
        else:
            extend_payload_len = None
            mask = info[2:6]
            decoded = info[6:]
 
        bytes_list = bytearray()
        for i in range(len(decoded)):
            chunk = decoded[i] ^ mask[i % 4]
            bytes_list.append(chunk)
        
        try:
            #logger.info('解析到参数：',bytes_list)
            body = str(bytes_list, encoding='utf-8')
            logger.info('接收参数：{}'.format(body))
            

            #保存控制端地址
            if(body == '控制端'):
                k_conn_pool=address
                logger.info("控制端地址:{}".format(k_conn_pool))


            if(body != '控制端' and body != '接收端'):
                #logger.info("传递参数:{}".format(body))
                send_msg(conn,address,body.encode('utf-8'))
            else:
                logger.info("{}连接成功".format(address))
            
        except Exception as e:
            logger.debug(repr(e))
            logger.warning('{}:已断开连接'.format(address))
            break
            
        
        
        
            
        

def run(hsot):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(host)
    sock.listen(5)
    return sock
 
    
 
    #sock.close()
def newthread_(conn,address):
    global thread_list
    logger.info('新建线程:  ==> {} '.format(address))
    thread = Thread(target=accept_client,args=(conn,address))
    
    thread.setDaemon(True)

    thread.start()
    thread_list.append(thread)
#打印存活线程
def thread_log(thread_list):

    logger.info("============================================={}".format(threading.current_thread().getName()))
    logger.info("线程数量：{}".format(len(thread_list)))
    #定义一个空数组，用于保存还存活的线程
    cur_thread_list=[]
    for i in range(len(thread_list)):
        cur_thread=thread_list[i]
        thread_name=cur_thread.getName()
        thread_active=cur_thread.isAlive()
        if not thread_active:
            pass
        else:
            cur_thread_list.append(cur_thread)
            logger.info('当前存在线程：{}'.format(thread_name))
    #更新线程池
    thread_list=cur_thread
    logger.info("=============================================")
if __name__ == '__main__':
   
    hostname = socket.gethostname()
    logger.info ( "Host name: %s" %hostname)
    sysinfo = socket.gethostbyname(hostname)
    logger.info("IP: %s"%sysinfo)
    if(len(sys.argv)==2):
        host=(sysinfo,int(sys.argv[1]))
    else:
        host=(sysinfo, 8889)
    sock=run(host)
    logger.info('socket服务以启动:%s:%d'%host)
    # 新开一个线程，用于接收新连接
    wait_client(sock)

    
    