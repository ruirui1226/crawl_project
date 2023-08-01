# -*- coding: utf-8 -*-
# @Time : 2023/5/24 14:16
# @Author: mayj
# 网站备案
import requests
import json
from loguru import logger
import os
import time
import math
import uuid
from untils.pysql import *
from conf.env import *
from untils.redis_conn import conn
from untils.urls import ICPRECORD_LIST

# 忽略requests证书警告
try:
    import urllib3
    from urllib3.exceptions import InsecureRequestWarning

    urllib3.disable_warnings(InsecureRequestWarning)
except:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = FILE_PATH + "/tyc_icpRecord_file__网站备案/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass
    file_nm = company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + str(pageNum) + ".json"
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_icpRecord_file__网站备案__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    url = ICPRECORD_LIST.format(tyc_id, pageNum)

    data = {"url": url, "version": version}

    r = requests.post(GET_AUTHORZATION_LOCAL_API, data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)

    return data


def get_icpRecord_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, X_AUTH_TOKEN):
    try:
        headers = {
            # """
            "x-b3-traceid-jindi": "",
            "x-b3-sampled-jindi": "",
            "Authorization": Authorization,
            "version": "Android 12.67.0",
            "X-Auth-Token": X_AUTH_TOKEN,
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

        url = ICPRECORD_LIST.format(tyc_id, "1")
        res = requests.get(url=url, headers=headers, verify=False).text

        logger.debug(res)
        res_json = json.loads(res)
        if res_json.get("state", "") == "error":
            logger.debug("%s当前数据异常" % company_name)
            pass

        elif "total" in str(res_json["data"]):
            pages_total = math.ceil(int(res_json["data"]["total"]) / 20)

            if pages_total:
                return pages_total
        elif int(res_json["data"].get("itemTotal", "")) != 0:
            pages_total = math.ceil(int(res_json["data"]["itemTotal"]) / 20)
            if pages_total:
                return pages_total

        else:
            logger.debug("%s没有ICP数据" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_icpRecord_info(info_id, company_name, tyc_id, pageNum):
    url = ICPRECORD_LIST.format(tyc_id, pageNum)
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
    create_json(pageNum, info_id, tyc_id, company_name, res_json)

    items = []
    for icp_info in res_json["data"]["item"]:
        item = {
            "info_id": info_id,
            "webSite": " ".join(webSite for webSite in icp_info["webSite"] if icp_info["webSite"]),
            "ym": icp_info["ym"],
            "companyType": icp_info["companyType"],
            "liscense": icp_info["liscense"],
            "companyName": icp_info["companyName"],
            "examineDate": icp_info["examineDate"],
            "tyc_id": tyc_id,
            "businessId": icp_info["businessId"],
            "company_name": company_name,
            "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        }
        items.append(item)

    return items


def main():
    data_list = get_company_230329_name()
    for data in data_list:
        info_id = data[0]
        company_name = data[1]
        tyc_id = data[2]
        pageNum = 1

        logger.warning("当前企业名称为%s" % company_name)
        if conn.sismember("tyc_get_icpRecord_info", tyc_id):
            logger.debug("{}=======>数据已经采集，无需再次采集".format(tyc_id))
            continue
        # time.sleep(1)
        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        pages_total = get_icpRecord_page(
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
                items = get_icpRecord_info(info_id, company_name, tyc_id, pageNum)
                if items:
                    mq = MysqlPipelinePublic()
                    for item in items:
                        logger.info(f"数据入库start：{item}")
                        mq.insert_sql("t_zx_company_icp_info", item)
                    mq.close()
        else:
            pass
        conn.sadd("tyc_get_icpRecord_info", tyc_id)


if __name__ == "__main__":
    main()
