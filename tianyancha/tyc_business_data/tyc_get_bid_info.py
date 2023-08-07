#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@desc: tianyancha-招投标
@version: python3
@author: QTH
@time: 2023/05/26
"""
import requests
import json
import os, math
import uuid
from untils.pysql import *

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning


from untils.sql_data import TYC_DATA
from untils.urls import BID_URL

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/tyc_bid_file_招投标/"
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

    logger.debug(("--tyc_bid_file_招投标__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"

    # url = f"https://api6.tianyancha.com/cloud-business-state/bid/listV2?area=-100&infoType=-100&pageSize=20&graphId={tyc_id}&pageNum={pageNum}&pubDate=-100"

    data = {"url": BID_URL.format(tyc_id, pageNum), "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)
    return data


def get_bid_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token):
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

        # url = f"https://api6.tianyancha.com/cloud-business-state/bid/listV2?area=-100&infoType=-100&pageSize=20&graphId={tyc_id}&pageNum=1&pubDate=-100"
        url = BID_URL.format(tyc_id, 1)

        res = requests.get(url, headers=headers, verify=False).text

        logger.debug(res)

        res_json = json.loads(res)

        if "realTotal" in str(res_json["data"]):
            pages_total = math.ceil(int(res_json["data"]["realTotal"]) / 20)

            if pages_total:
                return pages_total
        elif int(res_json["data"]["count"]) > 0:
            pages_total = math.ceil(int(res_json["data"]["count"]) / 20)
            if pages_total:
                return pages_total

        else:
            logger.debug("%s没有破产重整" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_bid_info(info_id, company_name, tyc_id, pageNum):
    try:
        # url = f"https://api6.tianyancha.com/cloud-business-state/bid/listV2?area=-100&infoType=-100&pageSize=20&graphId={tyc_id}&pageNum={pageNum}&pubDate=-100"
        url = BID_URL.format(tyc_id, pageNum)

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
        res_json = json.loads(res)
        # create_json(pageNum, info_id, tyc_id, company_name, res_json)
        items = []

        for bid_info in res_json["data"]["items"]:
            if bid_info["supplierList"]:
                supplierList_name = " ".join([name.get("name", "") for name in bid_info["supplierList"]])
            else:
                supplierList_name = None
            if bid_info["purchaserList"]:
                purchaserList_name = " ".join([name.get("name", "") for name in bid_info["purchaserList"]])
            else:
                purchaserList_name = None

            item = {
                "area": bid_info.get("area", ""),
                "bidAmountPaperWork": bid_info.get("bidAmountPaperWork", ""),
                "publishTime": bid_info.get("publishTime", ""),
                "infoCategory": bid_info.get("infoCategory", ""),
                "bidAmountCompany": bid_info.get("bidAmountCompany", ""),
                "bidUrl": bid_info.get("bidUrl", ""),
                "businessId": bid_info.get("businessId", ""),
                "link": bid_info.get("link", ""),
                "bidAmount": bid_info.get("bidAmount", ""),
                "title": bid_info.get("title", ""),
                "bid_type": bid_info.get("type", ""),
                "uuid": bid_info.get("uuid", ""),
                "proxy": bid_info.get("proxy", ""),
                "bid_id": bid_info.get("id", ""),
                "supplierList": supplierList_name,
                "purchaserList": purchaserList_name,
                "tyc_id": tyc_id,
                "info_id": info_id,
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

        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        logger.warning("当前企业名称为%s" % company_name)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        pages_total = get_bid_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token)

        if pages_total:
            print(company_name)
            for pageNum in range(1, int(pages_total) + 1):
                items = get_bid_info(info_id, company_name, tyc_id, pageNum)
                try:
                    # mq = MysqlPipeline()
                    # for item in items:
                    #     mq.insert_into_bid_info(item)
                    #     logger.info("数据 %s 插入成功" % item)
                    # mq.close()
                    for item in items:
                        mq.insert_sql("t_zx_company_bid_info", item)
                except Exception as e:
                    logger.debug(e)
        else:
            pass
    mq.close()


if __name__ == "__main__":
    main()
