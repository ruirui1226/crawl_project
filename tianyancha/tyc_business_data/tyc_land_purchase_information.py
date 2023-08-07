"""
@Time : 2023/5/26 11:11
@Author :QTH
@Desc : 天眼查--购地信息
@Software: PyCharmQTH
"""
import requests
import json
from loguru import logger
import os, time, math
import uuid
from conf.env import *
from untils.pysql import *

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from untils.redis_conn import conn

from untils.sql_data import TYC_DATA
from untils.urls import PURCHASE

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/tyc_purchase_file_购地信息/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = (
        company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + str(pageNum) + "_" + ".json"
    )
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_purchase_file_购地信息__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"

    url = PURCHASE.format(tyc_id, pageNum)
    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)
    return data


def get_land_purchase_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token):
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
        url = PURCHASE.format(tyc_id, "1")

        res = requests.get(url, headers=headers, verify=False).text

        res_json = json.loads(res)
        if "totalRows" in str(res_json["data"]):
            pages_total = math.ceil(int(res_json["data"]["totalRows"]) / 20)
            if pages_total:
                return pages_total
        elif int(res_json["data"]["totalRows"]) > 0:
            pages_total = math.ceil(int(res_json["data"]["totalRows"]) / 10)
            if pages_total:
                return pages_total

        else:
            logger.debug("%s没有购地信息" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_land_purchase_info(pageNum, info_id, company_name, tyc_id):
    try:
        url = PURCHASE.format(tyc_id, pageNum)
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
        # create_json(pageNum, info_id, tyc_id, company_name, res_json)
        items = []
        for zhaopin_info in res_json["data"]["companyPurchaseLandList"]:
            item = {
                "projectLocation": zhaopin_info["projectLocation"],
                "landUseType": zhaopin_info["landUseType"],
                "areaAll": zhaopin_info["areaAll"],
                "contractDate": zhaopin_info["contractDate"],
                "district": zhaopin_info["district"],
                "landSupplyMethod": zhaopin_info["landSupplyMethod"],
                "info_id": info_id,
                "company_name": company_name,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
                "tyc_id": tyc_id,
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
        ex = conn.sismember("tyc_land_purchase", tyc_id)
        if ex:
            logger.debug("%s---------数据已经采集，无需再次采集" % tyc_id)
            continue
        else:
            data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
            tyc_hi = data["data"]["tyc_hi"]
            Authorization = data["data"]["Authorization"]
            duid = data["data"]["duid"]
            deviceID = data["data"]["deviceID"]
            x_auth_token = data["data"]["x_auth_token"]

            pages_total = get_land_purchase_page(
                info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token
            )
            if pages_total:
                print(company_name)
                for pageNum in range(1, int(pages_total) + 1):
                    items = get_land_purchase_info(pageNum, info_id, company_name, tyc_id)
                    try:
                        for item in items:
                            mq.insert_sql("t_zx_tyc_land_purchase_information", item)
                            logger.info("数据 %s 插入成功", item)
                    except Exception as e:
                        logger.debug(e)
            else:
                pass
        conn.sadd("tyc_land_purchase", tyc_id)
    mq.close()


if __name__ == "__main__":
    main()
