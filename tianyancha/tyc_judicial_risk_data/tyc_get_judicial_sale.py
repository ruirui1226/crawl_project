#!/usr/bin/conf python
# -*- coding: utf-8 -*-
"""
@desc: tianyancha-司法拍卖
@version: python3
@author: shenr / xushaowei
@time: 2023/05/24
"""

import requests
import json

import uuid
from loguru import logger
import os
import time
import math
from untils.pysql import *
from untils.urls import JUDICIAL_SALE
from tyc_judicial_risk_data.tyc_distribute_task import task_distribution

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from untils.redis_conn import r

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



def get_authoriaztion(tyc_id, pageNum):
    version = "Android 12.67.0"
    url = JUDICIAL_SALE.format(tyc_id, pageNum)
    data = {"url": url, "version": version}
    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    data = json.loads(r.text)
    return data


def list_json(tyc_id, info_id, company_name, pageNum, pages_total, res_json):
    try:
        items = []
        for res in res_json['data']['resultList']:
            item = {
                "tyc_id": tyc_id,
                "company_name": company_name,
                "info_id": info_id,
                "pageNum": pageNum,
                "pages_total": pages_total,
                "h5Url": res.get('h5Url'),
                "auctionStage": res.get('auctionStage'),
                "auctionItem": res.get('auctionItem'),
                "businessId": res.get('businessId'),
                "priceEvaluated": res.get('priceEvaluated'),
                "priceStart": res.get('priceStart'),
                "court": res.get('court'),
                "title": res.get('title'),
                "auctionDate": res.get('auctionDate'),
            }
            items.append(item)
        return items

    except Exception as e:
        logger.debug(e)


def get_judicial_sale_nextpage(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token,
                               nextpageNum, pages_total):
    try:
        data = get_authoriaztion(tyc_id, nextpageNum)
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
        url = JUDICIAL_SALE.format(tyc_id, nextpageNum)
        res = requests.get(url=url, headers=headers, verify=False).text
        res_json = json.loads(res)
        res_thisitem = list_json(tyc_id, info_id, company_name, nextpageNum, pages_total, res_json)
        return res_thisitem
    except Exception as e:
        logger.debug(e)


def get_judicial_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, pageNum):
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
    url = JUDICIAL_SALE.format(tyc_id, pageNum)
    res = requests.get(url=url, headers=headers, verify=False).text
    res_json = json.loads(res)
    pages_total = None
    try:
        if 'data' in res_json:
            if res_json["data"]["total"]:
                if int(res_json["data"]["total"]) > 0:
                    pages_total = math.ceil(int(res_json["data"]["total"]) / 20)
                else:
                    logger.info("%s没有司法拍卖目录" % company_name)
                    pass
            else:
                logger.warning(res_json["data"]["total"])
                return
        else:
            logger.warning(res_json)
            return
    except Exception as e:
        logger.debug(e)
    if pages_total == 1:
        res_thisitem = list_json(tyc_id, info_id, company_name, pageNum, pages_total, res_json)
        return res_thisitem
    elif pages_total > 1:
        res_json_next = []
        res_thisitem = list_json(tyc_id, info_id, company_name, pageNum, pages_total, res_json)
        for oneitem in res_thisitem:
            res_json_next.append(oneitem)
        for nextpageNum in range(2, pages_total + 1):
            items = get_judicial_sale_nextpage(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID,
                                              x_auth_token, nextpageNum, pages_total)
            for item in items:
                res_json_next.append(item)
        return res_json_next
    else:
        logger.info("%s没有司法拍卖目录" % company_name)


def main():
    table_name = "t_zx_company_tyc_all_infos_judicialsale"
    redis_key = "tyc_task_judicialsale"
    sel_data = ['id', 'company_name', 'tyc_id']
    task_distribution(table_name, sel_data, {"is_cyl": 1, "state": 0}, redis_key)
    nums = r.scard(redis_key)
    for num in range(1, nums + 1):
        data = r.spop(redis_key).strip("()").split(",")
        info_id = int(data[0])
        company_name = data[1].replace("'", "").replace(" ", "")
        tyc_id = data[2].replace("'", "").replace(" ", "")
        mq = MysqlPipelinePublic()
        logger.info("当前企业名称为%s" % company_name + ",第%s个企业" % num + "总计%s个企业" % nums)
        pageNum = 1
        data = get_authoriaztion(tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        items = get_judicial_page(
            info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, pageNum
        )
        if items:
            try:
                mq.insert_all_sql("t_zx_company_judicial_judicialsale_info", items)
                logger.info("当前item数据为%s" % items)
            except Exception as e:
                logger.debug(e)
            mq.update_sql(table_name, {"state": 1}, {"id": info_id})
            logger.info("更新任务成功")
        else:
            mq.update_sql(table_name, {"state": -1}, {"id": info_id})
            logger.info(
                "当前企业名称为%s" % company_name + "第%s" % num + "总计%s" % nums + "========司法拍卖无数据======="
            )
        mq.close()

if __name__ == "__main__":
    main()
