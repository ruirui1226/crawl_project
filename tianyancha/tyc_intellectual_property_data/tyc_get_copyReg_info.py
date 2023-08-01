# -*- coding: utf-8 -*-
# @Time : 2023/5/23 15:34
# @Author: mayj
# 软件著作权


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

from untils.redis_conn import conn
from untils.urls import COPYREG_LIST

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(info_id, tyc_id, company_name, res_json):
    folder_name = FILE_PATH + "/tyc_copyreg_file__软件著作权/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + ".json"
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_copyreg__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    url = COPYREG_LIST.format(tyc_id, pageNum)

    data = {"url": url, "version": version}

    r = requests.post(GET_AUTHORZATION_LOCAL_API, data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)

    return data


def get_copyReg_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, X_AUTH_TOKEN):
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
        url = COPYREG_LIST.format(tyc_id, "1")

        res = requests.get(url=url, headers=headers, verify=False).text

        res_json = json.loads(res)
        if "total" in str(res_json["data"]):
            pages_total = math.ceil(int(res_json["data"]["realTotal"]) / 20)

            if pages_total:
                return pages_total
        elif int(res_json["data"]["count"]) > 0:
            pages_total = math.ceil(int(res_json["data"]["count"]) / 20)
            if pages_total:
                return pages_total

        else:
            logger.debug("%s没有软件著作权" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_copyReg_info(info_id, company_name, tyc_id, pageNum):
    try:
        url = COPYREG_LIST.format(tyc_id, pageNum)
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

        create_json(info_id, tyc_id, company_name, res_json)
        items = []
        for copyreg_info in res_json["data"]["items"]:
            item = {
                "info_id": info_id,
                "regtime": copyreg_info["regtime"],
                "publishtime": copyreg_info["publishtime"],
                "businessId": copyreg_info["businessId"],
                "simplename": copyreg_info.get("simplename", ""),
                "authorNationality": copyreg_info["authorNationality"],
                "regnum": copyreg_info["regnum"],
                "copyreg_id": copyreg_info.get("id", ""),
                "fullname": copyreg_info["fullname"],
                "version": copyreg_info.get("version", ""),
                "catnum": copyreg_info.get("catnum", ""),
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
    for data in data_list:
        info_id = data[0]
        company_name = data[1]
        tyc_id = data[2]
        pageNum = 1
        logger.warning("当前企业名称为%s" % company_name)
        if conn.sismember("tyc_get_copyReg_info", tyc_id):
            logger.debug("{}=======>数据已经采集，无需再次采集".format(tyc_id))
            continue

        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        pages_total = get_copyReg_page(
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
                items = get_copyReg_info(info_id, company_name, tyc_id, pageNum)
                if items:
                    mq = MysqlPipelinePublic()
                    for item in items:
                        # try:
                        mq.insert_sql("t_zx_company_copyreg_info", item)
                        req_data = {
                            "businessId": item["businessId"],
                            "info_id": item["info_id"],
                            "company_name": item["company_name"],
                            "tyc_id": item["tyc_id"],
                        }
                        conn.sadd(
                            "tyc_get_copyreg_info_det_req",
                            json.dumps(req_data, ensure_ascii=False),
                        )
                        # except Exception as e:
                        #     logger.error(e)
                    mq.close()
        else:
            pass
        conn.sadd("tyc_get_copyReg_info", tyc_id)
        # delete_to_mysql_wechat_main(info_id,company_name)


if __name__ == "__main__":
    main()
