#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/5/29 9：55
@Author : QTH
@Desc : 天眼查--供应商
@Software: PyCharm
"""

import json
import math
import os

import requests
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from untils.redis_conn import conn
from untils.pysql import *
import uuid

from untils.sql_data import TYC_DATA
from untils.urls import SUPPLY_URL

disable_warnings(InsecureRequestWarning)


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"

    # url = f"https://api6.tianyancha.com/cloud-business-state/supply/summaryList?gid={tyc_id}&year=-100&pageSize=20&pageNum={pageNum}"

    data = {"url": SUPPLY_URL.format(tyc_id, pageNum), "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)
    return data


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/tyc_supply_file_供应商/"
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

    logger.debug(("--tyc_supply_file_供应商__写入到-->" + file_nm))


def get_supply_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token):
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

        # url = f"https://api6.tianyancha.com/cloud-business-state/supply/summaryList?gid={tyc_id}&year=-100&pageSize=20&pageNum=1"
        url = SUPPLY_URL.format(tyc_id, 1)
        res = requests.get(url, headers=headers, verify=False).text

        logger.debug(res)

        res_json = json.loads(res)

        if "total" in str(res_json["data"]["pageBean"]):
            pages_total = math.ceil(int(res_json["data"]["pageBean"]["total"]) / 20)

            if pages_total:
                return pages_total
        elif int(res_json["data"]["count"]) > 0:
            pages_total = math.ceil(int(res_json["data"]["count"]) / 20)
            if pages_total:
                return pages_total

        else:
            logger.debug("没有%s供应商信息" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_supply_info(info_id, company_name, tyc_id, pageNum):
    try:
        url = SUPPLY_URL.format(tyc_id, pageNum)
        logger.warning(url)
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

        # url = f"https://api6.tianyancha.com/cloud-business-state/supply/summaryList?gid={tyc_id}&year=-100&pageSize=20&pageNum={pageNum}"
        url = SUPPLY_URL.format(tyc_id, pageNum)
        res = requests.get(url, headers=headers, verify=False).text

        logger.debug(res)

        res_json = json.loads(res)
        # create_json(pageNum, info_id, tyc_id, company_name, res_json)

        items = []
        for supplyl_info in res_json["data"]["pageBean"]["result"]:
            item = {
                "info_id": info_id,
                "tyc_id": tyc_id,
                "company_name": company_name,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
                "summary": supplyl_info.get("summary", ""),
                "announcement_date": supplyl_info.get("announcement_date", ""),
                "amt": supplyl_info.get("amt", ""),
                "companyUrl": supplyl_info.get("companyUrl", ""),
                "source": supplyl_info.get("source", ""),
                "supplier_graphId": supplyl_info.get("supplier_graphId", ""),
                "supplier_name": supplyl_info.get("supplier_name", ""),
                "relationship": supplyl_info.get("relationship", ""),
                "category": supplyl_info.get("category", ""),
                "client_name": supplyl_info.get("client_name", ""),
                "dataSource": supplyl_info.get("dataSource", ""),
                "source_name": supplyl_info.get("source_name", ""),
                "source_seq": supplyl_info.get("source_seq", ""),
                "ratio": supplyl_info.get("ratio", ""),
                "bid_url_app": supplyl_info.get("bid_url_app", ""),
                "alias": supplyl_info.get("alias", ""),
                "bid_uuid": supplyl_info.get("bid_uuid", ""),
                "logo": supplyl_info.get("logo", ""),
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
        ex = conn.sadd("tyc_gongyingshang_list_info.py", tyc_id)
        if ex == 1:
            logger.warning("当前企业名称为%s" % company_name)
            data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
            tyc_hi = data["data"]["tyc_hi"]
            Authorization = data["data"]["Authorization"]
            duid = data["data"]["duid"]
            deviceID = data["data"]["deviceID"]
            x_auth_token = data["data"]["x_auth_token"]
            pages_total = get_supply_page(
                info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token
            )
            if pages_total:
                print(company_name)
                for pageNum in range(1, int(pages_total) + 1):
                    items = get_supply_info(info_id, company_name, tyc_id, pageNum)
                    try:
                        for item in items:
                            mq.insert_sql("t_zx_company_supply_info", item)
                            logger.info("数据 %s 插入成功" % item)
                    except Exception as e:
                        logger.debug(e)
            else:
                pass
        else:
            logger.debug("%s---------数据已经采集，无需再次采集" % tyc_id)
            pass
    mq.close()


if __name__ == "__main__":
    main()
