#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/6/2 13:32
@Author : xushaowei
@File : tyc_get_judicialCase_detail.py
@Desc :
@Software:PyCharm
"""
# 司法解析详情
import re
import requests
import json

import urllib3
import os, time, math
from untils.pysql import *
from tyc_judicial_risk_data.tyc_distribute_task import task_distribution
from untils.redis_conn import r
from untils.urls import LITIGATIONRELATIONSHIP_LIST, LITIGATIONRELATIONSHIP_DETAILS, JUDICIALCASE_DETAILS

# 忽略requests证书警告
try:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_authoriaztion_detail():
    version = "Android 12.67.0"
    url = JUDICIALCASE_DETAILS
    data = {"url": url, "version": version}
    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    data = json.loads(r.text)
    return data

def create_judicialCase_detail(pageNum, info_id, tyc_id, company_name, res_json, uuid):
    # 数据入库
    try:
        if True is res_json.get("data").get("isCaseClosed"):
            isCaseClosed = 1
        else:
            isCaseClosed = 0
        if True is res_json.get("data").get("hasMonitor"):
            hasMonitor = 1
        else:
            hasMonitor = 0
        item = {
            "caseCodeList": str(res_json.get("data").get("caseCodeList")).replace("'", '"'),
            "tyc_id": tyc_id,
            "info_id": info_id,
            "companyName": res_json.get("data").get("companyName"),
            "caseTitle": res_json.get("data").get("caseTitle"),
            "uuid": res_json.get("data").get("uuid"),
            "caseReason": res_json.get("data").get("caseReason"),
            "isCaseClosed": isCaseClosed,
            "labels": str(res_json.get("data").get("labels")).replace("'", '"'),
            "caseType": res_json.get("data").get("caseType"),
            "hasMonitor": hasMonitor,
            "trialTime": res_json.get("data").get("trialTime"),
            "caseIdentity": str(res_json.get("data").get("caseIdentity")).replace("'", '"'),
            "case_id": res_json.get("data").get("id"),
            "items": str(res_json.get("data").get("items")).replace("'", '"'),
            "trialProcedure": res_json.get("data").get("trialProcedure"),
        }
        return item

    except:
        logger.debug("数据重复")

def get_judicialCase_detail_info(
    info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, pageNum, uuid
):
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
        data = {"cgid": tyc_id, "orderType": 1, "hgid": "0", "uuid": uuid}
        url = JUDICIALCASE_DETAILS
        res = requests.post(url, headers=headers, verify=False, data=json.dumps(data), timeout=10).text
        res_json = json.loads(res)
        item = create_judicialCase_detail(pageNum, info_id, tyc_id, company_name, res_json, uuid)
        return item

    except Exception as e:
        logger.debug(e)
def main():
    table_name = "t_zx_company_judicial_judicialcase_list_info"
    redis_key = "tyc_task_judicial_judicialcase_detail"
    sel_data = ["id", "company_name", "tyc_id", "uuid"]
    task_distribution(table_name, sel_data, {"is_crawl": 'zjtx_2023', "state": 0}, redis_key)
    nums = r.scard(redis_key)
    for num in range(1, nums + 1):
        data = r.spop(redis_key).strip("()").split(",")
        info_id = int(data[0])
        company_name = data[1].replace("'", "").replace(" ", "")
        tyc_id = data[2].replace("'", "").replace(" ", "")
        uuid = data[3].replace("'", "").replace(" ", "")
        mq = MysqlPipelinePublic()
        pageNum = 1
        data = get_authoriaztion_detail()
        logger.info("当前企业名称为%s" % company_name + ",第%s个详情" % num + "总计%s个详情" % nums)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        items = get_judicialCase_detail_info(
            info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, pageNum, uuid
        )
        if items:
            try:
                mq.insert_sql("t_zx_company_judicial_judicialcase_detail", items)
                logger.info("当前item数据为%s" % items)
            except Exception as e:
                logger.debug(e)
            mq.update_sql(table_name, {"state": 1}, {"id": info_id})
            logger.info("更新任务成功")
        else:
            mq.update_sql(table_name, {"state": -1}, {"id": info_id})
            logger.info(
                "当前企业名称为%s" % company_name + "第%s" % num + "总计%s" % nums + "========司法解析无数据======="
            )
        mq.close()

if __name__ == "__main__":
    main()
