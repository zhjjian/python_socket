socket = 'ws://192.168.10.115:8889'
data = {
    "boxStyle": { height: '1080px', width: '100%', background: 'url(./static/img/bg.png)' },
    "buttonStyle": {
        height: '50px',
        width: '120px',
        fontSize: '25px',
        margin: '12.5px'
    },
    "data": ["按钮1", "按钮2", "按钮3"]
}

ws = new WebSocket(socket)
ws.onopen = function(e) {
    console.log("连接服务器成功");
    ws.send("控制端");
}
ws.onclose = function(e) {
    console.log("服务器关闭");
}
ws.onerror = function() {
    console.log("连接出错");
}

ws.onmessage = function(e) {
    console.log(e);

}