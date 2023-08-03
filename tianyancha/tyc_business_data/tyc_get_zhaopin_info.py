#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@desc: tianyancha-招聘信息
@version: python3
@author: QTH
@time: 2023/05/26
"""

import requests
import json
from loguru import logger
import os, time, math
import uuid
from conf.env import *
from untils.pysql import *
from untils.redis_conn import conn

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from untils.sql_data import TYC_DATA

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/tyc_zhaopin_file__招聘信息/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + str(pageNum) + ".json"
    # data_json=json.dumps(response.text,sort_keys=True, separators=(',', ': '),indent=4,ensure_ascii=False)
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_zhaopin_file__招聘信息__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"

    url = f"https://api6.tianyancha.com/cloud-business-state/recruitment/list?city=-100&pageSize=10&graphId={tyc_id}&experience=-100&pageNum={pageNum}&startDate=-100"
    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)
    return data


def get_Zhaopin_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token):
    headers = {
        # """
        "x-b3-traceid-jindi": "",
        "x-b3-sampled-jindi": "",
        "Authorization": Authorization,
        "version": "Android 12.67.2",
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
    url = f"https://api6.tianyancha.com/cloud-business-state/recruitment/list?city=-100&pageSize=10&graphId={tyc_id}&experience=-100&pageNum=1&startDate=-100"
    res = requests.get(url, headers=headers, verify=False).text
    # logger.debug(res)
    res_json = json.loads(res)
    if res_json.get("state", "") == "error":
        logger.debug("%s当前数据异常" % company_name)
        pass

    elif "total" in str(res_json["data"]):
        pages_total = math.ceil(int(res_json["data"]["total"]) / 10)

        if pages_total:
            return pages_total
    elif int(res_json["data"].get("itemTotal", "")) != 0:
        pages_total = math.ceil(int(res_json["data"]["itemTotal"]) / 10)
        if pages_total:
            return pages_total


def get_Zhaopin_info(pageNum, info_id, company_name, tyc_id):
    try:
        url = f"https://api6.tianyancha.com/cloud-business-state/recruitment/list?city=-100&pageSize=10&graphId={tyc_id}&experience=-100&pageNum={pageNum}&startDate=-100"

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
        res = requests.get(url, headers=headers, verify=False).text

        logger.debug(res)
        res_json = json.loads(res)
        # create_json(pageNum, info_id, tyc_id, company_name, res_json)
        items = []
        for zhaopin_info in res_json["data"]["list"]:
            item = {
                "info_id": info_id,
                "education": zhaopin_info.get("education", ""),
                "city": zhaopin_info.get("city", ""),
                "companyName": zhaopin_info.get("companyName", ""),
                "webInfoPath": zhaopin_info.get("webInfoPath", ""),
                "source": zhaopin_info.get("source", ""),
                "title": zhaopin_info.get("title", ""),
                "experience": zhaopin_info.get("experience", ""),
                "salary": zhaopin_info.get("salary", ""),
                "welfare": zhaopin_info.get("welfare", ""),
                "isPromise": zhaopin_info.get("isPromise", ""),
                "companyGid": zhaopin_info.get("companyGid", ""),
                "welfareList": zhaopin_info.get("welfareList", ""),
                "allDirect": zhaopin_info.get("allDirect", ""),
                "startDate": zhaopin_info.get("startDate", ""),
                "wapInfoPath": zhaopin_info.get("wapInfoPath", ""),
                "company_name": company_name,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
                "tyc_id": tyc_id,
                "url": url,
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
        ex = conn.sismember("t_zx_company_zhaopin_info", tyc_id)
        if ex:
            logger.debug("%s---------数据已经采集，无需再次采集" % tyc_id)
            continue
        logger.warning("当前企业名称为%s" % company_name)
        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]

        pages_total = get_Zhaopin_page(
            info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token
        )
        if pages_total:
            for pageNum in range(1, int(pages_total) + 1):
                items = get_Zhaopin_info(pageNum, info_id, company_name, tyc_id)
                try:
                    pass
                    for item in items:
                        mq.insert_sql("t_zx_company_zhaopin_info", item)
                        logger.info("数据 %s 插入成功" % item)
                except Exception as e:
                    logger.debug(e)
        else:
            pass
        conn.sadd("t_zx_company_zhaopin_info", tyc_id)
    mq.close()


if __name__ == "__main__":
    main()
