#!/usr/bin/conf python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/19 16:11
# @Author  : wym
# @File    : tyc_get_holder_info.py
# 股东信息
import requests
import json
from loguru import logger
import os
import time
import math
from untils.pysql import *
from conf.env import *
import uuid
from untils.redis_conn import conn

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from untils.urls import INVESTMENTS_ABROAD
from untils.sql_data import TYC_DATA

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/tyc_holder_file__主要股东/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + ".json"
    # data_json=json.dumps(response.text,sort_keys=True, separators=(',', ': '),indent=4,ensure_ascii=False)
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_main_holder_file__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"

    # url = f"https://api6.tianyancha.com/cloud-company-background/companyV2/dim/holderForApp?gid={tyc_id}&shareHolderType=-100&pageSize=20&percentLevel=-100&pageNum={pageNum}&hkVersion=1"
    url = f"https://api6.tianyancha.com/cloud-listed-company/listed/holder/topTen?percentLevel=-100&gid={tyc_id}&type=1"
    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)
    return data


def get_main_holder_info(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token):
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

        # url = f"https://api6.tianyancha.com/cloud-company-background/companyV2/dim/holderForApp?gid={tyc_id}&shareHolderType=-100&pageSize=20&percentLevel=-100&pageNum=1&hkVersion=1"
        url = f"https://api6.tianyancha.com/cloud-listed-company/listed/holder/topTen?percentLevel=-100&gid={tyc_id}&type=1"
        res = requests.get(url=url, headers=headers, verify=False).text

        logger.debug(res)
        res_json = json.loads(res)
        # create_json(info_id, tyc_id, company_name, res_json)
        items = []
        for main_holder_info in res_json["data"]["holderList"]:
            item = {
                "tyc_id": tyc_id,
                "info_id": info_id,
                "company_name": company_name,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
                "serviceType": main_holder_info.get("serviceType"),
                "tenTotal": main_holder_info.get("tenTotal"),
                "proportion": main_holder_info.get("proportion"),
                "publishDate": main_holder_info.get("publishDate"),
                "compareChange": main_holder_info.get("compareChange"),
                "shareType": main_holder_info.get("shareType"),
                "holdingChange": main_holder_info.get("holdingChange"),
                "toco": main_holder_info.get("toco"),
                "sorting": main_holder_info.get("sorting"),
                "holdingNum": main_holder_info.get("holdingNum"),
                "logo": main_holder_info.get("logo"),
                "details": main_holder_info.get("details"),
                "main_id": main_holder_info.get("id"),
                "mtenTotal": main_holder_info.get("mtenTotal"),
                "holdingNumWithUnit": main_holder_info.get("holdingNumWithUnit"),
                "actual": main_holder_info.get("actual"),
                "tenPercent": main_holder_info.get("tenPercent"),
                "holdingChangeWithUnit": main_holder_info.get("holdingChangeWithUnit"),
                "cType": main_holder_info.get("cType"),
                "costEstimation": main_holder_info.get("costEstimation"),
                "tagList": str(main_holder_info.get("tagList")),
                "serviceCount": main_holder_info.get("serviceCount"),
                "shareUnit": main_holder_info.get("shareUnit"),
                "name": main_holder_info.get("name"),
                "mtenPercent": main_holder_info.get("mtenPercent"),
                "graphId": main_holder_info.get("graphId"),
                "alias": main_holder_info.get("alias"),
                "companyType": main_holder_info.get("companyType"),
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
        ex = conn.sadd("main_holder_id", tyc_id)
        if ex == 1:
            data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
            logger.warning("当前企业名称为%s" % company_name)
            tyc_hi = data["data"]["tyc_hi"]
            Authorization = data["data"]["Authorization"]
            duid = data["data"]["duid"]
            deviceID = data["data"]["deviceID"]
            x_auth_token = data["data"]["x_auth_token"]
            items = get_main_holder_info(
                info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token
            )
            try:
                for item in items:
                    mq.insert_sql("t_zx_company_main_holder_info_0321", item)
                    logger.info("数据 %s 插入成功" % item)
            except Exception as e:
                logger.debug(e)
            else:
                pass
        else:
            logger.debug("%s---------数据已经采集，无需再次采集" % tyc_id)
    mq.close()


if __name__ == "__main__":
    main()
