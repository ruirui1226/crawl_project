#!/usr/bin/conf python
# -*- coding: utf-8 -*-
"""
@desc: tianyancha-历史送达公告详情
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
from tianyancha.untils.pysql import *
from tianyancha.conf.env import *
import uuid
from tianyancha.untils.urls import HISTORICAL_NOTICE_OF_SERVICE, HISTORICAL_NOTICE_OF_SERVICE_DETAIL

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/jsondata/tyc_历史送达公告_file/"
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

    logger.debug(("--tyc_历史送达公告_file__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, businessid):
    version = "Android 12.67.0"
    url = HISTORICAL_NOTICE_OF_SERVICE_DETAIL.format(businessid)

    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)

    return data


def get_investments_abroad_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token):
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

        data = {"pageNum": "1", "pageSize": "20", "id": str(tyc_id)}
        url = HISTORICAL_NOTICE_OF_SERVICE

        res = requests.post(url=url, headers=headers, data=json.dumps(data), verify=False).text
        # logger.debug(res)
        res_json = json.loads(res)
        if "total" in str(res_json["data"]):
            # if math.ceil(int(res_json["data"]["total"]) / 20) < 27:
            pages_total = math.ceil(int(res_json["data"].get("total") or 0) / 20)

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


def get_investments_abroad_info(info_id, company_name, tyc_id, businessid):
    try:
        # print(url)
        # res = requests.get(url=url, headers=headers, verify=False).text

        data = get_authoriaztion(info_id, company_name, tyc_id, businessid)
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

        url = HISTORICAL_NOTICE_OF_SERVICE_DETAIL.format(businessid)
        res = requests.get(url=url, headers=headers, verify=False).text

        logger.debug(res)
        res_json = json.loads(res)
        create_json(1, info_id, tyc_id, company_name, res_json)
        items = []
        item = {
            "info_id": info_id,
            "businessid": businessid,
            "title": res_json["data"].get("title"),
            "court": res_json["data"].get("court"),
            "content": res_json["data"].get("content"),
            "startdate": res_json["data"].get("startDate"),
            "uniquet_id": tyc_id + "_" + businessid,
            "detail_url": url,
            "company_name": company_name,
            "tyc_id": tyc_id,
            "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        }
        items.append(item)
        return items

    except Exception as e:
        logger.debug(e)


def main():
    data_list = get_company_230420_name_detail()
    # data_list=get_company_wechat_name()
    for data in data_list:
        info_id = data[0]
        company_name = data[1]
        tyc_id = data[2]
        businessid = data[3]

        logger.warning("当前企业名称为%s" % company_name)
        items = get_investments_abroad_info(info_id, company_name, tyc_id, businessid)
        try:
            mq = MysqlPipelinePublic()
            for item in items:
                mq.insert_sql("t_zx_tyc_history_notice_delivery_detail", item)
            mq.close()

        except Exception as e:
            logger.debug(e)
        else:
            pass
        # delete_to_mysql_wechat_main(info_id,company_name)


if __name__ == "__main__":
    main()
