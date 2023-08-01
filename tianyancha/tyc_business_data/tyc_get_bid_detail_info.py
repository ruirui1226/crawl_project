# -*- coding: utf-8 -*-
# @Time : 2023/6/30 11:21
# @Author: mayj

# 招投标详情

import requests
import json

import time

from pymysql.converters import escape_string

from untils.pysql import *
from conf.env import *
from untils.redis_conn import conn
from untils.urls import BID_DETAIL

# 忽略requests证书警告
try:
    import urllib3
    from urllib3.exceptions import InsecureRequestWarning

    urllib3.disable_warnings(InsecureRequestWarning)
except:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_authoriaztion(p_id):
    version = "Android 12.67.0"
    url = BID_DETAIL.format(p_id)

    data = {"url": url, "version": version}

    r = requests.post(GET_AUTHORZATION_LOCAL_API, data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)

    return data


def get_bid_det_info(info_id, company_name, tyc_id, b_id):
    url = BID_DETAIL.format(b_id)
    logger.warning(url)
    data = get_authoriaztion(b_id)
    tyc_hi = data["data"]["tyc_hi"]
    Authorization = data["data"]["Authorization"]
    duid = data["data"]["duid"]
    deviceID = data["data"]["deviceID"]
    x_auth_token = data["data"]["x_auth_token"]

    headers = {
        "Host": "m.tianyancha.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Nexus 6P Build/N2G48C; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36 TYC/12.67.0 StatusBarHeight/84 Factory/google Channel/huawei ABI/arm64-v8a FromTYCAndroidClient(appVersion/Android 12.67.0,appDevice/google_QAQ_Nexus 6P)",
        "device-uuid": deviceID,
        "deviceid": deviceID,
        "tdid": "3c295beb1cb5a2558da314cd2b1ba571c",
        "content-type": "application/json",
        "version": "Android 12.67.0",
        "channelid": "huawei",
        "x-auth-token": x_auth_token,
        "duid": duid,
        "authorization": Authorization,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,en-US;q=0.8",
        "X-Requested-With": "com.tianyancha.skyeye",
    }

    res = requests.get(url=url, headers=headers, verify=False).text

    # logger.debug(res)

    if 'itemprop="name"' in res:
        item = {
            "info_id": info_id,
            "company_name": company_name,
            "tyc_id": tyc_id,
            "url": url,
            "bid_id": b_id,
            "html_con": escape_string(res),
            "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        }

        return item

    else:
        print('')
        return


def main():

    det_req_name = "tyc_bid:tyc_get_bid_req_info"
    det_filter_name = "tyc_bid:tyc_get_bid_det_info"
    data_list = conn.smembers(det_req_name)
    mq = MysqlPipelinePublic()
    for data_str in data_list:
        time.sleep(1)
        data = json.loads(data_str)
        info_id = data["info_id"]
        company_name = data["company_name"]
        tyc_id = data["tyc_id"]
        b_id = data["p_id"]

        unique_id = tyc_id + b_id
        logger.warning("当前招投标id为%s" % b_id)
        if conn.sismember(det_filter_name, unique_id):
            logger.debug("{}=======>数据已经采集，无需再次采集".format(b_id))
            conn.srem(det_req_name, data_str)
            continue
        item = get_bid_det_info(info_id, company_name, tyc_id, b_id)
        if item:
            logger.info(json.dumps(item))

            mq.insert_sql("t_zx_company_bid_det_info", item)
            conn.sadd(det_filter_name, unique_id)
            conn.srem(det_req_name, data_str)
        else:
            logger.error("获取详情信息失败：{}".format(b_id))


if __name__ == "__main__":
    main()
