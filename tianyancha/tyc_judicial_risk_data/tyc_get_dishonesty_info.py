#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/5/24 9:59
@Author : xushaowei
@File : tyc_get_dishonesty_info.py
@Desc :
@Software:PyCharm
"""
# 失信被执行人
import requests
import json

import urllib3
import os
import math

from tyc_judicial_risk_data.tyc_distribute_task import task_distribution
from untils.pysql import *
import uuid

from untils.redis_conn import r
from untils.urls import DISHONESTY_LIST

# 忽略requests证书警告
try:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/jsondata/tyc_trademark_file__失信被执行人/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = (
        company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + str(pageNum) + "_" + ".json"
    )
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_trademark_file__失信被执行人__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    url = DISHONESTY_LIST.format(company_name, tyc_id, pageNum)
    data = {"url": url, "version": version}
    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    data = json.loads(r.text)
    return data


def get_dishonesty_page(
    info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, initial_pageNum
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

        url = DISHONESTY_LIST.format(company_name, tyc_id, initial_pageNum)
        res = requests.get(url=url, headers=headers, verify=False).text

        # logger.debug(res)
        res_json = json.loads(res)
        if "total" in str(res_json["data"]):
            # if math.ceil(int(res_json["data"]["total"]) / 20) < 27:
            pages_total = math.ceil(int(res_json["data"]["total"]) / 20)

            if pages_total:
                return pages_total
        elif int(res_json["data"]["count"]) > 0:
            pages_total = math.ceil(int(res_json["data"]["count"]) / 20)
            if pages_total:
                return pages_total

        else:
            logger.debug("%s失信被执行人无信息" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_dishonesty_info(info_id, company_name, tyc_id, pageNum):
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

        url = DISHONESTY_LIST.format(company_name, tyc_id, pageNum)
        res = requests.get(url=url, headers=headers, verify=False).text

        res_json = json.loads(res)

        items = []
        try:
            head = res_json["data"]["headData"]
            headData = str(head).replace("'", '"')
        except:
            headData = None
        for trademark_info in res_json["data"]["items"]:
            item = {
                "info_id": info_id,
                "businessentity": trademark_info.get("businessentity", ""),
                "areaname": trademark_info.get("areaname", ""),
                "courtname": trademark_info.get("courtname", ""),
                "businessId": trademark_info.get("businessId", ""),
                "unperformPart": trademark_info.get("unperformPart", ""),
                "staff": str(trademark_info.get("staff", "")).replace("'", '"'),
                "type": trademark_info.get("type", ""),
                "cpwsUrl": trademark_info.get("cpwsUrl", ""),
                "performedPart": str(trademark_info.get("performedPart", "")),
                "iname": trademark_info.get("iname", ""),
                "disrupttypename": trademark_info.get("disrupttypename", ""),
                "casecode": trademark_info.get("casecode", ""),
                "cardnum": trademark_info.get("cardnum", ""),
                "performance": trademark_info.get("performance", ""),
                "regdate": trademark_info.get("regdate", ""),
                "publishdate": trademark_info.get("publishdate", ""),
                "gistunit": trademark_info.get("gistunit", ""),
                "duty": trademark_info.get("duty", ""),
                "explainMessage": trademark_info.get("explainMessage", ""),
                "gistid": trademark_info.get("gistid", ""),
                "t_id": trademark_info.get("id"),
                "cid": trademark_info.get("cid"),
                "company_name": company_name,
                "tyc_id": tyc_id,
                "headData": headData,
            }
            items.append(item)

        return items, headData

    except Exception as e:
        logger.debug(e)


def main():
    table_name = "t_zx_company_tyc_all_infos_dishonestexecutor"
    redis_key = "tyc_task_dishonestexecutor"
    sel_data = ['id', 'company_name', 'tyc_id']
    task_distribution(table_name, sel_data, {"is_crawl": 'zjtx_2023', "state": 0}, redis_key)
    nums = r.scard(redis_key)
    for num in range(1, nums + 1):
        data = r.spop(redis_key).strip("()").split(",")
        info_id = int(data[0])
        company_name = data[1].replace("'", "").replace(" ", "")
        tyc_id = data[2].replace("'", "").replace(" ", "")
        mq = MysqlPipelinePublic()
        initial_pageNum = 1
        headData = None
        logger.info("当前企业名称为%s" % company_name + ",第%s个企业" % num + "总计%s个企业" % nums)
        data = get_authoriaztion(info_id, company_name, tyc_id, initial_pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        pages_total = get_dishonesty_page(
            info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, initial_pageNum
        )
        if pages_total:
            for pageNum in range(1, int(pages_total) + 1):
                items = get_dishonesty_info(info_id, company_name, tyc_id, pageNum)
                if pageNum == 1:
                    headData = {"headData": str(items[1])}
                try:
                    for item in items[0]:
                        if str(items[1]) == "None":
                            item.update(headData)
                        mq.insert_sql("t_zx_company_judicial_dishonestexecutor_info", item)
                        logger.info("当前item数据为%s------------->" % item)
                except Exception as e:
                    logger.debug(e)
            mq.update_sql(table_name, {"state": 1}, {"id": info_id})
            logger.info("更新任务成功")
        else:
            mq.update_sql(table_name, {"state": -1}, {"id": info_id})
            logger.info("当前企业名称为%s" % company_name + ",第%s个企业" % num + "总计%s个企业" % nums + "========失信被执行人无数据=======更新任务成功")
        mq.close()


if __name__ == "__main__":
    main()
