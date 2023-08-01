# -*- coding: utf-8 -*-
# @Time : 2023/5/23 11:03
# @Author: mayj
# 商标文书
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


# 忽略requests证书警告
try:
    import urllib3
    from urllib3.exceptions import InsecureRequestWarning

    urllib3.disable_warnings(InsecureRequestWarning)
except:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = FILE_PATH + "/tyc_trademark_document_file__商标文书/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = (
        company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + str(pageNum) + "_" + ".json"
    )

    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_trademark__document_file__商标文书__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    url = "https://api6.tianyancha.com/cloud-intellectual-property/trademark/document/list"
    data = {"url": url, "version": version}
    r = requests.post(GET_AUTHORZATION_LOCAL_API, data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)
    return data


def get_Trademark_document_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token):
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

        data = {"pageNum": "1", "cgid": tyc_id, "pageSize": "20"}
        url = "https://api6.tianyancha.com/cloud-intellectual-property/trademark/document/list"
        res = requests.post(url=url, headers=headers, data=json.dumps(data), verify=False).text

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
            logger.debug("%s没有商标文书" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_Trademark_document_info(info_id, company_name, tyc_id, pageNum):
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

        data = {"pageNum": pageNum, "cgid": tyc_id, "pageSize": "20"}
        url = "https://api6.tianyancha.com/cloud-intellectual-property/trademark/document/list"
        res = requests.post(url=url, headers=headers, data=json.dumps(data), verify=False).text

        # logger.debug(res)
        res_json = json.loads(res)

        create_json(pageNum, info_id, tyc_id, company_name, res_json)
        items = []
        for trademark_info in res_json["data"]["tmDocsList"]:
            item = {
                "info_id": info_id,
                "title": trademark_info.get("title", "").replace("'", ""),
                "caseNo": trademark_info.get("caseNo", "").replace("'", ""),
                "applicant": json.dumps(trademark_info.get("applicant", []), ensure_ascii=False),
                "applicantAgent": json.dumps(trademark_info.get("applicantAgent", []), ensure_ascii=False),
                "respondent": json.dumps(trademark_info.get("respondent", []), ensure_ascii=False),
                "respondentAgent": json.dumps(trademark_info.get("respondentAgent", []), ensure_ascii=False),
                "docType": trademark_info.get("docType", ""),
                "pubDate": trademark_info.get("pubDate"),
                "businessId": trademark_info.get("businessId", ""),
                "company_name": company_name,
                "tyc_id": tyc_id,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            }
            items.append(item)

        return items

    except Exception as e:
        logger.debug(e)


def main():
    data_list = get_company_230329_name()
    # data_list=get_company_wechat_name()
    for data in data_list:
        info_id = data[0]
        company_name = data[1]
        tyc_id = data[2]
        pageNum = 1
        logger.warning("当前企业名称为%s" % company_name)
        if conn.sismember("tyc_get_trademark_document_info", tyc_id):
            logger.debug("{}=======>数据已经采集，无需再次采集".format(tyc_id))
            continue

        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        pages_total = get_Trademark_document_page(
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
            logger.info(f"共获取到{int(pages_total)}页数据")
            mq = MysqlPipelinePublic()
            for pageNum in range(1, int(pages_total) + 1):
                items = get_Trademark_document_info(info_id, company_name, tyc_id, pageNum)
                for item in items:
                    # try:
                    logger.debug(f"数据入库：{item}")
                    mq.insert_sql("t_zx_company_trademark_document_info", item)
                    # req_data = {
                    #     'regNo':item['regNo'],
                    #     'info_id':item['info_id'],
                    #     'company_name':item['company_name'],
                    #     'tyc_id':item['tyc_id'],
                    #     'tmClass':item['tmClass'],
                    # }
                    # conn.sadd('t_zx_company_trademark_document_info_det_req',json.dumps(req_data, ensure_ascii=False))
                    # except Exception as e:
                    #     logger.error(e)

            mq.close()
        else:
            pass
        conn.sadd("tyc_get_trademark_document_info", tyc_id)
        # delete_to_mysql_wechat_main(info_id,company_name)


if __name__ == "__main__":
    main()
