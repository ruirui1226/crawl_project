#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/9 22:30
# @Author  : wym
# @File    : tyc_get_zhaopin_list.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/29 12:10
# @Author  : wym
# @File    : get_authration.py
import requests
import json
from loguru import logger
import os, time, math
import uuid
from tyc_projects.conf.env import *
from tyc_projects.untils.pysql import *

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(pageNum, info_id, tyc_id, company_name, res_json):
    folder_name = os.getcwd() + "/tyc_zhaopin_file/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + "_" + tyc_id + "_" + str(uuid.uuid1()) + "_" + str(pageNum) + ".json"
    # data_json=json.dumps(response.text,sort_keys=True, separators=(',', ': '),indent=4,ensure_ascii=False)
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_zhaopin_file__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 12.67.0"

    url = f"https://api6.tianyancha.com/cloud-business-state/recruitment/list?city=-100&pageSize=10&graphId={tyc_id}&experience=-100&pageNum={pageNum}&startDate=-100"

    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9797/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)
    return data


def get_Zhaopin_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token):
    headers = {
        # """
        "x-b3-traceid-jindi": "",
        "x-b3-sampled-jindi": "",
        "Authorization": Authorization,
        "version": "Android 12.67.2",
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

    # url = "https://api6.tianyancha.com/services/v3/t/details/appComIcV4/631178350?pageSize=1000"
    url = f"https://api6.tianyancha.com/cloud-business-state/recruitment/list?city=-100&pageSize=10&graphId={tyc_id}&experience=-100&pageNum=1&startDate=-100"
    res = requests.get(url, headers=headers, verify=False).text
    logger.debug(res)
    logger.debug(res)
    res_json = json.loads(res)
    if res_json.get("state", "") == "error":
        logger.debug("%s当前数据异常" % company_name)
        pass

    elif "total" in str(res_json["data"]):
        pages_total = math.ceil(int(res_json["data"]["total"]) / 10)

        if pages_total:
            return pages_total
    elif int(res_json["data"].get("itemTotal", "")) != 0:
        pages_total = math.ceil(int(res_json["data"]["itemTotal"]) / 10)
        if pages_total:
            return pages_total


def get_Zhaopin_info(pageNum, info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token):
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

    url = "https://api6.tianyancha.com/services/v3/t/details/appComIcV4/631178350?pageSize=1000"

    res = requests.get(url, headers=headers, verify=False).text
    # logger.debug(res)
    logger.debug(res)
    res_json = json.loads(res)

    create_json(pageNum, info_id, tyc_id, company_name, res_json)


def main():
    data_list = get_company_name()
    for data in data_list:
        info_id = data[0]
        company_name = data[1]
        tyc_id = data[2]
        pageNum = 1
        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        # data=get_authoriaztion()
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        x_auth_token = data["data"]["x_auth_token"]

        pages_total = get_Zhaopin_page(
            info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token
        )
        if pages_total:
            print(company_name)
            for pageNum in range(1, int(pages_total) + 1):
                get_Zhaopin_info(
                    pageNum, info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID, x_auth_token
                )


if __name__ == "__main__":
    main()


#!/usr/bin/conf python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/19 21:55
# @Author  : wym
# @File    : tyc_get_icp_info.py
# 网站备案
# import requests
# import json
# from loguru import logger
#
# # 忽略requests证书警告
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
#
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#
#
# def get_authoriaztion():
#     version = "Android 11.4.0"
#
#     url = "https://api4.tianyancha.com/services/v3/ar/icp/page.json?pageSize=20&id=3381591494&pageNum=1"
#
#     data = {"url": url, "version": version}
#
#     r = requests.post("http://127.0.0.1:9898/get_authorzation", data=json.dumps(data))
#     print(r.text)
#     data = json.loads(r.text)
#     return data
#
#
# def get_baseinfo(tyc_hi, Authorization, duid, deviceID):
#     headers = {
#         "user-agent": "com.tianyancha.skyeye/Dalvik/2.1.0 (Linux; U; Android 8.1.0; Nexus 6P Build/OPM7.181205.001; appDevice/google_QAQ_Nexus 6P)",
#         "authorization": Authorization,
#         "x-auth-token": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzg1MjAxOTkzNSIsImlhdCI6MTY2MzU1MjY2NiwiZXhwIjoxNjc5MTA0NjY2fQ.xpp-UqTyNYcWNuTYmF0XIIG9x_zE0Rtv99eeJk-iplsL3oJRhql631x8tajpUf3KjJ7KZ6qglDSGW-g_kMtyZQ",
#         "channelid": "YingYongBao",
#         "deviceid": deviceID,
#         "tyc-hi": tyc_hi,
#         "version": "Android 11.4.0",
#         "duid": duid,
#         "content-type": "application/json",
#     }
#
#     url = "https://api4.tianyancha.com/services/v3/ar/icp/page.json?pageSize=20&id=3381591494&pageNum=1"
#     """
#     针对于多页数据，先获取第一个json，获取到total，将total/pageSize 获取到pageNum
#
#
#     """
#     res = requests.get(url=url, headers=headers, verify=False).text
#     logger.debug(res)
#
#
# def main():
#     data = get_authoriaztion()
#     tyc_hi = data["data"]["tyc_hi"]
#     Authorization = data["data"]["Authorization"]
#     duid = data["data"]["duid"]
#     deviceID = data["data"]["deviceID"]
#
#     get_baseinfo(tyc_hi, Authorization, duid, deviceID)
#
#
# if __name__ == "__main__":
#     main()
#
#

"""
{"state":"ok","message":"","special":"","vipMessage":"","isLogin":0,"data":{"item":[{"webSite":["www.dxmpay.com"],"ym":"dxmpay.com","companyType":"企业","liscense":"京ICP备18055445号-1","companyName":"北京度小满支付科技有限公司","examineDate":"2021-12-09","businessId":"94mo7m1799248e66db9d6a1a3l637399","webSiteSafe":[{"whitetype":"5","url":"www.dxmpay.com"}]},{"webSite":["www.paydxm.com"],"ym":"paydxm.com","companyType":"企业","liscense":"京ICP备18055445号-2","companyName":"北京度小满支付科技有限公司","examineDate":"2021-12-09","businessId":"94zoz77om0a73987d9565717cl2fz729","webSiteSafe":[]}],"itemTotal":2,"pageTotal":1,"historyIcpListCount":1}}
"""


import requests
import json
from loguru import logger
import os
import time
import math
from tyc_projects.untils.pysql import *

# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_json(company_name, res_json):
    folder_name = os.getcwd() + "/tyc_icp_file/"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    file_nm = company_name + str(time.time()).split(".")[0] + ".json"
    # data_json=json.dumps(response.text,sort_keys=True, separators=(',', ': '),indent=4,ensure_ascii=False)
    with open(folder_name + "/" + file_nm, "w", encoding="utf-8") as f:
        json.dump(res_json, f, indent=4, ensure_ascii=False)

    logger.debug(("--tyc_icp_file__写入到-->" + file_nm))


def get_authoriaztion(info_id, company_name, tyc_id, pageNum):
    version = "Android 11.4.0"

    # url = f"https://api4.tianyancha.com/services/v3/expanse/holder?pageSize=20&id={tyc_id}&pageNum={pageNum}"
    # url=f"https://api4.tianyancha.com/services/v3/expanse/publicWeChat?pageSize=20&id={tyc_id}&pageNum={pageNum}"
    # url = (
    #     f"https://api4.tianyancha.com/cloud-newdim/company/getWeiboList?pageSize=20&graphId={tyc_id}&pageNum={pageNum}"
    # )

    url = f"https://api4.tianyancha.com/services/v3/ar/icp/page.json?pageSize=20&id={tyc_id}&pageNum={pageNum}"
    data = {"url": url, "version": version}

    r = requests.post("http://127.0.0.1:9898/get_authorzation", data=json.dumps(data))
    logger.warning(r.text)
    data = json.loads(r.text)
    return data


def get_Icp_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID):
    try:
        headers = {
            "user-agent": "com.tianyancha.skyeye/Dalvik/2.1.0 (Linux; U; Android 8.1.0; Nexus 6P Build/OPM7.181205.001; appDevice/google_QAQ_Nexus 6P)",
            "authorization": Authorization,
            "x-auth-token": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzg1MjAxOTkzNSIsImlhdCI6MTY2MzU1MjY2NiwiZXhwIjoxNjc5MTA0NjY2fQ.xpp-UqTyNYcWNuTYmF0XIIG9x_zE0Rtv99eeJk-iplsL3oJRhql631x8tajpUf3KjJ7KZ6qglDSGW-g_kMtyZQ",
            "channelid": "YingYongBao",
            "deviceid": deviceID,
            "tyc-hi": tyc_hi,
            "version": "Android 11.4.0",
            "duid": duid,
            "content-type": "application/json",
        }

        # url = f"https://api4.tianyancha.com/services/v3/expanse/holder?pageSize=20&id={tyc_id}&pageNum=1"
        # url=f"https://api4.tianyancha.com/services/v3/expanse/publicWeChat?pageSize=20&id={tyc_id}&pageNum=1"
        # url = f"https://api4.tianyancha.com/cloud-newdim/company/getWeiboList?pageSize=20&graphId={tyc_id}&pageNum=1"

        url = f"https://api4.tianyancha.com/services/v3/ar/icp/page.json?pageSize=20&id={tyc_id}&pageNum=1"
        print(url)
        print(company_name)
        res = requests.get(url=url, headers=headers, verify=False).text

        logger.debug(res)
        res_json = json.loads(res)
        if res_json.get("state", "") == "error":
            logger.debug("%s当前数据异常" % company_name)
            pass

        elif "total" in str(res_json["data"]):
            pages_total = math.ceil(int(res_json["data"]["total"]) / 20)

            if pages_total:
                return pages_total
        elif int(res_json["data"].get("itemTotal", "")) != 0:
            pages_total = math.ceil(int(res_json["data"]["itemTotal"]) / 20)
            if pages_total:
                return pages_total

        else:
            logger.debug("%s没有ICP数据" % company_name)
            pass
    except Exception as e:
        logger.debug(e)


def get_Icp_info(info_id, company_name, tyc_id, pageNum):
    try:
        url = f"https://api4.tianyancha.com/services/v3/ar/icp/page.json?pageSize=20&id={tyc_id}&pageNum={pageNum}"
        logger.warning(url)
        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]

        headers = {
            "user-agent": "com.tianyancha.skyeye/Dalvik/2.1.0 (Linux; U; Android 8.1.0; Nexus 6P Build/OPM7.181205.001; appDevice/google_QAQ_Nexus 6P)",
            "authorization": Authorization,
            "x-auth-token": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzg1MjAxOTkzNSIsImlhdCI6MTY2MzU1MjY2NiwiZXhwIjoxNjc5MTA0NjY2fQ.xpp-UqTyNYcWNuTYmF0XIIG9x_zE0Rtv99eeJk-iplsL3oJRhql631x8tajpUf3KjJ7KZ6qglDSGW-g_kMtyZQ",
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

        create_json(company_name, res_json)
        # items = []
        # for icp_info in res_json["data"]["item"]:
        #     # if weibo_info["tags"]:
        #     #     tags="".join([tags.replace("/"," ") for tags in weibo_info.get("tags", "")])
        #     # else:
        #     #     tags=""
        #
        #     item = {
        #         "info_id": info_id,
        #         "webSite":" ".join(webSite for webSite in icp_info ["webSite"] if icp_info ["webSite"] ),
        #         "ym":icp_info["ym"],
        #         "companyType": icp_info["companyType"],
        #        "liscense": icp_info["liscense"],
        #         "companyName": icp_info["companyName"],
        #         "examineDate":icp_info["examineDate"],
        #         "businessId": icp_info["businessId"],
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
        data = get_authoriaztion(info_id, company_name, tyc_id, pageNum)
        tyc_hi = data["data"]["tyc_hi"]
        Authorization = data["data"]["Authorization"]
        duid = data["data"]["duid"]
        deviceID = data["data"]["deviceID"]
        pages_total = get_Icp_page(info_id, company_name, tyc_id, tyc_hi, Authorization, duid, deviceID)
        if pages_total:
            print(company_name)
            for pageNum in range(1, int(pages_total) + 1):
                get_Icp_info(info_id, company_name, tyc_id, pageNum)
                # try:
                #
                #     mq = MysqlPipeline()
                #     for item in items:
                #         mq.insert_into_Icp_info(item)
                #         logger.info("数据 %s 插入成功" % item)
                #     mq.close()
                #
                # except Exception as e:
                #     logger.debug(e)
        else:
            pass
        # delete_to_mysql_wechat_main(info_id,company_name)


if __name__ == "__main__":
    main()
