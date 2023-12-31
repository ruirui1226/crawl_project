#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 2023/6/1 16:34
@Author : xushaowei
@File : tyc_get_judicialCase_list.py
@Desc :
@Software:PyCharm
"""
# 司法解析
import requests
import json
import urllib3
import os, time, math
from untils.pysql import *
from tyc_judicial_risk_data.tyc_distribute_task import task_distribution
from untils.redis_conn import r
from untils.urls import JUDICIALCASE_LIST, JUDICIALCASE_DETAILS

# 忽略requests证书警告
try:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"
    url = JUDICIALCASE_LIST
    data = {"url": url, "version": version}
    r = requests.post("http://127.0.0.1:9966/get_authorzation", data=json.dumps(data))
    data = json.loads(r.text)
    return data


def list_json(tyc_id, info_id, company_name, pageNum, pages_total, res_json, is_lz, is_cyl, is_crawl):
    try:
        items = []
        for res in res_json['data']['items']:
            if True is res.get('hasCaseExplanation'):
                hasCaseExplanation = 1
            else:
                hasCaseExplanation = 0
            if True is res.get('isCaseClosed'):
                isCaseClosed = 1
            else:
                isCaseClosed = 0
            item = {
                "tyc_id": tyc_id,
                "company_name": company_name,
                "info_id": info_id,
                "pageNum": pageNum,
                "is_lz": is_lz,
                "is_cyl": is_cyl,
                "is_crawl": is_crawl,
                "pages_total": pages_total,
                "caseCodeList": str(res.get('caseCodeList')).replace("'", '"'),
                "caseReason": res.get('caseReason'),
                "caseType": res.get('caseType'),
                "courtList": str(res.get('courtList')).replace("'", '"'),
                "hasCaseExplanation": hasCaseExplanation,
                "list_id": res.get('id'),
                "isCaseClosed": isCaseClosed,
                "sameSerialCaseCount": res.get('sameSerialCaseCount'),
                "trialProcedure": res.get('trialProcedure'),
                "trialProcedureDetail": str(res.get('trialProcedureDetail')).replace("'", '"'),
                "trialTime": res.get('trialTime'),
                "uuid": res.get('uuid'),
                "labels": str(res.get('labels')).replace("'", '"'),
                "caseIdentityList": str(res.get('caseIdentityList')).replace("'", '"'),
            }
            items.append(item)
        return items

    except Exception as e:
        logger.debug(e)


def get_judicialCase_nextpage(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token,
                              nextpageNum, pages_total, is_lz, is_cyl, is_crawl):
    try:
        data = get_authoriaztion(info_id, company_name, tyc_id, nextpageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
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

        data = {
            "isSameSerialCaseAgg": "1",
            "gid": tyc_id,
            "caseIdentity": "-100",
            "pageSize": "20",
            "pageNum": nextpageNum,
            "caseReason": "-100",
            "caseType": "-100",
            "needFilter": "1",
        }
        url = JUDICIALCASE_LIST
        res = requests.post(url, headers=headers, verify=False, data=json.dumps(data), timeout=10).text
        res_json = json.loads(res)
        res_nextitem = list_json(tyc_id, info_id, company_name, nextpageNum, pages_total, res_json, is_lz, is_cyl, is_crawl)
        return res_nextitem
    except Exception as e:
        logger.debug(e)


def get_judicialCase_listinfo(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, pageNum, is_lz, is_cyl, is_crawl):
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

        data = {
            "isSameSerialCaseAgg": "1",
            "gid": tyc_id,
            "caseIdentity": "-100",
            "pageSize": "20",
            "pageNum": "1",
            "caseReason": "-100",
            "caseType": "-100",
            "needFilter": "1",
        }
        url = JUDICIALCASE_LIST
        res = requests.post(url, headers=headers, verify=False, data=json.dumps(data), timeout=10).text
        res_json = json.loads(res)
        pages_total = None
        try:
            if res_json["data"]["count"]:
                if int(res_json["data"]["count"]) > 0:
                    pages_total = math.ceil(int(res_json["data"]["count"]) / 20)
                else:
                    logger.info("%s没有司法解析目录" % company_name)
                    pass
            else:
                logger.warning(res_json["data"]["count"])
                return
        except Exception as e:
            logger.debug(e)
        if pages_total == 1:
            res_thisitem = list_json(tyc_id, info_id, company_name, pageNum, pages_total, res_json, is_lz, is_cyl, is_crawl)
            return res_thisitem
        elif pages_total > 1:
            res_json_next = []
            res_thisitem = list_json(tyc_id, info_id, company_name, pageNum, pages_total, res_json, is_lz, is_cyl, is_crawl)
            for oneitem in res_thisitem:
                res_json_next.append(oneitem)
            for nextpageNum in range(2, pages_total + 1):
                items = get_judicialCase_nextpage(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, nextpageNum, pages_total, is_lz, is_cyl, is_crawl)
                for item in items:
                    res_json_next.append(item)
            return res_json_next
        else:
            logger.info("%s没有涉诉关系目录" % company_name)
    except Exception as e:
        logger.debug(e)

def main():
    table_name = "t_zx_company_tyc_all_infos_judicialcase"
    redis_key = "tyc_task_judicialcase_list"
    sel_data = ["id", "company_name", "tyc_id", "is_lz", "is_cyl", "is_crawl"]
    task_distribution(table_name, sel_data, {"is_cyl": '1', "state": 0}, redis_key)
    nums = r.scard(redis_key)
    for num in range(1, nums + 1):
        data = r.spop(redis_key).strip("()").split(",")
        info_id = int(data[0])
        company_name = data[1].replace("'", "").replace(" ", "")
        tyc_id = data[2].replace("'", "").replace(" ", "")
        is_lz = data[3].replace("'", "").replace(" ", "")
        is_cyl = data[4].replace("'", "").replace(" ", "")
        is_crawl = data[5].replace("'", "").replace(" ", "")
        mq = MysqlPipelinePublic()
        pageNum = 1
        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        logger.info("当前企业名称为%s" % company_name + "第%s" % num + "总计%s" % nums)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]
        items = get_judicialCase_listinfo(
            info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token, pageNum, is_lz, is_cyl, is_crawl
        )
        if items:
            try:
                mq.insert_all_sql("t_zx_company_judicial_judicialcase_list_info", items)
                logger.info("当前item数据为%s" % items)
            except Exception as e:
                logger.debug(e)
            mq.update_sql(table_name, {"state": 1}, {"id": info_id})
            logger.info("更新任务成功")
        else:
            mq.update_sql(table_name, {"state": -1}, {"id": info_id})
            logger.info(
                "当前企业名称为%s" % company_name + "第%s" % num + "总计%s" % nums + "========司法解析列表无数据======="
            )
        mq.close()

if __name__ == "__main__":
    main()
