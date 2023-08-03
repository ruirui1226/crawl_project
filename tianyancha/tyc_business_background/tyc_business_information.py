#!/usr/bin/conf python
# -*- coding: utf-8 -*-
"""
@desc: tianyancha-工商信息
@version: python3
@author: shenr
@time: 2023/05/19

https://api6.tianyancha.com/services/v3/t/details/appComIcV4/21118801?pageSize=1000
"""


import requests
import json
from loguru import logger
import os, time, math
import uuid
from conf.env import *
from tianyancha.untils.pysql import *
from tianyancha.untils.redis_conn import conn

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from tianyancha.untils.urls import BUSINESS_INFORMATION
from untils.sql_data import TYC_DATA

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/tyc_business_information_file_工商信息/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = (
        company_name.replace("\n", "") + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + ".json"
    )
    # data_json=json.dumps(response.text,sort_keys=True, separators=(',', ': '),indent=4,ensure_ascii=False)
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_business__file_工商信息_写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    url = BUSINESS_INFORMATION.format(tyc_id)

    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)
    return data


def get_business_info(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token):
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
        url = BUSINESS_INFORMATION.format(tyc_id)

        res = requests.get(url, headers=headers, verify=False).text
        res_json = json.loads(res)
        logger.debug(res_json)
        create_json(info_id, tyc_id, company_name, res_json)
        if res_json["data"]:
            bussiness_info = res_json["data"]["baseInfo"]
        else:
            bussiness_info = None
        if "portray" in bussiness_info:
            portray = "".join([portray for portray in list(bussiness_info.get("portray"))])
        else:
            portray = None

        baseInfo_item = {
            "info_id": info_id,
            "tyc_id": tyc_id,
            "historyNames": bussiness_info.get("historyNames", ""),
            "serviceType": bussiness_info.get("serviceType", ""),
            "regStatus": bussiness_info.get("regStatus", ""),
            "estiblishTimeTitleName": bussiness_info.get("estiblishTimeTitleName", ""),
            "emailList": " ".join([email for email in bussiness_info.get("emailList", "")]),
            "headUrl": bussiness_info.get("headUrl", ""),
            "phoneList": " ".join([phone for phone in bussiness_info.get("phoneList", "")]),
            "baiduAuthURLWWW": bussiness_info.get("baiduAuthURLWWW", ""),
            "type": bussiness_info.get("type", ""),
            "equityUrl": bussiness_info.get("equityUrl", ""),
            "toco": bussiness_info.get("toco", ""),
            "ownId": bussiness_info.get("ownId", ""),
            "property3": bussiness_info.get("property3", ""),
            "companyShowBizTypeName": bussiness_info.get("companyShowBizTypeName", ""),
            "approvedTime": bussiness_info.get("approvedTime", ""),
            "logo": bussiness_info.get("logo", ""),
            "industry2017": bussiness_info.get("industry2017", ""),
            "bussiness_id": bussiness_info.get("id", ""),
            "orgNumber": bussiness_info.get("orgNumber", ""),
            "isClaimed": bussiness_info.get("isClaimed", ""),
            "sourceFlag": bussiness_info.get("sourceFlag", ""),
            "correctCompanyId": bussiness_info.get("correctCompanyId", ""),
            "longitude": bussiness_info.get("longitude", ""),
            "entityType": bussiness_info.get("entityType", ""),
            "companyBizOrgType": bussiness_info.get("companyBizOrgType", ""),
            "realCid": bussiness_info.get("realCid", ""),
            "businessScope": bussiness_info.get("businessScope", ""),
            "taxNumber": bussiness_info.get("taxNumber", ""),
            "portray": portray,
            "haveReport": bussiness_info.get("haveReport", ""),
            "tags": bussiness_info.get("tags", ""),
            "isBranch": bussiness_info.get("isBranch", ""),
            "companyId": bussiness_info.get("companyId", ""),
            "phoneNumber": bussiness_info.get("honeNumber", ""),
            "serviceCount": bussiness_info.get("serviceCount", ""),
            "taxQualification": bussiness_info.get("taxQualification", ""),
            "categoryScore": bussiness_info.get("categoryScore", ""),
            "isHightTech": bussiness_info.get("isHightTech", ""),
            "name": bussiness_info.get("name", ""),
            "percentileScore": bussiness_info.get("percentileScore", ""),
            "isMicroEnt": bussiness_info.get("isMicroEnt", ""),
            "baseInfo": bussiness_info.get("baseInfo", ""),
            "flag": bussiness_info.get("flag", ""),
            "regCapital": bussiness_info.get("regCapital", ""),
            "staffNumRange": bussiness_info.get("staffNumRange", ""),
            "latitude": bussiness_info.get("latitude", ""),
            "industry": bussiness_info.get("industry", ""),
            "legalTitleName": bussiness_info.get("", ""),
            "regTitleName": bussiness_info.get("regTitleName", ""),
            "updateTimes": bussiness_info.get("updateTimes", ""),
            "legalPersonName": bussiness_info.get("legalPersonName", ""),
            "regNumber": bussiness_info.get("regNumber", ""),
            "creditCode": bussiness_info.get("creditCode", ""),
            "weibo": bussiness_info.get("weibo", ""),
            "fromTime": bussiness_info.get("fromTime", ""),
            "socialStaffNum": bussiness_info.get("socialStaffNum", ""),
            "companyOrgType": bussiness_info.get("companyOrgType", ""),
            "alias": bussiness_info.get("alias", ""),
            "baiduAuthURLWAP": bussiness_info.get("baiduAuthURLWAP", ""),
            "email": bussiness_info.get("email", ""),
            "actualCapital": bussiness_info.get("actualCapital", ""),
            "estiblishTime": bussiness_info.get("estiblishTime", ""),
            "companyType": bussiness_info.get("companyType", ""),
            "regInstitute": bussiness_info.get("regInstitute", ""),
            "companyBizType": bussiness_info.get("ompanyBizType", ""),
            "regLocation": bussiness_info.get("regLocation", ""),
            "websiteList": bussiness_info.get("websiteList", ""),
            "safetype": bussiness_info.get("safetype", ""),
            "legalPersonId": bussiness_info.get("legalPersonId", ""),
            "updatetime": bussiness_info.get("updatetime", ""),
            "base": bussiness_info.get("base", ""),
            "company_name": company_name,
            "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        }
        branchList_info_items = []
        print(res_json["data"]["branchList"])
        for branchList_info in res_json["data"]["branchList"]:
            branchList_info_item = {
                "info_id": info_id,
                "tyc_id": tyc_id,
                "legalPersonId": branchList_info.get("legalPersonId", ""),
                "regStatus": branchList_info.get("regStatus", ""),
                "estiblishTime": branchList_info.get("estiblishTime", ""),
                "name": branchList_info.get("name", ""),
                "alias": branchList_info.get("alias", ""),
                "branch_id": branchList_info.get("id", ""),
                "pencertileScore": branchList_info.get("pencertileScore", ""),
                "personType": branchList_info.get("personType", ""),
                "category": branchList_info.get("category", ""),
                "type": branchList_info.get("type", ""),
                "base": branchList_info.get("base", ""),
                "legalPersonName": branchList_info.get("legalPersonName", ""),
                "company_name": company_name,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            }
            branchList_info_items.append(branchList_info_item)

        all_items = {
            "baseInfo": baseInfo_item,
            "branchList_infos": branchList_info_items,
        }

        return all_items

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
        # ex_d = conn.srem("patent_tyc_id", tyc_id)
        # if ex_d:
        ex = conn.sadd("business_tyc_id", tyc_id)
        if ex == 1:
            data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
            logger.warning("当前企业名称为%s" % company_name)
            tyc_hi = data["data"]["tyc_hi"]
            Authorization = data["data"]["Authorization"]
            duid = data["data"]["duid"]
            deviceID = data["data"]["deviceID"]
            x_auth_token = data["data"]["x_auth_token"]

            all_item = get_business_info(
                info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token
            )
            if all_item:
                baseInfo_item = all_item.get("baseInfo", "")
                if baseInfo_item:
                    baseInfo_item = baseInfo_item
                else:
                    baseInfo_item = None

                branchList_info_items = all_item.get("branchList_infos", "")
                if branchList_info_items:
                    branchList_info_items = branchList_info_items
                else:
                    branchList_info_items = None

                try:
                    # mq.insert_into_Bussiness_info("t_zx_company_bussiness_base_info", baseInfo_item)
                    mq.insert_sql("t_zx_company_bussiness_base_info", baseInfo_item)
                    logger.info("数据 %s 插入成功" % baseInfo_item)
                    if branchList_info_items:
                        for branchList_info_item in branchList_info_items:
                            # mq.insert_into_Branch_info(branchList_info_item)
                            mq.insert_sql("t_zx_company_branch_info", branchList_info_item)
                            logger.info("数据%s 插入成功" % branchList_info_item)
                except Exception as e:
                    logger.debug(e)
            else:
                pass
        else:
            logger.debug("%s---------数据已经采集，无需再次采集" % tyc_id)
            pass
    mq.close()


if __name__ == "__main__":
    main()
