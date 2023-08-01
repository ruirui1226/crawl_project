# -*- coding: utf-8 -*-
"""
@desc: 金采网 网站风控严重
@version: python3
@author: shenr
@time: 2023/07/13
"""
import base64
import json
import math
import random
import re
import time
import logging
import urllib
from datetime import datetime

import requests
import scrapy
from urllib.parse import quote
from pyquery import PyQuery as pq

from bid_scrapy_project.common.common import get_md5, gettime_day
from bid_scrapy_project.items import GovernmentProcurementItem, BidScrapyProjectItem


class ExampleSpider(scrapy.Spider):
    name = "jincaiwang"
    start_urls = "http://www.cfcpn.com/jcw/noticeinfo/noticeInfo/dataNoticeList"
    page = 1
    page_all = 1
    page_time = ""
    current_time,  tomorrow_time = gettime_day(tomorrow=1, cut=True)

    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://www.cfcpn.com",
        "Referer": "http://www.cfcpn.com/jcw/sys/index/goUrl?url=modules/sys/login/list&column=cggg",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    cookies = {"pageNo": "0", "pageSize": "10"}

    noticetype_dic = {
        "1": "采购公告",
        "2": "征集公告",
        "3": "更正公告",
        "4": "结果公告",
    }
    custom_settings = {"CONCURRENT_REQUESTS": 1, "DOWNLOAD_DELAY": 5}

    def start_requests(self):
        for kk, vv in self.noticetype_dic.items():
            data = {
                "noticeType": str(kk),
                "pageNo": "",
                "noticeState": "1",
                "isValid": "1",
                "orderBy": "publish_time desc",
                "noticeContent": "",
                "briefContent": "",
                "noticeTitle": "",
                "purchaseName": "",
                "purchaseId": "",
                "categoryLabName": "",
                "beginPublishTime": self.current_time,
                "endPublishTime": self.tomorrow_time,
                "areaProvince": "",
                "labelAllId": "",
            }

            yield scrapy.FormRequest(
                url=self.start_urls,
                headers=self.headers,
                cookies=self.cookies,
                formdata=data,
                dont_filter=True,
                callback=self.parse_1,
                method="POST",
                meta={"kk": kk, "next":False},
            )

    def parse_1(self, response, **kwargs):
        res = json.loads(response.text)
        meta = response.meta
        kk = meta.get("kk")
        rows = res.get("rows")
        if rows:
            for each in rows:
                # time.sleep(random.randint(1, 5))
                id_ = each.get("id")
                title = each.get("noticeTitle")
                area = each.get("area")
                detail_url = f"http://www.cfcpn.com/jcw/sys/index/goUrl?url=modules/sys/login/detail&column=undefined&searchVal={id_}"
                publishTime = each.get("publishTime")
                purchaseTypeLable = each.get("purchaseTypeLable")
                self.page_time = publishTime[:10]
                data = {"id": id_, "isDetail": "1"}
                yield scrapy.FormRequest(
                    url="http://www.cfcpn.com/jcw/noticeinfo/noticeInfo/dataNoticeList",
                    callback=self.detail_parse,
                    headers=self.headers,
                    cookies=self.cookies,
                    formdata=data,
                    method="POST",
                    meta={
                        "id_": id_,
                        "title": title,
                        "area": area,
                        "detail_url": detail_url,
                        "publishTime": publishTime,
                        "purchaseTypeLable": purchaseTypeLable,
                        "kk": kk,
                    },
                )
        next = response.meta.get('next', False)
        if next:
            total = res.get("total")
            totals = min(math.ceil(int(total) / 10), 2)
            for page in range(2, totals+1):
                data = {
                    "noticeType": str(kk),
                    "pageSize": "10",
                    "pageNo": str(page),
                    "noticeState": "1",
                    "isValid": "1",
                    "orderBy": "publish_time desc",
                    "noticeContent": "",
                    "briefContent": "",
                    "noticeTitle": "",
                    "purchaseName": "",
                    "purchaseId": "",
                    "categoryLabName": "",
                    "beginPublishTime": self.current_time,
                    "endPublishTime": self.tomorrow_time,
                    "areaProvince": "",
                    "labelAllId": ""
                }

                yield scrapy.FormRequest(
                    url=self.start_urls,
                    headers=self.headers,
                    cookies=self.cookies,
                    formdata=data,
                    dont_filter=True,
                    callback=self.parse_1,
                    method="POST",
                    meta={"kk": kk},
                )

    def detail_parse(self, response, **kwargs):
        # time.sleep(random.randint(1, 5))
        res = json.loads(response.text)
        meta = response.meta
        deatil_rows = res.get("rows")[0]
        id_ = deatil_rows.get("id")
        area = deatil_rows.get("area")
        title = deatil_rows.get("noticeTitle")
        content = deatil_rows.get("noticeContent")
        public_time = deatil_rows.get("publishTime")
        noticeSource = deatil_rows.get("noticeSource")
        purchaseTypeLable = deatil_rows.get("purchaseTypeLable")
        detail_url = meta.get("detail_url")
        if purchaseTypeLable == "采购公告":
            item = GovernmentProcurementItem()
            item["po_id"] = get_md5(id_)
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = detail_url
            item["po_province"] = area
            item["po_city"] = ""
            item["po_county"] = ""
            item["po_category"] = self.noticetype_dic.get(meta.get("kk"))
            item["po_info_type"] = purchaseTypeLable
            item["po_source"] = noticeSource
            item["bo_name"] = title
            item["po_public_time"] = public_time
            item["po_html_con"] = str(content).replace("'", '"')
            item["po_content"] = str(content).replace("'", '"')
            item["po_json_data"] = str(res).replace("'", '"')
            item["description"] = ""
            item["website_name"] = "金采网"
            item["website_url"] = "http://www.cfcpn.com/jcw/index"
            # logging.debug(item)

            yield item
        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = get_md5(id_)
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = detail_url
            item["bid_province"] = area
            item["bid_city"] = ""
            item["bid_county"] = ""
            item["bid_category"] = self.noticetype_dic.get(meta.get("kk"))
            item["bid_info_type"] = purchaseTypeLable
            item["bid_source"] = noticeSource
            item["bid_name"] = title
            item["bid_public_time"] = public_time
            item["bid_html_con"] = str(content).replace("'", '"')
            item["bid_content"] = str(content).replace("'", '"')
            item["bid_json_data"] = str(res).replace("'", '"')
            item["description"] = ""
            item["website_name"] = "金采网"
            item["website_url"] = "http://www.cfcpn.com/jcw/index"
            # logging.debug(item)
            yield item