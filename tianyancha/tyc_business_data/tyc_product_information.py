"""
@Time : 2023/5/26 11:11
@Author :QTH
@Desc : 天眼查--产品信息
@Software: PyCharmQTH
"""
import requests
import json
from loguru import logger
import os
import time
import math

from conf.env import *
import uuid

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from untils.pysql import *
from untils.redis_conn import conn

from untils.sql_data import TYC_DATA

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/tyc_appbkinfo_file_产品信息/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + str(pageNum) + ".json"
    # data_json=json.dumps(response.text,sort_keys=True, separators=(',', ': '),indent=4,ensure_ascii=False)
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_appbkinfo_file_产品信息__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"

    url = f"https://api6.tianyancha.com/cloud-business-state/v3/ar/appbkinfo?pageSize=20&id={tyc_id}&pageNum={pageNum}"

    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)
    return data


def get_product_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, X_AUTH_TOKEN):
    try:
        headers = {
            "user-agent": "com.tianyancha.skyeye/Dalvik/2.1.0 (Linux; U; Android 8.1.0; Nexus 6P Build/OPM7.181205.001; appDevice/google_QAQ_Nexus 6P)",
            "authorization": Authorization,
            "x-auth-token": X_AUTH_TOKEN,
            "channelid": "YingYongBao",
            "deviceid": deviceID,
            "tyc-hi": tyc_hi,
            "version": "Android 12.67.0",
            "duid": duid,
            "content-type": "application/json",
        }

        url = f"https://api6.tianyancha.com/cloud-business-state/v3/ar/appbkinfo?pageSize=20&id={tyc_id}&pageNum=1"

        res = requests.get(url=url, headers=headers, verify=False).text

        # logger.debug(res)
        res_json = json.loads(res)
        if "total" in str(res_json["data"]):
            pages_total = math.ceil(int(res_json["data"]["total"]) / 20)

            if pages_total:
                return pages_total
        elif len(res_json["data"]) == 0:
            logger.info("%s没有产品信息" % company_name)

        elif int(res_json["data"]["count"]) > 0:
            pages_total = math.ceil(int(res_json["data"]["count"]) / 20)
            if pages_total:
                return pages_total

        else:
            logger.debug("%s没有产品信息" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_product_info(info_id, company_name, tyc_id, pageNum):
    try:
        url = f"https://api6.tianyancha.com/cloud-business-state/v3/ar/appbkinfo?pageSize=20&id={tyc_id}&pageNum={pageNum}"
        logger.warning(url)
        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        X_AUTH_TOKEN = data["data"]["x_auth_token"]
        headers = {
            "user-agent": "com.tianyancha.skyeye/Dalvik/2.1.0 (Linux; U; Android 8.1.0; Nexus 6P Build/OPM7.181205.001; appDevice/google_QAQ_Nexus 6P)",
            "authorization": Authorization,
            "x-auth-token": X_AUTH_TOKEN,
            "channelid": "YingYongBao",
            "deviceid": deviceID,
            "tyc-hi": tyc_hi,
            "version": "Android 12.67.0",
            "duid": duid,
            "content-type": "application/json",
        }
        res = requests.get(url=url, headers=headers, verify=False).text

        logger.debug(res)
        res_json = json.loads(res)

        # create_json(pageNum, info_id, tyc_id, company_name, res_json)
        items = []
        for bk_info in res_json["data"]["items"]:
            item = {
                "info_id": info_id,
                "brief": bk_info.get("brief", ""),
                "classes": bk_info.get("classes", ""),
                "businessId": bk_info.get("businessId", ""),
                "icon": bk_info.get("icon", ""),
                "name": bk_info.get("name", ""),
                "filterName": bk_info.get("filterName", ""),
                "type": bk_info.get("type", ""),
                "uuid": bk_info.get("uuid", ""),
                "tyc_id": tyc_id,
                "company_name": company_name,
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
        ex = conn.sismember("t_zx_tyc_appbkinfo_file", tyc_id)
        if ex:
            logger.debug("%s---------数据已经采集，无需再次采集" % tyc_id)
            continue
        logger.warning("当前企业名称为%s" % company_name)
        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        pages_total = get_product_page(
            info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token
        )
        if pages_total:
            print(company_name)
            for pageNum in range(1, int(pages_total) + 1):
                items = get_product_info(info_id, company_name, tyc_id, pageNum)
                try:
                    for item in items:
                        mq.insert_sql("t_zx_tyc_appbkinfo_file", item)
                        logger.info("数据 %s 插入成功" % item)
                except Exception as e:
                    logger.debug(e)
        else:
            pass
        conn.sadd("t_zx_tyc_appbkinfo_file", tyc_id)
    mq.close()


if __name__ == "__main__":
    main()
