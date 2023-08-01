#!/usr/bin/conf python
# -*- coding: utf-8 -*-
"""
@desc: tianyancha-最终受益人
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
from tianyancha.untils.pysql import *
from tianyancha.conf.env import *
import uuid
from untils.redis_conn import conn
# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from tianyancha.untils.urls import FINAL_BENEFICIARY

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/tyc_final_beneficiary_最终受益人/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = (
        company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + str(pageNum) + "_" + ".json"
    )
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_final_beneficiary_最终受益人__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    url = FINAL_BENEFICIARY.format(tyc_id, "1")

    params = {"url": url, "version": version}
    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(params))
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

        url = FINAL_BENEFICIARY.format(tyc_id, "1")
        res = requests.get(url=url, headers=headers, verify=False).text

        logger.debug(res)
        res_json = json.loads(res)
        if "total" in str(res_json["data"]):
            pages_total = math.ceil(int(res_json["data"]["total"]) / 20)

            if pages_total:
                # print(1)
                return pages_total
            else:
                # print(2)
                return 1
        # elif int(res_json["data"]["count"]) > 0:
        elif "total" in str(res_json["data"]):
            pages_total = math.ceil(int(res_json["data"]["count"]) / 20)
            if pages_total:
                # print(3)
                return pages_total
        else:
            logger.debug("%s没有信息" % company_name)
            # print(4)
            return 1
    # except Exception as e:
    #     logger.debug(e)


def get_Trademark_info(info_id, company_name, tyc_id, pageNum):
    try:
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

        url = FINAL_BENEFICIARY.format(tyc_id, pageNum)
        # res = requests.post(url=url, headers=headers, data=json.dumps(data), verify=False).text
        res = requests.get(url=url, headers=headers, verify=False).text

        # logger.debug(res)
        res_json = json.loads(res)
        logger.info(f"内容{res}")

        # create_json(pageNum, info_id, tyc_id, company_name, res_json)
        items = []
        for each in res_json["data"]["list"]:
            item = {
                "info_id": info_id,
                "servicetype": each.get("serviceType", ""),
                "total": each.get("total", ""),
                "chainlist": str(each.get("chainList", "")).replace("'", '"'),
                "servicecount": each.get("serviceCount", ""),
                "name": each.get("name", ""),
                "u_id": each.get("id", ""),
                "type": each.get("type", ""),
                "holderid": each.get("holderId", ""),
                "percent": each.get("percent", ""),
                "cid": each.get("cid", ""),
                "unique_id": str(tyc_id) + "_" + str(each.get("id", "")),
                "company_name": company_name,
                "tyc_id": tyc_id,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            }
            items.append(item)

        return items

    except Exception as e:
        logger.debug(e)


def main():
    data_list = get_company_230420_name()
    # data_list=get_company_wechat_name()
    for data in data_list:
        info_id = data[0]
        company_name = data[1]
        tyc_id = data[2]
        pageNum = 1

        logger.warning("当前企业名称为%s" % company_name)

        if conn.sismember("tyc_final_beneficiary", tyc_id):
            logger.debug("{}=======>数据已经采集，无需再次采集".format(tyc_id))
            continue

        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
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
                mq = MysqlPipelinePublic()
                for item in items:
                    mq.insert_sql("t_zx_tyc_final_beneficiary", item)
                    # print(f"======插入===={item}====")
                mq.close()
            except Exception as e:
                logger.debug(e)
            else:
                pass
        # delete_to_mysql_wechat_main(info_id,company_name)
        conn.sadd("tyc_final_beneficiary", tyc_id)


if __name__ == "__main__":
    main()
