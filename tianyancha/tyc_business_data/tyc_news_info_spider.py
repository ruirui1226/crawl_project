#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/5/29 9：55
@Author : QTH
@Desc : 天眼查--新闻舆情
@Software: PyCharm
"""

import requests
import json
from loguru import logger
import os, time, math
import uuid
from tianyancha.conf.env import *
from tianyancha.untils.pysql import *

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from untils.redis_conn import conn

from untils.sql_data import TYC_DATA

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/tyc_newsinfo_file_新闻舆情/"
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

    logger.debug(("--tyc_newsinfo_file_新闻舆情__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"

    url = f"https://api6.tianyancha.com/cloud-yq-news/company/detail/publicmsg/news/web.json?ps=20&emotion=-100&id={tyc_id}&event=-100&type=0&pn={pageNum}"
    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)
    return data


def get_news_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token):
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

        url = f"https://api6.tianyancha.com/cloud-yq-news/company/detail/publicmsg/news/web.json?ps=20&emotion=-100&id={tyc_id}&event=-100&type=0&pn=1"

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
            logger.debug("没有新闻舆情%s" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_news_info(info_id, company_name, tyc_id, pageNum):
    try:
        url = f"https://api6.tianyancha.com/cloud-yq-news/company/detail/publicmsg/news/web.json?ps=20&emotion=-100&id={tyc_id}&event=-100&type=0&pn={pageNum}"

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

        for news_info in res_json["data"]["items"]:
            item = {
                "firstImg": news_info.get("firstImg", ""),
                "title": news_info.get("title", ""),
                "relevantList": str(news_info.get("relevantList", "")),
                "imgsList": str(news_info.get("imgsList", "")),
                "orgGidsList": str(news_info.get("orgGidsList", "")),
                "website": news_info.get("website", ""),
                "eventLabels": str(news_info.get("eventLabels", "")),
                "abstracts": str(news_info.get("abstracts", "")),
                "docid": news_info.get("docid", ""),
                "emotionLabels": str(news_info.get("emotionLabels", "")),
                "rtm": news_info.get("rtm", ""),
                "imgsCount": news_info.get("imgsCount", ""),
                "uri": news_info.get("uri", ""),
                "tags_json": str(news_info.get("tags_json", "")),
                "labels": str(news_info.get("labels", "")),
                "comGidsList": str(news_info.get("comGidsList", "")),
                "hGidsList": str(news_info.get("hGidsList", "")),
                "company_name": company_name,
                "tyc_id": tyc_id,
                "info_id": info_id,
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
        ex = conn.sadd("news_tyc_id", tyc_id)
        if ex == 1:
            data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
            logger.warning("当前企业名称为%s" % company_name)
            tyc_hi = data["data"]["tyc_hi"]
            Authorization = data["data"]["Authorization"]
            duid = data["data"]["duid"]
            deviceID = data["data"]["deviceID"]
            x_auth_token = data["data"]["x_auth_token"]
            pages_total = get_news_page(
                info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token
            )
            if pages_total:
                for pageNum in range(1, int(pages_total) + 1):
                    items = get_news_info(info_id, company_name, tyc_id, pageNum)
                    logger.warning(items)
                    for item in items:
                        try:
                            mq.insert_sql("t_zx_company_newslist_info", item)
                            logger.info("数据 %s 插入成功" % item)
                        except Exception as e:
                            logger.debug(e)
            else:
                pass
        else:
            logger.debug("%s---------数据已经采集，无需再次采集" % tyc_id)
            pass
        #
        # delete_to_news_info(info_id, company_name)
    mq.close()


if __name__ == "__main__":
    main()
