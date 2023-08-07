#!/usr/bin/conf python
# -*- coding: utf-8 -*-
"""
@desc: tianyancha-对外投资
@version: python3
@author: shenr
@time: 2023/05/22
"""
import requests
import json
from loguru import logger
import os
import time
import math
from untils.pysql import *
from conf.env import *
import uuid
from untils.redis_conn import conn

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from untils.urls import INVESTMENTS_ABROAD
from untils.sql_data import TYC_DATA

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/tyc_investments_abroad_file_对外投资/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + ".json"
    # data_json=json.dumps(response.text,sort_keys=True, separators=(',', ': '),indent=4,ensure_ascii=False)
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_investments_abroad_file_对外投资__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"

    url = INVESTMENTS_ABROAD
    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    data = json.loads(r.text)
    return data


def get_Invest_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token):
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

        data = {"pageNum": "1", "sortField": "", "gid": tyc_id, "pageSize": "20", "sortType": "-1"}
        url = INVESTMENTS_ABROAD
        print(url)
        res = requests.post(url=url, headers=headers, data=json.dumps(data), verify=False).text
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
            logger.debug("%s对外投资数据" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_Invest_info(info_id, company_name, tyc_id, pageNum, x_auth_token):
    try:
        url = INVESTMENTS_ABROAD
        logger.warning(url)

        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]

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
        params = {"pageNum": pageNum, "sortField": "", "gid": tyc_id, "pageSize": "20", "sortType": "-1"}
        res = requests.post(url=url, headers=headers, data=json.dumps(params), verify=False).text

        print("kkkkk", res)
        res_json = json.loads(res)

        # create_json(info_id, tyc_id, company_name, res_json)
        items = []
        for invest_info in res_json["data"]["result"]:
            item = {
                "info_id": info_id,
                "regStatus": invest_info.get("regStatus", ""),
                "regCapital": invest_info.get("regCapital", ""),
                "source": invest_info.get("source", ""),
                "pencertileScore": invest_info.get("pencertileScore", ""),
                "type": invest_info.get("type", ""),
                "percent": invest_info.get("percent", ""),
                "productName": invest_info.get("productName", ""),
                "legalPersonName": invest_info.get("legalPersonName", ""),
                "orgType": invest_info.get("orgType", ""),
                "toco": invest_info.get("toco", ""),
                "creditCode": invest_info.get("creditCode", ""),
                "alias": invest_info.get("alias", ""),
                "logo": invest_info.get("logo", ""),
                "invest_id": invest_info.get("id", ""),
                "personType": invest_info.get("personType", ""),
                "amount": invest_info.get("amount", ""),
                "estiblishTime": invest_info.get("estiblishTime", ""),
                "productId": invest_info.get("productId", ""),
                "productLogo": invest_info.get("productLogo", ""),
                "amountSuffix": invest_info.get("amountSuffix", ""),
                "business_scope": invest_info.get("business_scope", ""),
                "legalPersonId": invest_info.get("legalPersonId", ""),
                "name": invest_info.get("name", ""),
                "time": invest_info.get("time", ""),
                "category": invest_info.get("category", ""),
                "graphId": invest_info.get("graphId", ""),
                "base": invest_info.get("base", ""),
                "total": res_json["data"]["total"],
                "tyc_id": tyc_id,
                "company_name": company_name,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
                "jigouId": invest_info.get("jigouId", ""),
                "jigouLogo": invest_info.get("jigouLogo", ""),
                "jigouName": invest_info.get("jigouName", ""),
                "legalLogo": invest_info.get("legalLogo", ""),
                "serviceCount": invest_info.get("serviceCount", ""),
                "legalPersonTitle": invest_info.get("legalPersonTitle", ""),
            }
            items.append(item)
        return items
    except Exception as e:
        logger.debug(e)


def main():
    mq = MysqlPipelinePublic()
    data_list = TYC_DATA
    for data in data_list:
        info_id = data.get("id")
        company_name = data.get("co_name")
        tyc_id = data.get("co_id")
        pageNum = 1

        logger.warning("当前企业名称为%s" % company_name)
        if conn.sismember("tyc_investments_abroad", tyc_id):
            logger.debug("{}=======>数据已经采集，无需再次采集".format(tyc_id))
            continue

        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        pages_total = get_Invest_page(
            info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token
        )
        if pages_total:
            for pageNum in range(1, int(pages_total) + 1):
                # get_publicWechat_info(info_id, company_name, tyc_id, pageNum)
                items = get_Invest_info(info_id, company_name, tyc_id, pageNum, x_auth_token)
                try:
                    for item in items:
                        mq.insert_sql("t_zx_company_invest_info", item)
                        # logger.info("插入成功---------------------数据 %s " % item)
                except Exception as e:
                    logger.debug(e)
        else:
            pass
        conn.sadd("tyc_investments_abroad", tyc_id)
    mq.close()


if __name__ == "__main__":
    main()
