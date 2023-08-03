# -*- coding: utf-8 -*-
# @Time : 2023/5/19 13:53
# @Author: mayj

# 商标信息
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
    folder_name = FILE_PATH + "/tyc_trademark_file__商标信息/"
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

    logger.debug(("--tyc_trademark_file__商标信息__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    url = "https://api6.tianyancha.com/cloud-intellectual-property/intellectualProperty/trademarkList"
    data = {"url": url, "version": version}

    r = requests.post(GET_AUTHORZATION_LOCAL_API, data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)

    return data


def get_Trademark_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token):
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

        data = {
            "ps": "20",
            "regYear": "-100",
            "sortIndex": "-100",
            "app_year": "-100",
            "int_cls": "-100",
            "id": tyc_id,
            "pn": "1",
            "status": "-100",
        }
        url = "https://api6.tianyancha.com/cloud-intellectual-property/intellectualProperty/trademarkList"
        res = requests.post(url=url, headers=headers, data=json.dumps(data), verify=False).text

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


def get_Trademark_info(info_id, company_name, tyc_id, pageNum):
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
            "deviceVersion": "7.1.2",
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
            "User-Agent": "com.tianyancha.skyeye/Dalvik/2.1.0 (Linux; U; Android 7.1.2; Nexus 6P Build/N2G48C; appDevice/google_QAQ_Nexus 6P)",
            "Cache-Control": "no-cache, no-store",
            "Host": "api6.tianyancha.com",
            "Accept-Encoding": "gzip",
        }

        data = {
            "ps": "20",
            "regYear": "-100",
            "sortIndex": "-100",
            "app_year": "-100",
            "int_cls": "-100",
            "id": tyc_id,
            "pn": pageNum,
            "status": "-100",
        }
        url = "https://api6.tianyancha.com/cloud-intellectual-property/intellectualProperty/trademarkList"
        res = requests.post(url=url, headers=headers, data=json.dumps(data), verify=False).text

        # logger.debug(res)
        res_json = json.loads(res)

        create_json(pageNum, info_id, tyc_id, company_name, res_json)
        items = []
        for trademark_info in res_json["data"]["items"]:
            item = {
                "info_id": info_id,
                "regNo": trademark_info.get("regNo", ""),
                "tmPic": trademark_info.get("tmPic", ""),
                "appDate": trademark_info.get("appDate", ""),
                "tmClass": trademark_info.get("tmClass", ""),
                "intClsV2": trademark_info.get("intClsV2", ""),
                "intCls": trademark_info.get("intCls", ""),
                "applicantCn": trademark_info.get("applicantCn", ""),
                "tmName": trademark_info.get("tmName", ""),
                # "tmFlow": str(trademark_info.get("tmFlow", "")),
                "eventTime": trademark_info.get("eventTime", ""),
                "trademark_id": trademark_info.get("id", ""),
                "category": trademark_info.get("category", ""),
                "status": trademark_info.get("status", ""),
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
        pageNum = 1
        logger.warning("当前企业名称为%s" % company_name)
        if conn.sismember("tyc_get_trademark_info", tyc_id):
            logger.debug("{}=======>数据已经采集，无需再次采集".format(tyc_id))
            continue

        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        pages_total = get_Trademark_page(
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
            for pageNum in range(1, int(pages_total) + 1):
                items = get_Trademark_info(info_id, company_name, tyc_id, pageNum)
                for item in items:
                    try:
                        return_str = mq.insert_sql("t_zx_company_trademark_info", item)
                    except:
                        continue
                    if return_str == "数据已存在":
                        continue
                    req_data = {
                        "regNo": item["regNo"],
                        "info_id": item["info_id"],
                        "company_name": item["company_name"],
                        "tyc_id": item["tyc_id"],
                        "tmClass": item["tmClass"],
                    }
                    conn.sadd(
                        "t_zx_company_trademark_info_det_req",
                        json.dumps(req_data, ensure_ascii=False),
                    )

            mq.close()
        else:
            pass
        conn.sadd("tyc_get_trademark_info", tyc_id)
        # delete_to_mysql_wechat_main(info_id,company_name)
    mq.close()


if __name__ == "__main__":
    main()
