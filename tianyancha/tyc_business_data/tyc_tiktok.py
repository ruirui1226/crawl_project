#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/5/26 14：34
@Author : QTH
@File : tyc_on_the_list.py
@Desc : 天眼查--抖音
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

from untils.redis_conn import conn
from untils.urls import PUBLICITY_OF_LAND_PLOtS, GENERAL_TAXPAYER, DOUYIN_LIST

from untils.sql_data import TYC_DATA

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/jsondata/tyc_tiktok_file__抖音/"
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

    logger.debug(("--tyc_tiktok_file__抖音__写入-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    # url = "https://api6.tianyancha.com/cloud-business-state/livebroad/list?gid={}&pageSize=20&type=1&pageNum={}".format(
    #     tyc_id, pageNum
    # )
    url = DOUYIN_LIST.format(tyc_id, pageNum)
    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9964/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)

    return data


def get_tyc_tiktok_info(info_id, company_name, tyc_id, pageNum):
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

        # url = "https://api6.tianyancha.com/cloud-business-state/livebroad/list?gid={}&pageSize=20&type=1&pageNum={}".format(
        #     tyc_id, pageNum
        # )
        url = DOUYIN_LIST.format(tyc_id, pageNum)
        res = requests.get(url=url, headers=headers, verify=False).text
        logger.debug(res)
        res_json = json.loads(res)
        # create_json(pageNum, info_id, tyc_id, company_name, res_json)
        items_list = res_json["data"]["list"]
        items = []
        for ite in items_list:
            item = {
                "info_id": str(info_id),
                "name": ite.get("name", ""),
                "gid": ite.get("gid", ""),
                "logo": ite.get("logo", ""),
                "accountNum": ite.get("accountNum", ""),
                "recommend": str(ite.get("recommend", "")),
                "businessId": ite.get("businessId", ""),
                "company_name": company_name,
                "tyc_id": tyc_id,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            }

            items.append(item)

        return items

    except Exception as e:
        conn.srem("tyc_tiktok", tyc_id)
        logger.debug(e)


def main():
    mq = MysqlPipelinePublic()
    data_list = TYC_DATA
    for data in data_list:
        info_id = data.get("id")
        company_name = data.get("co_name")
        tyc_id = data.get("co_id")
        pageNum = 1
        ex = conn.sismember("tyc_tiktok", tyc_id)
        if ex:
            logger.debug("%s---------数据已经采集，无需再次采集" % tyc_id)
        else:
            conn.sadd("tyc_tiktok", tyc_id)
            logger.warning("当前企业名称为-------%s" % company_name)
            items = get_tyc_tiktok_info(info_id, company_name, tyc_id, pageNum)
            try:
                for item in items:
                    mq.insert_sql("t_zx_tyc_tiktok", item)
                    logger.info("数据 %s 插入成功" % item)
            except Exception as e:
                logger.debug(e)
    mq.close()


if __name__ == "__main__":
    main()
