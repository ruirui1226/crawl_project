#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/5/26 14:46
@Author : zhangpf
@File : tyc_pledge_of_stock_right.py
@Desc : 股权质押
@Software: PyCharm
"""
import sys

import requests
import json
from loguru import logger
import os
import time
import math
from untils.urls import *
from untils.pysql import *
from untils.redis_conn import conn


from conf.env import *
import uuid

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/jsondata/tyc_股权质押_file/"
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

    logger.debug(("--tyc_股权质押_file__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    url = PLEDGE_OF_STOCK_RIGHT.format(tyc_id, pageNum)

    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)

    return data


def get_pledge_of_stock_right_page(
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

        url = PLEDGE_OF_STOCK_RIGHT.format(tyc_id, initial_pageNum)
        res = requests.get(url=url, headers=headers, verify=False).text
        print(res)
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
            logger.debug("%s没有商标信息" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_pledge_of_stock_right_info(info_id, company_name, tyc_id, pageNum):
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
            # "Connection": close
            "User-Agent": "com.tianyancha.skyeye/Dalvik/2.1.0 (Linux; U; Android 8.1.0; Nexus 6P Build/OPM7.181205.001; appDevice/google_QAQ_Nexus 6P)",
            "Cache-Control": "no-cache, no-store",
            "Host": "api6.tianyancha.com",
            "Accept-Encoding": "gzip",
        }

        url = PLEDGE_OF_STOCK_RIGHT.format(tyc_id, pageNum)
        res = requests.get(url=url, headers=headers, verify=False).text
        # logger.debug(res)
        res_json = json.loads(res)
        # create_json(pageNum, info_id, tyc_id, company_name, res_json)
        items = []
        for re in res_json["data"]["items"]:
            item = {
                "info_id": info_id,
                "shareHolderLogo": re.get("shareHolderLogo", ""),
                "startDate": re.get("startDate", ""),
                "graphId": re.get("graphId", ""),
                "lastValue": re.get("lastValue", ""),
                "pledgeAmount": re.get("pledgeAmount", ""),
                "status": re.get("status", ""),
                "proOfSelf": re.get("proOfSelf", ""),
                "companyName": re.get("companyName", ""),
                "lastValueUnit": re.get("lastValueUnit", ""),
                "businessId": re.get("businessId", ""),
                "shareHolderId": re.get("shareHolderId", ""),
                "joinStockEnterpriseGid": re.get("joinStockEnterpriseGid", ""),
                "annDate": re.get("annDate", ""),
                "pledgeAmountUnit": re.get("pledgeAmountUnit", ""),
                "shareHolderAlias": re.get("shareHolderAlias", ""),
                "companyCount": re.get("companyCount", ""),
                "shareHolderType": re.get("shareHolderType", ""),
                "joinStockEnterprise": re.get("joinStockEnterprise", ""),
                "shGraphId": re.get("shGraphId", ""),
                "endDate": re.get("endDate", ""),
                "joinStockEnterpriseAlias": re.get("joinStockEnterpriseAlias", ""),
                "shareHolder": re.get("shareHolder", ""),
                "joinStockEnterpriseLogo": re.get("joinStockEnterpriseLogo", ""),
                "company_name": company_name,
                "tyc_id": tyc_id,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
                "unique_id": str(re.get("businessId", "")) + "_" + tyc_id,
            }
            items.append(item)
        print(items)
        return items

    except Exception as e:
        logger.debug(e)
        conn.srem("tyc_pledge_of_stock_right", tyc_id)
        sys.exit(1)


def main():
    data_list = get_company_230420_name()
    # data_list=get_company_wechat_name()
    for data in data_list:
        info_id = data[0]
        company_name = data[1]
        tyc_id = data[2]
        initial_pageNum = 1
        ex = conn.sadd("tyc_pledge_of_stock_right", tyc_id)
        logger.warning("当前企业ID为-------%s" % tyc_id)
        if ex == 1:
            logger.warning("当前企业名称为%s" % company_name)
            data = get_authoriaztion(info_id, company_name, tyc_id, initial_pageNum)
            tyc_hi = data["data"]["tyc_hi"]
            Authorization = data["data"]["Authorization"]
            duid = data["data"]["duid"]
            deviceID = data["data"]["deviceID"]
            x_auth_token = data["data"]["x_auth_token"]
            pages_total = get_pledge_of_stock_right_page(
                info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, initial_pageNum
            )
            if pages_total:
                print(company_name)
                for pageNum in range(1, int(pages_total) + 1):
                    items = get_pledge_of_stock_right_info(info_id, company_name, tyc_id, pageNum)
                    try:
                        mq = MysqlPipelinePublic()
                        for item in items:
                            mq.insert_sql("t_zx_pledge_of_stock_right", item)
                        mq.close()

                    except Exception as e:
                        logger.debug(e)
            else:
                pass
        else:
            logger.debug("%s======>数据已经采集，无需再次采集" % tyc_id)
            pass
        # delete_to_mysql_wechat_main(info_id,company_name)


if __name__ == "__main__":
    main()
