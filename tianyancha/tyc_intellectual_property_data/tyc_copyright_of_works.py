#!/usr/bin/conf python
# -*- coding: utf-8 -*-
# @Time : 2023/5/19
# @Author: mayj
# 作品著作权
import os
import time
import math
import uuid
import json

import requests
from untils.pysql import *
from loguru import logger
from untils.redis_conn import conn
from conf.env import *


from untils.urls import Copyright_Of_Works_Url

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
    folder_name = FILE_PATH + "/jsondata/tyc_copyright_of_work_file__作品著作权/"
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

    logger.debug(("--tyc_copyright_of_work_file__作品著作权__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    url = Copyright_Of_Works_Url.format(tyc_id, pageNum)

    data = {"url": url, "version": version}

    r = requests.post(GET_AUTHORZATION_LOCAL_API, data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)

    return data


def get_Copyright_Of_Works_page(
    info_id,
    company_name,
    tyc_id,
    tyc_hi,
    Authorization,
    duid,
    deviceID,
    x_auth_token,
    pageNum,
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
        url = Copyright_Of_Works_Url.format(tyc_id, pageNum)
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
            logger.debug("%s没有作品著作权" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_Copyright_Of_Works_info(info_id, company_name, tyc_id, pageNum):
    try:
        # print(url)
        # res = requests.get(url=url, headers=headers, verify=False).text

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

        url = Copyright_Of_Works_Url.format(tyc_id, pageNum)
        res = requests.get(url=url, headers=headers, verify=False).text

        # logger.debug(res)
        res_json = json.loads(res)
        create_json(pageNum, info_id, tyc_id, company_name, res_json)
        items_list = res_json["data"]["resultList"]
        items = []

        for ite in items_list:
            item = {
                "info_id": info_id,
                "type": ite.get("type", "").replace("'", "‘") if ite.get("type", "") else ite.get("type", ""),
                "finishTime": ite.get("finishTime", ""),
                "createTime": ite.get("createTime", ""),
                "regnum": ite.get("regnum", ""),
                "fullname": ite.get("fullname", "").replace("'", "‘")
                if ite.get("fullname", "")
                else ite.get("fullname", ""),
                "authorNationality": ite.get("authorNationality", "").replace("'", "‘")
                if ite.get("authorNationality", "")
                else ite.get("authorNationality", ""),
                "publishtime": ite.get("publishtime", ""),
                "regtime": ite.get("regtime", ""),
                "businessId": ite.get("businessId", ""),
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
        initial_pageNum = 1
        logger.warning("当前企业名称为%s" % company_name)
        if conn.sismember("tyc_copyright_of_works", tyc_id):
            logger.debug("{}=======>数据已经采集，无需再次采集".format(tyc_id))
            continue

        data = get_authoriaztion(info_id, company_name, tyc_id, initial_pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        pages_total = get_Copyright_Of_Works_page(
            info_id,
            company_name,
            tyc_id,
            tyc_hi,
            Authorization,
            duid,
            deviceID,
            x_auth_token,
            initial_pageNum,
        )
        if pages_total:
            for pageNum in range(1, int(pages_total) + 1):
                items = get_Copyright_Of_Works_info(info_id, company_name, tyc_id, pageNum)
                # try:
                for item in items:
                    logger.info(item)
                    mq.insert_sql("t_zx_copyright_of_works", item)
                    # req_data = {
                    #     "businessId": item["businessId"],
                    #     "info_id": item["info_id"],
                    #     "company_name": item["company_name"],
                    #     "tyc_id": item["tyc_id"],
                    # }
                    # conn.sadd("tyc_copyright_of_works_det_req", json.dumps(req_data, ensure_ascii=False))
                # except Exception as e:
                #     logger.error(e)
        else:
            pass
        conn.sadd("tyc_copyright_of_works", tyc_id)
        # delete_to_mysql_wechat_main(info_id,company_name)
    mq.close()


if __name__ == "__main__":
    main()
