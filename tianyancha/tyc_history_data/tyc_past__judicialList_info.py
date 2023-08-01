#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/10 11:25
# @Author  : wym
# @File    : tyc_past_holder_info.py
import requests
import json
from loguru import logger
import os
import time
import math
from tyc_projects.untils.pysql import *
from tyc_projects.conf.env import *
import uuid

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# def create_json(company_name, res_json):
#     folder_name = os.getcwd() + "/tyc_past_holder_file/"
#     if not os.path.exists(folder_name):
#         os.makedirs(folder_name)
#     else:
#         pass
#
#     file_nm = company_name + str(time.time()).split(".")[0] + ".json"
#     # data_json=json.dumps(response.text,sort_keys=True, separators=(',', ': '),indent=4,ensure_ascii=False)
#     with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
#         json.dump(res_json, f, indent=4, ensure_ascii=False)
#
#     logger.debug(("--tyc_weibo_file__写入到-->" + file_nm))


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/tyc_past_judicialList_file_历史司法协助/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + str(pageNum) + ".json"
    # data_json=json.dumps(response.text,sort_keys=True, separators=(',', ': '),indent=4,ensure_ascii=False)
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_past_judicialList_file__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 11.4.0"

    # url = f"https://api4.tianyancha.com/services/v3/expanse/holder?pageSize=20&id={tyc_id}&pageNum={pageNum}"
    # url=f"https://api4.tianyancha.com/services/v3/expanse/publicWeChat?pageSize=20&id={tyc_id}&pageNum={pageNum}"
    # url = (
    #     f"https://api4.tianyancha.com/cloud-newdim/company/getWeiboList?pageSize=20&graphId={tyc_id}&pageNum={pageNum}"
    # )

    # url=f"https://api4.tianyancha.com/services/v3/past/holder?pageSize=20&id={tyc_id}&pageNum={pageNum}"

    # url=f"https://api4.tianyancha.com/services/v3/past/announcement?pageSize=20&id={tyc_id}&pageNum={pageNum}"

    # url=f"https://api4.tianyancha.com/services/v3/past/courtV3/{tyc_id}?pageSize=20&pageNum={pageNum}"

    url = f"https://api4.tianyancha.com/cloud-newdim/past/judicialList?pageSize=20&id={tyc_id}&pageNum={pageNum}"

    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9898/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)
    return data


def get_past_judicialList_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID):
    try:
        headers = {
            "user-agent": "com.tianyancha.skyeye/Dalvik/2.1.0 (Linux; U; Android 8.1.0; Nexus 6P Build/OPM7.181205.001; appDevice/google_QAQ_Nexus 6P)",
            "authorization": Authorization,
            "x-auth-token": X_AUTH_TOKEN,
            "channelid": "YingYongBao",
            "deviceid": deviceID,
            "tyc-hi": tyc_hi,
            "version": "Android 11.4.0",
            "duid": duid,
            "content-type": "application/json",
        }

        # url = f"https://api4.tianyancha.com/services/v3/expanse/holder?pageSize=20&id={tyc_id}&pageNum=1"
        # url=f"https://api4.tianyancha.com/services/v3/expanse/publicWeChat?pageSize=20&id={tyc_id}&pageNum=1"
        # url = f"https://api4.tianyancha.com/services/v3/past/holder?pageSize=20&id={tyc_id}&pageNum=1"
        # url = f"https://api4.tianyancha.com/services/v3/past/announcement?pageSize=20&id={tyc_id}&pageNum=1"
        # url = f"https://api4.tianyancha.com/services/v3/past/courtV3/{tyc_id}?pageSize=20&pageNum=1"

        # url=f"https://api4.tianyancha.com/cloud-newdim/company/getHistoryAbnormalList.json?gid={tyc_id}&pageSize=20&pageNum=1"
        url = f"https://api4.tianyancha.com/cloud-newdim/past/judicialList?pageSize=20&id={tyc_id}&pageNum=1"
        res = requests.get(url=url, headers=headers, verify=False).text

        # logger.debug(res)
        res_json = json.loads(res)
        if "totalCount" in str(res_json["data"]):
            pages_total = math.ceil(int(res_json["data"]["totalCount"]) / 20)

            if pages_total:
                return pages_total
        elif int(res_json["data"]["count"]) > 0:
            pages_total = math.ceil(int(res_json["data"]["count"]) / 20)
            if pages_total:
                return pages_total

        else:
            logger.debug("%s没有历史法院公告" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_past_judicialList_info(info_id, company_name, tyc_id, pageNum):
    try:
        url = f"https://api4.tianyancha.com/cloud-newdim/past/judicialList?pageSize=20&id={tyc_id}&pageNum={pageNum}"
        logger.warning(url)
        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]

        headers = {
            "user-agent": "com.tianyancha.skyeye/Dalvik/2.1.0 (Linux; U; Android 8.1.0; Nexus 6P Build/OPM7.181205.001; appDevice/google_QAQ_Nexus 6P)",
            "authorization": Authorization,
            "x-auth-token": X_AUTH_TOKEN,
            "channelid": "YingYongBao",
            "deviceid": deviceID,
            "tyc-hi": tyc_hi,
            "version": "Android 11.4.0",
            "duid": duid,
            "content-type": "application/json",
        }
        res = requests.get(url=url, headers=headers, verify=False).text

        logger.debug(res)
        res_json = json.loads(res)

        create_json(pageNum, info_id, tyc_id, company_name, res_json)
        # items = []
        # for weibo_info in res_json["data"]["result"]:
        #     if weibo_info["tags"]:
        #         tags="".join([tags.replace("/"," ") for tags in weibo_info.get("tags", "")])
        #     else:
        #         tags=""
        #
        #     item = {
        #         "info_id": info_id,
        #         "ico": weibo_info.get("ico", ""),
        #         "name": weibo_info.get("name", ""),
        #         "href": weibo_info.get("href", ""),
        #         "info": weibo_info.get("info", ""),
        #         "tags": tags,
        #         "company_name": company_name,
        #         "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        #     }
        #     items.append(item)
        #
        # return items

    except Exception as e:
        logger.debug(e)


def main():
    data_list = get_company_name()
    for data in data_list:
        info_id = data[0]
        company_name = data[1]
        tyc_id = data[2]
        pageNum = 1
        logger.warning("当前企业名称为%s" % company_name)
        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        # get_Weibo_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID)
        pages_total = get_past_judicialList_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID)
        if pages_total:
            print(company_name)
            for pageNum in range(1, int(pages_total) + 1):
                get_past_judicialList_info(info_id, company_name, tyc_id, pageNum)

                # items = get_Weibo_info(info_id, company_name, tyc_id, pageNum)
        #         try:
        #
        #             mq = MysqlPipeline()
        #             for item in items:
        #                 mq.insert_into_Weibo_info(item)
        #                 logger.info("数据 %s 插入成功" % item)
        #             mq.close()
        #
        #         except Exception as e:
        #             logger.debug(e)
        # else:
        #     pass
        # delete_to_mysql_wechat_main(info_id,company_name)


if __name__ == "__main__":
    main()
