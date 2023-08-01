#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/5/22 17:08
@Author : xushaowei
@File : tyc_get_limit_consumption_info.py
@Desc :
@Software:PyCharm
"""
# 限制消费令
import re
import requests
import json

import urllib3
import os, time, math
from tianyancha.untils.pysql import *
from tyc_judicial_risk_data.tyc_distribute_task import task_distribution
from untils.redis_conn import r
from untils.urls import LIMIT_CONSUMPTION_LIST

# 忽略requests证书警告
try:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    url = LIMIT_CONSUMPTION_LIST.format(tyc_id, pageNum)
    data = {"url": url, "version": version}
    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    data = json.loads(r.text)
    return data


def get_limitconsumption_page(
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
        url = LIMIT_CONSUMPTION_LIST.format(tyc_id, pageNum)
        res = requests.get(url, headers=headers, verify=False, timeout=10).text
        res_json = json.loads(res)
        try:
            if "caseCount" in str(res_json["data"]["caseCount"]):
                pages_total = math.ceil(int(res_json["data"]["caseCount"]) / 20)

                if pages_total:
                    return pages_total
            elif int(res_json["data"]["count"]) > 0:
                pages_total = math.ceil(int(res_json["data"]["count"]) / 20)
                if pages_total:
                    return pages_total
            else:
                logger.info("%s没有限制消费令目录" % company_name)
                pass
        except:
            if int(res_json["data"]["count"]) > 0:
                pages_total = math.ceil(int(res_json["data"]["count"]) / 20)
                if pages_total:
                    return pages_total
            else:
                logger.info("%s没有限制消费令目录" % company_name)
                pass

    except Exception as e:
        logger.debug(e)


def get_limitconsumption_info(info_id, company_name, tyc_id, pageNum):
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
        url = LIMIT_CONSUMPTION_LIST.format(tyc_id, pageNum)
        res = requests.get(url, headers=headers, verify=False, timeout=10).text
        res_json = json.loads(res)
        items = []
        for item in res_json["data"]["items"]:
            url = item.get(
                "detailUrl",
                "",
            )
            res = requests.get(url, verify=False).text
            if re.findall('<div class="content">(.*?)</div></div></div>', res, re.S):
                lawsuitData = re.findall('<div class="content">(.*?)</div></div></div>', res, re.S)[0]
            else:
                lawsuitData = None
            item = {
                "info_id": info_id,
                "tyc_id": tyc_id,
                "caseCode": item.get("caseCode"),
                "serviceType": item.get("serviceType"),
                "gid": item.get("gid"),
                "qyinfoToco": item.get("qyinfoToco"),
                "applicantList": str(item.get("applicantList")).replace("'", '"'),
                "publishDate": item.get("publishDate"),
                "businessId": item.get("businessId"),
                "type": item.get("type"),
                "xname": item.get("xname"),
                "toco": item.get("toco"),
                "caseCreateTime": item.get("caseCreateTime", ""),
                "logo": item.get("logo"),
                "alias": item.get("alias"),
                "limit_list_id": item.get("id"),
                "qyinfoGid": item.get("qyinfoGid"),
                "ossPath": item.get("ossPath"),
                "qyinfoCid": item.get("qyinfoCid"),
                "zhixingId": item.get("zhixingId"),
                "filePath": item.get("filePath"),
                "webDetailUrl": item.get("webDetailUrl"),
                "qyinfoType": item.get("qyinfoType"),
                "applicant": item.get("applicant"),
                "qyinfoAlias": item.get("qyinfoAlias"),
                "serviceCount": item.get("serviceCount"),
                "hasOssPath": item.get("hasOssPath"),
                "qyinfo": item.get("qyinfo"),
                "explainMessage": item.get("explainMessage"),
                "qyinfoLogo": item.get("qyinfoLogo"),
                "detailUrl": item.get("detailUrl"),
                "cid": item.get("cid"),
                "lawsuitData": lawsuitData,
            }
            items.append(item)
            return items
    except Exception as e:
        logger.debug(e)


def main():
    table_name = "t_zx_company_tyc_all_infos_limitconsumption"
    redis_key = "tyc_task_limitconsumption"
    sel_data = ['info_id', 'company_name', 'tyc_id']
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
        pages_total = get_limitconsumption_page(
            info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, pageNum
        )
        if pages_total:
            for pageNum in range(1, int(pages_total) + 1):
                items = get_limitconsumption_info(info_id, company_name, tyc_id, pageNum)
                try:
                    for item in items:
                        mq.insert_sql("t_zx_company_judicial_limitconsumption_info", item)
                        logger.info("当前item数据为%s------------->" % item)
                except Exception as e:
                    logger.debug(e)
            mq.update_sql(table_name, {"state": 1}, {"id": info_id})
            logger.info("更新任务成功")
        else:
            mq.update_sql(table_name, {"state": -1}, {"id": info_id})
            logger.info(
                "当前企业名称为%s" % company_name + ",第%s个企业" % num + "总计%s个企业" % nums + "========限制消费令无数据=======更新任务成功"
            )
        mq.close()


if __name__ == "__main__":
    main()
