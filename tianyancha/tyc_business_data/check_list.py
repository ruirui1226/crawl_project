"""
@desc: tianyancha-抽查检查
@version: python3
@author: QTH
@time: 2023/05/26
"""

import datetime
import json
import math
import os
import time

import requests
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

# from conf.env import X_AUTH_TOKEN
from untils.pysql import *
from conf.env import *
from untils.sql_data import TYC_DATA
from untils.urls import CHECK_LIST

disable_warnings(InsecureRequestWarning)


def get_auth(pCompanyName, pTycId, pPageNum=1):
    iVersion = "Android 12.67.0"
    iUrl = CHECK_LIST.format(pTycId, pCompanyName, pPageNum)
    # iUrl = f"https://api6.tianyancha.com/cloud-business-state/check/list?gid={pTycId}&name={pCompanyName}&pageSize=20&pageNum={pPageNum}"

    iData = {"url": iUrl, "version": iVersion}
    iResp = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(iData))
    iRespJson = iResp.json()
    logger.info(iRespJson)
    return iRespJson


def create_json(pCompanyName, pResJson):
    iFolderName = os.getcwd() + "/tyc_check_list_file_抽查检查/"
    if not os.path.exists(iFolderName):
        os.makedirs(iFolderName)
    else:
        pass

    iFileName = pCompanyName + str(time.time()).split(".")[0] + ".json"
    with open(iFolderName + "/" + iFileName, "w", encoding="utf-8") as f:
        json.dump(pResJson, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_summary_check_file__ 抽查检查__写入到-->" + iFileName))


def get_total_page(pCompanyName, pTycId, pPageNum=1):
    iUrl = CHECK_LIST.format(pTycId, pCompanyName, pPageNum)

    iData = get_auth(pTycId=pTycId, pPageNum=pPageNum, pCompanyName=pCompanyName)
    iTycHi = iData["data"]["tyc_hi"]
    iAuthorization = iData["data"]["Authorization"]
    iDeviceID = iData["data"]["deviceID"]
    X_AUTH_TOKEN = iData["data"]["x_auth_token"]

    iHeaders = {
        "x-b3-traceid-jindi": "",
        "x-b3-sampled-jindi": "",
        "Authorization": iAuthorization,
        "version": "Android 12.67.0",
        "X-Auth-Token": X_AUTH_TOKEN,
        "Content-Type": "application/json",
        "channelID": "huawei",
        "deviceID": "1bbaf81111eb23c5",
        "deviceModel": "Nexus 6P",
        "deviceVersion": "8.1.0",
        "tyc-hi": iTycHi,
        "sensorsAnonymousId": iDeviceID,
        "device-uuid": iDeviceID,
        "tdid": "36c73d82d939322125bf91fa8ae59b3d5",
        "device_uuid": iDeviceID,
        "app_channel": "huawei",
        "app-code": "670",
        "androidid": iDeviceID,
        "oaid": "00000000-0000-0000-0000-000000000000",
        # "Connection": close
        "User-Agent": "com.tianyancha.skyeye/Dalvik/2.1.0 (Linux; U; Android 8.1.0; Nexus 6P Build/OPM7.181205.001; appDevice/google_QAQ_Nexus 6P)",
        "Cache-Control": "no-cache, no-store",
        "Host": "api6.tianyancha.com",
        "Accept-Encoding": "gzip",
    }
    iRes = requests.get(url=iUrl, headers=iHeaders, verify=False).json()

    logger.success(iRes)
    if iRes["data"] in [{}, None]:
        return None
    elif "total" in str(iRes["data"]):
        iPagesTotal = math.ceil(int(iRes["data"]["total"]) / 20)
        if iPagesTotal:
            return iPagesTotal
    elif int(iRes["data"]["count"]) > 0:
        iPagesTotal = math.ceil(int(iRes["data"]["count"]) / 20)
        if iPagesTotal:
            return iPagesTotal


def get_bond_info(pInfoId, pCompanyName, pTycId, pPageNum=1):
    iUrl = CHECK_LIST.format(pTycId, pCompanyName, pPageNum)

    iData = get_auth(pTycId=pTycId, pPageNum=pPageNum, pCompanyName=pCompanyName)
    iTycHi = iData["data"]["tyc_hi"]
    iAuthorization = iData["data"]["Authorization"]
    iDeviceID = iData["data"]["deviceID"]
    X_AUTH_TOKEN = iData["data"]["x_auth_token"]

    iHeaders = {
        "x-b3-traceid-jindi": "",
        "x-b3-sampled-jindi": "",
        "Authorization": iAuthorization,
        "version": "Android 12.67.0",
        "X-Auth-Token": X_AUTH_TOKEN,
        "Content-Type": "application/json",
        "channelID": "huawei",
        "deviceID": "1bbaf81111eb23c5",
        "deviceModel": "Nexus 6P",
        "deviceVersion": "8.1.0",
        "tyc-hi": iTycHi,
        "sensorsAnonymousId": iDeviceID,
        "device-uuid": iDeviceID,
        "tdid": "36c73d82d939322125bf91fa8ae59b3d5",
        "device_uuid": iDeviceID,
        "app_channel": "huawei",
        "app-code": "670",
        "androidid": iDeviceID,
        "oaid": "00000000-0000-0000-0000-000000000000",
        # "Connection": close
        "User-Agent": "com.tianyancha.skyeye/Dalvik/2.1.0 (Linux; U; Android 8.1.0; Nexus 6P Build/OPM7.181205.001; appDevice/google_QAQ_Nexus 6P)",
        "Cache-Control": "no-cache, no-store",
        "Host": "api6.tianyancha.com",
        "Accept-Encoding": "gzip",
    }
    iRes = requests.get(url=iUrl, headers=iHeaders, verify=False).json()

    logger.success(iRes)
    iResut = iRes["data"]
    if iResut is not None:
        # create_json(pCompanyName, iRes)
        iItems = []
        for eInfo in iRes["data"]["items"]:
            iItem = {
                "check_type": eInfo.get("checkType", ""),
                "check_org": eInfo.get("checkOrg", ""),
                "check_result": eInfo.get("checkResult", ""),
                "check_date": eInfo.get("checkDate", ""),
                "info_id": pInfoId,
                "co_name": pCompanyName,
                "create_time": datetime.datetime.now(),
                "tyc_id": pTycId,
            }
            logger.error(iItem)
            iItems.append(iItem)
        return iItems
    else:
        logger.error(f"无数据={iResut}")
        return None


def main():
    mq = MysqlPipelinePublic()
    data_list = TYC_DATA
    for data in data_list:
        info_id = data.get("id")
        company_name = data.get("co_name")
        tyc_id = data.get("co_id")
        iTotalPage = get_total_page(pTycId=tyc_id, pCompanyName=company_name)
        logger.info(f"iTotalPage={iTotalPage}")
        if iTotalPage is not None:
            for ePageNum in range(1, int(iTotalPage) + 1):
                iItems = get_bond_info(pInfoId=info_id, pCompanyName=company_name, pTycId=tyc_id, pPageNum=ePageNum)
                if iItems:
                    # iSqlCi = MysqlPipeline()
                    # for eItem in iItems:
                    #     iSqlCi.insert_into_company_check_list_info(eItem)
                    #     logger.info("数据 %s 插入成功" % eItem)
                    # iSqlCi.close()
                    mq = MysqlPipelinePublic()
                    for item in iItems:
                        mq.insert_sql("t_zx_company_check_list_info_new", item)
    mq.close()


if __name__ == "__main__":
    main()
