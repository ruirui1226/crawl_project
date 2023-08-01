#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/5/23 16:40
# @Author: mayj
# 竞品信息
import sys
import time
import json
import os, math
import uuid

import requests

sys.path.append("..")

from untils.pysql import *
from conf.env import *
from untils.redis_conn import conn
from untils.urls import FINDJINGPIN_LIST

# 忽略requests证书警告
try:
    import urllib3
    from urllib3.exceptions import InsecureRequestWarning

    urllib3.disable_warnings(InsecureRequestWarning)
except:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(info_id, tyc_id, company_name, res_json):
    folder_name = FILE_PATH + "/tyc_findJingpin_file_竞品信息/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + ".json"
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_findJingpin_file_竞品信息__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"

    url = FINDJINGPIN_LIST.format(tyc_id, pageNum)

    data = {"url": url, "version": version}

    r = requests.post(GET_AUTHORZATION_LOCAL_API, data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)
    return data


def get_Jingpin_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token):
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

        url = FINDJINGPIN_LIST.format(tyc_id, "1")
        res = requests.get(url, headers=headers, verify=False).text

        logger.debug(res)

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
            logger.debug("%s没有竞品信息" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_Jingpin_info(info_id, company_name, tyc_id, pageNum):
    try:
        url = FINDJINGPIN_LIST.format(tyc_id, pageNum)
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

        logger.debug(res)
        res_json = json.loads(res)
        create_json(info_id, tyc_id, company_name, res_json)
        items = []
        for jingping_info in res_json["data"]["page"]["rows"]:
            item = {
                "info_id": info_id,
                "jingpin_id": jingping_info.get("jingpin_id", ""),
                "productId": jingping_info.get("productId", ""),
                "product": jingping_info.get("product", ""),
                "jingpinProductId": jingping_info.get("jingpinProductId", ""),
                "jingpinProduct": jingping_info.get("jingpinProduct", "").replace("'", "’"),
                "sourceWeb": jingping_info.get("sourceWeb", ""),
                "createTime": jingping_info.get("createTime", ""),
                "updateTime": jingping_info.get("updateTime", ""),
                "isDeleted": jingping_info.get("isDeleted", ""),
                "companyName": jingping_info.get("companyName", "").replace("'", "’"),
                "graphId": jingping_info.get("graphId", ""),
                "companyId": jingping_info.get("companyId", ""),
                "icon": jingping_info.get("icon", ""),
                "iconOssPath": jingping_info.get("iconOssPath", ""),
                "yewu": jingping_info.get("yewu", ""),
                "setupDate": jingping_info.get("setupDate", ""),
                "date": jingping_info.get("date", ""),
                "round": jingping_info.get("round", ""),
                "value": jingping_info.get("value", ""),
                "hangye": jingping_info.get("hangye", ""),
                "location": jingping_info.get("location", ""),
                "jingpinBrandId": jingping_info.get("jingpinBrandId", ""),
                "portray": json.dumps(jingping_info.get("portray", []), ensure_ascii=False).replace("'", "’"),
                "portrayStr": json.dumps(jingping_info.get("portrayStr", ""), ensure_ascii=False).replace("'", "’"),
                "logo": jingping_info.get("logo", ""),
                "alias": jingping_info.get("alias", "").replace("'", "’"),
                "hangyeId": jingping_info.get("hangyeId", ""),
                "tyc_id": tyc_id,
                "company_name": company_name,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            }
            items.append(item)

        return items

    except Exception as e:
        logger.debug(e)


def main():
    data_list = get_company_230329_name()
    for data in data_list:
        info_id = data[0]
        company_name = data[1]
        tyc_id = data[2]
        pageNum = 1
        logger.warning("当前企业名称为%s" % company_name)
        if conn.sismember("tyc_get_Jingpin_info", tyc_id):
            logger.debug("{}=======>数据已经采集，无需再次采集".format(tyc_id))
            continue

        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        pages_total = get_Jingpin_page(
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
            mq = MysqlPipelinePublic()
            for pageNum in range(1, int(pages_total) + 1):
                items = get_Jingpin_info(info_id, company_name, tyc_id, pageNum)
                if items:
                    # for item in items:
                    # logger.info(json.dumps(item, ensure_ascii=False))
                    mq.insert_all_sql("t_zx_company_findjingping_info", items)

            mq.close()
        else:
            pass
        conn.sadd("tyc_get_Jingpin_info", tyc_id)


if __name__ == "__main__":
    main()
