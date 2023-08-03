#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/5/23 16:24
# @Author: mayj
# 投资事件
import time

import requests
import json

import os, math
import uuid
from untils.pysql import *
from conf.env import *
from untils.redis_conn import conn
from untils.urls import TZANLI_LIST

# 忽略requests证书警告
try:
    import urllib3
    from urllib3.exceptions import InsecureRequestWarning

    urllib3.disable_warnings(InsecureRequestWarning)
except:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    from untils.sql_data import TYC_DATA

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(info_id, tyc_id, company_name, res_json):
    folder_name = FILE_PATH + "/tyc_touzishijian_file_投资事件/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + ".json"
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    # logger.debug(("--tyc_touzishijian_file_投资事件__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"

    url = TZANLI_LIST.format(tyc_id, pageNum)

    data = {"url": url, "version": version}

    r = requests.post(GET_AUTHORZATION_LOCAL_API, data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)
    return data


def get_tzanli_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token):
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

        url = TZANLI_LIST.format(tyc_id, "1")
        res = requests.get(url, headers=headers, verify=False).text

        # logger.debug(res)

        res_json = json.loads(res)

        if "total" in str(res_json["data"]["page"]):
            pages_total = math.ceil(int(res_json["data"]["page"]["total"]) / 20)

            if pages_total:
                return pages_total
        elif int(res_json["data"]["count"]) > 0:
            pages_total = math.ceil(int(res_json["data"]["count"]) / 20)
            if pages_total:
                return pages_total

        else:
            logger.debug("%s没有投资事件" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_tzanli_info(info_id, company_name, tyc_id, pageNum):
    try:
        url = TZANLI_LIST.format(tyc_id, pageNum)
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
        res = requests.get(url=url, headers=headers, verify=False).text

        # logger.debug(res)
        res_json = json.loads(res)
        create_json(info_id, tyc_id, company_name, res_json)
        items = []
        for tzsj_info in res_json["data"]["page"]["rows"]:
            item = {
                "info_id": info_id,
                "product": tzsj_info.get("product", ""),
                "lunci": tzsj_info.get("lunci", ""),
                "icon": tzsj_info.get("icon", ""),
                "tzdate": tzsj_info.get("tzdate", ""),
                "yewu": tzsj_info.get("yewu", ""),
                "money": tzsj_info.get("money", ""),
                "company": tzsj_info.get("company", ""),
                "location": tzsj_info.get("location", ""),
                "tzanli_id": tzsj_info.get("id", ""),
                "iconOssPath": tzsj_info.get("iconOssPath", ""),
                "hangye1": tzsj_info.get("hangye1", ""),
                "hangyeId": tzsj_info.get("hangyeId", ""),
                "mainPortrayId": tzsj_info.get("mainPortrayId", ""),
                "tzrIdsType": tzsj_info.get("tzrIdsType", ""),
                "tzrList": json.dumps(tzsj_info.get("tzrList", []), ensure_ascii=False).replace("'", "’"),
                "rongzi_map": json.dumps(tzsj_info.get("rongzi_map", ""), ensure_ascii=False).replace("'", "’"),
                "organization_name": tzsj_info.get("organization_name", "").replace("'", "’"),
                "jigou_map": json.dumps(tzsj_info.get("jigou_map", ""), ensure_ascii=False).replace("'", "’"),
                "product_id": tzsj_info.get("product_id", ""),
                "company_name": company_name,
                "tyc_id": tyc_id,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
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
        if conn.sismember("tyc_get_tzanli_info", tyc_id):
            logger.debug("{}=======>数据已经采集，无需再次采集".format(tyc_id))
            continue

        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        pages_total = get_tzanli_page(
            info_id,
            company_name,
            tyc_id,
            tyc_hi,
            Authorization,
            duid,
            deviceID,
            x_auth_token,
        )
        if pages_total:
            for pageNum in range(1, int(pages_total) + 1):
                items = get_tzanli_info(info_id, company_name, tyc_id, pageNum)
                if items:
                    for item in items:
                        # try:
                        logger.info(f'数据入库：{item["product_id"]}')
                        mq.insert_sql("t_zx_company_tzanli_info", item)
                        # except Exception as e:
                        #     logger.error(e)
        else:
            pass
        conn.sadd("tyc_get_tzanli_info", tyc_id)
    mq.close()


if __name__ == "__main__":
    main()
