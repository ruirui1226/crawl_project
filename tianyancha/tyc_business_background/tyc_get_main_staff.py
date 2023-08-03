#!/usr/bin/conf python
# -*- coding: utf-8 -*-
"""
@desc: tianyancha-主要人员
@version: python3
@author: shenr
@time: 2023/05/22
"""

import requests
import json
from loguru import logger
import os
import time
import math
import uuid
from tianyancha.untils.pysql import *

from tianyancha.untils.urls import KEY_PERSONNEL

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from tianyancha.untils.redis_conn import conn
from untils.sql_data import TYC_DATA

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/tyc_main_staff_file_主要人员/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + ".json"
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_main_staff_file_主要人员__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id):
    version = "Android 12.67.0"

    url = KEY_PERSONNEL.format(tyc_id, 1)
    logger.warning(url)

    data = {"url": url, "version": version}

    r = requests.post(GET_AUTHORZATION_LOCAL_API, data=json.dumps(data))
    print(r.text)
    data = json.loads(r.text)
    return data


def get_Trademark_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token):
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

    url = KEY_PERSONNEL.format(tyc_id, 1)
    res = requests.get(url=url, headers=headers, verify=False).text

    # logger.debug(res)
    res_json = json.loads(res)
    print("-----", res_json)
    if "total" in str(res_json["data"]):
        # if math.ceil(int(res_json["data"]["total"]) / 20) < 27:
        pages_total = math.ceil(int(res_json["data"]["total"]) / 20)

        if pages_total:
            return pages_total
        else:
            return 1
    # elif int(res_json["data"].get("count")) > 0:
    #     pages_total = math.ceil(int(res_json["data"]["count"]) / 20)
    #     if pages_total:
    #         return pages_total
    else:
        logger.debug("%s没有信息" % company_name)
        return 1
    # except Exception as e:
    #     logger.debug(e)


def get_Trademark_info(info_id, company_name, tyc_id, pageNum):
    try:
        data = get_authoriaztion(info_id, company_name, tyc_id)
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

        url = KEY_PERSONNEL.format(tyc_id, pageNum)
        # res = requests.post(url=url, headers=headers, data=json.dumps(data), verify=False).text
        res = requests.get(url=url, headers=headers, verify=False).text

        # logger.debug(res)
        res_json = json.loads(res)
        logger.info(f"内容{res}")

        # create_json(pageNum, info_id, tyc_id, company_name, res_json)
        items = []
        for each in res_json["data"]["result"]:
            item = {
                "info_id": info_id,
                "tyc_id": tyc_id,
                "company_name": company_name,
                "serviceType": each.get("serviceType", ""),
                "existBenefitDetail": each.get("existBenefitDetail", ""),
                "typeSore": each.get("typeSore", ""),
                "pid": each.get("pid", ""),
                "type": each.get("type", ""),
                "percent": each.get("percent", ""),
                "hcgid": each.get("hcgid", ""),
                "typeJoin": str(each.get("typeJoin", "")).replace("'", '"'),
                "tagList": str(each.get("tagList", "")).replace("'", '"'),
                "toco": each.get("toco", ""),
                "serviceCount": each.get("serviceCount", ""),
                "finalBenefitShares": each.get("finalBenefitShares", ""),
                "name": each.get("name", ""),
                "logo": each.get("logo", ""),
                "staff_id": each.get("id", ""),
                "url": url,
                "existHoldingPath": each.get("existHoldingPath", ""),
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
        info_id = data[0]
        company_name = data[1]
        tyc_id = data[2]
        ex = conn.sadd("main_staff_tyc_id", tyc_id)
        if ex == 1:
            data = get_authoriaztion(info_id, company_name, tyc_id)
            tyc_hi = data["data"]["tyc_hi"]
            Authorization = data["data"]["Authorization"]
            duid = data["data"]["duid"]
            deviceID = data["data"]["deviceID"]
            x_auth_token = data["data"]["x_auth_token"]
            pages_total = get_Trademark_page(
                info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token
            )
            if pages_total:
                print("=*=*=*=*=*=", pages_total)
            for pageNum in range(1, int(pages_total) + 1):
                items = get_Trademark_info(info_id, company_name, tyc_id, pageNum)
                try:
                    for item in items:
                        mq.insert_sql("t_zx_company_main_staff_info", item)
                        logger.debug(f"======插入===={item}====")
                except Exception as e:
                    logger.debug(e)
                else:
                    pass
        else:
            logger.debug("%s---------数据已经采集，无需再次采集" % tyc_id)
            pass
    mq.close()


if __name__ == "__main__":
    main()
