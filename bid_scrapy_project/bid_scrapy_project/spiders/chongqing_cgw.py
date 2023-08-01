# -*- coding: utf-8 -*-
"""
@desc: 重庆政府采购网
@version: python3
@author: shenr
@time: 2023/06/30
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
    name = "chongqing_cgw"
    # allowed_domains = ["https://www.ccgp-chongqing.gov.cn/info-notice/procument-notice"]
    start_urls = "https://www.ccgp-chongqing.gov.cn/gwebsite/api/v1/notices/stable/new"
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
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Referer": "https://www.ccgp-chongqing.gov.cn/info-notice/procument-notice",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }
    cookies = {
        "Hm_lvt_a41ec8f07afa1805aa0eaeec292c8be0": "1688016752",
        "Hm_lpvt_a41ec8f07afa1805aa0eaeec292c8be0": "1688016771",
    }

    def start_requests(self):
        params = {
            "__platDomain__": "www.ccgp-chongqing.gov.cn",
            "endDate": self.current_time,
            "isResult": "1",
            "pi": "1",
            "ps": "20",
            "startDate": self.current_time,
            "type": "100,200,201,202,203,204,205,206,207,208,309,400,401,402,3091,4001",
        }
        yield scrapy.FormRequest(
            url=self.start_urls,
            headers=self.headers,
            cookies=self.cookies,
            formdata=params,
            dont_filter=True,
            callback=self.parse_1,
            method="GET",
        )
        # break

    def parse_1(self, response, **kwargs):
        res = json.loads(response.text)
        meta = response.meta
        for each in res.get("notices"):
            self.page_time = each["issueTime"]
            title = each["title"]
            id_ = each["id"]
            districtName = each["districtName"]
            detail_url = f"https://www.ccgp-chongqing.gov.cn/info-notice/procument-notice-detail/{id_}?title={title}"
            json_url = f"https://www.ccgp-chongqing.gov.cn/gwebsite/api/v1/notices/stable/{id_}?__platDomain__=www.ccgp-chongqing.gov.cn"
            yield scrapy.Request(
                url=json_url,
                callback=self.detail_parse,
                # dont_filter=True,
                meta={
                    "detail_url": detail_url,
                    "title": title,
                    "id_": id_,
                },
            )
        if self.current_time == self.page_time:
            self.page += 1
            params = {
                "__platDomain__": "www.ccgp-chongqing.gov.cn",
                "endDate": self.current_time,
                "isResult": self.page,
                "pi": "1",
                "ps": "20",
                "startDate": self.current_time,
                "type": "100,200,201,202,203,204,205,206,207,208,309,400,401,402,3091,4001",
            }
            yield scrapy.FormRequest(
                url=self.start_urls,
                headers=self.headers,
                cookies=self.cookies,
                formdata=params,
                # dont_filter=True,
                callback=self.parse_1,
                method="GET",
            )

    def detail_parse(self, response, **kwargs):
        res = json.loads(response.text)
        meta = response.meta
        detail_url = meta.get("detail_url")
        title = meta.get("title")
        id_ = meta.get("id_")
        item = GovernmentProcurementItem()
        item["po_id"] = get_md5(id_)
        item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        item["bid_url"] = detail_url
        item["po_province"] = "重庆市"
        item["po_city"] = "重庆市"
        item["po_county"] = res.get("notice").get("districtName")
        item["po_category"] = "采购公告"
        item["po_info_type"] = res.get("notice").get("projectPurchaseWayName")
        item["po_source"] = res.get("notice").get("creatorOrgName")
        item["bo_name"] = title
        item["po_public_time"] = res.get("notice").get("issueTime")
        item["po_html_con"] = str(res.get("notice").get("html")).replace("'", '"')
        item["po_content"] = str(pq(res.get("notice").get("html")).text()).replace("'", '"')
        item["description"] = ""
        item["website_name"] = "重庆政府采购网"
        item["website_url"] = "https://www.ccgp-chongqing.gov.cn/"
        logging.debug(item)
        yield item
