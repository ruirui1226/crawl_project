"""
@Time : 2023/5/19 13：57
@Author : QTH
@File : tyc_on_the_list.py
@Desc : 天眼查--微博
@Software: PyCharm
"""
import requests
import json
from loguru import logger
import os
import time
import math
from untils.pysql import *

# from tyc_projects.conf.env import *

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(company_name, res_json):
    folder_name = os.getcwd() + "/tyc_weibo_file/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + str(time.time()).split(".")[0] + ".json"
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_weibo_file微博__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    url = f"https://api6.tianyancha.com/cloud-business-state/weibo/list?pageSize=20&graphId={tyc_id}&pageNum={pageNum}"
    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9964/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)
    return data


def get_Weibo_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, X_AUTH_TOKEN):
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

        url = f"https://api6.tianyancha.com/cloud-business-state/weibo/list?pageSize=20&graphId={tyc_id}&pageNum=1"
        # print(url)
        res = requests.get(url=url, headers=headers, verify=False).text

        # logger.debug(res)
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
            logger.debug("%s没有微博数据" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_Weibo_info(info_id, company_name, tyc_id, pageNum):
    try:
        url = f"https://api6.tianyancha.com/cloud-business-state/weibo/list?pageSize=20&graphId={tyc_id}&pageNum={pageNum}"
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

        # create_json(company_name, res_json)
        items = []
        for weibo_info in res_json["data"]["result"]:
            if weibo_info["tags"]:
                tags = "".join([tags.replace("/", " ") for tags in weibo_info.get("tags", "")])
            else:
                tags = ""

            item = {
                "info_id": info_id,
                "ico": weibo_info.get("ico", ""),
                "name": weibo_info.get("name", ""),
                "href": weibo_info.get("href", ""),
                "info": weibo_info.get("info", ""),
                "tags": tags,
                "company_name": company_name,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
                "tyc_id": tyc_id,
            }
            items.append(item)

        return items

    except Exception as e:
        logger.debug(e)


def main():
    mq = MysqlPipelinePublic()
    data_list = mq.select_sql("t_zx_company_tyc_all_infos", ["id", "company_name", "tyc_id"], {"is_lz": "1"})
    for data in data_list:
        info_id = data.get("id")
        company_name = data.get("company_name")
        tyc_id = data.get("tyc_id")
        pageNum = 1
        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        pages_total = get_Weibo_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token)
        if pages_total:
            print(company_name)
            for pageNum in range(1, int(pages_total) + 1):
                items = get_Weibo_info(info_id, company_name, tyc_id, pageNum)
                try:
                    # mq = MysqlPipeline()
                    # for item in items:
                    #     mq.insert_into_Weibo_info(item)
                    #     logger.info("数据 %s 插入成功" % item)
                    # mq.close()
                    mq = MysqlPipelinePublic()
                    for item in items:
                        mq.insert_sql("t_zx_company_weibo_info", item)
                        logger.info("数据 %s 插入成功" % item)
                    mq.close()
                except Exception as e:
                    logger.debug(e)
        else:
            pass


if __name__ == "__main__":
    main()
