#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/29 09:59
# @Author  : wym
# @File    : frida_tyc_server.py
import frida
from fastapi import FastAPI
import uvicorn


def on_message(message, data):
    if message["type"] == "send":
        print("[*] {0}".format(message["payload"]))
    else:
        print(message)


js_code = """
rpc.exports = {
    getsign: function (url, version) {
        var sig="aa";
        Java.perform(
            function () {
                send('getsign');
                var w2 = Java.use('com.tianyancha.base.utils.w2');
                var o3 = Java.use('com.tianyancha.base.utils.o3.c');
                //var y2 = Java.use('com.tianyancha.base.network.ExceptionInterceptor.generateTraceId');
                var Authorization = w2.E();
                send("Authorization:"+Authorization);
                var version = w2.Q();
                send("version:"+version);
                var deviceID = w2.r();
                send("deviceID:"+deviceID);
                var duid = w2.m();
                send("duid:"+duid);
                var x_auth_token=o3.W0().V();
                send("x_auth_token:"+x_auth_token);
                var tyc_hi =w2.a(url,Authorization,version,"",deviceID,"slat-20190819");
                send("tyc_hi:"+tyc_hi);

                sig={"tyc_hi":tyc_hi, "Authorization":Authorization, "duid":duid, "deviceID":deviceID,"x_auth_token":x_auth_token}

            }
        )
        return sig;
    }
}
function getBytes(s) {
        var bytes = [];
            for (var i = 0; i < s.length; i++) {
                bytes.push(s.charCodeAt(i));
            }
        return bytes;
}
"""

str_host = "192.168.191.3:8787"
# str_host = "10.69.6.14:8787"
# str_host = "172.16.0.185:877"
manager = frida.get_device_manager()
remote_device = manager.add_remote_device(str_host)
# process = frida.get_usb_device(1000).attach("com.tianyancha.skyeye")
# process = frida.get_usb_device(1000).attach("天眼查")

session = remote_device.attach("com.tianyancha.skyeye")
# session = remote_device.attach("天眼查")
script = session.create_script(js_code)
# script = process.create_script(js_code)
script.on("message", on_message)
script.load()

from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    url: str
    version: str


@app.post("/get_authorzation")
async def get_authorzation(item: Item):
    result = script.exports.getsign(item.url, item.version)
    return {"data": result}


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=9966)
