#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@desc: tianyancha-实际控制人
@version: python3
@author: shenr
@time: 2023/05/23
"""
import requests
import json

import uuid
from loguru import logger
import os
import time
import math
from tianyancha.conf.env import *
from tianyancha.untils.pysql import *
from untils.redis_conn import conn
# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning


from tianyancha.untils.urls import ACTUAL_CONTROL_INFO

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/tyc_actual_control_info_file_疑似实际控制人/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + ".json"
    # data_json=json.dumps(response.text,sort_keys=True, separators=(',', ': '),indent=4,ensure_ascii=False)
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_actual_control_info_file_疑似实际控制人__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"

    # url=f"https://capi.tianyancha.com/cloud-equity-provider/v4/actualControl/company/list?id={tyc_id}&height=750&width=610"
    url = ACTUAL_CONTROL_INFO.format(tyc_id)
    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    print("====", r)
    data = json.loads(r.text)
    return data


def get_actualcontrol_detail(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token):
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

    # url = "https://api6.tianyancha.com/services/v3/t/details/appComIcV4/631178350?pageSize=1000"
    # url=f"https://api6.tianyancha.com/cloud-business-state/recruitment/list?city=-100&pageSize=10&graphId={tyc_id}&experience=-100&pageNum=1&startDate=-100"
    # url = f"https://capi.tianyancha.com/cloud-equity-provider/v4/actualControl/company/list?id={tyc_id}&height=750&width=610"
    url = ACTUAL_CONTROL_INFO.format(tyc_id)
    res = requests.get(url, headers=headers, verify=False).text

    # logger.debug(res)

    res_json = json.loads(res)
    print("====", res_json)
    create_json(info_id, tyc_id, company_name, res_json)
    if res_json["data"]:
        item = {
            "company_name": company_name,
            "tyc_id": tyc_id,
            "info_id": info_id,
            "coordinate": str(res_json.get("data", "").get("coordinate", "")).replace("'", '"'),
            "pathMap": str(res_json.get("data", "").get("pathMap", "")).replace("'", '"'),
            "hid": res_json.get("data", "").get("actualControllerList", "")[0].get("hId", ""),
            "hPid": res_json.get("data", "").get("actualControllerList", "")[0].get("hPid", ""),
            "gId": res_json.get("data", "").get("actualControllerList", "")[0].get("gId", ""),
            "autualcontrol_name": res_json.get("data", "").get("actualControllerList", "")[0].get("name", ""),
            "autualcontrol_type": res_json.get("data", "").get("actualControllerList", "")[0].get("type", ""),
            "ratio": res_json.get("data", "").get("actualControllerList", "")[0].get("ratio", ""),
            "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        }
        return item
    else:
        logger.debug("%s当前企业没有实际控制人" % company_name)
        item = {}
        return item


def main():
    data_list = get_company_230420_name()
    for data in data_list:
        info_id = data[0]
        company_name = data[1]
        tyc_id = data[2]
        pageNum = 1

        if conn.sismember("tyc_investments_abroad", tyc_id):
            logger.debug("{}=======>数据已经采集，无需再次采集".format(tyc_id))
            continue

        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        item = get_actualcontrol_detail(
            info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token
        )
        if item:
            try:
                mq = MysqlPipelinePublic()
                mq.insert_sql("t_zx_company_actualcontrol_detail", item)
                mq.close()

            except Exception as e:
                logger.debug(e)
        else:
            pass
        conn.sadd("tyc_investments_abroad", tyc_id)


if __name__ == "__main__":
    main()
