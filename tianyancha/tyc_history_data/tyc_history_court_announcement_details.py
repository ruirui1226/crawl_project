#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/5/16 9:41
@Author : zhangpf
@File : tyc_history_court_announcement_details.py
@Desc : tianyancha-历史法院公告详情
@Software: PyCharm
"""

import requests
import json
from loguru import logger
import os
import time
import math
from untils.pysql import *
from conf.env import *
import uuid

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from untils.urls import HISTORY_COURT_ANNOUNCEMENT_DETAILS

from untils.sql_data import TYC_DATA

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/jsondata/tyc_历史法院公告详情_file/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + "_" + ".json"
    # data_json=json.dumps(response.text,sort_keys=True, separators=(',', ': '),indent=4,ensure_ascii=False)
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_历史法院公告详情_file__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, businessId):
    version = "Android 12.67.0"
    url = HISTORY_COURT_ANNOUNCEMENT_DETAILS

    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)

    return data


def get_court_announcement_details_info(info_id, company_name, tyc_id, uuid):
    try:
        data = get_authoriaztion(info_id, company_name, tyc_id, uuid)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
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

        data = {"cgid": tyc_id, "detailId": uuid, "type": "court_announcement"}
        url = HISTORY_COURT_ANNOUNCEMENT_DETAILS
        res = requests.post(url=url, headers=headers, verify=False, data=json.dumps(data)).text
        res_json = json.loads(res)
        # create_json(info_id, tyc_id, company_name, res_json)
        items = []
        if res_json["data"]["data"] is not None:
            data = res_json["data"]["data"]
            item = {
                # "id": uuid,
                "info_id": str(info_id),
                "caseCodeList": ",".join(format(log) for log in data.get("caseCodeList"))
                if data.get("caseCodeList") is not None
                else "",
                "caseReason": data.get("caseReason"),
                "caseTitle": data.get("caseTitle"),
                "caseType": data.get("caseType"),
                "courtList": ",".join(format(log) for log in data.get("courtList"))
                if data.get("courtList") is not None
                else "",
                "hasCaseExplanation": data.get("hasCaseExplanation"),
                "t_id": data.get("id"),
                "isCaseClosed": data.get("isCaseClosed"),
                "sameSerialCaseCount": data.get("sameSerialCaseCount"),
                "trialProcedure": data.get("trialProcedure"),
                "trialProcedureDetail": ",".join(format(log) for log in data.get("trialProcedureDetail"))
                if data.get("trialProcedureDetail") is not None
                else "",
                "trialTime": data.get("trialTime"),
                "uuid": data.get("uuid"),
                "labels": ",".join(format(log) for log in data.get("labels")),
                "caseIdentityList": ",".join(format(log) for log in data.get("caseIdentityList"))
                if data.get("caseIdentityList") is not None
                else "",
                "company_name": company_name,
                "tyc_id": tyc_id,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            }
            items.append(item)
            print(items)
        return items

    except Exception as e:
        logger.debug(e)


def main():
    mq = MysqlPipelinePublic()
    data_list = mq.select_sql("t_zx_history_court_announcement", ["id", "company_name", "tyc_id", "uuid"], {"1": "1"})
    # data_list=get_company_wechat_name()
    for data in data_list:
        info_id = data.get("id")
        company_name = data.get("company_name")
        tyc_id = data.get("tyc_id")
        uuid = data.get("uuid")

        logger.warning("当前企业名称为-------%s" % company_name)
        items = get_court_announcement_details_info(info_id, company_name, tyc_id, uuid)
        try:
            for item in items:
                mq.insert_sql("t_zx_history_court_announcement_details", item)
        except Exception as e:
            logger.debug(e)
    mq.close()


if __name__ == "__main__":
    main()
