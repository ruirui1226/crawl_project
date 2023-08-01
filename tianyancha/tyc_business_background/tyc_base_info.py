#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/31 17:20
# @Author  :  shenr
# @File    : tyc_base_info_12_67_0.py
"""
基本信息
https://api6.tianyancha.com/services/v3/t/common/baseinfoV5ForApp/6923813

"""
import requests
import json
from loguru import logger
import os, time, math
import uuid
from tianyancha.conf.env import *
from tianyancha.untils.pysql import *
from tianyancha.untils.redis_conn import conn

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from tianyancha.untils.urls import BASIC_INFO

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/tyc_base_new_file__基本信息/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + "_" + str(info_id) + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + ".json"
    # data_json=json.dumps(response.text,sort_keys=True, separators=(',', ': '),indent=4,ensure_ascii=False)
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_base_new_file_基本信息__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"

    # # url = f"https://api6.tianyancha.com/cloud-judicial-risk/bankruptcy/list?gid={tyc_id}&pageSize=20&pageNum={pageNum}"
    # url = f"https://api6.tianyancha.com/cloud-business-state/bid/listV2?area=-100&infoType=-100&pageSize=20&graphId={tyc_id}&pageNum={pageNum}&pubDate=-100"

    url = BASIC_INFO.format(tyc_id)
    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)
    return data


def get_base_info(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token):
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

        url = BASIC_INFO.format(tyc_id)

        res = requests.get(url, headers=headers, verify=False).text
        res_json = json.loads(res)
        logger.debug(res_json)
        # create_json(info_id, tyc_id, company_name, res_json)
        if res_json["data"]:
            base_info = res_json["data"]
        else:
            base_info = None

        item = {
            "info_id": info_id,
            "company_name": company_name,
            "tyc_id": tyc_id,
            "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            "reg_status": base_info.get("regStatus", ""),
            "estiblishTimeTitleName": base_info.get("estiblishTimeTitleName", ""),
            "websiteRiskType": base_info.get("websiteRiskType", ""),
            "other_e_mail": str(base_info.get("emailList", "")),
            "other_mobile": str(base_info.get("phoneList", "")),
            "videoId": base_info.get("videoId", ""),
            "baiduAuthURLWWW": base_info.get("baiduAuthURLWWW", ""),
            "base_type": base_info.get("type", ""),
            "inverstStatus": base_info.get("inverstStatus", ""),
            "equity_link": base_info.get("equityUrl", ""),
            "legal_rep_type": base_info.get("legalPersonType", ""),
            "sensitiveEntityType": base_info.get("sensitiveEntityType", ""),
            "english_name": base_info.get("property3", ""),
            "co_type_name": base_info.get("companyShowBizTypeName", ""),
            "co_type_scale": base_info.get("regCapitalLabel", ""),
            "co_synopsis": base_info.get("companyProfilePlainText", ""),
            "appro_date": base_info.get("approvedTime", ""),
            "industry_name": base_info.get("industry2017", ""),
            "logo_link": base_info.get("logo", ""),
            "base_id": base_info.get("id", ""),
            "originalPercentileScore": base_info.get("originalPercentileScore", ""),
            "org_code": base_info.get("orgNumber", ""),
            "isClaimed": base_info.get("isClaimed", ""),
            "listedStatusTypeForSenior": base_info.get("listedStatusTypeForSenior", ""),
            "longitude": base_info.get("longitude", ""),
            "tax_bank_mobile": base_info.get("taxPhone", ""),
            "tax_bank": base_info.get("taxBankName", ""),
            "entityType": base_info.get("entityType", ""),
            "companyBizOrgType": base_info.get("companyBizOrgType", ""),
            "bus_scope": base_info.get("businessScope", ""),
            "taxpayer_no": base_info.get("taxNumber", ""),
            "portray": base_info.get("portray", ""),
            "regCapitalCurrency": base_info.get("regCapitalCurrency", ""),
            "tags": base_info.get("tags", ""),
            "regCapitalAmount": base_info.get("regCapitalAmount", ""),
            "mobile": base_info.get("phoneNumber", ""),
            "taxpayer_qualification": base_info.get("taxQualification", ""),
            "co_names": base_info.get("name", ""),
            "percentileScore": base_info.get("percentileScore", ""),
            "extraInfo": base_info.get("extraInfo", ""),
            "base_info": base_info.get("baseInfo", ""),
            "reg_amount": base_info.get("regCapital", ""),
            "regLocationTitle": base_info.get("regLocationTitle", ""),
            "staffNumRange": base_info.get("staffNumRange", ""),
            "latitude": base_info.get("latitude", ""),
            "link": base_info.get("link", ""),
            "industry": base_info.get("industry", ""),
            "legalTitleName": base_info.get("legalTitleName", ""),
            "regTitleName": base_info.get("regTitleName", ""),
            "updateTimes": base_info.get("updateTimes", ""),
            "legal_rep": base_info.get("legalPersonName", ""),
            "tagListV2": str(base_info.get("tagListV2", "")),
            "reg_no": base_info.get("regNumber", ""),
            "social_credit_code": base_info.get("creditCode", ""),
            "pv_count": base_info.get("pvCount", ""),
            "fromTime": base_info.get("fromTime", ""),
            "insured_quantity": base_info.get("socialStaffNum", ""),
            "companyOrgType": base_info.get("companyOrgType", ""),
            "co_alias": base_info.get("alias", ""),
            "actualCapitalCurrency": base_info.get("actualCapitalCurrency", ""),
            "baiduAuthURLWAP": base_info.get("baiduAuthURLWAP", ""),
            "office_address": base_info.get("taxAddress", ""),
            "claimLabelStyle": base_info.get("claimLabelStyle", ""),
            "e_mail": base_info.get("email", ""),
            "paid_amount": base_info.get("actualCapital", ""),
            "hasVideo": str(base_info.get("hasVideo", "")),
            "phoneSourceList": str(base_info.get("phoneSourceList", "")),
            "start_date": base_info.get("estiblishTime", ""),
            "tax_bank_account": base_info.get("taxBankAccount", ""),
            "reg_authority": base_info.get("regInstitute", ""),
            "listedStatusType": base_info.get("listedStatusType", ""),
            "companyBizType": base_info.get("companyBizType", ""),
            "reg_address": base_info.get("regLocation", ""),
            "regCapitalAmountUnit": base_info.get("regCapitalAmountUnit", ""),
            "fund_info": str(base_info.get("rongziInfo", "")),
            "co_website": str(base_info.get("websiteList", "")),
            "safetype": base_info.get("safetype", ""),
            "tagList": str(base_info.get("tagList", "")),
            "legal_rep_code": base_info.get("legalPersonId", ""),
            "complexName": base_info.get("complexName", ""),
            "companyProfileRichText": str(base_info.get("companyProfileRichText", "")),
            "updatetime": base_info.get("updatetime", ""),
            "province_pysx": base_info.get("base", ""),
            "history_name": None,
        }

        return item
    except Exception as e:
        logger.debug(e)


def main():
    data_list = get_company_230420_name()
    for data in data_list:
        info_id = data[0]
        company_name = data[1]
        tyc_id = data[2]
        pageNum = 1

        ex = conn.sadd("tyc_id", tyc_id)
        if ex == 1:
            data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
            logger.warning("当前企业名称为%s" % company_name)
            tyc_hi = data["data"]["tyc_hi"]
            Authorization = data["data"]["Authorization"]
            duid = data["data"]["duid"]
            deviceID = data["data"]["deviceID"]
            x_auth_token = data["data"]["x_auth_token"]
            item = get_base_info(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token)

            try:
                mq = MysqlPipeline()

                mq.insert_into_company_base_info(item)
                logger.info("数据 %s 插入成功" % item)
                mq.close()

            except Exception as e:
                logger.debug(e)
            else:
                pass

        else:
            logger.debug("%s---------数据已经采集，无需再次采集" % tyc_id)
            pass


if __name__ == "__main__":
    main()
