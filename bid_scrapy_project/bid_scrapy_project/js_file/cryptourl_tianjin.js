// -*- coding: utf-8 -*-

//@desc: 天津市公共资源交易平台-js
//@version: js
//@author: shenr
//@time: 2023/6/20

//引入crypto-js
var CryptoJS = require("crypto-js");


var s = "qnbyzzwmdgghmcnm";

// 解密
function getCryptoUrl(hh) {
  var aa = hh.split("/");
  var aaa = aa.length;
  var bbb = aa[aaa - 1].split(".");
  var ccc = bbb[0];
  var cccc = bbb[1];
  var r = /^\+?[1-9][0-9]*$/;
  var srcs = CryptoJS.enc.Utf8.parse(ccc);
  var k = CryptoJS.enc.Utf8.parse(s);
  var en = CryptoJS.AES.encrypt(srcs, k, {
    mode: CryptoJS.mode.ECB,
    padding: CryptoJS.pad.Pkcs7,
  });
  var ddd = en.toString();
  ddd = ddd.replace(/\//g, "^");
  ddd = ddd.substring(0, ddd.length - 2);
  var bbbb = ddd + "." + bbb[1];
  aa[aaa - 1] = bbbb;
  var uuu = "";
  for (i = 0; i < aaa; i++) {
    uuu += aa[i] + "/";
  }
  uuu = uuu.substring(0, uuu.length - 1);
  return uuu;
  // }
}


