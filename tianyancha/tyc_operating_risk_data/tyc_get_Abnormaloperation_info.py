#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/5/26 14:36
@Author : xushaowei
@File : tyc_get_Abnormaloperation_info.py
@Desc :
@Software:PyCharm
"""
# 经营异常
import requests
import json

import urllib3
from loguru import logger
import os
import time
import math
import uuid
from untils.pysql import *
from conf.env import *
from untils.urls import ABNORMALOPERATION_LIST

# 忽略requests证书警告
try:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = FILE_PATH + "/company_abnormaloperation_info__经营异常/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass
    file_nm = company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + str(pageNum) + ".json"
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--company_abnormaloperation_info__经营异常__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    url = ABNORMALOPERATION_LIST.format(tyc_id, pageNum)

    data = {"url": url, "version": version}

    r = requests.post(GET_AUTHORZATION_LOCAL_API, data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)

    return data


def get_AbnormalList_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, pageNum):
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
        url = ABNORMALOPERATION_LIST.format(tyc_id, pageNum)
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
            logger.debug("%s没有经营异常公告" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_AbnormalList_info(info_id, company_name, tyc_id, pageNum):
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
        url = ABNORMALOPERATION_LIST.format(tyc_id, pageNum)
        res = requests.get(url=url, headers=headers, verify=False).text

        logger.debug(res)
        res_json = json.loads(res)
        items = []
        for abnormaloperation_item in res_json["data"]["result"]:
            if True is abnormaloperation_item.get("isShowPutReasonType"):
                isShowPutReasonType = 1
            else:
                isShowPutReasonType = 0
            if True is abnormaloperation_item.get("isRemoved"):
                isRemoved = 1
            else:
                isRemoved = 0
            item = {
                "info_id": info_id,
                "tyc_id": tyc_id,
                "removeDate": abnormaloperation_item.get("removeDate", ""),
                "putReason": abnormaloperation_item.get("putReason", ""),
                "putReasonType": abnormaloperation_item.get("putReasonType", ""),
                "putDepartment": abnormaloperation_item.get("putDepartment", ""),
                "isShowPutReasonType": isShowPutReasonType,
                "businessId": abnormaloperation_item.get("businessId", ""),
                "reasonType": abnormaloperation_item.get("reasonType"),
                "type": abnormaloperation_item.get("type"),
                "isRemoved": isRemoved,
                "createTime": abnormaloperation_item.get("createTime", ""),
                "removeDepartment": abnormaloperation_item.get("removeDepartment", ""),
                "removeReason": abnormaloperation_item.get("removeReason", ""),
                "putReasonTypeId": abnormaloperation_item.get("putReasonTypeId"),
                "abnormaloperatuib_id": abnormaloperation_item.get("id"),
                "putDate": abnormaloperation_item.get("putDate", ""),
                "company_name": company_name,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            }

            items.append(item)
        return items
    except Exception as e:
        logger.debug(e)


def main():
    data_list = get_company_230529_name()
    for data in data_list:
        info_id = data[0]
        company_name = data[1]
        tyc_id = data[2]
        # tyc_id = "5264255710"
        pageNum = 1
        logger.warning("当前企业名称为%s" % company_name)
        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        pages_total = get_AbnormalList_page(
            info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, pageNum
        )
        if pages_total:
            print(company_name)
            for pageNum in range(1, int(pages_total) + 1):
                items = get_AbnormalList_info(info_id, company_name, tyc_id, pageNum)
                if items:
                    mq = MysqlPipelinePublic()
                    for item in items:
                        logger.info(f"数据入库start：{item}")
                        mq.insert_sql("t_zx_company_abnormaloperation_info", item)
                    mq.close()
        else:
            logger.info("当前企业名称为%s" % company_name + "========经营异常无数据=======")


if __name__ == "__main__":
    main()
