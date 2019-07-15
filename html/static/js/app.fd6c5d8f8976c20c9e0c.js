webpackJsonp([1], { NHnr: function(t, e, n) { "use strict";
        Object.defineProperty(e, "__esModule", { value: !0 }); var o = n("/5sW"),
            i = { render: function() { var t = this.$createElement,
                        e = this._self._c || t; return e("div", { attrs: { id: "app" } }, [e("router-view")], 1) }, staticRenderFns: [] }; var r = n("VU/8")({ name: "App" }, i, !1, function(t) { n("aoam") }, null, null).exports,
            a = n("/ocq");
        data.buttonStyle || (data.buttonStyle = { height: "50px", width: "80px", fontSize: "25px", margin: "12.5px" }), data.boxStyle || (data.boxStyle = { height: "500px", width: "100%", background: "black" }); var u = { name: "HelloWorld", data: function(t) {
                    function e() { return t.apply(this, arguments) } return e.toString = function() { return t.toString() }, e }(function() { return data }), methods: { buclick: function(t) { ws.send(t) } }, mounted: function() { this.$el.children[0].click() } },
            l = { render: function() { var t = this,
                        e = t.$createElement,
                        n = t._self._c || e; return n("div", { style: { height: t.boxStyle.height ? t.boxStyle.height : "1080px", width: t.boxStyle.width ? t.boxStyle.width : "100%", background: t.boxStyle.background ? t.boxStyle.background : "rgba(255,0,0,1)" } }, [n("div", { attrs: { id: "laylebox" } }, t._l(t.data, function(e, o) { return n("el-button", { key: o, staticClass: "transition-box", style: { margin: t.buttonStyle.margin ? t.buttonStyle.margin : "25px", height: t.buttonStyle.height ? t.buttonStyle.height : "60px", width: t.buttonStyle.width ? t.buttonStyle.width : "90px", fontSize: t.buttonStyle.fontSize ? t.buttonStyle.fontSize : "30px" }, attrs: { type: "primary", plain: "", autofocus: 0 == o }, on: { click: function(n) { return t.buclick(e) } } }, [t._v(t._s(e))]) }), 1)]) }, staticRenderFns: [] }; var c = n("VU/8")(u, l, !1, function(t) { n("etFw") }, null, null).exports;
        o.default.use(a.a); var d = new a.a({ routes: [{ path: "/", name: "HelloWorld", component: c }] }),
            s = n("zL8q");
        n("tvR6");
        o.default.config.productionTip = !1, o.default.use(s.Button), new o.default({ el: "#app", router: d, render: function(t) { return t(r) } }) }, aoam: function(t, e) {}, etFw: function(t, e) {}, tvR6: function(t, e) {} }, ["NHnr"]);
//# sourceMappingURL=app.fd6c5d8f8976c20c9e0c.js.map