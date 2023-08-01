#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/7 12:05
# @Author  : wym
# @File    : tyc_search_result_info.py
#!/usr/bin/conf python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/22 8:51
# @Author  : wym
# @File    : tyc_shares_data.py

import requests
import json

import pymysql
import datetime, time
from urllib import parse

# import redis
# import pymongo
import random

# from w3lib.html import remove_tags
import os
from loguru import logger
import uuid

from untils.pysql import MysqlPipelinePublic

requests.packages.urllib3.disable_warnings()


# mongo_client = pymongo.MongoClient(host='49.233.47.161', port=27017,username='root',password='wym121314.')
# db = mongo_client.crawler_data
#
# mongo_collection = db.tyc_enterprise_baseinfo


# 创建文件夹
def create_folder():
    floder = os.getcwd() + "\\tyc_zjtx_230424_search_josn_file\\"
    if not os.path.exists(floder):
        os.makedirs(floder)
    else:
        pass
    return floder


# 查询数据库获取企业信息
def get_enterprise():
    conn = pymysql.connect(
        database="industrial_chain_enterprise_project_0727",
        user="root",
        password="Qw12.?qw",
        host="10.67.78.131",
        port=3306,
    )

    cursor = conn.cursor()
    cursor.execute(r"select '1', co_name from company_name_0727_new where co_id is null ")
    enterprise_title = cursor.fetchall()
    # cursor.close()-
    # conn.close()
    return enterprise_title


# 获取企业信息
def get_list(enterprise_id, enterprise_name):
    # enterprise_name_quote = parse.quote(enterpzrise_name)
    # try:

    headers = {
        # """
        "x-b3-traceid-jindi": "",
        "x-b3-sampled-jindi": "",
        "Authorization": "+EIU3mf/S3A5/dLCu+qptFA/GR+S7Z12gSZi130ysksn0/N9drEV8a7IFoRDefGsEkgU5fLpD8bAi/85uPIJdKwniL+y0SOy7hnvGqqUwwUiZr8Eq1eBl9i4doqbi6Y1OG3YesggRgCIQb6bfY6eYAFLARndp9AsDhKkQZpRAS4=",
        "version": "Android 12.67.0",
        "X-Auth-Token": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTI4MTA0NTkzMyIsImlhdCI6MTY2NjYwMjk0NywiZXhwIjoxNzI5Njc0OTQ3fQ.rH2Z0T-ZPFuTswFaenwtGV1YfyHySpMnIe4tSqPIX1Uo-6lBTBHiTEmnsRPDkiHQurg7gpqNX9cZhZGSWhi5WQ",
        "Content-Type": "application/json",
        "channelID": "huawei",
        "deviceID": "1bbaf81111eb23c5",
        "deviceModel": "Nexus 5P",
        "deviceVersion": "8.1.0",
        "tyc-hi": "836f7f7ca0a2223d176fd750b2549cd7",
        "sensorsAnonymousId": "dc84ce12a0bf5227",
        "device-uuid": "dc84ce12a0bf5227",
        "tdid": "36c73d82d939322125bf91fa8ae59b3d5",
        "device_uuid": "dc84ce12a0bf5227",
        "app_channel": "huawei",
        "app-code": "670",
        "androidid": "dc84ce12a0bf5227",
        "oaid": "00000000-0000-0000-0000-000000000000",
        "User-Agent": "com.tianyancha.skyeye/Dalvik/2.1.0 (Linux; U; Android 8.1.0; Nexus 6P Build/OPM7.181205.001; appDevice/google_QAQ_Nexus 6P)",
        "Cache-Control": "no-cache, no-store",
        "Host": "api6.tianyancha.com",
        "Accept-Encoding": "gzip",
    }
    data = {
        "allowModifyQuery": "1",
        "pageNum": "1",
        "word": enterprise_name,
        "sessionNo": "1667792904.81940813",
        "pageSize": "20",
        "sortType": "0",
        "reportInfo": {
            "page_id": "SearchResult",
            "page_name": "主搜搜索结果页",
            "tab_id": "CompanySearchResult",
            "tab_name": "公司",
            "search_channel": '{"page_id":"SearchMiddle","tab_id":"company","module_id":"Search"}',
            "os": "Android",
            "device_id": "dc84ce12a0bf5227",
            "distinct_id": "qqQcC9fK6WQ0iv3KT+vglA==",
            "login_id": "qqQcC9fK6WQ0iv3KT+vglA==",
            "search_trace_id": "1667792859.91679084",
            "search_session_id": "1667792904.81940813",
            "dev_type": "Native",
            "global_trace_id": "1f43d28a-205d-4028-87a7-d4211d892db5",
            "plat_type": "Android",
            "da_version": "1005",
            "ab_test_new": '{"ab_info":{"companydetail0829":1,"homepage0530":0,"bus_bottom_tab":1,"company_detail_struct_1128":1,"persondetail_structure1128":0,"home_tab0216":1,"homepage_search_0227":2,"detaildim_filter0310":1,"paypoint_pic_rwxq":1,"paypoint_recommend202203":1,"dui_zzzsdetail_202204":1,"companydetail_dim202204":1,"qos_enable":0,"fps_monitor_test":0,"dim_viprenew_2204":1,"monitor_dynamic_202205":1,"qosPageStartup20220525":0,"QOS_Qos,type=Error":0,"QOS_Qos,type=Performance":0,"tracker_Qos,type=Error":0,"tracker_Qos,type=Performance,performance_type=Launch":0,"tracker_Qos,type=Performance,performance_type=ScrollFps":0,"track_v2_Qos,type=Performance,performance_type=ScrollFps":0,"track_v2_Qos,type=Performance,performance_type=Launch":0,"track_v2_Qos,type=Error":0,"Qos,qos_type=Common,qos_subtype=FlowAnalysis,flow_name=h5_bridge":0,"track_v2_Qos,qos_type=Common,qos_subtype=FlowAnalysis,flow_name=h5_bridge":0,"track_v2_Qos,flow_name=h5_bridge,api_name=https://m.tianyancha.com/app/h5/vip_package":1,"popup_window_close":"1","history_paypoint_2208":"1","contact_vip_process":"1"},"api_ab_info":{}}',
        },
    }
    url = "https://api6.tianyancha.com/cloud-tempest/app/searchCompanyV3"
    response = requests.post(data=json.dumps(data), url=url, headers=headers)

    # logger.warning(response.text)
    # data_json = json.loads(response.text)

    # folder_name = create_folder()
    # file_nm = enterprise_name + str(uuid.uuid1()) + "_" + str(enterprise_id) + ".json"
    #
    # with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
    #     json.dump(data_json, f, indent=4, ensure_ascii=False)
    #
    # logger.debug(("--zjtx_data__写入到-->" + file_nm))

    res_json = json.loads(response.text)
    items = []
    company_info = res_json["data"]["companyList"][0]
    item_register = {
        # "shares_code": shares_code,
        # "share_code": share_code,
        # "shares_name": shares_name,
        "enterprise_name": enterprise_name,
        "company_name": company_info["name"].replace("<em>", "").replace("</em>", ""),
        "tyc_id": company_info["id"],
        # 'eid': enterprise_id,
        # 联系方式
        "tele_phone": company_info["phoneNum"],
        # 邮箱
        "email": company_info["emails"],
        # 官网地址
        "website": company_info["websites"],
        "eid": enterprise_id,
        # 法人
        "legal_person": company_info["legalPersonName"],
        # 注册资本
        "register_capital": company_info["regCapital"],
        # 企业状态
        "enterprise_status": company_info["regStatus"],
        "register_id": company_info["regNumber"],
        # 组织机构代码
        "org_id": company_info["orgNumber"],
        # 统一信用代码
        "credit_id": company_info["creditCode"],
        # # 企业类型
        # 'enterprise_type': None,
        # 纳税人识别号
        "revenue_id": company_info["taxCode"],
        # 行业类型
        "industry_type": company_info["categoryStr"],
        # 注册日期
        "register_date": company_info["estiblishTime"],
        # 注册地址
        "register_address": company_info["regLocation"],
        # 经营范围
        "business_scope": company_info["businessScope"],
        # 股票名称
        "bondname": company_info["bondName"],
        # 股票代码
        "bondnum": company_info["bondNum"],
        # 股票类型
        "bondtype": company_info["bondType"],
        "base": company_info["base"],
        "city": company_info["city"],
        "district": company_info["district"],
        "create_time": datetime.datetime.today(),
    }
    # write_to_mysql_base(item_base)
    items.append(item_register)
    write_to_tyc_mysql_register_data(items)

    # logger.debug(item_register)
    # return item_register
    #
    # return item
    # except Exception as e:
    #     print(e)


from pymysql import IntegrityError


# 将企业信息写入到数据库
def write_to_tyc_mysql_register_data(items):
    # try:
    conn = pymysql.connect(
        database="industrial_chain_enterprise_project_0727",
        user="root",
        password="Qw12.?qw",
        host="10.67.78.131",
        port=3306,
    )
    cursor = conn.cursor()
    for item in items:
        logger.warning(item)
        # conn = pymysql.connect(database="crawler_data", user="root", password="654321", host="60.208.77.163",
        #                        port=8319)

        insert_sql = "insert into t_zx_tyc_zjtx_company_search_info_20230725(enterprise_name,company_name,bondname,bondnum,bondtype,tele_phone,email,website,tyc_id,eid,legal_person,register_capital,enterprise_status,register_id,org_id,credit_id,revenue_id,industry_type,register_date,register_address,business_scope,base,city,district,create_time)VALUES (%(enterprise_name)s,%(company_name)s,%(bondname)s,%(bondnum)s,%(bondtype)s,%(tele_phone)s,%(email)s,%(website)s,%(tyc_id)s,%(eid)s,%(legal_person)s,%(register_capital)s,%(enterprise_status)s,%(register_id)s,%(org_id)s,%(credit_id)s,%(revenue_id)s,%(industry_type)s,%(register_date)s,%(register_address)s,%(business_scope)s,%(base)s,%(city)s,%(district)s,%(create_time)s)"
        cursor.execute(insert_sql, item)

    print("register数据已经插入到mysql")
    conn.commit()
    conn.close()

    # except IntegrityError as f:
    #     logger.warning("数据重复")


# 主程序
def main():
    enterprise_title = get_enterprise()
    for enterprise in enterprise_title:
        time.sleep(1)
        enterprise = list(enterprise)
        enterprise_id = enterprise[0]
        enterprise_name = enterprise[1]
        print(enterprise_id, enterprise_name)
        get_list(enterprise_id, enterprise_name)
        # delete_to_mysql_main(enterprise_id, enterprise_name)




def main_1():
    conn = pymysql.connect(
        database="industrial_chain_enterprise_project_0727",
        user="root",
        password="Qw12.?qw",
        host="10.67.78.131",
        port=3306,
    )
    cursor = conn.cursor()
    # conn = pymysql.connect(database="crawler_data", user="root", password="654321", host="60.208.77.163",
    #                        port=8319)

    # select_sql_0725 = """select tyc_id, credit_id, enterprise_name from t_zx_tyc_zjtx_company_search_info_20230725"""
    # cursor.execute(select_sql_0725)
    # enterprise_title_0725 = cursor.fetchall()
    #
    cursor.execute(r"select id, co_name from company_name_0727_new")
    enterprise_title = cursor.fetchall()
    # for each in enterprise_title_0725:
    #     for rows in enterprise_title:
    #         if each[2] == rows[1]:
    #             upd_data = {"co_id": each[0], "social_credit_code": each[1]}
    #             where_data = {"co_name": each[2]}
    mq = MysqlPipelinePublic()
    i = 0
    for each in enterprise_title:
        i += 1
        mq.update_sql("company_name_0727_new", {"id": i}, {"co_name": each[1]})
                # print("已修改=====", each[2])


    print("register数据已经插入到mysql")
    conn.commit()
    conn.close()




if __name__ == "__main__":
    # main()
    main_1()
