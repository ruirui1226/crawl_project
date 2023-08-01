#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@desc: tianyancha-担保风险
@version: python3
@author: shenr
@time: 2023/05/26
"""
import requests
import json
from loguru import logger
import os
import time
import math
import uuid
from untils.pysql import *
from conf.env import *
from untils.redis_conn import conn
from untils.urls import GUARANTY_INSURANCE

# 忽略requests证书警告
try:
    import urllib3
    from urllib3.exceptions import InsecureRequestWarning

    urllib3.disable_warnings(InsecureRequestWarning)
except:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/tyc_guaranty_insurance__担保风险/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass
    file_nm = company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + str(pageNum) + ".json"
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_guaranty_insurance__担保风险__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    url = GUARANTY_INSURANCE

    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)

    return data


def get_business_info(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token):
    try:
        headers = {
            # """
            "x-b3-traceid-jindi": "",
            "x-b3-sampled-jindi": "",
            "Authorization": Authorization,
            "version": "Android 12.67.0",
            "X-Auth-Token": x_auth_token,
            "Content-Type": "application/json",
            "channelID": "huawei",
            "deviceID": "1bbaf81111eb23c5",
            "deviceModel": "Nexus 6P",
            "deviceVersion": "8.1.0",
            "tyc-hi": tyc_hi,
            "sensorsAnonymousId": deviceID,
            "device-uuid": deviceID,
            "tdid": "36c73d82d939322125bf91fa8ae59b3d5",
            "device_uuid": deviceID,
            "app_channel": "huawei",
            "app-code": "670",
            "androidid": deviceID,
            "oaid": "00000000-0000-0000-0000-000000000000",
            # "Connection": close
            "User-Agent": "com.tianyancha.skyeye/Dalvik/2.1.0 (Linux; U; Android 8.1.0; Nexus 6P Build/OPM7.181205.001; appDevice/google_QAQ_Nexus 6P)",
            "Cache-Control": "no-cache, no-store",
            "Host": "api6.tianyancha.com",
            "Accept-Encoding": "gzip",
        }

        data = {"pageNum": "1", "gid": str(tyc_id), "pageSize": "20"}
        url = GUARANTY_INSURANCE
        res = requests.post(url=url, headers=headers, data=json.dumps(data), verify=False).text

        logger.debug(res)
        res_json = json.loads(res)
        print("=====", res_json)
        if not res_json.get("data", "").get("totalRiskCount"):
            logger.debug("%s当前数据异常" % company_name)
            pass
        elif "total" in str(res_json["data"]):
            pages_total = math.ceil(int(res_json["data"]["totalRiskCount"]) / 20)
            if pages_total:
                return pages_total
            else:
                return 1
        else:
            logger.debug("%s没有guaranty_insurance数据" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_guaranty_insurance_info(info_id, company_name, tyc_id, pageNum):
    url = GUARANTY_INSURANCE
    logger.warning(url)
    data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
    tyc_hi = data["data"]["tyc_hi"]
    Authorization = data["data"]["Authorization"]
    duid = data["data"]["duid"]
    deviceID = data["data"]["deviceID"]
    x_auth_token = data["data"]["x_auth_token"]
    headers = {
        # """
        "x-b3-traceid-jindi": "",
        "x-b3-sampled-jindi": "",
        "Authorization": Authorization,
        "version": "Android 12.67.0",
        "X-Auth-Token": x_auth_token,
        "Content-Type": "application/json",
        "channelID": "huawei",
        "deviceID": "1bbaf81111eb23c5",
        "deviceModel": "Nexus 6P",
        "deviceVersion": "8.1.0",
        "tyc-hi": tyc_hi,
        "sensorsAnonymousId": deviceID,
        "device-uuid": deviceID,
        "tdid": "36c73d82d939322125bf91fa8ae59b3d5",
        "device_uuid": deviceID,
        "app_channel": "huawei",
        "app-code": "670",
        "androidid": deviceID,
        "oaid": "00000000-0000-0000-0000-000000000000",
        # "Connection": close
        "User-Agent": "com.tianyancha.skyeye/Dalvik/2.1.0 (Linux; U; Android 8.1.0; Nexus 6P Build/OPM7.181205.001; appDevice/google_QAQ_Nexus 6P)",
        "Cache-Control": "no-cache, no-store",
        "Host": "api6.tianyancha.com",
        "Accept-Encoding": "gzip",
    }

    data = {"pageNum": str(pageNum), "gid": str(tyc_id), "pageSize": "20"}
    res = requests.post(url=url, headers=headers, data=json.dumps(data), verify=False).text

    logger.debug(res)
    res_json = json.loads(res)
    create_json(pageNum, info_id, tyc_id, company_name, res_json)

    items = []
    for invest_info in res_json["data"]["result"]:
        item = {
            "info_id": info_id,
            "u_index": invest_info.get("index", ""),
            "guarantyType": invest_info.get("guarantyType", ""),
            "guarantor": str(invest_info.get("guarantor", "")).replace("'", '"'),
            "vouchee": str(invest_info.get("vouchee", "")).replace("'", '"'),
            "creditor": str(invest_info.get("creditor", "")).replace("'", '"'),
            "capitalAmount": invest_info.get("capitalAmount"),
            "judgeTime": invest_info.get("judgeTime"),
            "publishTime": invest_info.get("publishTime", ""),
            "u_uuid": invest_info.get("uuid", ""),
            "lawsuitUrl": invest_info.get("lawsuitUrl", ""),
            "tyc_id": tyc_id,
            "company_name": company_name,
            "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        }
        items.append(item)

    return items


def main():
    data_list = get_company_230529_name()
    for data in data_list:
        info_id = data[0]
        company_name = data[1]
        tyc_id = data[2]
        pageNum = 1

        logger.warning("当前企业名称为%s" % company_name)
        ex = conn.sadd("tyc_guaranty_insurance", tyc_id)
        if ex == 1:
            data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
            tyc_hi = data["data"]["tyc_hi"]
            Authorization = data["data"]["Authorization"]
            duid = data["data"]["duid"]
            deviceID = data["data"]["deviceID"]
            x_auth_token = data["data"]["x_auth_token"]

            pages_total = get_business_info(
                info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token
            )
            if pages_total:
                for pageNum in range(1, int(pages_total) + 1):
                    items = get_guaranty_insurance_info(info_id, company_name, tyc_id, pageNum)
                    if items:
                        mq = MysqlPipelinePublic()
                        for item in items:
                            logger.info(f"数据入库start：{item}")
                            mq.insert_sql("t_zx_tyc_guaranty_insurance", item)
                        mq.close()
            else:
                pass
            conn.sadd("tyc_guaranty_insurance", tyc_id)
        else:
            print("==========数据已采集==========")


if __name__ == "__main__":
    main()
