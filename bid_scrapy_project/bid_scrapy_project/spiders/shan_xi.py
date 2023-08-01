# -*- coding: utf-8 -*-
"""
@desc: 山西政府采购网
@version: python3
@author: shenr
@time: 2023/06/29
"""
import base64
import json
import logging
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
    name = "shan_xi_cgw"
    # allowed_domains = ["http://www.ccgp-shanxi.gov.cn/"]
    start_urls = "http://www.ccgp-shanxi.gov.cn/portal/category"
    page = 1
    page_all = 1
    page_time = ""
    current_time = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))

    list_ = [
        "ZcyAnnouncement1",
        "ZcyAnnouncement2",
        "ZcyAnnouncement3",
        "ZcyAnnouncement4",
        "ZcyAnnouncement5",
        "ZcyAnnouncement6",
        "ZcyAnnouncement7",
        "ZcyAnnouncement8",
    ]

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "http://www.ccgp-shanxi.gov.cn",
        "Referer": "http://www.ccgp-shanxi.gov.cn/luban/category?parentId=138010&childrenCode=ZcyAnnouncement&utm=luban.luban-PC-31363.959-pc-websitegroup-navBar-front.6.0e63d6e0162111ee99abbfa98413b830",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    cookies = {"_zcy_log_client_uuid": "d1917140-13f1-11ee-a1f5-a10a8d85d592"}

    def start_requests(self):
        for each in self.list_:
            data = {"pageNo": 1, "pageSize": 15, "categoryCode": each, "_t": time.time()}
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
                self.page_time = time.localtime(rows.get("publishDate") / 1000)[:10]
                detail_url = f"http://www.ccgp-shanxi.gov.cn/luban/detail?parentId=138010&articleId={rows.get('articleId')}=&utm=luban.luban-PC-37513.1024-pc-wsg-secondLevelPage-front.1.96ac9a50162111ee80a06dea46ceb215"
                json_url = (
                    f"http://www.ccgp-shanxi.gov.cn/portal/detail?articleId="
                    + rows.get("articleId")
                    + "&parentId=138010&timestamp=1688006064"
                )
                yield scrapy.Request(
                    url=json_url.replace("+", "%2B"),
                    callback=self.detail_parse,
                    # dont_filter=True,
                    meta={"detail_url": detail_url, "city": rows.get("districtName")},
                )
            if self.current_time == self.page_time:
                self.page += 1
                data__ = {"pageNo": self.page, "pageSize": 15, "categoryCode": each, "_t": time.time()}
                yield scrapy.FormRequest(
                    url=self.start_urls,
                    headers=self.headers,
                    cookies=self.cookies,
                    body=json.dumps(data__),
                    dont_filter=True,
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
        item["po_province"] = "山西省"
        item["po_city"] = meta.get("city")
        item["po_county"] = ""
        item["po_category"] = detail_data.get("categoryNames")[1]
        item["po_info_type"] = detail_data.get("categoryNames")[2]
        item["po_source"] = detail_data.get("author")
        item["bo_name"] = detail_data.get("title")
        item["po_public_time"] = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(detail_data.get("publishDate") / 1000)
        )
        item["po_html_con"] = str(detail_data.get("content")).replace("'", '"')
        item["po_content"] = str(pq(detail_data.get("content")).text()).replace("'", '"')
        item["description"] = ""
        item["website_name"] = "山西政府采购网"
        item[
            "website_url"
        ] = "http://www.ccgp-shanxi.gov.cn/luban/category?parentId=138010&childrenCode=ZcyAnnouncement&utm=luban.luban-PC-31363.959-pc-websitegroup-navBar-front.6.0e63d6e0162111ee99abbfa98413b830"
        logging.debug(item)
        yield item
