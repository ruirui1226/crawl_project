# -*- coding: utf-8 -*-
# @Time : 2023/5/23 14:05
# @Author: mayj
# 专利详情信息
from multiprocessing import Pool

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
from untils.urls import PATENT_DETAIL

# 忽略requests证书警告
try:
    import urllib3
    from urllib3.exceptions import InsecureRequestWarning

    urllib3.disable_warnings(InsecureRequestWarning)
except:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


mq = MysqlPipelinePublic()


def create_json(p_id, info_id, tyc_id, company_name, res_json):
    folder_name = FILE_PATH + "/tyc_patent_file__专利详情信息/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + str(p_id) + ".json"
    # data_json=json.dumps(response.text,sort_keys=True, separators=(',', ': '),indent=4,ensure_ascii=False)
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_patent_file__专利详情信息——写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, p_id):
    version = "Android 12.67.0"
    url = PATENT_DETAIL.format(p_id)

    data = {"url": url, "version": version}

    r = requests.post(GET_AUTHORZATION_LOCAL_API, data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)

    return data


def get_Patent_det_info(info_id, company_name, tyc_id, p_id):
    url = PATENT_DETAIL.format(p_id)
    logger.warning(url)
    data = get_authoriaztion(info_id, company_name, p_id)
    tyc_hi = data["data"]["tyc_hi"]
    Authorization = data["data"]["Authorization"]
    duid = data["data"]["duid"]
    deviceID = data["data"]["deviceID"]
    x_auth_token = data["data"]["x_auth_token"]
    headers = {
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
    create_json(p_id, info_id, tyc_id, company_name, res_json)
    patent_det_info = res_json["data"]
    if patent_det_info:
        item = {
            "info_id": info_id,
            "p_id": patent_det_info.get("id", ""),
            "patentId": patent_det_info.get("patentId", ""),
            "patentNum": patent_det_info.get("patentNum", ""),
            "applicationPublishNum": patent_det_info.get("applicationPublishNum", ""),
            "applicationTime": patent_det_info.get("applicationTime", ""),
            "appubDate": patent_det_info.get("appubDate", ""),
            "grantDate": patent_det_info.get("grantDate", ""),
            "applicationPublishTime": patent_det_info.get("applicationPublishTime", ""),
            "patentName": patent_det_info.get("patentName", "").replace("'", "‘"),
            "mainCatNum": patent_det_info.get("mainCatNum", ""),
            "allCatNum": patent_det_info.get("allCatNum", "").replace("'", "‘")
            if patent_det_info.get("allCatNum", "")
            else patent_det_info.get("allCatNum", ""),
            "inventor": patent_det_info.get("inventor", ""),
            "agency": patent_det_info.get("agency", ""),
            "agent": patent_det_info.get("agent", ""),
            "agencyLink": patent_det_info.get("agencyLink", ""),
            "address": patent_det_info.get("address", ""),
            "postCode": patent_det_info.get("postCode", ""),
            "lprs": patent_det_info.get("lprs", ""),
            "patentType": patent_det_info.get("patentType", ""),
            "statusCode": patent_det_info.get("statusCode", ""),
            "applicantNameAgo": patent_det_info.get("applicantNameAgo", "").replace("'", "‘"),
            "applicantNameNow": patent_det_info.get("applicantNameNow", ""),
            "pdfPath": patent_det_info.get("pdfPath", ""),
            "lprsInfoPath": patent_det_info.get("lprsInfoPath", ""),
            "priorityPath": patent_det_info.get("priorityPath", ""),
            "familyPath": patent_det_info.get("familyPath", ""),
            "familyNo": patent_det_info.get("familyNo", ""),
            "compareFilesPath": patent_det_info.get("compareFilesPath", ""),
            "addrProvince": patent_det_info.get("addrProvince", ""),
            "addrCity": patent_det_info.get("addrCity", ""),
            "addrCounty": patent_det_info.get("addrCounty", ""),
            "iapp": patent_det_info.get("iapp", ""),
            "ipub": patent_det_info.get("ipub", ""),
            "den": patent_det_info.get("den", ""),
            "clPath": patent_det_info.get("clPath", ""),
            "proCode": patent_det_info.get("proCode", ""),
            "appCoun": patent_det_info.get("appCoun", ""),
            "issueDate": patent_det_info.get("issueDate", ""),
            "isDeleted": patent_det_info.get("isDeleted", ""),
            "sourceWeb": patent_det_info.get("sourceWeb", ""),
            "dbName": patent_det_info.get("dbName", ""),
            "tifDistributePath": patent_det_info.get("tifDistributePath", ""),
            "pages": patent_det_info.get("pages", ""),
            "divideInitAppNo": patent_det_info.get("divideInitAppNo", ""),
            "pid": patent_det_info.get("pid", ""),
            "sysid": patent_det_info.get("sysid", ""),
            "property1": patent_det_info.get("property1", ""),
            "property2": patent_det_info.get("property2", ""),
            "property3": patent_det_info.get("property3", ""),
            "createDate": patent_det_info.get("createDate", ""),
            "updateTime": patent_det_info.get("updateTime", ""),
            "abstracts": patent_det_info.get("abstracts", "").replace("'", "‘")
            if patent_det_info.get("abstracts", "")
            else patent_det_info.get("abstracts", ""),
            "claims": patent_det_info.get("claims", "").replace("'", "‘")
            if patent_det_info.get("claims", "")
            else patent_det_info.get("claims", ""),
            "description": patent_det_info.get("description", "").replace("'", "‘")
            if patent_det_info.get("description", "")
            else patent_det_info.get("description", ""),
            "imageUrlList": json.dumps(patent_det_info.get("imageUrlList", ""), ensure_ascii=False),
            "applicantName": patent_det_info.get("applicantName", "").replace("'", "‘")
            if patent_det_info.get("applicantName", "")
            else patent_det_info.get("applicantName", ""),
            "applicantNames": json.dumps(patent_det_info.get("applicantNames", ""), ensure_ascii=False).replace(
                "'", "‘"
            )
            if patent_det_info.get("applicantNames", "")
            else patent_det_info.get("applicantNames", ""),
            "agencyId": patent_det_info.get("agencyId", ""),
            "applicationType": patent_det_info.get("applicationType", ""),
            "stateOfLaw": json.dumps(patent_det_info.get("stateOfLaw", ""), ensure_ascii=False),
            "priorityList": json.dumps(patent_det_info.get("priorityList", ""), ensure_ascii=False),
            "applyFlow": json.dumps(patent_det_info.get("applyFlow", ""), ensure_ascii=False),
            "grantNumber": patent_det_info.get("grantNumber", ""),
            "expectEndDate": patent_det_info.get("expectEndDate", ""),
            "reviewPath": patent_det_info.get("reviewPath", ""),
            "company_name": company_name,
            "tyc_id": tyc_id,
            "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        }

        return item

    else:
        pass


def main():
    data_list = conn.smembers("tyc_get_patent_req_info")

    for data_str in data_list:
        data = json.loads(data_str)
        info_id = data["info_id"]
        company_name = data["company_name"]
        tyc_id = data["tyc_id"]
        p_id = data["p_id"]
        logger.warning("当前商标id为%s" % p_id)
        if conn.sismember("tyc_get_patent_det_info", p_id):
            logger.debug("{}=======>数据已经采集，无需再次采集".format(p_id))
            conn.srem("tyc_get_patent_req_info", data_str)
            continue
        item = get_Patent_det_info(info_id, company_name, tyc_id, p_id)
        logger.info(json.dumps(item))
        try:
            mq.insert_sql("t_zx_company_patent_det_info", item)
        except:
            pass
        conn.sadd("tyc_get_patent_det_info", p_id)
        conn.srem("tyc_get_patent_req_info", data_str)


def main1(data_str):
    # data_list = conn.smembers("tyc_get_patent_req_info")

    # for data_str in data_list:
    data = json.loads(data_str)
    info_id = data["info_id"]
    company_name = data["company_name"]
    tyc_id = data["tyc_id"]
    p_id = data["p_id"]
    logger.warning("当前商标id为%s" % p_id)
    if conn.sismember("tyc_get_patent_det_info", p_id):
        logger.debug("{}=======>数据已经采集，无需再次采集".format(p_id))
        conn.srem("tyc_get_patent_req_info", data_str)
        # continue
        return
    item = get_Patent_det_info(info_id, company_name, tyc_id, p_id)
    logger.info(json.dumps(item))
    try:
        mq.insert_sql("t_zx_company_patent_det_info", item)
    except:
        pass
    conn.sadd("tyc_get_patent_det_info", p_id)
    conn.srem("tyc_get_patent_req_info", data_str)


if __name__ == "__main__":
    # main()

    data_list = conn.smembers("tyc_get_patent_req_info")
    pool = Pool(processes=8)
    pool.map(main1, data_list)
    pool.close()
    pool.join()
