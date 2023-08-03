#!/usr/bin/conf python
# -*- coding: utf-8 -*-
"""
@desc: tianyancha-变更记录
@version: python3
@author: shenr
@time: 2023/05/23
"""
import requests
import json
from loguru import logger
import os
import time
import math
from tianyancha.conf.env import *
from tianyancha.untils.pysql import *
from untils.redis_conn import conn

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from tianyancha.untils.urls import CHANGE_INFO
from untils.sql_data import TYC_DATA

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(company_name, res_json):
    folder_name = os.getcwd() + "/tyc_get_changeinfo_file_变更记录/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + str(time.time()).split(".")[0] + ".json"
    # data_json=json.dumps(response.text,sort_keys=True, separators=(',', ': '),indent=4,ensure_ascii=False)
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_get_changeinfo_file_变更记录__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 11.4.0"
    url = f"https://api4.tianyancha.com/services/v3/expanse/changeinfoEm3?pageSize=20&id={tyc_id}&pageNum={pageNum}"
    # url=f"https://api4.tianyancha.com/services/v3/expanse/bid?pageSize=20&id={tyc_id}&pageNum={pageNum}"
    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    # print("pppppppp", r.text)
    data = json.loads(r.text)
    return data


def get_Change_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token):
    # try:
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

    url = CHANGE_INFO.format(tyc_id, "1")
    print(company_name)
    res = requests.get(url=url, headers=headers, verify=False).text

    logger.debug(res)
    res_json = json.loads(res)

    if "total" in res_json and res_json["data"]["total"] and int(res_json["data"]["total"]) > 0:
        pages_total = math.ceil(int(res_json["data"]["total"]) / 20)
        if pages_total:
            return pages_total
    elif "total" in str(res_json["data"]):
        pages_total = math.ceil(int(res_json["data"]["total"]) / 20)

        if pages_total:
            return pages_total
    else:
        logger.debug("%s变更记录数据" % company_name)
        return 1
    # except Exception as e:
    #     logger.debug(e)


def get_Change_info(info_id, company_name, tyc_id, pageNum, x_auth_token):
    try:
        url = CHANGE_INFO.format(tyc_id, pageNum)
        logger.warning(url)

        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        # print("=====123132", data)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        X_AUTH_TOKEN = data["data"]["x_auth_token"]

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
        res = requests.get(url=url, headers=headers, verify=False).text

        logger.debug(res)
        res_json = json.loads(res)

        # create_json(company_name, res_json)
        items = []
        for changer_info in res_json["data"]["result"]:
            item = {
                "tyc_id": tyc_id,
                "info_id": info_id,
                "changeTime": changer_info.get("changeTime", ""),
                "havePsersion": changer_info.get("havePsersion", ""),
                "contentAfter": changer_info.get("contentAfter", ""),
                "createTime": changer_info.get("createTime", ""),
                "contentBefore": changer_info.get("contentBefore", ""),
                "changeItem": changer_info.get("changeItem", ""),
                "total": res_json["data"]["total"],
                "company_name": company_name,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            }
            items.append(item)
        return items
    except Exception as e:
        logger.debug(e)


def main():
    mq = MysqlPipelinePublic()
    data_list = TYC_DATA
    for data in data_list:
        info_id = data.get("id")
        company_name = data.get("co_name")
        tyc_id = data.get("co_id")
        pageNum = 1
        if conn.sismember("tyc_get_changeinfo", tyc_id):
            logger.debug("{}=======>数据已经采集，无需再次采集".format(tyc_id))
            continue
        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        X_AUTH_TOKEN = data["data"]["x_auth_token"]
        pages_total = get_Change_page(
            info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, X_AUTH_TOKEN
        )
        if pages_total:
            for pageNum in range(1, int(pages_total) + 1):
                # get_publicWechat_info(info_id, company_name, tyc_id, pageNum)
                items = get_Change_info(info_id, company_name, tyc_id, pageNum, X_AUTH_TOKEN)
                try:
                    for item in items:
                        mq.insert_sql("t_zx_company_change_info", item)
                        logger.info("插入成功---------------------数据 %s " % item)
                except Exception as e:
                    logger.debug(e)
        else:
            pass
        conn.sadd("tyc_get_changeinfo", tyc_id)
    mq.close()


if __name__ == "__main__":
    main()
