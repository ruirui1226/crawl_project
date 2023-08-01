#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/5/24 10:18
@Author : zhangpf
@File : tyc_history_equity_pledge.py
@Desc : 历史股权出质
@Software: PyCharm
"""
import sys

import requests
import json
from loguru import logger
import os
import time
import math
from untils.pysql import *
import uuid
from untils.redis_conn import conn

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from untils.urls import HISTORY_EQUITY_PLEDGE

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/jsondata/tyc_历史股权出质_file/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = (
        company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + str(pageNum) + "_" + ".json"
    )
    # data_json=json.dumps(response.text,sort_keys=True, separators=(',', ': '),indent=4,ensure_ascii=False)
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_历史股权出质_file__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    url = HISTORY_EQUITY_PLEDGE.format(tyc_id, pageNum)

    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)

    return data


def get_history_equity_pledge_page(
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

        # data = {
        #     "ps": "20",
        #     "regYear": "-100",
        #     "sortIndex": "-100",
        #     "app_year": "-100",
        #     "int_cls": "-100",
        #     "id": tyc_id,
        #     "pn": "1",
        #     "status": "-100",
        # }
        url = HISTORY_EQUITY_PLEDGE.format(tyc_id, pageNum)
        res = requests.get(url=url, headers=headers, verify=False).text

        # logger.debug(res)
        res_json = json.loads(res)
        if "totalCount" in str(res_json["data"]):
            # if math.ceil(int(res_json["data"]["total"]) / 20) < 27:
            pages_total = math.ceil(int(res_json["data"]["totalCount"]) / 20)

            if pages_total:
                return pages_total
        elif int(res_json["data"]["count"]) > 0:
            pages_total = math.ceil(int(res_json["data"]["count"]) / 20)
            if pages_total:
                return pages_total

        else:
            logger.debug("%s没有商标信息" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_history_equity_pledge_info(info_id, company_name, tyc_id, pageNum):
    try:
        # print(url)
        # res = requests.get(url=url, headers=headers, verify=False).text

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
            "User-Agent": "com.tianyancha.skyeye/Dalvik/2.1.0 (Linux; U; Android 8.1.0; Nexus 6P Build/OPM7.181205.001; appDevice/google_QAQ_Nexus 6P)",
            "Cache-Control": "no-cache, no-store",
            "Host": "api6.tianyancha.com",
            "Accept-Encoding": "gzip",
        }

        url = HISTORY_EQUITY_PLEDGE.format(tyc_id, pageNum)
        res = requests.get(url=url, headers=headers, verify=False).text
        # logger.debug(res)
        res_json = json.loads(res)
        create_json(pageNum, info_id, tyc_id, company_name, res_json)
        items_list = res_json["data"]["items"]
        items = []

        for ite in items_list:
            item = {
                "info_id": info_id,
                "cancel": ite.get("cancel", ""),
                "cancelDate": ite.get("cancelDate", ""),
                "pledgeeStr": ite.get("pledgeeStr", ""),
                "businessId": ite.get("businessId", ""),
                "regDate": ite.get("regDate", ""),
                "pledgor": ite.get("pledgor", ""),
                "certifNumberR": ite.get("certifNumberR", ""),
                "pledgee": ite.get("pledgee", ""),
                "targetCompanyGid": ite.get("targetCompanyGid", ""),
                "changeSituation": ite.get("changeSituation", ""),
                "regNumber": ite.get("regNumber", ""),
                "certifNumber": ite.get("certifNumber", ""),
                "companyList": ",".join(format(log) for log in ite.get("companyList"))
                if ite.get("companyList") is not None
                else "",
                "targetCompany": ite.get("targetCompany", ""),
                "equityAmount": ite.get("equityAmount", ""),
                "t_id": ite.get("id", ""),
                "state": ite.get("state", ""),
                "pledgeeList": ",".join(format(log) for log in ite.get("pledgeeList"))
                if ite.get("pledgeeList") is not None
                else "",
                "pledgorStr": ite.get("pledgorStr", ""),
                "pledgorList": ",".join(format(log) for log in ite.get("pledgorList"))
                if ite.get("pledgorList") is not None
                else "",
                "putDate": ite.get("putDate", ""),
                "remarks": ite.get("remarks", ""),
                "base": ite.get("base", ""),
                "unique_id": str(tyc_id) + ite.get("businessId", ""),
                "company_name": company_name,
                "tyc_id": tyc_id,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            }
            items.append(item)
        print(items)
        return items

    except Exception as e:
        logger.debug(e)
        sys.exit(1)


def main():
    data_list = get_company_230420_name()
    # data_list=get_company_wechat_name()
    for data in data_list:
        info_id = data[0]
        company_name = data[1]
        tyc_id = data[2]
        initial_pageNum = 1
        logger.warning("当前企业名称为%s" % company_name)
        if conn.sismember("tyc_history_equity_pledge", tyc_id):
            logger.debug("{}=======>数据已经采集，无需再次采集".format(tyc_id))
            continue
        data = get_authoriaztion(info_id, company_name, tyc_id, initial_pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        pages_total = get_history_equity_pledge_page(
            info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, initial_pageNum
        )
        if pages_total:
            print(company_name)
            for pageNum in range(1, int(pages_total) + 1):
                items = get_history_equity_pledge_info(info_id, company_name, tyc_id, pageNum)
                try:
                    mq = MysqlPipelinePublic()
                    for item in items:
                        mq.insert_sql("t_zx_history_equity_pledge", item)
                    mq.close()

                except Exception as e:
                    logger.debug(e)
        else:
            pass
        conn.sadd("tyc_history_equity_pledge", tyc_id)
        # delete_to_mysql_wechat_main(info_id,company_name)


if __name__ == "__main__":
    main()