# -*- coding: utf-8 -*-
# @Time : 2023/5/24 9:51
# @Author: mayj
# 商标信息详情
import os
import time
import math
import uuid
import json
from multiprocessing import Pool

import requests
from untils.pysql import *
from loguru import logger
from untils.redis_conn import conn
from conf.env import *
from untils.urls import TRADEMARK_DETAILS

# 忽略requests证书警告
try:
    import urllib3
    from urllib3.exceptions import InsecureRequestWarning

    urllib3.disable_warnings(InsecureRequestWarning)
except:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

mq = MysqlPipelinePublic()

def create_json(pageNum, info_id, tyc_id, company_name, res_json, regNo):
    folder_name = FILE_PATH + "/tyc_trademark_detail_file__商标信息详情/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = (
        company_name
        + "_"
        + str(info_id)
        + "_"
        + regNo
        + "_"
        + tyc_id
        + "_"
        + str(uuid.uuid1())
        + "_"
        + str(pageNum)
        + "_"
        + ".json"
    )

    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_trademark_detail_file__商标信息详情__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum, regNo, tmClass):
    version = "Android 12.67.0"
    url = TRADEMARK_DETAILS.format(regNo, tmClass)
    data = {"url": url, "version": version}

    r = requests.post(GET_AUTHORZATION_LOCAL_API, data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)
    return data


def get_Trademark_detail_info(
    tyc_hi,
    Authorization,
    duid,
    info_id,
    deviceID,
    x_auth_token,
    company_name,
    tyc_id,
    pageNum,
    regNo,
    tmClass,
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

        url = TRADEMARK_DETAILS.format(regNo, tmClass)
        res = requests.get(url=url, headers=headers, verify=False).text
        res_json = json.loads(res)
        create_json(pageNum, info_id, tyc_id, company_name, res_json, regNo)
        trademark_detail_info = res_json["data"]

        item = {
            "url": url,
            "info_id": info_id,
            "company_name": company_name,
            "baseInfo": json.dumps(trademark_detail_info.get("baseInfo"), ensure_ascii=False),
            "agentInfo": json.dumps(trademark_detail_info.get("agentInfo"), ensure_ascii=False),
            "stautsList": json.dumps(trademark_detail_info.get("stautsList"), ensure_ascii=False),
            "goodsList": json.dumps(trademark_detail_info.get("goodsList"), ensure_ascii=False),
            "issueList": json.dumps(trademark_detail_info.get("issueList"), ensure_ascii=False),
            "flowStep": str(trademark_detail_info.get("flowStep", "")),
            "monitoredCount": str(trademark_detail_info.get("monitoredCount", "")),
            "monitored": str(trademark_detail_info.get("monitored", "")),
            "tabList": json.dumps(trademark_detail_info.get("tabList"), ensure_ascii=False),
            "companyId": str(trademark_detail_info.get("companyId", "")),
            "announcementList": json.dumps(trademark_detail_info.get("announcementList"), ensure_ascii=False),
            "applicantInfo": json.dumps(trademark_detail_info.get("applicantInfo"), ensure_ascii=False),
            "trademarkAnnouncementInfo": json.dumps(
                trademark_detail_info.get("trademarkAnnouncementInfo"),
                ensure_ascii=False,
            ),
            "tmImgOssPath": str(trademark_detail_info.get("tmImgOssPath", "")),
            "monitorListUrl": str(trademark_detail_info.get("monitorListUrl", "")),
            "flowList": json.dumps(trademark_detail_info.get("flowList"), ensure_ascii=False),
            "flowStepList": json.dumps(trademark_detail_info.get("flowStepList"), ensure_ascii=False),
            "regNo": regNo,
            "tyc_id": tyc_id,
            "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        }

        return item

    except Exception as e:
        logger.debug(e)


def main():
    # data_list = get_company_230420_name_detail()
    # data_list=get_company_wechat_name()
    data_list = conn.smembers("t_zx_company_trademark_info_det_req")
    # mq = MysqlPipelinePublic()
    for data_str in data_list:
        data = json.loads(data_str)
        info_id = data["info_id"]
        company_name = data["company_name"]
        tyc_id = data["tyc_id"]
        tmClass = data["tmClass"]
        regNo = data["regNo"]
        key_id = str(tyc_id) + str(regNo)
        logger.warning("当前企业名称为%s" % company_name)
        if conn.sismember("tyc_get_trademark_det_info", key_id):
            logger.debug("{}=======>数据已经采集，无需再次采集".format(regNo))
            conn.srem("t_zx_company_trademark_info_det_req", data_str)
            continue
        data_uthoriaztion = get_authoriaztion(info_id, company_name, tyc_id, "1", regNo, tmClass)
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
            "1",
            regNo,
            tmClass,
        )
        try:
            mq.insert_sql("t_zx_company_trademark_detail_info", item)
        except:
            pass
        conn.sadd("tyc_get_trademark_det_info", key_id)
        conn.srem("t_zx_company_trademark_info_det_req", data_str)


def main_process(data_str):
    # data_list = conn.smembers("t_zx_company_trademark_info_det_req")

    data = json.loads(data_str)
    info_id = data["info_id"]
    company_name = data["company_name"]
    tyc_id = data["tyc_id"]
    tmClass = data["tmClass"]
    regNo = data["regNo"]
    key_id = str(tyc_id) + str(regNo)
    logger.warning("当前企业名称为%s" % company_name)
    if conn.sismember("tyc_get_trademark_det_info", key_id):
        logger.debug("{}=======>数据已经采集，无需再次采集".format(regNo))
        conn.srem("t_zx_company_trademark_info_det_req", data_str)
        return
    data_uthoriaztion = get_authoriaztion(info_id, company_name, tyc_id, "1", regNo, tmClass)
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
        "1",
        regNo,
        tmClass,
    )
    try:
        mq.insert_sql("t_zx_company_trademark_detail_info", item)
    except:
        pass
    conn.sadd("tyc_get_trademark_det_info", key_id)
    conn.srem("t_zx_company_trademark_info_det_req", data_str)


if __name__ == "__main__":
    data_list = conn.smembers("t_zx_company_trademark_info_det_req")
    pool = Pool(processes=4)
    pool.map(main, data_list)
    pool.close()
    pool.join()
