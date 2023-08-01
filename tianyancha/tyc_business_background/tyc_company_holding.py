# -*- coding: utf-8 -*-
"""
@desc: tianyancha-实际控制权
@version: python3
@author: shenr
@time: 2023/05/23
"""
import requests
import json
from loguru import logger
import os, time, math
import uuid
from tianyancha.conf.env import *
from tianyancha.untils.pysql import *
from untils.redis_conn import conn
# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from tianyancha.untils.urls import COMPANY_HOLDING

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/tyc_company_holding_file_实际控制权/"
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

    logger.debug(("--tyc_company_holding_file_实际控制权__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"

    url = COMPANY_HOLDING.format(tyc_id, pageNum)
    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)
    return data


def get_companyholding_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token):
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

        url = COMPANY_HOLDING.format(tyc_id, "1")
        res = requests.get(url, headers=headers, verify=False).text

        logger.debug(res)

        res_json = json.loads(res)

        if "total" in str(res_json["data"]):
            pages_total = math.ceil(int(res_json["data"]["total"]) / 20)

            if pages_total:
                return pages_total
        elif int(res_json["data"]["count"]) > 0:
            pages_total = math.ceil(int(res_json["data"]["count"]) / 20)
            if pages_total:
                return pages_total

        else:
            logger.debug("%s没有实际控制权" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_companyholding_info(info_id, company_name, tyc_id, pageNum):
    try:
        url = COMPANY_HOLDING.format(tyc_id, pageNum)
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

        # logger.debug(res)
        res_json = json.loads(res)

        create_json(pageNum, info_id, tyc_id, company_name, res_json)
        items = []
        for hold_info in res_json["data"]["list"]:
            item = {
                "legal_personId": hold_info.get("legalPersonId", ""),
                "reg_status": hold_info.get("regStatus", ""),
                "chain_list": str(hold_info.get("chainList", "")).replace("'", '"'),
                "estiblish_time": hold_info.get("estiblishTime", ""),
                "legal_type": hold_info.get("legalType", ""),
                "reg_capital": hold_info.get("regCapital", ""),
                "name": hold_info.get("name", ""),
                "alias": hold_info.get("alias", ""),
                "logo": hold_info.get("logo", ""),
                "percent": hold_info.get("percent", ""),
                "cid": hold_info.get("cid", ""),
                "legal_person_name": hold_info.get("legalPersonName", ""),
                "info_id": info_id,
                "tyc_id": tyc_id,
                "company_name": company_name,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            }
            items.append(item)
        return items

    except Exception as e:
        logger.debug(e)


def main():
    data_list = get_company_230420_name()
    for data in data_list:
        info_id = data[0]
        company_name = data[1]
        tyc_id = data[2]
        pageNum = 1

        if conn.sismember("tyc_company_holding", tyc_id):
            logger.debug("{}=======>数据已经采集，无需再次采集".format(tyc_id))
            continue

        # delete_to_all_company_name(info_id, company_name)
        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        logger.warning("当前企业名称为%s" % company_name)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        pages_total = get_companyholding_page(
            info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token
        )

        if pages_total:
            print(company_name)
            for pageNum in range(1, int(pages_total) + 1):
                items = get_companyholding_info(info_id, company_name, tyc_id, pageNum)
                try:
                    mq = MysqlPipelinePublic()
                    for item in items:
                        mq.insert_sql("t_zx_company_holding_info", item)
                        logger.info("数据 %s 插入成功" % item)
                    mq.close()

                except Exception as e:
                    logger.debug(e)
            # else:
            pass
        conn.sadd("tyc_company_holding", tyc_id)


if __name__ == "__main__":
    main()
