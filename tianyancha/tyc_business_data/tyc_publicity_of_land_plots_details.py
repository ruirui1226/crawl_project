#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/5/15 17:37
@Author : zhangpf
@File : tyc_publicity_of_land_plots_details.py
@Desc : 地块公示详情
@Software: PyCharm
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

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from untils.urls import PUBLICITY_OF_LAND_PLOtS_DETAILS

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/jsondata/tyc_地块公示详情_file/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + "_" + ".json"
    # data_json=json.dumps(response.text,sort_keys=True, separators=(',', ': '),indent=4,ensure_ascii=False)
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_地块公示详情_file__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, businessId):
    version = "Android 12.67.0"
    url = PUBLICITY_OF_LAND_PLOtS_DETAILS.format(businessId)

    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)

    return data


def get_publicity_of_land_plots_info(info_id, company_name, tyc_id, businessId):
    try:
        data = get_authoriaztion(info_id, company_name, tyc_id, businessId)
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

        url = PUBLICITY_OF_LAND_PLOtS_DETAILS.format(businessId)
        res = requests.get(url=url, headers=headers, verify=False).text
        res_json = json.loads(res)
        # create_json(info_id, tyc_id, company_name, res_json)
        items = []
        data = res_json["data"]
        item = {
            # "id": businessId,
            "info_id": str(info_id),
            "publicationOrganize": data.get("publicationOrganize", ""),
            "feedbackMethod": data.get("feedbackMethod", ""),
            "postalCode": data.get("postalCode", ""),
            "landArea": data.get("landArea", ""),
            "contactPerson": data.get("contactPerson", ""),
            "remark": data.get("remark", ""),
            "landLocation": data.get("landLocation", ""),
            "landAreaAll": data.get("landAreaAll", ""),
            "electronicMail": data.get("electronicMail", ""),
            "landAreaUnit": data.get("landAreaUnit", ""),
            "contactOrganize": data.get("contactOrganize", ""),
            "landUsefulness": data.get("landUsefulness", ""),
            "landNum": data.get("landNum", ""),
            "contactNumber": data.get("contactNumber", ""),
            "publicAnnouncementPeriod": data.get("publicAnnouncementPeriod", ""),
            "organizeLocation": data.get("organizeLocation", ""),
            "projectName": data.get("projectName", ""),
            "publicationDate": data.get("publicationDate", ""),
            "landuserClean": str(data.get("publicationDate", "")).replace("'", '"')
            if data.get("landuserClean") is not None
            else "",
            "landuserCleanApp": str(data.get("landuserCleanApp", "")).replace("'", '"')
            if data.get("landuserCleanApp") is not None
            else "",
            "company_name": company_name,
            "businessId": businessId,
            "tyc_id": tyc_id,
            "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        }
        items.append(item)
        print(items)
        return items

    except Exception as e:
        logger.debug(e)


def main():
    mq = MysqlPipelinePublic()
    data_list = mq.select_sql(
        "t_zx_publicity_of_land_plots", ["id", "company_name", "tyc_id", "businessId"], {"1": "1"}
    )
    # data_list=get_company_wechat_name()
    for data in data_list:
        info_id = data.get("id")
        company_name = data.get("company_name")
        tyc_id = data.get("tyc_id")
        businessId = data.get("businessId")
        logger.warning("当前企业名称为-------%s" % company_name)
        items = get_publicity_of_land_plots_info(info_id, company_name, tyc_id, businessId)
        try:
            for item in items:
                mq.insert_sql("t_zx_publicity_of_land_plots_details", item)
            mq.close()

        except Exception as e:
            logger.debug(e)


if __name__ == "__main__":
    main()
