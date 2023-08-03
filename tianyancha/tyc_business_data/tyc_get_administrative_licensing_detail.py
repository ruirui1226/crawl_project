#!/usr/bin/conf python
# -*- coding: utf-8 -*-
"""
@desc: tianyancha-行政许可详情
@version: python3
@author: shenr
@time: 2023/05/15
"""

import requests
import json
from loguru import logger
import os
import time
import math
from tianyancha.untils.pysql import *
from tianyancha.conf.env import *

# from untils.redis_conn import conn
# from untils.urls import ADMINISTRATIVE_LICENSING
import uuid

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from tianyancha.untils.urls import ADMINISTRATIVE_LICENSING, ADMINISTRATIVE_LICENSING_DETAIL

from untils.sql_data import TYC_DATA

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/tyc_get_administrative_licensing_detail_file_行政许可详情/"
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

    logger.debug(("--tyc_trademark_file__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, detail_id):
    version = "Android 12.67.0"
    url = ADMINISTRATIVE_LICENSING_DETAIL.format(tyc_id, detail_id)

    params = {"url": url, "version": version}
    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(params))
    data = json.loads(r.text)
    return data


def get_Trademark_info(info_id, company_name, tyc_id, detail_id, detailbusinessid, businessid):
    # try:

    data = get_authoriaztion(info_id, company_name, tyc_id, detail_id)
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

    url = ADMINISTRATIVE_LICENSING_DETAIL.format(tyc_id, detail_id)
    # res = requests.post(url=url, headers=headers, data=json.dumps(data), verify=False).text
    res = requests.get(url=url, headers=headers, verify=False).text

    # logger.debug(res)
    res_json = json.loads(res)
    print("cccc", res_json, "cccc")
    logger.info(f"内容{res}")

    # create_json(pageNum, info_id, tyc_id, company_name, res_json)
    items = []
    # for each in res_json["data"]:
    #     print("55555", each)
    item = {
        "info_id": info_id,
        "licencecontent": str(res_json["data"].get("licenceContent", "")).replace("'", '"'),
        "validitytime": res_json["data"].get("validityTime", ""),
        "legalpersonid": res_json["data"].get("legalPersonId", ""),
        "enddate": res_json["data"].get("endDate", ""),
        "licencenumber": res_json["data"].get("licenceNumber", ""),
        "localcode": res_json["data"].get("localCode", ""),
        "department": res_json["data"].get("department", ""),
        "auditype": res_json["data"].get("audiType", ""),
        "dataupdatetime": res_json["data"].get("dataUpdateTime", ""),
        "decisiondate": res_json["data"].get("decisionDate", ""),
        "legalpersonname": res_json["data"].get("legalPersonName", ""),
        "cid": res_json["data"].get("cid", ""),
        "detailbusinessid": detailbusinessid,
        "businessid": businessid,
        "company_name": company_name,
        "tyc_id": tyc_id,
        "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
    }
    items.append(item)

    return items

    # except Exception as e:
    #     logger.debug(e)


def main():
    data_list = get_company_230420_name_detail()
    # data_list=get_company_wechat_name()
    for data in data_list:
        info_id = data[0]
        company_name = data[1]
        tyc_id = data[2]
        detail_id = data[3] or data[4]
        detailbusinessid = data[3]
        businessid = data[4]

        logger.warning("当前企业名称为%s" % company_name)
        items = get_Trademark_info(info_id, company_name, tyc_id, detail_id, detailbusinessid, businessid)
        try:
            mq = MysqlPipelinePublic()
            for item in items:
                # mq.insert_into_administrative_licensing_detail(item)
                mq.insert_sql("t_zx_tyc_administrative_licensing_detail", item)
                # print(f"======插入===={item}====")
        except Exception as e:
            logger.debug(e)
        else:
            pass
        # delete_to_mysql_wechat_main(info_id,company_name)
    mq.close()


if __name__ == "__main__":
    main()
