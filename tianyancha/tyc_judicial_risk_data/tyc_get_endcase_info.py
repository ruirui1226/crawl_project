# -*- coding:utf-8 -*-
# @author: xrx / xushaowei
# @time: 2022/9/29 13:49
# @project: zxDailyProject
# @file: tyc_get_endcase_info.py
# @software: PyCharm
# desc: 终本案件


import datetime
import json
import math
import os
import time

import requests
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

from tyc_judicial_risk_data.tyc_distribute_task import task_distribution
from untils.pysql import *
from untils.redis_conn import r
from untils.urls import ENDCASE_LIST

disable_warnings(InsecureRequestWarning)


def get_auth(pCompanyName, pTycId, pPageNum=1):
    iVersion = "Android 11.4.0"
    iUrl = ENDCASE_LIST.format(pTycId, pPageNum)
    iData = {"url": iUrl, "version": iVersion}
    iResp = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(iData))
    iRes = json.loads(iResp.text)
    return iRes


def create_json(pCompanyName, pResJson):
    iFolderName = os.getcwd() + "/tyc_case_info_file/"
    if not os.path.exists(iFolderName):
        os.makedirs(iFolderName)
    else:
        pass

    iFileName = pCompanyName + str(time.time()).split(".")[0] + ".json"
    with open(iFolderName + "/" + iFileName, "w", encoding="utf-8") as f:
        json.dump(pResJson, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_final_case_file__写入到-->" + iFileName))


def get_total_page(pCompanyName, pTycId, pPageNum=1):
    iUrl = ENDCASE_LIST.format(pTycId, pPageNum)
    iData = get_auth(pTycId=pTycId, pPageNum=pPageNum, pCompanyName=pCompanyName)
    tyc_hi = iData["data"]["tyc_hi"]
    Authorization = iData["data"]["Authorization"]
    iDuid = iData["data"]["duid"]
    deviceID = iData["data"]["deviceID"]
    x_auth_token = iData["data"]["x_auth_token"]
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
    iRes = requests.get(url=iUrl, headers=headers, verify=False).json()
    try:
        if "totalRows" in str(iRes["data"]):
            pages_total = math.ceil(int(iRes["data"]["totalRows"]) / 20)
            if pages_total:
                return pages_total
        elif int(iRes["data"]["count"]) > 0:
            pages_total = math.ceil(int(iRes["data"]["count"]) / 20)
            if pages_total:
                return pages_total
        else:
            logger.info("%s没有终本案件案件目录" % pCompanyName)
            pass
    except Exception as e:
        logger.debug(e)

def get_end_case_info(pInfoId, pCompanyName, pTycId, pPageNum=1):
    iUrl = ENDCASE_LIST.format(pTycId, pPageNum)
    iData = get_auth(pTycId=pTycId, pPageNum=pPageNum, pCompanyName=pCompanyName)
    tyc_hi = iData["data"]["tyc_hi"]
    Authorization = iData["data"]["Authorization"]
    iDuid = iData["data"]["duid"]
    deviceID = iData["data"]["deviceID"]
    x_auth_token = iData["data"]["x_auth_token"]
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
    iRes = requests.get(url=iUrl, headers=headers, verify=False).json()
    iResut = iRes["data"]
    if iResut is not None:
        try:
            total = iRes["data"]["headData"][0]
            nototal = iRes["data"]["headData"][1]
            Unfulfilled = iRes["data"]["headData"][2]
            Total_execution_amount = total.get("value") + total.get("unit")
            Total_outstanding_amount = nototal.get("value") + nototal.get("unit")
            Unfulfilled_proportion = Unfulfilled.get("value")
        except:
            Total_execution_amount = None
            Total_outstanding_amount = None
            Unfulfilled_proportion = None
        iItems = []
        for eInfo in iRes["data"]["items"]:
            iItem = {
                "caseCode": eInfo.get("caseCode", ""),
                "caseFinalTime": eInfo.get("caseFinalTime", ""),
                "zhixingId": eInfo.get("zhixingId"),
                "businessId": eInfo.get("businessId"),
                "caseCreateTime": eInfo.get("caseCreateTime", ""),
                "execCourtName": eInfo.get("execCourtName", ""),
                "i_id": eInfo.get("id"),
                "execMoney": eInfo.get("execMoney", "") + eInfo.get("noExecMoneyUnit", ""),
                "noExecMoney": eInfo.get("noExecMoney", "") + eInfo.get("execMoneyUnit", ""),
                "zname": eInfo.get("zname", ""),
                "cid": eInfo.get("cid"),
                "info_id": pInfoId,
                "tyc_id": pTycId,
                "company_name": pCompanyName,
                "Total_execution_amount": Total_execution_amount,
                "Total_outstanding_amount": Total_outstanding_amount,
                "Unfulfilled_proportion": Unfulfilled_proportion,
            }
            iItems.append(iItem)
        return iItems
    else:
        logger.warning(f"无数据={iResut}")
        return None


def main():
    table_name = "t_zx_company_tyc_all_infos_finalcase"
    redis_key = "tyc_task_finalcase"
    sel_data = ['id', 'company_name', 'tyc_id']
    task_distribution(table_name, sel_data, {"is_crawl": 'zjtx_2023', "state": 0}, redis_key)
    nums = r.scard(redis_key)
    for num in range(1, nums + 1):
        data = r.spop(redis_key).strip("()").split(",")
        info_id = int(data[0])
        company_name = data[1].replace("'", "").replace(" ", "")
        tyc_id = data[2].replace("'", "").replace(" ", "")
        mq = MysqlPipelinePublic()
        iTotalPage = get_total_page(pTycId=tyc_id, pCompanyName=company_name)
        logger.info("当前企业名称为%s" % company_name + ",第%s个企业" % num + "总计%s个企业" % nums)
        if iTotalPage is not None:
            for ePageNum in range(1, int(iTotalPage) + 1):
                iItems = get_end_case_info(pInfoId=info_id, pCompanyName=company_name, pTycId=tyc_id, pPageNum=ePageNum)
                if iItems:
                    for eItem in iItems:
                        mq.insert_sql("t_zx_company_judicial_finalcase_info", eItem)
                        logger.info("数据 %s 插入成功" % eItem)
            mq.update_sql(table_name, {"state": 1}, {"id": info_id})
            logger.info("更新任务成功")
        else:
            mq.update_sql(table_name, {"state": -1}, {"id": info_id})
            logger.info(
                "当前企业名称为%s" % company_name + ",第%s个企业" % num + "总计%s个企业" % nums + "========终本案件无数据=======更新任务成功"
            )
        mq.close()

if __name__ == "__main__":
    main()
