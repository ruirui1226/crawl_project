# -*- coding: utf-8 -*-
"""
@desc: 广西政府采购网
@version: python3
@author: shenr
@time: 2023/06/27
"""
import base64
import json
import re
import time
import logging
import urllib
from datetime import datetime

import requests
import scrapy
from urllib.parse import quote
from pyquery import PyQuery as pq

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import GovernmentProcurementItem


class ExampleSpider(scrapy.Spider):
    name = "guangxi_cg"
    # allowed_domains = ["http://www.ccgp-guangxi.gov.cn/"]
    start_urls = "http://www.ccgp-guangxi.gov.cn/portal/category"
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
        "ZcyAnnouncement10",
        "ZcyAnnouncement11",
        "ZcyAnnouncement20",
        "ZcyAnnouncement21",
        "ZcyAnnouncement22",
        "ZcyAnnouncement23",
    ]

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "http://www.ccgp-guangxi.gov.cn",
        "Referer": "http://www.ccgp-guangxi.gov.cn/luban/category?parentId=66485&childrenCode=ZcyAnnouncement&utm=luban.luban-PC-38919.959-pc-websitegroup-navBar-front.5.ffa2d62014b211eeb3b72f0bc6664491",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    cookies = {
        "acw_tc": "ac11000116878469359297429e44c9017b23224da1cdb01bea103abca97d6b",
        "_zcy_log_client_uuid": "f6101f50-14b2-11ee-a6cc-719a354b5bc1",
    }

    def start_requests(self):
        for each in self.list_:
            data = {"pageNo": 1, "pageSize": 15, "categoryCode": each, "_t": time.time()}
            yield scrapy.FormRequest(
                url=self.start_urls,
                headers=self.headers,
                cookies=self.cookies,
                body=json.dumps(data),
                meta={"each": each},
                # dont_filter=True,
                callback=self.parse_1,
                method="POST",
            )
            # break

    def parse_1(self, response, **kwargs):
        res = json.loads(response.text)
        data_ = res.get("result").get("data").get("data")
        meta = response.meta
        if data_:
            for rows in data_:
                self.page_time = time.localtime(rows.get("publishDate") / 1000)[:10]
                detail_url = f"http://www.ccgp-guangxi.gov.cn/luban/detail?parentId=66485&articleId={rows.get('articleId')}&utm=luban.luban-PC-38919.1085-pc-wsg-guangxi-secondPage-front.17.310cfba014b311ee9f9fe3406243b6e8"
                json_url = (
                    f"http://www.ccgp-guangxi.gov.cn/portal/detail?articleId="
                    + rows.get("articleId")
                    + "&parentId=66485"
                )
                yield scrapy.Request(
                    url=json_url.replace("+", "%2B"),
                    callback=self.detail_parse,
                    dont_filter=True,
                    meta={"detail_url": detail_url, "city": rows.get("districtName")},
                )
        if self.current_time == self.page_time:
            self.page += 1
            data = {"pageNo": self.page, "pageSize": 15, "categoryCode": meta.get("each"), "_t": time.time()}
            yield scrapy.FormRequest(
                url=self.start_urls,
                headers=self.headers,
                cookies=self.cookies,
                body=json.dumps(data),
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
        item["po_province"] = "广西省"
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
        item["website_name"] = "广西政府采购网"
        item[
            "website_url"
        ] = "http://www.ccgp-guangxi.gov.cn/luban/home?utm=luban.luban-PC-38921.960-pc-websitegroup-headerSearchBar-front.1.8326c81014bf11ee8b5d3f9131071798"
        logging.debug(item)
        yield item
