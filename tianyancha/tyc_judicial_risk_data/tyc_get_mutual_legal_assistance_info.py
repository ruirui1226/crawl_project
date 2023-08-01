#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/5/24 18:05
@Author : xushaowei
@File : tyc_get_mutual_legal_assistance_info.py
@Desc :
@Software:PyCharm
"""
# 司法协助
import requests
import json

import urllib3
import os, time, math
from tianyancha.untils.pysql import *
from tyc_judicial_risk_data.tyc_distribute_task import task_distribution
from untils.redis_conn import r
from untils.urls import MUTUALLEGALASSISTANCE_LIST, MUTUALLEGALASSISTANCE_DETAILS

# 忽略requests证书警告
try:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_detail_json(pageNum, info_id, tyc_id, company_name, res_json, assId):
    # 数据入库
    """"""
    try:
        res = res_json.get("data").get("frozen")
        item = {
            "tyc_id": tyc_id,
            "info_id": info_id,
            "company_name": company_name,
            "assId": assId,
            "executeNoticeNum": res.get("executeNoticeNum"),
            "period": res.get("period"),
            "toDate": res.get("toDate"),
            "executedPersonCid": res.get("executedPersonCid"),  # int
            "stockExecutedType": res.get("stockExecutedType"),  # int
            "executeOrderNum": res.get("executeOrderNum"),
            "stockExecutedCompany": res.get("stockExecutedCompany"),
            "licenseNum": res.get("licenseNum"),
            "equityAmountOther": res.get("equityAmountOther"),
            "publicityAate": res.get("publicityAate"),
            "stockExecutedHgid": res.get("stockExecutedHgid"),
            "stockExecutedCid": res.get("stockExecutedCid"),  # int
            "executedPerson": res.get("executedPerson"),
            "fromDate": res.get("fromDate"),
            "licenseType": res.get("licenseType"),
            "implementationMatters": res.get("implementationMatters"),
            "executedPersonType": res.get("executedPersonType"),  # int
            "executiveCourt": res.get("executiveCourt"),
        }
        return item
    except IntegrityError as f:
        logger.warning("数据重复")


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    url = MUTUALLEGALASSISTANCE_LIST.format(tyc_id, pageNum)
    data = {"url": url, "version": version}
    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    data = json.loads(r.text)
    return data


def get_mutuallegalassistance_page(
    info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, pageNum
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
        url = MUTUALLEGALASSISTANCE_LIST.format(tyc_id, pageNum)
        res = requests.get(url, headers=headers, verify=False, timeout=10).text
        res_json = json.loads(res)

        if "totalCount" in str(res_json["data"]):
            pages_total = math.ceil(int(res_json["data"]["totalCount"]) / 20)

            if pages_total:
                return pages_total
        elif int(res_json["data"]["count"]) > 0:
            pages_total = math.ceil(int(res_json["data"]["count"]) / 20)
            if pages_total:
                return pages_total

        else:
            logger.warning("%s没有司法协助案件目录" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_mutuallegalassistance_info(info_id, company_name, tyc_id, pageNum):
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
        url = MUTUALLEGALASSISTANCE_LIST.format(tyc_id, pageNum)
        res = requests.get(url, headers=headers, verify=False, timeout=10).text
        res_json = json.loads(res)
        return res_json

    except Exception as e:
        logger.debug(e)


def get_mutuallegalassistance_detail_info(info_id, company_name, tyc_id, pageNum, assId):
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
        url = MUTUALLEGALASSISTANCE_DETAILS.format(assId)
        res = requests.get(url, headers=headers, verify=False, timeout=10).text
        res_json = json.loads(res)
        return res_json
    except Exception as e:
        logger.debug(e)


def main():
    table_name = "t_zx_company_tyc_all_infos_mutuallegalassistance"  # 任务表
    redis_key = "tyc_task_mutuallegalassistance"
    sel_data = ['id', 'company_name', 'tyc_id']
    task_distribution(table_name, sel_data, {"is_lz": 1, "state": 0}, redis_key)
    nums = r.scard(redis_key)
    for num in range(1, nums + 1):
        data = r.spop(redis_key).strip("()").split(",")
        info_id = int(data[0])
        company_name = data[1].replace("'", "").replace(" ", "")
        tyc_id = data[2].replace("'", "").replace(" ", "")
        mq = MysqlPipelinePublic()
        pageNum = 1
        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        logger.info("当前企业名称为%s" % company_name)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        pages_total = get_mutuallegalassistance_page(
            info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, pageNum
        )
        if pages_total:
            for pageNum in range(1, int(pages_total) + 1):
                res_json = get_mutuallegalassistance_info(info_id, company_name, tyc_id, pageNum)
                if res_json["data"]["list"]:
                    for assId in res_json["data"]["list"]:
                        assId = assId["assId"]
                        items = get_mutuallegalassistance_detail_info(info_id, company_name, tyc_id, pageNum, assId)
                        item = create_detail_json(pageNum, info_id, tyc_id, company_name, items, assId)
                        mq.insert_sql(
                            "t_zx_company_judicial_mutuallegalassistance_info", item
                        )  # 此处不可以用上面的table_name这里插入的是结果表，上面的table_name是任务表
                        logger.info("当前item数据为%s------------->" % item)
                else:
                    mq.update_sql(table_name, {"state": -1}, {"id": info_id})
                    logger.info("当前企业名称为%s" % company_name + "========司法协助无数据=======更新任务成功")
            mq.update_sql(table_name, {"state": 1}, {"id": info_id})
            logger.info("更新任务成功")
        else:
            mq.update_sql(table_name, {"state": -1}, {"id": info_id})
            logger.info("当前企业名称为%s" % company_name + "========司法协助无数据=======更新任务成功")


if __name__ == "__main__":
    main()
