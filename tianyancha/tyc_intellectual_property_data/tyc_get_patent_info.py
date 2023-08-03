# -*- coding: utf-8 -*-
# @Time : 2023/5/23 14:05
# @Author: mayj
# 专利信息

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
from untils.urls import PATENT_LIST

# 忽略requests证书警告
try:
    import urllib3
    from urllib3.exceptions import InsecureRequestWarning

    urllib3.disable_warnings(InsecureRequestWarning)
except:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    from untils.sql_data import TYC_DATA

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = FILE_PATH + "/tyc_patent_file__专利信息/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + str(pageNum) + ".json"
    # data_json=json.dumps(response.text,sort_keys=True, separators=(',', ': '),indent=4,ensure_ascii=False)
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_patent_file__专利信息——写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    url = PATENT_LIST.format(tyc_id, pageNum)

    data = {"url": url, "version": version}

    r = requests.post(GET_AUTHORZATION_LOCAL_API, data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)

    return data


def get_Patent_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, X_AUTH_TOKEN):
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

        url = PATENT_LIST.format(tyc_id, "1")
        res = requests.get(url=url, headers=headers, verify=False).text

        res_json = json.loads(res)
        if res_json["data"] == "null":
            pass

        elif res_json.get("state", "") == "error":
            logger.error("%s当前数据异常" % company_name)
            pass

        elif int(res_json["data"].get("viewtotal", "")) > 0:
            pages_total = math.ceil(int(res_json["data"]["viewtotal"]) / 20)
            if pages_total:
                return pages_total
        elif int(res_json["data"].get("itemTotal", "")) != 0:
            pages_total = math.ceil(int(res_json["data"]["itemTotal"]) / 20)
            if pages_total:
                return pages_total

        elif "total" in str(res_json["data"]):
            pages_total = math.ceil(int(res_json["data"]["total"]) / 20)

            if pages_total:
                return pages_total
        else:
            logger.debug("%s没有发明专利数据" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_Patent_info(info_id, company_name, tyc_id, pageNum):
    url = PATENT_LIST.format(tyc_id, pageNum)
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
    if res_json["data"]["items"]:
        for patent_info in res_json["data"]["items"]:
            item = {
                "info_id": info_id,
                "businessId": patent_info.get("businessId", ""),
                "title": patent_info.get("title", ""),
                "patentNum": patent_info.get("patentNum", ""),
                "uuid": patent_info.get("uuid", ""),
                "pubnumber": patent_info.get("pubnumber", ""),
                "applicationTime": patent_info.get("applicationTime", ""),
                "cat": patent_info.get("cat", ""),
                # "applicantname": " ".join([applicantname for applicantname in patent_info["applicantname"]]),
                "eventTime": patent_info.get("eventTime", ""),
                "inventor": patent_info.get("inventor", ""),
                "patent_id": patent_info.get("id", ""),
                "lawStatus": json.dumps(patent_info.get("lawStatus", []), ensure_ascii=False),
                "address": patent_info.get("address", ""),
                "agency": patent_info.get("agency", ""),
                "abstracts": patent_info.get("abstracts", ""),
                "applicantName": patent_info.get("applicantName", ""),
                "pubDate": patent_info.get("pubDate", ""),
                "applicationPublishTime": patent_info.get("applicationPublishTime", ""),
                "appnumber": patent_info.get("appnumber", ""),
                "patentType": patent_info.get("patentType", ""),
                "imgUrl": patent_info.get("imgUrl", ""),
                "mainCatNum": patent_info.get("mainCatNum", ""),
                "createTime": patent_info.get("createTime", ""),
                "lprs": patent_info.get("lprs", ""),
                "patentName": patent_info.get("patentName", ""),
                "applicationPublishNum": patent_info.get("applicationPublishNum", ""),
                "allCatNum": patent_info.get("allCatNum", ""),
                "company_name": company_name,
                "tyc_id": tyc_id,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            }
            items.append(item)

        return items

    else:
        pass


def main():
    mq = MysqlPipelinePublic()
    data_list = TYC_DATA
    for data in data_list:
        info_id = data.get("id")
        company_name = data.get("co_name")
        tyc_id = data.get("co_id")
        pageNum = 1

        logger.warning("当前企业名称为%s" % company_name)
        if conn.sismember("tyc_get_patent_info", tyc_id):
            logger.debug("{}=======>数据已经采集，无需再次采集".format(tyc_id))
            continue

        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        pages_total = get_Patent_page(
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
                items = get_Patent_info(info_id, company_name, tyc_id, pageNum)
                if items:
                    for item in items:
                        logger.debug(item)
                        try:
                            mq.insert_sql("t_zx_company_patent_info", item)
                        except:
                            continue
                        req_data = {
                            "p_id": item["uuid"],
                            "info_id": item["info_id"],
                            "company_name": item["company_name"],
                            "tyc_id": item["tyc_id"],
                        }
                        conn.sadd("tyc_get_patent_req_info", json.dumps(req_data, ensure_ascii=False))
        else:
            pass
        conn.sadd("tyc_get_patent_info", tyc_id)
    mq.close()


if __name__ == "__main__":
    main()
