#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/6/5 10:36
@Author : xushaowei
@File : tyc_get_mutual_legal_assistance_list.py
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

def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    url = MUTUALLEGALASSISTANCE_LIST.format(tyc_id, pageNum)
    data = {"url": url, "version": version}
    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    data = json.loads(r.text)
    return data


def list_json(tyc_id, info_id, company_name, pageNum, pages_total, res_json, is_lz, is_cyl, is_crawl):
    items = res_json['data']['list']
    res_js = []
    for res in items:
        item = {
            "tyc_id": tyc_id,
            "info_id": info_id,
            "company_name": company_name,
            "pageNum": pageNum,
            "pages_total": pages_total,
            "is_lz": is_lz,
            "is_cyl": is_cyl,
            "is_crawl": is_crawl,
            "executeNoticeNum": res.get('executeNoticeNum'),
            "publicityDate": res.get('publicityDate'),
            "stockExecutedType": res.get('stockExecutedType'),
            "executedPersonCid": res.get('executedPersonCid'),
            "businessId": res.get('businessId'),
            "stockExecutedCompany": res.get('stockExecutedCompany'),
            "type": res.get('type'),
            "stockExecutedHgid": res.get('stockExecutedHgid'),
            "stockExecutedCid": res.get('stockExecutedCid'),
            "assId": res.get('assId'),
            "executedPerson": res.get('executedPerson'),
            "equityAmount": res.get('equityAmount'),
            "explainMessage": res.get('explainMessage'),
            "list_id": res.get('id'),
            "state_list": res.get('state'),
            "mainId": res.get('mainId'),
            "executedPersonType": res.get('executedPersonType'),
            "typeState": res.get('typeState'),
            "executiveCourt": res.get('executiveCourt')
        }
        res_js.append(item)
    return res_js


def get_mutuallegalassistance_nextpage(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID,
                                       x_auth_token, nextpageNum, pages_total, is_lz, is_cyl, is_crawl):
    try:
        data = get_authoriaztion(info_id, company_name, tyc_id, nextpageNum)
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
        url = MUTUALLEGALASSISTANCE_LIST.format(tyc_id, nextpageNum)
        res = requests.get(url, headers=headers, verify=False, timeout=10).text
        res_json = json.loads(res)
        res_thisitem = list_json(tyc_id, info_id, company_name, nextpageNum, pages_total, res_json, is_lz, is_cyl,
                                 is_crawl)
        return res_thisitem
    except Exception as e:
        logger.debug(e)


def get_mutuallegalassistance_info(
    info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, pageNum, is_lz, is_cyl, is_crawl
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
        pages_total = None
        try:
            if res_json["data"]["totalCount"]:
                if int(res_json["data"]["totalCount"]) > 0:
                    pages_total = math.ceil(int(res_json["data"]["totalCount"]) / 20)
                else:
                    logger.info("%s没有司法协助案件目录" % company_name)
                    return
            else:
                logger.warning(res_json["data"]["totalCount"])
                return
        except Exception as e:
            logger.debug(e)
        if pages_total == 1:
            res_thisitem = list_json(tyc_id, info_id, company_name, pageNum, pages_total, res_json, is_lz, is_cyl,
                                     is_crawl)
            return res_thisitem
        elif pages_total > 1:
            res_json_next = []
            res_thisitem = list_json(tyc_id, info_id, company_name, pageNum, pages_total, res_json, is_lz, is_cyl,
                                     is_crawl)
            for oneitem in res_thisitem:
                res_json_next.append(oneitem)
            for nextpageNum in range(2, pages_total + 1):
                items = get_mutuallegalassistance_nextpage(info_id, company_name, tyc_id, tyc_hi, Authorization, duid,
                                                        deviceID, x_auth_token, nextpageNum, pages_total, is_lz, is_cyl,
                                                        is_crawl)
                for item in items:
                    res_json_next.append(item)
            return res_json_next
        else:
            logger.warning("%s没有司法协助案件目录" % company_name)

    except Exception as e:
        logger.debug(e)

def main():
    table_name = "t_zx_company_tyc_all_infos_mutuallegalassistance"  # 任务表
    redis_key = "tyc_task_mutuallegalassistance_list"
    sel_data = ['id', 'company_name', 'tyc_id', 'is_lz', 'is_cyl', 'is_crawl']
    task_distribution(table_name, sel_data, {"is_cyl": 1, "state": 0}, redis_key)
    nums = r.scard(redis_key)
    for num in range(1, nums + 1):
        data = r.spop(redis_key).strip("()").split(",")
        info_id = int(data[0])
        company_name = data[1].replace("'", "").replace(" ", "")
        tyc_id = data[2].replace("'", "").replace(" ", "")
        is_lz = data[3].replace("'", "").replace(" ", "")
        is_cyl = data[4].replace("'", "").replace(" ", "")
        is_crawl = data[5].replace("'", "").replace(" ", "")
        mq = MysqlPipelinePublic()
        pageNum = 1
        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        logger.info("当前企业名称为%s" % company_name)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        items = get_mutuallegalassistance_info(
            info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, pageNum, is_lz, is_cyl, is_crawl
        )
        if items:
            try:
                mq.insert_all_sql("t_zx_company_judicial_mutuallegalassistance_list_info", items)
                logger.info("当前item数据为%s" % items)
            except Exception as e:
                logger.debug(e)
            mq.update_sql(table_name, {"state": 1}, {"id": info_id})
            logger.info("更新任务成功")
        else:
            mq.update_sql(table_name, {"state": -1}, {"id": info_id})
            logger.info(
                "当前企业名称为%s" % company_name + "第%s" % num + "总计%s" % nums + "========司法协助列表无数据======="
            )
        mq.close()

if __name__ == "__main__":
    main()
