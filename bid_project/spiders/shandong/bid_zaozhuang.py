#!/usr/bin/conf python
# -*- coding: utf-8 -*-
"""
@desc: 招投标-山东省-枣庄市
@version: python3
@author: shenr
@time: 2023/06/07
"""


import json
import logging
import time

import requests
from pyquery import PyQuery as pq

from bid_project.untils.common import get_md5
from bid_project.untils.pysql import MysqlPipelinePublic

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Authorization": "Bearer fbd1b1ec7721ca5a95781543802ac919",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "http://ggzy.zaozhuang.gov.cn",
    "Referer": "http://ggzy.zaozhuang.gov.cn/jyxx/about_jyxx.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}
cookies = {
    "_gscu_1637901767": "86042016s6kq6s71",
    "userGuid": "-1177458307",
    "noOauthRefreshToken": "bc09b89334f5ea3b30a7f6e22ddbe7f8",
    "noOauthAccessToken": "fbd1b1ec7721ca5a95781543802ac919",
    "oauthClientId": "wzds",
    "oauthPath": "http://127.0.0.1:8080/EpointWebBuilder",
    "oauthLoginUrl": "http://127.0.0.1:1112/membercenter/login.html?redirect_uri=",
    "oauthLogoutUrl": "",
    "_gscbrs_1637901767": "1",
    "_gscs_1637901767": "86108140q3y6an19|pv:8",
}
url_post = "http://ggzy.zaozhuang.gov.cn/EpointWebBuilder/rest/jyxxAction/getListjy"


def get_list(code, region, pagenum):
    data = {
        "params": json.dumps(
            {
                "categorynum": "018",
                "wd": "",
                "sdt": "",
                "edt": "",
                "areacode": code,
                "pageSize": 15,
                "pageIndex": pagenum,
                "siteGuid": "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a",
            }
        )
    }
    logging.info(f"===========当前爬取{pagenum}页===========")
    response = requests.post(url=url_post, headers=headers, cookies=cookies, data=data, verify=False)
    res = json.loads(response.text)

    infodata = res.get("infodata")
    for each in infodata:
        url = "http://ggzy.zaozhuang.gov.cn/" + each["infourl"]
        detail = get_detail(url)
        if detail.get("bid_info_type") == "政府采购":
            item = {}
            item["po_id"] = get_md5(each["infoid"])
            item["po_city"] = "枣庄市"
            item["po_county"] = region
            item["bid_url"] = "http://ggzy.zaozhuang.gov.cn/" + each["infourl"]
            item["po_category"] = detail.get("bid_category")
            item["po_info_type"] = detail.get("bid_info_type")
            item["po_source"] = detail.get("bid_source")
            item["po_html_con"] = str(detail.get("bid_html_con")).replace("'", '"')
            item["po_content"] = str(detail.get("bid_content")).replace("'", '"')
            item["bo_name"] = each["title"]
            item["po_public_time"] = each["infodate"]
            item["website_name"] = "枣庄市公共资源交易中心"
            item["website_url"] = "http://ggzy.zaozhuang.gov.cn/jyxx/about_jyxx.html"
            item["bid_orgin_url"] = "http://ggzy.zaozhuang.gov.cn/jyxx/about_jyxx.html"
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            logging.info(item)
            mq = MysqlPipelinePublic()
            mq.insert_sql("t_zx_po_crawl_info", item)
        else:
            item = {}
            item["bid_id"] = get_md5(each["infoid"])
            item["bid_city"] = "枣庄市"
            item["bid_county"] = region
            item["bid_url"] = "http://ggzy.zaozhuang.gov.cn/" + each["infourl"]
            item["bid_category"] = detail.get("bid_category")
            item["bid_info_type"] = detail.get("bid_info_type")
            item["bid_source"] = detail.get("bid_source")
            item["bid_html_con"] = str(detail.get("bid_html_con")).replace("'", '"')
            item["bid_content"] = str(detail.get("bid_content")).replace("'", '"')
            item["bid_name"] = each["title"]
            item["bid_public_time"] = each["infodate"]
            item["website_name"] = "枣庄市公共资源交易中心"
            item["website_url"] = "http://ggzy.zaozhuang.gov.cn/jyxx/about_jyxx.html"
            item["bid_orgin_url"] = "http://ggzy.zaozhuang.gov.cn/jyxx/about_jyxx.html"
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            logging.info(item)
            mq = MysqlPipelinePublic()
            mq.insert_sql("t_zx_bid_crawl_info", item)
    # 下一页
    # if res.get("TotalCount")/15 + 1 < pagenum:
    #     pagenum += 1
    #     get_list(pagenum)


def get_detail(url):
    res = requests.get(url=url, headers=headers, cookies=cookies, verify=False)
    res_t = pq(res.text)
    # 层级
    bid_category = res_t('div[class="ewb-route"] p a').eq(1).text()
    bid_info_type = res_t('div[class="ewb-route"] p a').eq(2).text()
    # 详情
    content = res_t('div[class="col-md-24"]').text()
    html_content = res_t('div[class="col-md-24"]').outerHtml()
    return {
        "bid_content": content,
        "bid_html_con": html_content,
        "bid_category": bid_category,
        "bid_info_type": bid_info_type,
    }


if __name__ == "__main__":
    zz_region = {
        "370401": "市本级",
        "370481": "滕州市",
        "370403": "薛城区",
        "370406": "山亭区",
        "370402": "市中区",
        "370404": "峄城区",
        "370405": "台儿庄市",
        "370407": "高新区",
    }
    for code, region in zz_region.items():
        pagenum = 1
        get_list(code, region, pagenum)
        # break
