# -*- coding: utf-8 -*-
# @Time : 2023/5/24 11:29
# @Author: mayj
# 私募基金

import os
import time
import uuid
import json

import requests
from untils.pysql import *
from loguru import logger
from untils.redis_conn import conn
from conf.env import *
from untils.urls import HEDGEFUND_INFOS

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
    folder_name = FILE_PATH + "/tyc_hedgefundinfos_file_私募基金/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + ".json"
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_hedgefundinfos_file_私募基金__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id):
    version = "Android 12.67.0"
    url = HEDGEFUND_INFOS.format(tyc_id)
    data = {"url": url, "version": version}
    r = requests.post(GET_AUTHORZATION_LOCAL_API, data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)
    return data


def get_Trademark_detail_info(tyc_hi, Authorization, duid, info_id, deviceID, x_auth_token, company_name, tyc_id):
    # try:

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

    url = HEDGEFUND_INFOS.format(tyc_id)
    res = requests.get(url=url, headers=headers, verify=False).text
    res_json = json.loads(res)
    create_json(info_id, tyc_id, company_name, res_json)
    hedgefundinfos_info = res_json["data"]
    if "allCount" in str(hedgefundinfos_info):
        logger.debug(f"无私募基金数据：{tyc_id}")
        return
    item = {
        "info_id": info_id,
        "org_info": json.dumps(hedgefundinfos_info.get("org_info", {}), ensure_ascii=False),
        "product": json.dumps(hedgefundinfos_info.get("product", {}), ensure_ascii=False),
        "integrity": json.dumps(hedgefundinfos_info.get("integrity", {}), ensure_ascii=False),
        "staff_info": json.dumps(hedgefundinfos_info.get("staff_info", []), ensure_ascii=False),
        "boss_info": json.dumps(hedgefundinfos_info.get("boss_info", {}), ensure_ascii=False),
        "membership": json.dumps(hedgefundinfos_info.get("membership", {}), ensure_ascii=False),
        "bossListCount": hedgefundinfos_info.get("bossListCount"),
        "boss_list": json.dumps(hedgefundinfos_info.get("boss_list", []), ensure_ascii=False),
        "legal_opinion": json.dumps(hedgefundinfos_info.get("legal_opinion", {}), ensure_ascii=False),
        "company_name": company_name,
        "tyc_id": tyc_id,
        "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
    }

    return item


# except Exception as e:
#     logger.debug(e)


def main():
    mq = MysqlPipelinePublic()
    data_list = TYC_DATA
    for data in data_list:
        info_id = data.get("id")
        company_name = data.get("co_name")
        tyc_id = data.get("co_id")
        logger.warning("当前企业名称为%s" % company_name)
        if conn.sismember("tyc_get_hedgefundinfos_info", tyc_id):
            logger.debug("{}=======>数据已经采集，无需再次采集".format(tyc_id))
            continue
        data_uthoriaztion = get_authoriaztion(info_id, company_name, tyc_id)
        tyc_hi = data_uthoriaztion["data"]["tyc_hi"]
        Authorization = data_uthoriaztion["data"]["Authorization"]
        duid = data_uthoriaztion["data"]["duid"]
        deviceID = data_uthoriaztion["data"]["deviceID"]
        x_auth_token = data_uthoriaztion["data"]["x_auth_token"]
        item = get_Trademark_detail_info(
            tyc_hi,
            Authorization,
            duid,
            info_id,
            deviceID,
            x_auth_token,
            company_name,
            tyc_id,
        )
        if item:
            mq.insert_sql("t_zx_company_hedgefundinfos_info", item)
            conn.sadd("tyc_get_hedgefundinfos_info", tyc_id)
    mq.close()


if __name__ == "__main__":
    main()
