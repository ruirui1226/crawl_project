# -*- coding: utf-8 -*-
"""
@desc: 枣庄公共交易资源网
@version: python3
@author: shenr
@time: 2023/07/04
"""
import base64
import json
import logging
import re
import time
import urllib
from datetime import datetime

import scrapy
from pyquery import PyQuery as pq

from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import GovernmentProcurementItem, BidScrapyProjectItem


class ExampleSpider(scrapy.Spider):
    name = "zaozhuang_ggjy"
    # allowed_domains = ["http://ggzy.zaozhuang.gov.cn/EpointWebBuilder/rest/jyxxAction/getListjy"]
    start_urls = "http://ggzy.zaozhuang.gov.cn/EpointWebBuilder/rest/jyxxAction/getListjy"
    page = 1
    page_all = 1
    page_time = ""
    current_time = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))

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

    def start_requests(self):
        for code, region in self.zz_region.items():
            data = {
                "params": json.dumps(
                    {
                        "categorynum": "018",
                        "wd": "",
                        "sdt": "",
                        "edt": "",
                        "areacode": code,
                        "pageSize": 15,
                        "pageIndex": 1,
                        "siteGuid": "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a",
                    }
                )
            }
            yield scrapy.FormRequest(
                url=self.start_urls,
                headers=self.headers,
                cookies=self.cookies,
                formdata=data,
                meta={"region": region, "code": code},
                dont_filter=True,
                callback=self.parse_1,
                method="POST",
            )

    def parse_1(self, response, **kwargs):
        res = json.loads(response.text)
        meta = response.meta
        infodata = res.get("infodata")
        for each in infodata:
            infoid = each["infoid"]
            title = each["title"]
            infodate = each["infodate"]
            self.current_time = infodate
            url = "http://ggzy.zaozhuang.gov.cn/" + each["infourl"]
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                cookies=self.cookies,
                meta={"infoid": infoid, "region": meta.get("region"), "title": title, "infodate": infodate},
                # dont_filter=True,
                callback=self.detail_parse,
            )
        if self.page_time == self.current_time:
            self.page += 1
            data_ = {
                "params": json.dumps(
                    {
                        "categorynum": "018",
                        "wd": "",
                        "sdt": "",
                        "edt": "",
                        "areacode": meta.get("each"),
                        "pageSize": 15,
                        "pageIndex": 1,
                        "siteGuid": "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a",
                    }
                )
            }
            yield scrapy.FormRequest(
                url=self.start_urls,
                headers=self.headers,
                cookies=self.cookies,
                formdata=data_,
                meta={"region": meta.get("region")},
                dont_filter=True,
                callback=self.parse_1,
                method="POST",
            )

    def detail_parse(self, response, **kwargs):
        res_t = pq(response.text)
        meta = response.meta
        bid_category = res_t('div[class="ewb-route"] p a').eq(2).text()
        bid_info_type = res_t('span[id="viewGuid"]').text()
        # 来源
        bid_source = res_t('span[id="dljg"]').text()
        # 详情
        content = res_t('div[class="col-md-24"]').text()
        html_content = res_t('div[class="col-md-24"]').outerHtml()
        if bid_category == "政府采购":
            item = GovernmentProcurementItem()
            item["po_id"] = get_md5(meta["infoid"])
            item["po_province"] = "山东省"
            item["po_city"] = "枣庄市"
            item["po_county"] = meta.get("region")
            item["bid_url"] = response.url
            item["po_category"] = bid_category
            item["po_info_type"] = bid_info_type
            item["po_source"] = bid_source
            item["po_html_con"] = str(html_content).replace("'", '"')
            item["po_content"] = remove_node(html_content, ["script"]).text
            item["bo_name"] = meta["title"]
            item["po_public_time"] = meta["infodate"]
            item["website_name"] = "枣庄市公共资源交易中心"
            item["website_url"] = "http://ggzy.zaozhuang.gov.cn/jyxx/about_jyxx.html"
            item["bid_orgin_url"] = "http://ggzy.zaozhuang.gov.cn/jyxx/about_jyxx.html"
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            logging.debug(item)
            yield item
        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = get_md5(meta["infoid"])
            item["bid_province"] = "山东省"
            item["bid_city"] = "枣庄市"
            item["bid_county"] = meta.get("region")
            item["bid_url"] = response.url
            item["bid_category"] = bid_category
            item["bid_info_type"] = bid_info_type
            item["bid_source"] = bid_source
            item["bid_html_con"] = str(html_content).replace("'", '"')
            item["bid_content"] = remove_node(html_content, ["script"]).text
            item["bid_name"] = meta["title"]
            item["bid_public_time"] = meta["infodate"]
            item["website_name"] = "枣庄市公共资源交易中心"
            item["website_url"] = "http://ggzy.zaozhuang.gov.cn/jyxx/about_jyxx.html"
            item["bid_orgin_url"] = "http://ggzy.zaozhuang.gov.cn/jyxx/about_jyxx.html"
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            logging.debug(item)
            yield item
