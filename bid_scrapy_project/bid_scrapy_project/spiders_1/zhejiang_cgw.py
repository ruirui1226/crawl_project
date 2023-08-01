# -*- coding: utf-8 -*-
"""
@desc: 浙江政府采购网
@version: python3
@author: shenr
@time: 2023/06/28
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
    name = "zhejiang_cgw"
    # allowed_domains = ["http://www.ccgp-zhejiang.gov.cn/portal/category"]
    start_urls = "http://www.ccgp-zhejiang.gov.cn/portal/category"
    page = 1
    page_all = 1
    page_time = ""
    current_time = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))

    list_ = [
        "110-175885",
        "110-246839",
        "110-978863",
        "110-943756",
        "110-900461",
        "110-567245",
        "110-198517",
        "110-341071",
        "110-978920",
        "110-312114",
        "110-789803",
        "110-181331",
        "110-420383",
    ]

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "http://www.ccgp-zhejiang.gov.cn",
        "Referer": "http://www.ccgp-zhejiang.gov.cn/luban/category?parentId=600007&childrenCode=ZcyAnnouncement&utm=luban.luban-PC-36447.959-pc-websitegroup-navBar-front.3.a7de4c50157311ee9105314e275c446a",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    cookies = {
        "_zcy_log_client_uuid": "5e916b90-0b28-11ee-81ba-ebe7b936fb58",
        "acw_tc": "ac11000116879296983994700e247e57bb0092f155a066c2b4b8d1576abfdd",
        "arialoadData": "false",
    }

    def start_requests(self):
        for each in self.list_:
            data = {
                "pageNo": 1,
                "pageSize": 100,
                "categoryCode": each,
                "includeGovDistrict": 1,
                "publishDateBegin": time.strftime("%Y-%m-%d", time.localtime(int(time.time()))),
                "publishDateEnd": time.strftime("%Y-%m-%d", time.localtime(int(time.time()))),
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
                detail_url = f"http://www.ccgp-zhejiang.gov.cn/luban/detail?parentId=600007&articleId={rows.get('articleId')}&utm=luban.luban-PC-37000.979-pc-websitegroup-zhejiang-secondPage-front.1.0e0d8cb0157511ee9fbabd248a5a2c1d"
                json_url = (
                    f"http://www.ccgp-zhejiang.gov.cn/portal/detail?articleId="
                    + rows.get("articleId")
                    + "&timestamp=1687930398"
                )
                yield scrapy.Request(
                    url=json_url.replace("+", "%2B"),
                    callback=self.detail_parse,
                    # dont_filter=True,
                    meta={"detail_url": detail_url, "city": rows.get("districtName")},
                )
            self.page += 1
            if self.page < 3:
                data__ = {
                    "pageNo": self.page,
                    "pageSize": 100,
                    "categoryCode": each,
                    "includeGovDistrict": 1,
                    "publishDateBegin": time.strftime("%Y-%m-%d", time.localtime(int(time.time()))),
                    "publishDateEnd": time.strftime("%Y-%m-%d", time.localtime(int(time.time()))),
                    "_t": time.time(),
                }
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
        item["po_province"] = "浙江省"
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
        item["website_name"] = "浙江政府采购网"
        item[
            "website_url"
        ] = "http://www.ccgp-zhejiang.gov.cn/luban/category?parentId=600007&childrenCode=ZcyAnnouncement&utm=luban.luban-PC-37000.959-pc-websitegroup-navBar-front.3.0e0d8cb0157511ee9fbabd248a5a2c1d"
        # logging.debug(item)
        yield item
