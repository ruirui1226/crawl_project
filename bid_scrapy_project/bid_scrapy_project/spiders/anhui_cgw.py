# -*- coding: utf-8 -*-
"""
@desc: 安徽政府采购网
@version: python3
@author: shenr
@time: 2023/06/28
"""
import base64
import json
import re
import time
import urllib
from datetime import datetime

import requests
import scrapy
from urllib.parse import quote
from pyquery import PyQuery as pq

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import GovernmentProcurementItem


class ExampleSpider(scrapy.Spider):
    name = "anhui_cgw"
    # allowed_domains = ["http://www.ccgp-anhui.gov.cn/portal/category"]
    start_urls = "http://www.ccgp-anhui.gov.cn/portal/category"
    page = 1
    page_all = 1
    page_time = ""
    current_time = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))

    list_ = [
        "ZcyAnnouncement3012",
        "ZcyAnnouncement1",
        "ZcyAnnouncement2",
        "ZcyAnnouncement3",
        "ZcyAnnouncement4",
        "ZcyAnnouncement5",
        "ZcyAnnouncement7",
        "ZcyAnnouncement10",
        "ZcyAnnouncement20",
        "ZcyAnnouncement21",
        "ZcyAnnouncement22",
        "ZcyAnnouncement23",
        "ZcyAnnouncement24",
        "ZcyAnnouncement40",
    ]

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "http://www.ccgp-anhui.gov.cn",
        "Referer": "http://www.ccgp-anhui.gov.cn/site/category?parentId=oJCosldFbaJFzmyFhz1c6Q==&childrenCode=ZcyAnnouncement3012&utm=luban.luban-PC-4718.564-pc-websitegroup-nav-front.6.3191d840155111ee964dcfbd14989399",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    cookies = {
        "wzws_sessionid": "oGSbiZCAMTI0LjEyOC42OS4xMjaBZDljNTQ0gjQ2NTdiYQ==",
        "_zcy_log_client_uuid": "319114f0-1551-11ee-964d-cfbd14989399",
    }

    def start_requests(self):
        for each in self.list_:
            data = {
                "publishDateBegin": time.strftime("%Y-%m-%d", time.localtime(int(time.time()))),
                "publishDateEnd": time.strftime("%Y-%m-%d", time.localtime(int(time.time()))),
                "pageNo": 1,
                "pageSize": 15,
                "categoryCode": each,
                "districtCode": None,
                "leaf": None,
                "_t": time.time(),
            }
            yield scrapy.FormRequest(
                url=self.start_urls,
                headers=self.headers,
                cookies=self.cookies,
                body=json.dumps(data),
                meta={"each": each},
                dont_filter=True,
                callback=self.parse_1,
                method="POST",
            )
        # break

    def parse_1(self, response, **kwargs):
        res = json.loads(response.text)
        meta = response.meta
        each = meta.get("each")
        data_ = res.get("result").get("data").get("data")
        if data_:
            for rows in data_:
                detail_url = f"http://www.ccgp-anhui.gov.cn/site/detail?parentId=oJCosldFbaJFzmyFhz1c6Q==&articleId={rows.get('articleId')}&utm=luban.luban-PC-4720.878-pc-websitegroup-anhuisecondLevelPage-front.1.01d9dc50156111eea9d043f4ceb4ca5a"
                json_url = (
                    f"http://www.ccgp-anhui.gov.cn/portal/detail?articleId="
                    + rows.get("articleId")
                    + "&timestamp=1687922447"
                )
                self.page_time = rows.get("publishDate")
                yield scrapy.Request(
                    url=json_url.replace("+", "%2B"),
                    callback=self.detail_parse,
                    # dont_filter=True,
                    meta={"detail_url": detail_url, "city": rows.get("districtName")},
                )
            if self.current_time == rows.get("publishDate"):
                self.page += 1
                data__ = {
                    "publishDateBegin": time.strftime("%Y-%m-%d", time.localtime(int(time.time()))),
                    "publishDateEnd": time.strftime("%Y-%m-%d", time.localtime(int(time.time()))),
                    "pageNo": self.page,
                    "pageSize": 15,
                    "categoryCode": each,
                    "districtCode": None,
                    "leaf": None,
                    "_t": time.time(),
                }
                yield scrapy.FormRequest(
                    url=self.start_urls,
                    headers=self.headers,
                    cookies=self.cookies,
                    body=json.dumps(data__),
                    # dont_filter=True,
                    callback=self.parse_1,
                    method="POST",
                )

    def detail_parse(self, response, **kwargs):
        res = json.loads(response.text)
        meta = response.meta
        detail_data = res.get("result").get("data")
        detail_url = meta.get("detail_url")
        item = GovernmentProcurementItem()
        item["po_id"] = get_md5(detail_data.get("articleId"))
        item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        item["bid_url"] = detail_url
        item["po_province"] = "安徽省"
        item["po_city"] = meta.get("city")
        item["po_county"] = ""
        item["po_category"] = detail_data.get("categoryNames")[1]
        item["po_info_type"] = detail_data.get("categoryNames")[2] if len(detail_data.get("categoryNames")) > 2 else detail_data.get("categoryNames")[1]
        item["po_source"] = detail_data.get("author")
        item["bo_name"] = detail_data.get("title")
        item["po_public_time"] = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(detail_data.get("publishDate") / 1000)
        )
        item["po_html_con"] = str(detail_data.get("content")).replace("'", '"')
        item["po_content"] = str(pq(detail_data.get("content")).text()).replace("'", '"')
        item["description"] = ""
        item["website_name"] = "安徽政府采购网"
        item[
            "website_url"
        ] = "http://www.ccgp-guangxi.gov.cn/luban/home?utm=luban.luban-PC-38921.960-pc-websitegroup-headerSearchBar-front.1.8326c81014bf11ee8b5d3f9131071798"
        yield item
