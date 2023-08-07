#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/6/5 9:45
@Author : xushaowei
@File : tyc_get_financialblacklist_detail.py
@Desc :
@Software:PyCharm
"""
# 涉金融黑名单详情
import requests
import json

import urllib3
from loguru import logger
import os, time, math
import uuid
from conf.env import *
from untils.pysql import *
from tyc_judicial_risk_data.tyc_distribute_task import task_distribution
from untils.redis_conn import r
from untils.urls import FINANCIALBLACKLIST_LIST, FINANCIALBLACKLIST_DETAILS

# 忽略requests证书警告
try:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_detail_json(info_id, tyc_id, company_name, res_json, businessId):
    # 数据入库
    """"""
    try:
        item = {
            "tyc_id": tyc_id,
            "info_id": info_id,
            "company_name": company_name,
            "businessId": businessId,
            "jkptmc": res_json.get("data").get("jkptmc", ""),
            "gid": res_json.get("data").get("gid"),
            "ah": res_json.get("data").get("ah", ""),
            "involvedType": res_json.get("data").get("involvedType", ""),
            "qymc": res_json.get("data").get("qymc", ""),
            "tyshxydm": res_json.get("data").get("tyshxydm", ""),
            "pjzcjg": res_json.get("data").get("pjzcjg"),
            "zm": res_json.get("data").get("zm", ""),
            "showType": res_json.get("data").get("showType"),
            "fddbr": res_json.get("data").get("fddbr", ""),
            "financial_id": res_json.get("data").get("id"),
            "dataSource": res_json.get("data").get("dataSource", ""),
            "zzjgdm": res_json.get("data").get("zzjgdm", ""),
        }
        return item
    except IntegrityError as f:
        logger.debug("数据重复")



def get_authoriaztion_detail(info_id, company_name, tyc_id, pageNum, businessId):
    version = "Android 12.67.0"
    url = FINANCIALBLACKLIST_DETAILS.format(tyc_id, businessId)
    data = {"url": url, "version": version}
    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    data = json.loads(r.text)
    return data


def get_financialblacklist_detail_info(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, businessId):
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
        url = FINANCIALBLACKLIST_DETAILS.format(tyc_id, businessId)
        res = requests.get(url, headers=headers, verify=False, timeout=10).text
        items = json.loads(res)
        res_json = create_detail_json(info_id, tyc_id, company_name, items, businessId)
        return res_json

    except Exception as e:
        logger.debug(e)


def main():
    table_name = "t_zx_company_judicial_financialblacklist_list_info"
    redis_key = "tyc_task_financialblacklist_detail"
    sel_data = ['id', 'company_name', 'tyc_id', 'businessId']
    task_distribution(table_name, sel_data, {"is_cyl": 1, "state": 0}, redis_key)
    nums = r.scard(redis_key)
    for num in range(1, nums + 1):
        data = r.spop(redis_key).strip("()").split(",")
        info_id = int(data[0])
        company_name = data[1].replace("'", "").replace(" ", "")
        tyc_id = data[2].replace("'", "").replace(" ", "")
        businessId = data[3].replace("'", "").replace(" ", "")
        mq = MysqlPipelinePublic()
        pageNum = 1
        data = get_authoriaztion_detail(info_id, company_name, tyc_id, pageNum, businessId)
        logger.info("当前企业名称为%s" % company_name)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        items = get_financialblacklist_detail_info(
            info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, businessId
        )
        if items:
            try:
                mq.insert_sql("t_zx_company_judicial_financialblacklist_detail", items)
                logger.info("当前item数据为%s" % items)
            except Exception as e:
                logger.debug(e)
            mq.update_sql(table_name, {"state": 1}, {"id": info_id})
            logger.info("更新任务成功")
        else:
            mq.update_sql(table_name, {"state": -1}, {"id": info_id})
            logger.info(
                "当前企业名称为%s" % company_name + "第%s" % num + "总计%s" % nums + "========涉金融黑名单详情无数据======="
            )
        mq.close()

if __name__ == "__main__":
    main()
