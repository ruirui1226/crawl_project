#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/6/1 14:10
@Author : xushaowei
@File : tyc_get_litigationrelationshio_detail.py
@Desc :
@Software:PyCharm
"""
# 涉诉关系详情
import re
import requests
import json

import urllib3
import os, time, math
from untils.pysql import *
from tyc_judicial_risk_data.tyc_distribute_task import task_distribution
from untils.redis_conn import r
from untils.urls import LITIGATIONRELATIONSHIP_LIST, LITIGATIONRELATIONSHIP_DETAILS

# 忽略requests证书警告
try:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_authoriaztion_detail(info_id, company_name, tyc_id, pageNum, oppositeGid, subjectType, caseCount):
    version = "Android 12.67.0"
    url = LITIGATIONRELATIONSHIP_DETAILS.format(pageNum, oppositeGid, subjectType, tyc_id, caseCount)
    data = {"url": url, "version": version}
    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    data = json.loads(r.text)
    return data


def get_litigationrelationship_nextdetail(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID,
                                          x_auth_token, pageNum, oppositeGid, subjectType, caseCount):
    try:
        data = get_authoriaztion_detail(info_id, company_name, tyc_id, pageNum, oppositeGid, subjectType, caseCount)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
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
        url = LITIGATIONRELATIONSHIP_DETAILS.format(pageNum, oppositeGid, subjectType, tyc_id, caseCount)
        res = requests.get(url, headers=headers, verify=False, timeout=10).text
        res_json = json.loads(res)
        res_nextitem = detail_ftp(info_id, company_name, tyc_id, res_json)
        return res_nextitem
    except Exception as e:
        logger.debug(e)
def get_litigationrelationship_info(
    info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, pageNum, oppositeGid, subjectType, caseCount
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
        url = LITIGATIONRELATIONSHIP_DETAILS.format(pageNum, oppositeGid, subjectType, tyc_id, caseCount)
        res = requests.get(url, headers=headers, verify=False, timeout=10).text
        res_json = json.loads(res)
        pages_total = None
        try:
            if res_json["data"]["count"]:
                if int(res_json["data"]["count"]) > 0:
                    pages_total = math.ceil(int(res_json["data"]["count"]) / 20)
                else:
                    logger.info("%s没有涉诉关系详情目录" % company_name)
                    pass
            else:
                logger.warning(res_json["data"]["count"])
                return
        except Exception as e:
            logger.debug(e)
        if pages_total == 1:
            res_thisitem = detail_ftp(info_id, company_name, tyc_id, res_json)
            return res_thisitem
        elif pages_total > 1:
            res_json_next = []
            res_thisitem = detail_ftp(info_id, company_name, tyc_id, res_json)
            for oneitem in res_thisitem:
                res_json_next.append(oneitem)
            for pageNum in range(2, pages_total + 1):
                items = get_litigationrelationship_nextdetail(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, pageNum, oppositeGid, subjectType, caseCount)
                for item in items:
                    res_json_next.append(item)
            return res_json_next
        else:
            logger.info("%s涉诉关系页数pages_total_BUG" % company_name)
    except Exception as e:
        logger.debug(e)

def detail_ftp(info_id, company_name, tyc_id, items):
    res = []
    for res_json in items['data']['items']:
        try:
            if True is res_json.get("hasCaseExplanation"):
                hasCaseExplanation = 1
            else:
                hasCaseExplanation = 0
            if True is res_json.get("isCaseClosed"):
                isCaseClosed = 1
            else:
                isCaseClosed = 0
            item = {
                "tyc_id": tyc_id,
                "info_id": info_id,
                "companyName": company_name,
                "caseTitle": res_json.get('caseTitle'),
                "caseCodeList": str(res_json.get("caseCodeList")).replace("'", '"'),
                "caseReason": res_json.get("caseReason"),
                "caseType": res_json.get("caseType"),
                "courtList": str(res_json.get("courtList")).replace("'", '"'),
                "hasCaseExplanation": hasCaseExplanation,
                "case_id": res_json.get("id"),
                "isCaseClosed": isCaseClosed,
                "sameSerialCaseCount": str(res_json.get("sameSerialCaseCount")),
                "trialProcedure": res_json.get("trialProcedure"),
                "trialProcedureDetail": str(res_json.get("trialProcedureDetail")).replace("'", '"'),
                "trialTime": res_json.get("trialTime"),
                "uuid": res_json.get("uuid"),
                "labels": str(res_json.get("labels")).replace("'", '"'),
                "caseIdentityList": str(res_json.get("caseIdentityList")).replace("'", '"'),
            }
            res.append(item)
        except:
            logger.debug("数据重复")
    return res
def main():
    table_name = "t_zx_company_judicial_litigationrelationship_list_info"
    redis_key = "tyc_task_litigationrelationship_detail"
    sel_data = ["id", "company_name", "tyc_id", "oppositeGid", "subjectType", "caseCount"]
    task_distribution(table_name, sel_data, {"is_crawl": 'zjtx_2023', "state": 0}, redis_key)
    nums = r.scard(redis_key)
    for num in range(1, nums + 1):
        data = r.spop(redis_key).strip("()").split(",")
        info_id = int(data[0])
        company_name = data[1].replace("'", "").replace(" ", "")
        tyc_id = data[2].replace("'", "").replace(" ", "")
        oppositeGid = data[3].replace("'", "").replace(" ", "")
        subjectType = data[4].replace("'", "").replace(" ", "")
        caseCount = data[5].replace("'", "").replace(" ", "")
        mq = MysqlPipelinePublic()
        pageNum = 1
        data = get_authoriaztion_detail(info_id, company_name, tyc_id, pageNum, oppositeGid, subjectType, caseCount)
        logger.info("当前企业名称为%s" % company_name + ",第%s个详情" % num + "总计%s个详情" % nums)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        items = get_litigationrelationship_info(
            info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, pageNum, oppositeGid, subjectType, caseCount
        )
        if items:
            try:
                mq.insert_all_sql("t_zx_company_judicial_litigationrelationship_info", items)
                logger.info("当前item数据为%s------------->" % items)
            except Exception as e:
                logger.debug(e)
            mq.update_sql(table_name, {"state": 1}, {"id": info_id})
            logger.info("更新任务成功")
        else:
            mq.update_sql(table_name, {"state": -1}, {"id": info_id})
            logger.info(
                "当前企业名称为%s" % company_name + "第%s" % num + "总计%s" % nums + "========涉诉关系无数据======="
            )
        mq.close()

if __name__ == "__main__":
    main()
