"""
@desc: tianyancha-进口出口
@version: python3
@author: QTH
@time: 2023/05/26
"""
import requests
import json
from loguru import logger
import os
import time
import math

# from tyc_projects.untils.pysql import *

from conf.env import *

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from untils.pysql import get_company_230420_name, MysqlPipeline
from untils.redis_conn import conn

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(company_name, res_json):
    folder_name = os.getcwd() + "/tyc_importAndExport_file/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + str(time.time()).split(".")[0] + ".json"
    # data_json=json.dumps(response.text,sort_keys=True, separators=(',', ': '),indent=4,ensure_ascii=False)
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_importAndExport_file进口出口__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"

    url = f"https://api6.tianyancha.com/cloud-business-state/import/export/credit/info?graphId={tyc_id}"
    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)
    return data


def get_importAndExport_info(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, X_AUTH_TOKEN):
    try:
        url = f"https://api6.tianyancha.com/cloud-business-state/import/export/credit/info?graphId={tyc_id}"

        logger.warning(url)

        headers = {
            "user-agent": "com.tianyancha.skyeye/Dalvik/2.1.0 (Linux; U; Android 8.1.0; Nexus 6P Build/OPM7.181205.001; appDevice/google_QAQ_Nexus 6P)",
            "authorization": Authorization,
            "x-auth-token": X_AUTH_TOKEN,
            "channelid": "huawei",
            "deviceid": deviceID,
            "tyc-hi": tyc_hi,
            "version": "Android 12.67.0",
            "duid": duid,
            "content-type": "application/json",
        }
        res = requests.get(url=url, headers=headers, verify=False).text

        logger.warning(res)
        res_json = json.loads(res)

        # create_json(company_name, res_json)
        if res_json["data"]:
            if res_json["data"]["baseInfo"]:
                importAndExport_base_info = res_json["data"]["baseInfo"]
                importAndExport_base_item = {
                    "info_id": info_id,
                    "types": importAndExport_base_info.get("types", ""),
                    "specialTradeArea": importAndExport_base_info.get("specialTradeArea", ""),
                    "industryCategory": importAndExport_base_info.get("ndustryCategory", ""),
                    "managementCategory": importAndExport_base_info.get("managementCategory", ""),
                    "companyName": importAndExport_base_info.get("companyName", ""),
                    "businessId": importAndExport_base_info.get("businessId", ""),
                    "crCode": importAndExport_base_info.get("crCode", ""),
                    "administrativeDivision": importAndExport_base_info.get("administrativeDivision", ""),
                    "economicDivision": importAndExport_base_info.get("economicDivision", ""),
                    "companyId": importAndExport_base_info.get("companyId", ""),
                    "validityDate": importAndExport_base_info.get("validityDate", ""),
                    "recordDate": importAndExport_base_info.get("recordDate", ""),
                    "customsRegisteredAddress": importAndExport_base_info.get("customsRegisteredAddress", ""),
                    "annualReport": importAndExport_base_info.get("annualReport", ""),
                    "status": importAndExport_base_info.get("status", ""),
                    "company_name": company_name,
                    "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
                    "tyc_id": tyc_id,
                    "creditLevel": importAndExport_base_info.get("creditLevel", "")
                }
            else:
                importAndExport_base_item = None
                pass

            if res_json["data"]["creditRating"]:
                creditRating_items = []
                for importAndExport_creditRating_info in res_json["data"]["creditRating"]:
                    importAndExport_creditRating_item = {
                        "info_id": info_id,
                        "authenticationCode": importAndExport_creditRating_info.get("authenticationCode", ""),
                        "identificationTime": importAndExport_creditRating_info.get("identificationTime", ""),
                        "creditRating": importAndExport_creditRating_info.get("creditRating", ""),
                        "company_name": company_name,
                        "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
                        "tyc_id": tyc_id,
                    }
                    creditRating_items.append(importAndExport_creditRating_item)
            else:
                creditRating_items = None
                pass

            if res_json["data"]["sanction"]:
                sanction_items = []
                for importAndExport_sanction_info in res_json["data"]["sanction"]:
                    importAndExport_sanction_item = {
                        "info_id": info_id,
                        "gid": importAndExport_sanction_info.get("gid", ""),
                        "decisionNumber": importAndExport_sanction_info.get("decisionNumber", ""),
                        "penaltyDate": importAndExport_sanction_info.get("penaltyDate", ""),
                        "natureOfCase": importAndExport_sanction_info.get("natureOfCase", ""),
                        "type": importAndExport_sanction_info.get("type", ""),
                        "party": importAndExport_sanction_info.get("party", ""),
                        "company_name": company_name,
                        "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
                        "tyc_id": tyc_id,
                    }

                    sanction_items.append(importAndExport_sanction_item)
            else:
                sanction_items = None

            all_data = {
                "base_info": importAndExport_base_item,
                "creditRating_items": creditRating_items,
                "sanction_items": sanction_items,
            }

            return all_data

        else:
            pass

    except Exception as e:
        conn.srem("importandexport_id", tyc_id)
        logger.debug(e)


def main():
    data_list = get_company_230420_name()
    for data in data_list:
        info_id = data[0]
        company_name = data[1]
        tyc_id = data[2]
        pageNum = 1
        ex = conn.sadd("importandexport_id", tyc_id)
        if ex == 1:
            logger.warning("当前企业名称为%s" % company_name)
            data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
            tyc_hi = data["data"]["tyc_hi"]
            Authorization = data["data"]["Authorization"]
            duid = data["data"]["duid"]
            deviceID = data["data"]["deviceID"]
            x_auth_token = data["data"]["x_auth_token"]
            all_data = get_importAndExport_info(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token)
            if all_data:
                base_info = all_data.get("base_info", "")
                creditRating_items = all_data.get("creditRating_items", "")
                sanction_items = all_data.get("sanction_items", "")
                try:
                    mq = MysqlPipeline()
                    if base_info:
                        mq.insert_into_importAndExport_base_info(base_info)
                        logger.info("数据 %s 插入成功" % base_info)
                    if creditRating_items:
                        for creditRating_item in creditRating_items:
                            mq.insert_into_importAndExport_creditRating_info(creditRating_item)
                            logger.info("数据%s 插入成功" % creditRating_item)
                    if sanction_items:
                        for sanction_item in sanction_items:
                            mq.insert_into_importAndExport_sanction_info(sanction_item)
                            logger.info("数据%s 插入成功" % sanction_item)
                    mq.close()
                except Exception as e:
                    logger.debug(e)
            else:
                pass
        else:
            logger.debug("%s---------数据已经采集，无需再次采集" % tyc_id)


if __name__ == "__main__":
    main()
