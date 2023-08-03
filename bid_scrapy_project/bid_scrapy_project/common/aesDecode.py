#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/27 13:01
# @Author  : xm
# @File    : aesDecode.py
# @Description :  aes 加密 解密工具类
# pip install pycryptodome
import hashlib

import pyDes
from Crypto.Cipher import AES
import base64
import binascii


# 数据类
class MData:
    def __init__(self, data=b"", characterSet="utf-8"):
        # data肯定为bytes
        self.data = data
        self.characterSet = characterSet

    def saveData(self, FileName):
        with open(FileName, "wb") as f:
            f.write(self.data)

    def fromString(self, data):
        self.data = data.encode(self.characterSet)
        return self.data

    def fromBase64(self, data):
        self.data = base64.b64decode(data.encode(self.characterSet))
        return self.data

    def fromHexStr(self, data):
        self.data = binascii.a2b_hex(data)
        return self.data

    def toString(self):
        return self.data.decode(self.characterSet)

    def toBase64(self):
        return base64.b64encode(self.data).decode()

    def toHexStr(self):
        return binascii.b2a_hex(self.data).decode()

    def toBytes(self):
        return self.data

    def __str__(self):
        try:
            return self.toString()
        except Exception:
            return self.toBase64()


### 封装类
class AEScryptor:
    def __init__(self, key, mode, iv="", paddingMode="NoPadding", characterSet="utf-8", isHeskey_iv=False):
        """
        构建一个AES对象
        key: 秘钥，字节型数据
        mode: 使用模式，只提供两种，AES.MODE_CBC, AES.MODE_ECB
        iv： iv偏移量，字节型数据
        paddingMode: 填充模式，默认为NoPadding, 可选NoPadding，ZeroPadding，PKCS5Padding，PKCS7Padding
        characterSet: 字符集编码
        """
        self.key = key
        self.mode = mode
        self.iv = iv
        self.characterSet = characterSet
        self.paddingMode = paddingMode
        self.data = ""
        self.isHeskey_iv = isHeskey_iv

    def __ZeroPadding(self, data):
        data += b"\x00"
        while len(data) % 16 != 0:
            data += b"\x00"
        return data

    def __StripZeroPadding(self, data):
        data = data[:-1]
        while len(data) % 16 != 0:
            data = data.rstrip(b"\x00")
            if data[-1] != b"\x00":
                break
        return data

    def __PKCS5_7Padding(self, data):
        needSize = 16 - len(data) % 16
        if needSize == 0:
            needSize = 16
        return data + needSize.to_bytes(1, "little") * needSize

    def __StripPKCS5_7Padding(self, data):
        paddingSize = data[-1]
        return data.rstrip(paddingSize.to_bytes(1, "little"))

    def __paddingData(self, data):
        if self.paddingMode == "NoPadding":
            if len(data) % 16 == 0:
                return data
            else:
                return self.__ZeroPadding(data)
        elif self.paddingMode == "ZeroPadding":
            return self.__ZeroPadding(data)
        elif self.paddingMode == "PKCS5Padding" or self.paddingMode == "PKCS7Padding":
            return self.__PKCS5_7Padding(data)
        else:
            print("不支持Padding")

    def __stripPaddingData(self, data):
        if self.paddingMode == "NoPadding":
            return self.__StripZeroPadding(data)
        elif self.paddingMode == "ZeroPadding":
            return self.__StripZeroPadding(data)

        elif self.paddingMode == "PKCS5Padding" or self.paddingMode == "PKCS7Padding":
            return self.__StripPKCS5_7Padding(data)
        else:
            print("不支持Padding")

    def setCharacterSet(self, characterSet):
        """
        设置字符集编码
        characterSet: 字符集编码
        """
        self.characterSet = characterSet

    def setPaddingMode(self, mode):
        """
        设置填充模式
        mode: 可选NoPadding，ZeroPadding，PKCS5Padding，PKCS7Padding
        """
        self.paddingMode = mode

    def decryptFromBase64(self, entext):
        """
        从base64编码字符串编码进行AES解密
        entext: 数据类型str
        """
        mData = MData(characterSet=self.characterSet)
        self.data = mData.fromBase64(entext)
        return self.__decrypt()

    def decryptFromHexStr(self, entext):
        """
        从hexstr编码字符串编码进行AES解密
        entext: 数据类型str
        """
        mData = MData(characterSet=self.characterSet)
        if self.isHeskey_iv == True:
            self.iv = mData.fromHexStr(self.iv)
            self.key = mData.fromHexStr(self.key)

        self.data = mData.fromHexStr(entext)
        return self.__decrypt()

    def decryptFromString(self, entext):
        """
        从字符串进行AES解密
        entext: 数据类型str
        """
        mData = MData(characterSet=self.characterSet)
        self.data = mData.fromString(entext)
        return self.__decrypt()

    def decryptFromBytes(self, entext):
        """
        从二进制进行AES解密
        entext: 数据类型bytes
        """
        self.data = entext
        return self.__decrypt()

    def encryptFromString(self, data):
        """
        对字符串进行AES加密
        data: 待加密字符串，数据类型为str
        """
        self.data = data.encode(self.characterSet)
        return self.__encrypt()

    def __encrypt(self):
        if self.mode == AES.MODE_CBC:
            aes = AES.new(self.key, self.mode, self.iv)
        elif self.mode == AES.MODE_ECB:
            aes = AES.new(self.key, self.mode)
        else:
            print("不支持这种模式")
            return

        data = self.__paddingData(self.data)
        enData = aes.encrypt(data)
        return MData(enData)

    def __decrypt(self):
        if self.mode == AES.MODE_CBC:
            aes = AES.new(self.key, self.mode, self.iv)
        elif self.mode == AES.MODE_ECB:
            aes = AES.new(self.key, self.mode)
        else:
            print("不支持这种模式")
            return
        data = aes.decrypt(self.data)
        mData = MData(self.__stripPaddingData(data), characterSet=self.characterSet)
        return mData

from pyDes import des, CBC, PAD_PKCS5, ECB
#pip install pyDes

class Descryptor():
    import binascii
    # 秘钥
    # def __init__(self):
        # self.KEY = key

    def des_encrypt(self,s, key, type, padmode,iv=None):
        """
        DES 加密
        :param s: 原始字符串
        :return: 加密后字符串，16进制
        """
        secret_key = key
        # iv = secret_key type:CBC ECB
        # padmode:PAD_PKCS5   PAD_PKCS7
        k = des(secret_key, type, iv, pad=None, padmode=padmode)
        en = k.encrypt(s, padmode=padmode)
        return MData(en)

    def des_descrypt(self,s, key,type, padmode):
        """
        DES 解密
        :param s: 加密后的字符串，16进制
        :return:  解密后的字符串
        """
        # secret_key = self.KEY
        secret_key = key[:8]
        iv = key[8:]
        k = des(secret_key, type, iv, pad=None, padmode=padmode)
        de = k.decrypt(base64.b64decode(s), padmode=padmode)
        # print(de.decode(encoding='GB2312',errors='strict'))
        # print(str(de, encoding="gb18030"))
        ddee = de.decode()
        return MData(ddee)

if __name__ == "__main__":
    key = b"dc93ac38"
    # key = binascii.b2a_hex(key).decode()
    # iv = b"A8909931867B0425"
    aes = AEScryptor(key, AES.MODE_ECB, paddingMode="PKCS7Padding", characterSet="utf-8", isHeskey_iv=True)
    #
    data = "777FA8F2C4A550736DAD88E2FC309CC0A713C7B51FD2BEDA2B872B4DAC1B86A9D409722C6CAD3B8FD943BD160B1A20B0396709DBD8FCB47B3BA3A58B29805380"
    # rData = aes.encryptFromString(data)
    # print("密文：", rData.toHexStr())
    # rData = "N1jfMuHUNZzAwf7B5RzFD1GKX36sb7XvQRsSMfdmdOx/1WX3k3GOQMhghQvUUaHApXvAsRE+irIPLlzLawwKZYYGY/9lGuRG7gmARjXOO61EpzRaTleeC8Rd6yMXxhPiMnUAztdDWfV+kT1F6urGfA97sKFXxcZ1vloozlCxvWoHEIeREd03j9d7Xn7ViK5iEN5EFMUnBAmSoXZMg6K9pVZsiEpWytwi/vLM2ljd2wRFCbJTmxtPxG5EAtuCTp0VfyxVzDa0RAzKs7JeXnECQQjs8Kkoe9NMdVpd8sU8u7jWdkG/V6H2cpWZFiNiGy5QcxRUNbJY/d2lJSWU88QUz+i0HIZCEa6KePW5uxpZv72laazvjC7Ff/EcuVOYnAWtmWT0JvzeBaQi935if0928+aBN43KVvAgL/wPq4cdS7t/hAIyHcbUbRvQ9lhg6nRD5hfVglCnYRqRslhPDlCW0kGCybhz2Qaj6NaefekJUNW2laiMsEoQWwQuU3qF+D8izmJj7PMhQ/YL/gtlkXyv2rS5bxmx1Hs2jm4jgw28LPPwL5L/S7Q7D2eZSVY6qMWPWZnbrcJm/Hp4pmrzIQcNTMxJFLcE36SQE1VbP9r2SSK3klOlGunv+6szD1Hvh+IS+BE1LaGgPgnIeoLLMub1wXfidMdKAfayouxY9pGbda9v6ADOrPX7tczDpEzWMNAH2onsEpjPK0tU/hc2/ywSFkXUjFUMh6HUcslwfYnT1HoleYO1PlWYPnKwuB9a2mhH+GWSaIX8A5PgPSColS5EZzrQd2YdRZOdDoVm/9UVnv2PQCOKjHSFHG+ZlofEweKaVJd2wkKAyJlGv4ub5tp/1AkF2KpfT9bxHZhEXr5UbwiuXTtXc0gWu5VmWhxRZctdHN8IHFjNmwdTT9wmarcMTRSxaaEDDTrWj3G7xyzbRRjfduCPZZLf15INOIdfVuX1RklQ7CSUdlsKvcATrWiPmWbRIHCZadGH3OnmyOu6FknU0zTRlK4wkr8rjyTMM8xh7U99Vos/av4e5huWni4MSs8YoifS3HVTX6N10KJe/+L2ERTCGjJ8YqLHz36PhC3PmlAPTv66Nrh9mzbKwowxtzZhHScqaiNvL2Y4NepPzMhAzHGZL5BKd5h4Sc4YkrgYUEHayXWP/IcGiOz4t/WU4XDkqgxAvOV4ukGU/txlq733UMZDqGGp541EqZ+48l/LYpg8W7UVXQqAAJGFm2X44PIXrQkIargzWyTXAaoNgkIOjnU6M4iU44H/Mrq+JTwsKyL2E+hO/y8T5klcogNhua3ZWZbJZPZn9ZLIRnzWtLNAJD8xNuqX59n8GlBUg/ZL03H8IOONm0Uc1LjdWYm49fk7bF/Ti2905V7KmFoHikHYAGl1Dwc/yqf7lkXb09+3KwIGq/pk6d/fof4oMP34eVgmmRzPs2blj4Z/AFdRKQt5Zgvlgr+X6amLFqsbvtH8pArkC3jCbnYpyJ1Vkdd1TQcLSjv1hoz540Nme3UqiShNUVVlX24TynOhtEJ1Odt1YJNeeMACQGB8GSOQ5KwkZeVINo3yzDHRPT517MzXrcl2JKMobouq8CoYcEugKiqKopxJV7or59yp0zEITNDSFVbu2hVdD31/q6UY02Y02QAaFPXpzvspQD9eqVWG4uwiLbqZB7QwNb/y5V23s+7UVzqZmB/JidC19KutzLCDVKIXkmeGxEO0pFob3fXZsDReL7gfJZMGi22+EZwfJQ2ccySsrAmySBoPJfWXvXWDbxCWJnOJUq5ycDdxvxcGwhkgPDSMBLtUX1h+X6n4sI1fw3jQasgeuCgccaQ+aDhsYE9uOxaMT8bnCXm/X2jXdANjKl+x4kTcGaKV3ieX/1TboYNXHSAsn09i9jDcdd6vqMzi/M+aRd6ybRerqWyQ+pezqDQdOxoMEzNPaf1ueSH2LUAl4xvuotiIJNZaMnLPaUI="
    # rData = aes.decryptFromBase64(rData)
    # print("明文：", rData)
    # print("明文：", type(rData.data))

    ##md5
    # ll = get_md5("3637CB36B2E54A72A7002978D0506CDFBeginTime2022-12-27 00:00:00createTime[]EndTime2023-06-27 23:59:59GGTYPE1KINDGCJSpageNo1pageSize40PROTYPEA02timeType6total960ts1687845604882")
    # print(ll)
    ##++++++++des+++++++
    datas = Descryptor().des_encrypt(data, key, ECB, pyDes.PAD_PKCS5)
    print(datas.toHexStr())
    # print(bytes(key))