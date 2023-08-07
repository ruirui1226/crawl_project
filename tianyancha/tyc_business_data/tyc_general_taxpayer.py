#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@desc: tianyancha-一般纳税人
@version: python3
@author: QTH
@time: 2023/05/26
"""
import hashlib

import requests
import json
import os
import math
from untils.pysql import *

import uuid

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from untils.redis_conn import conn
from untils.urls import GENERAL_TAXPAYER

from untils.sql_data import TYC_DATA

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/jsondata/tyc_general_file__一般纳税人/"
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

    logger.debug(("--tyc_general_file_一般纳税人__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    url = GENERAL_TAXPAYER.format(tyc_id, pageNum)

    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)

    return data


def get_general_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, pageNum):
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

        url = GENERAL_TAXPAYER.format(tyc_id, pageNum)
        res = requests.get(url=url, headers=headers, verify=False).text

        # logger.debug(res)

        res_json = json.loads(res)
        if "total" in str(res_json["data"]):
            # if math.ceil(int(res_json["data"]["total"]) / 20) < 27:
            pages_total = math.ceil(int(res_json["data"]["total"]) / 20)

            if pages_total:
                return pages_total
        elif int(res_json["data"]["count"]) > 0:
            pages_total = math.ceil(int(res_json["data"]["count"]) / 20)
            if pages_total:
                return pages_total

        else:
            logger.debug("%s没有一般纳税人信息" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_general_info(info_id, company_name, tyc_id, pageNum):
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

        url = GENERAL_TAXPAYER.format(tyc_id, pageNum)
        res = requests.get(url=url, headers=headers, verify=False).text

        # logger.debug(res)
        res_json = json.loads(res)
        # create_json(pageNum, info_id, tyc_id, company_name, res_json)
        items_list = res_json["data"]["rows"]
        items = []

        for ite in items_list:
            uu_item = [
                str(info_id),
                ite.get("name", "1"),
                str(ite.get("gid", "3")),
                str(ite.get("alias", "4")),
                ite.get("taxpayerIdentificationNumber", "5"),
                ite.get("taxpayerQualificationType", "6"),
                ite.get("tyc_id", "7"),
            ]
            b = "".join(uu_item)
            uuid = hashlib.md5(b.encode(encoding="utf-8")).hexdigest()
            item = {
                "info_id": str(info_id),
                "name": ite.get("name", ""),
                "gid": ite.get("gid", ""),
                "logo": ite.get("logo", ""),
                "alias": ite.get("alias", ""),
                "taxpayerIdentificationNumber": ite.get("taxpayerIdentificationNumber", ""),
                "taxpayerQualificationType": ite.get("taxpayerQualificationType", ""),
                "taxAuthority": ite.get("taxAuthority", ""),
                "startDate": ite.get("startDate", ""),
                "endDate": ite.get("endDate", ""),
                "company_name": company_name,
                "tyc_id": tyc_id,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
                "uuid": uuid,
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
        initial_pageNum = 1
        ex = conn.sismember("tyc_general_taxpayer", tyc_id)
        if ex:
            logger.debug("%s---------数据已经采集，无需再次采集" % tyc_id)
            continue
        else:
            logger.warning("当前企业名称为-------%s" % company_name)
            data = get_authoriaztion(info_id, company_name, tyc_id, initial_pageNum)
            tyc_hi = data["data"]["tyc_hi"]
            Authorization = data["data"]["Authorization"]
            duid = data["data"]["duid"]
            deviceID = data["data"]["deviceID"]
            x_auth_token = data["data"]["x_auth_token"]
            pages_total = get_general_page(
                info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, initial_pageNum
            )
            if pages_total:
                print(company_name)
                for pageNum in range(1, int(pages_total) + 1):
                    items = get_general_info(info_id, company_name, tyc_id, pageNum)
                    try:
                        for item in items:
                            mq.insert_sql("t_zx_tyc_general_taxpayer", item)
                    except Exception as e:
                        logger.debug(e)
            else:
                pass
        conn.sadd("tyc_general_taxpayer", tyc_id)
    mq.close()


if __name__ == "__main__":
    main()
