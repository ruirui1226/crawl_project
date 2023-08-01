#!/usr/bin/conf python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/19 16:46
# @Author  : wym
# @File    : tyc_get_courtregister.py
# 立案信息
import requests
import json
import urllib3
import math

from tyc_judicial_risk_data.tyc_distribute_task import task_distribution
from untils.pysql import *
from untils.redis_conn import r
from untils.urls import COURTREGISTER_LIST

# 忽略requests证书警告
try:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    url = COURTREGISTER_LIST.format(pageNum, tyc_id)
    data = {"url": url, "version": version}
    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    data = json.loads(r.text)
    return data


def get_CourtRegister_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, pageNum):
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
        url = COURTREGISTER_LIST.format(pageNum, tyc_id)
        res = requests.get(url=url, headers=headers, verify=False).text
        res_json = json.loads(res)

        if int(res_json["data"]["total"]) > 0:
            pages_total = math.ceil(int(res_json["data"]["total"]) / 20)
            if pages_total:
                return pages_total
        elif "total" in str(res_json["data"]):
            pages_total = math.ceil(int(res_json["data"]["total"]) / 20)

            if pages_total:
                return pages_total
        else:
            logger.debug("%s立案信息数据" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_CourtRegister_info(info_id, company_name, tyc_id, pageNum):
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
    url = COURTREGISTER_LIST.format(pageNum, tyc_id)
    res = requests.get(url=url, headers=headers, verify=False).text
    res_json = json.loads(res)

    items = []
    for CourtRegister_info in res_json["data"]["result"]:
        item = {
            "info_id": info_id,
            "tyc_id": tyc_id,
            "getcourtreg_id": CourtRegister_info.get("id"),
            "plaintiffList": str(CourtRegister_info.get("plaintiffList")).replace("'", '"'),
            "litigantGids": CourtRegister_info.get("litigantGids", ""),
            "litigant": CourtRegister_info.get("litigant", ""),
            "filingDate": CourtRegister_info.get("filingDate", ""),
            "caseStatus": CourtRegister_info.get("caseStatus", ""),
            "businessId": CourtRegister_info.get("busnessIid", ""),
            "source": CourtRegister_info.get("source", ""),
            "content": CourtRegister_info.get("content", ""),
            "caseType": CourtRegister_info.get("caseType", ""),
            "sourceUrl": CourtRegister_info.get("sourceUrl", ""),
            "isDeleted": CourtRegister_info.get("isDeleted"),  # TINYINT
            "defendant": CourtRegister_info.get("defendant", ""),
            "startTime": CourtRegister_info.get("startTime", ""),
            "department": CourtRegister_info.get("department", ""),
            "defendantList": str(CourtRegister_info.get("defendantList")).replace("'", '"'),
            "area": CourtRegister_info.get("area", ""),
            "plaintiff": CourtRegister_info.get("plaintiff", ""),
            "assistant": CourtRegister_info.get("assistant", ""),
            "court": CourtRegister_info.get("court", ""),
            "caseNo": CourtRegister_info.get("caseNo", ""),
            "caseReason": CourtRegister_info.get("caseReason", ""),
            "closeDate": CourtRegister_info.get("closeDate", ""),
            "third": CourtRegister_info.get("third", ""),
            "createTime": CourtRegister_info.get("createTime", ""),
            "cid": CourtRegister_info.get("cid"),
            "total": res_json["data"]["total"],
            "company_name": company_name,
        }
        items.append(item)

    return items


def main():
    table_name = "t_zx_company_tyc_all_infos_caseinformation"
    redis_key = "tyc_task_caseinformation"
    sel_data = ['id', 'company_name', 'tyc_id']
    task_distribution(table_name, sel_data, {"is_crawl": 'zjtx_2023', "state": 0}, redis_key)
    nums = r.scard(redis_key)
    for num in range(1, nums + 1):
        data = r.spop(redis_key).strip("()").split(",")
        info_id = int(data[0])
        company_name = data[1].replace("'", "").replace(" ", "")
        tyc_id = data[2].replace("'", "").replace(" ", "")
        mq = MysqlPipelinePublic()
        pageNum = 1
        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        logger.info("当前企业名称为%s" % company_name + ",第%s个企业" % num + "总计%s个企业" % nums)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        pages_total = get_CourtRegister_page(
            info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, pageNum
        )
        if pages_total:
            for pageNum in range(1, int(pages_total) + 1):
                items = get_CourtRegister_info(info_id, company_name, tyc_id, pageNum)
                try:
                    for item in items:
                        mq.insert_sql("t_zx_company_judicial_caseinformation_info", item)
                        logger.info("插入成功----------数据 %s " % item)
                except Exception as e:
                    logger.debug(e)
            mq.update_sql(table_name, {"state": 1}, {"id": info_id})
            logger.info("更新任务成功")
        else:
            mq.update_sql(table_name, {"state": -1}, {"id": info_id})
            logger.info(
                "当前企业名称为%s" % company_name + ",第%s个企业" % num + "总计%s个企业" % nums + "========立案信息无数据=======更新任务成功"
            )
        mq.close()


if __name__ == "__main__":
    main()
