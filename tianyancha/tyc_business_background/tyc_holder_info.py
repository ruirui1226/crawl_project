#!/usr/bin/conf python
# -*- coding: utf-8 -*-
"""
@desc: tianyancha-股东信息
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
from tianyancha.untils.redis_conn import conn

# from tyc_projects.untils.pysql import get_company_name, delete_to_mysql_main, MysqlPipeline


from tianyancha.untils.pysql import *
from tianyancha.conf.env import *

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import uuid

from tianyancha.untils.urls import HOLDER_INFO

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/tyc_holder_file__股东信息/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + ".json"
    # data_json=json.dumps(response.text,sort_keys=True, separators=(',', ': '),indent=4,ensure_ascii=False)
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_holder_file_股东信息__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"

    url = HOLDER_INFO.format(tyc_id, pageNum)
    #
    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)
    return data


def get_holder_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token):
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

        url = HOLDER_INFO.format(tyc_id, "1")
        print(url)
        res = requests.get(url=url, headers=headers, verify=False).text

        logger.debug(res)

        res_json = json.loads(res)
        if res_json["data"]:
            if "total" in str(res_json["data"]):
                pages_total = math.ceil(int(res_json["data"]["total"]) / 20)
                if pages_total:
                    return pages_total
            else:
                pass
        else:
            pass

    except Exception as e:
        logger.debug(e)


def get_holder_info(info_id, company_name, tyc_id, pageNum):
    try:
        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        logger.warning("当前企业名称为%s" % company_name)
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

        url = HOLDER_INFO.format(tyc_id, pageNum)
        res = requests.get(url=url, headers=headers, verify=False).text

        logger.debug(res)
        res_json = json.loads(res)

        # create_json(info_id, tyc_id, company_name, res_json)
        items = []
        for holder_info in res_json["data"]["result"]:
            item = {
                "tyc_id": tyc_id,
                "info_id": info_id,
                "company_name": company_name,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
                "tagList": str(holder_info.get("tagList", "")),
                "toco": holder_info.get("toco", ""),
                "amount": holder_info.get("amount", ""),
                "name": holder_info.get("name", ""),
                "capital": str(holder_info.get("capital", "")),
                "capitalActl": str(holder_info.get("capitalActl", "")),
                "logo": holder_info.get("logo", ""),
                "holder_id": holder_info.get("id", ""),
                "type": holder_info.get("type", ""),
                "shareHolderType": holder_info.get("shareHolderType", ""),
                "percent": holder_info.get("percent", ""),
                "hcgid": holder_info.get("hcgid", ""),
                "finalBenefitShares": holder_info.get("finalBenefitShares", ""),
                "position": holder_info.get("position", ""),
                "jigouName": holder_info.get("jigouName", ""),
                "jigouLogo": holder_info.get("jigouLogo", ""),
                "jigouId": holder_info.get("jigouId", ""),
                "productId": holder_info.get("productId", ""),
                "productName": holder_info.get("productName", ""),
                "productLogo": holder_info.get("productLogo", ""),
                "existHoldingPath": holder_info.get("existHoldingPath", ""),
                "existBenefitDetail": holder_info.get("existBenefitDetail", ""),
                "serviceType": holder_info.get("serviceType", ""),
                "serviceCount": holder_info.get("serviceCount", ""),
            }
            items.append(item)

        return items
    except Exception as e:
        logger.debug(e)


def main():
    data_list = get_company_230420_name()
    for data in data_list:
        info_id = data[0]
        company_name = data[1]
        tyc_id = data[2]
        pageNum = 1
        ex = conn.sadd("tyc_holder_info", tyc_id)
        if ex == 1:
            data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
            logger.warning("当前企业名称为%s" % company_name)
            tyc_hi = data["data"]["tyc_hi"]
            Authorization = data["data"]["Authorization"]
            duid = data["data"]["duid"]
            deviceID = data["data"]["deviceID"]
            x_auth_token = data["data"]["x_auth_token"]
            pages_total = get_holder_page(
                info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token
            )
            if pages_total:
                print(company_name)
                for pageNum in range(1, int(pages_total) + 1):
                    items = get_holder_info(info_id, company_name, tyc_id, pageNum)
                    try:
                        mq = MysqlPipeline()
                        for item in items:
                            mq.insert_into_holder_info_info(item)
                            logger.info("数据 %s 插入成功" % item)
                        mq.close()

                    except Exception as e:
                        logger.debug(e)
            else:
                pass
        else:
            logger.debug("%s---------数据已经采集，无需再次采集" % tyc_id)
            pass
        # delete_to_mysql_main(info_id,company_name)


if __name__ == "__main__":
    main()
