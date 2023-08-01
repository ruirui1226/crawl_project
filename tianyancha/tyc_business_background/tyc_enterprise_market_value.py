#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/5/17 13:31
@Author : zhangpf
@File : tyc_enterprise_market_value.py
@Desc : 市值A股  港股
@Software: PyCharm
"""

import requests
import json
from loguru import logger
import os
import time
import math
from untils.pysql import *
from conf.env import *
import uuid
from untils.redis_conn import conn

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from untils.urls import ENTERPRISE_MARKET_VALUE

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/jsondata/tyc_企业市值_file/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + "_" + ".json"
    # data_json=json.dumps(response.text,sort_keys=True, separators=(',', ': '),indent=4,ensure_ascii=False)
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_企业市值_file__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, bondNum):
    version = "Android 12.67.0"
    url = ENTERPRISE_MARKET_VALUE.format(tyc_id, bondNum)

    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)

    return data


def get_enterprise_market_value_info(info_id, company_name, tyc_id, bondNum):
    try:
        # print(url)
        # res = requests.get(url=url, headers=headers, verify=False).text

        data = get_authoriaztion(info_id, company_name, tyc_id, bondNum)
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

        url = ENTERPRISE_MARKET_VALUE.format(tyc_id, bondNum)
        res = requests.get(url=url, headers=headers, verify=False).text

        # logger.debug(res)
        res_json = json.loads(res)
        create_json(info_id, tyc_id, company_name, res_json)
        data = res_json["data"]
        items = []
        item = {
            "info_id": info_id,
            "stockcode": data.get("stockcode", ""),
            "stockname": data.get("stockname", ""),
            "timeshow": data.get("timeshow", ""),
            "fvaluep": data.get("fvaluep", ""),
            "tvalue": data.get("tvalue", ""),
            "flowvalue": data.get("flowvalue", ""),
            "tvaluep": data.get("tvaluep", ""),
            "topenprice": data.get("topenprice", ""),
            "tamount": data.get("tamount", ""),
            "trange": data.get("trange", ""),
            "thighprice": data.get("thighprice", ""),
            "tamounttotal": data.get("tamounttotal", ""),
            "tchange": data.get("tchange", ""),
            "tlowprice": data.get("tlowprice", ""),
            "pprice": data.get("pprice", ""),
            "tmaxprice": data.get("tmaxprice", ""),
            "tminprice": data.get("tminprice", ""),
            "hexm_curPrice": data.get("hexm_curPrice", ""),
            "hexm_float_price": data.get("hexm_float_price", ""),
            "hexm_float_rate": data.get("hexm_float_rate", ""),
            "stop": data.get("stop", ""),
            "stockStatus": data.get("stockStatus", ""),
            "marketType": data.get("marketType", ""),
            "stockType": data.get("stockType", ""),
            "code_type": data.get("code_type", ""),
            "graphId": data.get("graphId", ""),
            "plate_weight_num": data.get("plate_weight_num", ""),
            "onlineIssueDate": data.get("onlineIssueDate    ", ""),
            "listingDate": data.get("listingDate", ""),
            "flag": data.get("flag", ""),
            "listingStatus": data.get("listingStatus", ""),
            "listingType": data.get("listingType", ""),
            "company_name": company_name,
            "tyc_id": tyc_id,
            "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            "unique_id": str(data.get("graphId", "")) + "_" + str(tyc_id),
        }
        items.append(item)
        print(items)
        return items

    except Exception as e:
        logger.debug(e)


def main():
    data_list = get_company_code_info_0411()
    for data in data_list:
        info_id = data[0]
        company_name = data[1]
        tyc_id = data[2]
        bondNum = data[3]
        ex = conn.sadd("tyc_enterprise_market_value", tyc_id)
        logger.warning("当前企业ID为-------%s" % tyc_id)
        if ex == 1:
            logger.warning("当前企业名称为-------%s" % company_name)
            items = get_enterprise_market_value_info(info_id, company_name, tyc_id, bondNum)
            try:
                mq = MysqlPipelinePublic()
                for item in items:
                    mq.insert_sql("t_zx_enterprise_market_value", item)
                mq.close()

            except Exception as e:
                logger.debug(e)
        else:
            logger.debug("%s======>数据已经采集，无需再次采集" % tyc_id)
            pass
        # delete_to_mysql_wechat_main(info_id,company_name)


if __name__ == "__main__":
    main()
