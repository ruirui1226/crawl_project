#!/usr/bin/conf python
# -*- coding: utf-8 -*-
"""
@desc: tianyancha-历史法律诉讼详情
@version: python3
@author: shenr
@time: 2023/05/16
"""
import re

import requests
import json
from loguru import logger
import os
import time
import math
from tianyancha.untils.pysql import *
from tianyancha.conf.env import *
import uuid
from pyquery import PyQuery as pq

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from tianyancha.untils.urls import HISTORY_ACTION_AT_LAW

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/jsondata/tyc_历史法律诉讼详情_file/"
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

    logger.debug(("--tyc_历史法律诉讼详情_file__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, deatil_url):
    version = "Android 12.67.0"
    url = deatil_url

    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)

    return data


def get_History_Action_At_Law_page(
    info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, pageNum
):
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

        # data = {
        #     "ps": "20",
        #     "regYear": "-100",
        #     "sortIndex": "-100",
        #     "app_year": "-100",
        #     "int_cls": "-100",
        #     "id": tyc_id,
        #     "pn": "1",
        #     "status": "-100",
        # }
        url = HISTORY_ACTION_AT_LAW.format(tyc_id, pageNum)
        res = requests.get(url=url, headers=headers, verify=False).text

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


def get_History_Action_At_Law_info_detail(info_id, company_name, tyc_id, deatil_url):
    # try:

    url = deatil_url
    res = requests.get(url=url, verify=False).text

    doc = pq(res)
    li_list = re.findall("lawsuitData = (.*?);\n</script", str(doc), re.S)[0]
    js_data = json.loads(li_list)
    print("========", js_data)
    # create_json(deatil_url, info_id, tyc_id, company_name, js_data)
    data_dic = js_data["data"]
    items = []
    item = {}
    item["info_id"] = info_id
    item["company_name"] = company_name
    item["tyc_id"] = tyc_id
    item["title"] = data_dic.get("title", "")
    item["court"] = data_dic.get("court", "")
    item["caseno"] = data_dic.get("caseno", "")
    item["uuid"] = data_dic.get("uuid", "")
    item["url"] = data_dic.get("url", "")
    item["doctype"] = data_dic.get("doctype", "")
    item["lawfirmlist"] = str(data_dic.get("lawFirmList", ""))
    item["judgetime"] = data_dic.get("judgetime", "")
    item["companylist"] = str(data_dic.get("companyList", ""))
    item["planintextlist"] = str(data_dic.get("planinTextList", ""))
    item["lawlist"] = str(data_dic.get("lawList", ""))
    item["casetype"] = data_dic.get("casetype", "")
    item["sourcename"] = data_dic.get("sourceName", "")
    item["monitorstatus"] = data_dic.get("monitorStatus", "")
    item["create_time"] = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),)
    print("======", item)
    items.append(item)
    return items

    # except Exception as e:
    #     logger.debug(e)


def main():
    data_list = get_istory_action_at_law_detail()
    # data_list=get_company_wechat_name()
    for data in data_list:
        info_id = data[0]
        company_name = data[1]
        tyc_id = data[2]
        deatil_url = data[3]

        logger.warning("当前企业名称为-------%s" % company_name)

        items = get_History_Action_At_Law_info_detail(info_id, company_name, tyc_id, deatil_url)
        try:
            mq = MysqlPipelinePublic()
            for item in items:
                # mq.insert_into_HistoryActionAtLaw_info_detail(item)
                mq.insert_sql("t_zx_history_action_at_law_detail", item)
            mq.close()
        except Exception as e:
            logger.debug(e)
        else:
            pass
        # delete_to_mysql_wechat_main(info_id,company_name)


if __name__ == "__main__":
    main()
