#!/usr/bin/conf python
# -*- coding: utf-8 -*-
"""
@desc: tianyancha-历史法院公告
@version: python3
@author: zhangpf
@time: 2023/05/10
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

from untils.urls import HISTORY_COURT_ANNOUNCEMENT

from untils.sql_data import TYC_DATA

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/jsondata/tyc_历史法院公告_file/"
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

    logger.debug(("--tyc_历史法院公告_file__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    url = HISTORY_COURT_ANNOUNCEMENT.format(tyc_id, pageNum)

    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)

    return data


def get_court_announcement_page(
    info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, pagenum
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
        url = HISTORY_COURT_ANNOUNCEMENT.format(tyc_id, pagenum)
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
            logger.debug("%s没有商标信息" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_court_announcement_info(info_id, company_name, tyc_id, pageNum):
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

        url = HISTORY_COURT_ANNOUNCEMENT.format(tyc_id, pageNum)
        res = requests.get(url=url, headers=headers, verify=False).text

        # logger.debug(res)
        res_json = json.loads(res)
        # create_json(pageNum, info_id, tyc_id, company_name, res_json)
        items = []
        for re in res_json["data"]["list"]:
            item = {
                "id": str(tyc_id) + str(re.get("id", "")),
                "info_id": info_id,
                "announce_id": re.get("announce_id", ""),
                "party2StrApp": ",".join(format(log) for log in re.get("party2StrApp"))
                if re.get("party2StrApp") is not None
                else "",
                "party1": re.get("party1", ""),
                "reason": re.get("reason", ""),
                "bltnno": re.get("bltnno", ""),
                "party2": re.get("party2", ""),
                "businessId": re.get("businessId", ""),
                "judgephone": re.get("judgephone", ""),
                "party1StrApp": ",".join(format(log) for log in re.get("party1StrApp"))
                if re.get("party1StrApp") is not None
                else "",
                "caseno": re.get("caseno", ""),
                "identityList": ",".join(format(log) for log in re.get("identityList"))
                if re.get("identityList") is not None
                else "",
                "uuid": re.get("uuid", ""),
                "bltntypename": re.get("bltntypename", ""),
                "content": re.get("content", ""),
                "courtcode": re.get("courtcode", ""),
                "province": re.get("province", ""),
                "mobilephone": re.get("mobilephone", ""),
                "publishpage": re.get("publishpage", ""),
                "party2Str": re.get("party2Str", ""),
                "publishdate": re.get("publishdate", ""),
                "t_id": re.get("id", ""),
                "party1Str": re.get("party1Str", ""),
                "company_name": company_name,
                "tyc_id": tyc_id,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
                "unique_id": str(re.get("id", "")) + "_" + tyc_id,
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
        initial_pageNum = 1

        logger.warning("当前企业名称为%s" % company_name)
        data = get_authoriaztion(info_id, company_name, tyc_id, initial_pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        pages_total = get_court_announcement_page(
            info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, initial_pageNum
        )
        if pages_total:
            print(company_name)
            for pageNum in range(1, int(pages_total) + 1):
                items = get_court_announcement_info(info_id, company_name, tyc_id, pageNum)
                try:
                    for item in items:
                        mq.insert_sql("t_zx_history_court_announcement", item)
                except Exception as e:
                    logger.debug(e)
        else:
            pass
        # delete_to_mysql_wechat_main(info_id,company_name)
    mq.close()


if __name__ == "__main__":
    main()
