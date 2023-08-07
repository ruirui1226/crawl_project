#!/usr/bin/conf python
# -*- coding: utf-8 -*-
"""
@desc: tianyancha-历史送达公告
@version: python3
@author: shenr
@time: 2023/05/10
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
from untils.urls import HISTORICAL_NOTICE_OF_SERVICE

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning


from untils.sql_data import TYC_DATA

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/jsondata/tyc_历史送达公告_file/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = (
        company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + str(pageNum) + "_" + ".json"
    )
    # data_json=json.dumps(response.text,sort_keys=True, separators=(',', ': '),indent=4,ensure_ascii=False)
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_历史送达公告_file__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    url = HISTORICAL_NOTICE_OF_SERVICE

    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)

    return data


def get_investments_abroad_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token):
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

    data = {"pageNum": "1", "pageSize": "20", "id": str(tyc_id)}
    url = HISTORICAL_NOTICE_OF_SERVICE

    res = requests.post(url=url, headers=headers, data=json.dumps(data), verify=False).text
    # logger.debug(res)
    res_json = json.loads(res)
    if "total" in str(res_json["data"]):
        # if math.ceil(int(res_json["data"]["total"]) / 20) < 27:
        pages_total = math.ceil(int(res_json["data"].get("total") or 0) / 20)

        if pages_total:
            return pages_total
    elif int(res_json["data"]["count"]) > 0:
        pages_total = math.ceil(int(res_json["data"]["count"]) / 20)
        if pages_total:
            return pages_total

    else:
        logger.debug("%s没有商标信息" % company_name)
        pass
    # except Exception as e:
    #     logger.debug(e)


def get_investments_abroad_info(info_id, company_name, tyc_id, pageNum):
    # try:
    # print(url)
    # res = requests.get(url=url, headers=headers, verify=False).text

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
    data = {"pageNum": str(pageNum), "pageSize": "20", "id": str(tyc_id)}

    url = HISTORICAL_NOTICE_OF_SERVICE
    res = requests.post(url=url, headers=headers, data=json.dumps(data), verify=False).text

    # logger.debug(res)
    res_json = json.loads(res)
    # create_json(pageNum, info_id, tyc_id, company_name, res_json)
    items = []
    item = {
        "info_id": info_id,
        "businessid": res_json["data"]["notices"][0].get("businessId"),
        "title": res_json["data"]["notices"][0].get("title"),
        "court": res_json["data"]["notices"][0].get("court"),
        "startdate": str(res_json["data"]["notices"][0].get("startDate")),
        "caseno": res_json["data"]["notices"][0].get("caseNo"),
        "casereason": res_json["data"]["notices"][0].get("caseReason"),
        "identitylist": str(res_json["data"]["notices"][0].get("identityList")),
        "content": res_json["data"]["notices"][0].get("content"),
        "identityitems": str(res_json["data"].get("identityItems")),
        "casereasonitems": str(res_json["data"].get("caseReasonItems")),
        "yearsitems": str(res_json["data"].get("yearsItems")),
        "total": res_json["data"].get("total"),
        "pagenum": res_json["data"].get("pageNum"),
        "pagesize": res_json["data"].get("pageSize"),
        "explainnotices": res_json["data"].get("explainNotices"),
        "hotsearchhuman": res_json["data"].get("hotSearchHuman"),
        "hotcompany": res_json["data"].get("hotCompany"),
        "uniquet_id": tyc_id + "_" + str(res_json["data"]["notices"][0].get("businessId")),
        "company_name": company_name,
        "tyc_id": tyc_id,
        "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
    }
    items.append(item)
    return items

    # except Exception as e:
    #     logger.debug(e)


def main():
    mq = MysqlPipelinePublic()
    data_list = TYC_DATA
    for data in data_list:
        info_id = data.get("id")
        company_name = data.get("co_name")
        tyc_id = data.get("co_id")
        pageNum = 1

        logger.warning("当前企业名称为%s" % company_name)
        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        pages_total = get_investments_abroad_page(
            info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token
        )
        if pages_total:
            print(company_name)
            for pageNum in range(1, int(pages_total) + 1):
                items = get_investments_abroad_info(info_id, company_name, tyc_id, pageNum)
                try:
                    for item in items:
                        mq.insert_sql("t_zx_tyc_history_notice_delivery", item)
                except Exception as e:
                    logger.debug(e)
        else:
            pass
        # delete_to_mysql_wechat_main(info_id,company_name)
    mq.close()


if __name__ == "__main__":
    main()
