#!/usr/bin/conf python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/19 16:39
# @Author  : wym / xushaowei
# @File    : tyc_get_announcement_info.py
# 开庭公告

import requests
import json
import math

from tyc_judicial_risk_data.tyc_distribute_task import task_distribution
from untils.pysql import *
import urllib3

from untils.redis_conn import conn, r
from untils.urls import ANNOUNCEMENT_LIST

# 忽略requests证书警告
try:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    url = ANNOUNCEMENT_LIST.format(tyc_id, pageNum)
    data = {"url": url, "version": version}
    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    data = json.loads(r.text)
    return data


def get_announcement_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, pageNum):
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
        url = ANNOUNCEMENT_LIST.format(tyc_id, pageNum)
        res = requests.get(url=url, headers=headers, verify=False).text
        res_json = json.loads(res)
        if "total" in str(res_json["data"]):
            pages_total = math.ceil(int(res_json["data"]["total"]) / 20)

            if pages_total:
                return pages_total
        elif int(res_json["data"]["count"]) > 0:
            pages_total = math.ceil(int(res_json["data"]["count"]) / 20)
            if pages_total:
                return pages_total

        else:
            logger.info("%s开庭公告数据" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_announcement_info(info_id, company_name, tyc_id, pageNum):
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
    url = ANNOUNCEMENT_LIST.format(tyc_id, pageNum)
    res = requests.get(url=url, headers=headers, verify=False).text
    res_json = json.loads(res)
    items = []
    for announcement_info in res_json["data"]["resultList"]:
        item = {
            "info_id": info_id,
            "tyc_id": tyc_id,
            "area": announcement_info.get("area", ""),
            "plaintiff": " ".join([plaintiff.get("name", "") for plaintiff in announcement_info["plaintiff"]]),
            "litigant": announcement_info.get("litigant", ""),
            "businessId": announcement_info.get("businessId", ""),
            "court": announcement_info.get("court", ""),
            "caseNo": announcement_info.get("caseNo", ""),
            "caseReason": announcement_info.get("caseReason", ""),
            "contractors": announcement_info.get("contractors", ""),
            "courtroom": announcement_info.get("courtroom", ""),
            "defendant": " ".join([defendant.get("name", "") for defendant in announcement_info["defendant"]]),
            "eventTime": announcement_info.get("eventTime", ""),
            "announcement_id": announcement_info.get("id", ""),
            "judge": announcement_info.get("judge", ""),
            "startDate": announcement_info.get("startDate", ""),
            "total": res_json["data"]["count"],
            "company_name": company_name,
        }
        items.append(item)
    return items


def main():
    table_name = "t_zx_company_tyc_all_infos_announcement"
    redis_key = "tyc_task_announcement"
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
        pages_total = get_announcement_page(
            info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, pageNum
        )
        if pages_total:
            for pageNum in range(1, int(pages_total) + 1):
                items = get_announcement_info(info_id, company_name, tyc_id, pageNum)
                try:
                    for item in items:
                        mq.insert_sql("t_zx_company_judicial_announcement_info", item)
                        logger.info("插入成功---------------------数据 %s " % item)
                except Exception as e:
                    logger.debug(e)
            mq.update_sql(table_name, {"state": 1}, {"id": info_id})
            logger.info("更新任务成功")
        else:
            mq.update_sql(table_name, {"state": -1}, {"id": info_id})
            logger.info("当前企业名称为%s" % company_name + ",第%s个企业" % num + "总计%s个企业" % nums + "========开庭公告无数据======更新任务成功")
        mq.close()


if __name__ == "__main__":
    main()
