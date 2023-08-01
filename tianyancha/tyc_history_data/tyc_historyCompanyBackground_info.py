#!/usr/bin/conf python
# -*- coding: utf-8 -*-
"""
@desc: tianyancha-历史工商信息
@version: python3
@author: shenr
@time: 2023/05/10
"""


import requests
import json
from loguru import logger
import os, time, math
import uuid
from tianyancha.conf.env import *
from tianyancha.untils.pysql import *
from tianyancha.untils.urls import HISTORY_INDUSTRY_COMMERCE_DATA

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/tyc_historyCompanyBackground_历史工商信息/"
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

    logger.debug(("--tyc_historyCompanyBackground_历史工商信息__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"

    # url = f"https://api6.tianyancha.com/cloud-judicial-risk/bankruptcy/list?gid={tyc_id}&pageSize=20&pageNum={pageNum}"
    # url = f"https://api6.tianyancha.com/cloud-business-state/bid/listV2?area=-100&infoType=-100&pageSize=20&graphId={tyc_id}&pageNum={pageNum}&pubDate=-100"
    url = HISTORY_INDUSTRY_COMMERCE_DATA.format(tyc_id)

    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)
    return data


def get_historyCompanyBackground_page(
    info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token
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

        # url = f"https://api6.tianyancha.com/cloud-business-state/client/summaryList?gid={tyc_id}&pageSize=20&pageNum=1"
        # url = f"https://api6.tianyancha.com/cloud-business-state/standard/list?gid={tyc_id}&pageSize=20&pageNum=1"
        # url = f"https://api6.tianyancha.com/cloud-judicial-risk/risk/courtApp?keyWords={company_name}&pageSize=20&gid={tyc_id}&pageNum=1"
        # url = f"https://api6.tianyancha.com/cloud-judicial-risk/bankruptcy/list?gid={tyc_id}&pageSize=20&pageNum=1"
        # url = f"https://api6.tianyancha.com/cloud-business-state/bid/listV2?area=-100&infoType=-100&pageSize=20&graphId={tyc_id}&pageNum=1&pubDate=-100"
        # url = "https://api6.tianyancha.com/cloud-history-information/historyCompanyBackground/industrialCommercialInformation?needHidden=1&cid=329007081"
        url = HISTORY_INDUSTRY_COMMERCE_DATA.format(tyc_id)
        res = requests.get(url, headers=headers, verify=False).text

        logger.debug(res)

        res_json = json.loads(res)
        print(res_json)

        if "realTotal" in str(res_json["data"]):
            pages_total = math.ceil(int(res_json["data"]["realTotal"]) / 20)

            if pages_total:
                return pages_total
        elif int(res_json["data"]["total"]) > 0:
            pages_total = math.ceil(int(res_json["data"]["total"]) / 20)
            if pages_total:
                return pages_total

        else:
            logger.debug("%s没有破产重整" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_historyCompanyBackground_info(info_id, company_name, tyc_id, pageNum):
    try:
        # url = f"https://api6.tianyancha.com/cloud-business-state/standard/list?gid={tyc_id}&pageSize=20&pageNum={pageNum}"
        # url = f"https://api6.tianyancha.com/cloud-judicial-risk/risk/courtApp?keyWords={company_name}&pageSize=20&gid={tyc_id}&pageNum={pageNum}"
        # url = f"https://api6.tianyancha.com/cloud-judicial-risk/bankruptcy/list?gid={tyc_id}&pageSize=20&pageNum={pageNum}"
        # url = f"https://api6.tianyancha.com/cloud-business-state/bid/listV2?area=-100&infoType=-100&pageSize=20&graphId={tyc_id}&pageNum={pageNum}&pubDate=-100"
        # url = "https://api6.tianyancha.com/cloud-history-information/historyCompanyBackground/industrialCommercialInformation?needHidden=1&cid=329007081"
        url = HISTORY_INDUSTRY_COMMERCE_DATA.format(tyc_id)
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
        item = {
            "locationlist": str(res_json["data"].get("locationlist", "")),
            "creditcodelist": str(res_json["data"].get("creditCodeList", "")),
            "total": str(res_json["data"].get("total", "")),
            "businessscopelist": str(res_json["data"].get("businessScopeList", "")),
            "typelist": str(res_json["data"].get("typeList", "")),
            "orgnumberlist": str(res_json["data"].get("orgNumberList", "")),
            "deadlinelist": str(res_json["data"].get("deadLineList", "")),
            "regcapitallist": str(res_json["data"].get("regCapitalList", "")),
            "regnumberlist": str(res_json["data"].get("regNumberList", "")),
            "historynamelist": str(res_json["data"].get("historyNameList", "")),
            "tyc_id": tyc_id,
            "info_id": info_id,
            "company_name": company_name,
            "uniquet_id": str(tyc_id) + "_" + str(company_name),
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

        # delete_to_all_company_name(info_id, company_name)
        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        logger.warning("当前企业名称为%s" % company_name)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        pages_total = get_historyCompanyBackground_page(
            info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token
        )

        if pages_total:
            print(company_name)
            for pageNum in range(1, int(pages_total) + 1):
                # get_historyCompanyBackground_info(info_id, company_name, tyc_id, pageNum)

                items = get_historyCompanyBackground_info(info_id, company_name, tyc_id, pageNum)
                try:
                    mq = MysqlPipeline()
                    for item in items:
                        mq.insert_into_history_company_background_info(item)
                        logger.info("数据 %s 插入成功" % item)
                    mq.close()

                except Exception as e:
                    logger.debug(e)
        else:
            pass
        # delete_to_all_company_name(info_id,company_name)


if __name__ == "__main__":
    main()
