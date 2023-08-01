#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@desc: tianyancha-微信公众号
@version: python3
@author: QTH
@time: 2023/05/26
"""

import requests
import json
from loguru import logger
import os
import time
import math
from untils.pysql import *
# from tyc_projects.conf.env import *

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(company_name, res_json):
    folder_name = os.getcwd() + "/tyc_wechat_file/微信公众号/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + str(time.time()).split(".")[0] + ".json"
    # data_json=json.dumps(response.text,sort_keys=True, separators=(',', ': '),indent=4,ensure_ascii=False)
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_wechat_file_微信公众号__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"

    url = f"https://api6.tianyancha.com/cloud-business-state/wechat/list?pageSize=20&graphId={tyc_id}&pageNum={pageNum}"

    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9964/get_authorzation", data=json.dumps(data))
    print(r.text)
    data = json.loads(r.text)
    return data


def get_publicWechat_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, X_AUTH_TOKEN):
    try:
        headers = {
            "user-agent": "com.tianyancha.skyeye/Dalvik/2.1.0 (Linux; U; Android 8.1.0; Nexus 6P Build/OPM7.181205.001; appDevice/google_QAQ_Nexus 6P)",
            "authorization": Authorization,
            "x-auth-token": X_AUTH_TOKEN,
            "channelid": "YingYongBao",
            "deviceid": deviceID,
            "tyc-hi": tyc_hi,
            "version": "Android 12.67.0",
            "duid": duid,
            "content-type": "application/json",
        }

        url = f"https://api6.tianyancha.com/cloud-business-state/wechat/list?pageSize=20&graphId={tyc_id}&pageNum=1"
        res = requests.get(url=url, headers=headers, verify=False).text

        logger.debug(res)
        res_json = json.loads(res)
        if "total" in str(res_json["data"]):
            pages_total = math.ceil(int(res_json["data"]["total"]) / 20)

            if pages_total:
                return pages_total
        elif int(res_json["data"]["count"]) > 0:
            pages_total = math.ceil(int(res_json["data"]["count"]) / 20)
            if pages_total:
                return pages_total

        else:
            logger.debug("%s没有公众号数据" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_publicWechat_info(info_id, company_name, tyc_id, pageNum):
    try:
        url = f"https://api6.tianyancha.com/cloud-business-state/wechat/list?pageSize=20&graphId={tyc_id}&pageNum={pageNum}"
        logger.warning(url)

        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        X_AUTH_TOKEN = data["data"]["x_auth_token"]
        headers = {
            "user-agent": "com.tianyancha.skyeye/Dalvik/2.1.0 (Linux; U; Android 8.1.0; Nexus 6P Build/OPM7.181205.001; appDevice/google_QAQ_Nexus 6P)",
            "authorization": Authorization,
            "x-auth-token": X_AUTH_TOKEN,
            "channelid": "YingYongBao",
            "deviceid": deviceID,
            "tyc-hi": tyc_hi,
            "version": "Android 12.67.0",
            "duid": duid,
            "content-type": "application/json",
        }
        res = requests.get(url=url, headers=headers, verify=False).text

        logger.debug(res)
        res_json = json.loads(res)

        create_json(company_name, res_json)
        items = []
        for wechat_info in res_json["data"]["resultList"]:
            item = {
                "info_id": info_id,
                "publicNum": wechat_info.get("publicNum", ""),
                "codeImg": wechat_info.get("codeImg", ""),
                "recommend": wechat_info.get("recommend", ""),
                "title": wechat_info.get("title", ""),
                "titleImgURL": wechat_info.get("titleImgURL", ""),
                "titleImgOriginalURL": wechat_info.get("titleImgOriginalURL", ""),
                "company_name": company_name,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            }
            items.append(item)

        return items
    except Exception as e:
        logger.debug(e)


def main():
    data_list = get_company_name()
    for data in data_list:
        info_id = data[0]
        company_name = data[1]
        tyc_id = data[2]
        pageNum = 1
        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        pages_total = get_publicWechat_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token)
        if pages_total:
            print(company_name)
            for pageNum in range(1, int(pages_total) + 1):
                items = get_publicWechat_info(info_id, company_name, tyc_id, pageNum)
                try:
                    pass
                    mq = MysqlPipeline()
                    for item in items:
                        mq.insert_into_wechat_public_info(item)
                        logger.info("数据 %s 插入成功" % item)
                    mq.close()

                except Exception as e:
                    logger.debug(e)
        else:
            pass


if __name__ == "__main__":
    main()
