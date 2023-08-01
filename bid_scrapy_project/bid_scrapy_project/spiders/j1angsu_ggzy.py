#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/6/27 17:01
@Author : zhangpf
@File : j1angsu_ggzy.py
@Desc : 江苏省
@Software: PyCharm
"""
import json
import math
import re
import time

import datetime
from pyquery import PyQuery as pq
import scrapy
# from loguru import logger

from bid_scrapy_project.common.common import urljoin_url, get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem

now_time = datetime.datetime.now()

that_day = now_time.strftime("%Y-%m-%d 23:59:59")
that_day_3 = (now_time + datetime.timedelta(days=0)).strftime("%Y-%m-%d 00:00:00")


class jiangsuSpider(scrapy.Spider):
    name = "j1angsu_spider"
    source_url = "http://jsggzy.jszwfw.gov.cn"
    start_urls = "http://jsggzy.jszwfw.gov.cn/inteligentsearch/rest/esinteligentsearch/getFullTextDataNew"

    pn = 0

    json_data = {
        "token": "",
        "pn": 0,
        "rn": 20,
        "sdt": "",
        "edt": "",
        "wd": "",
        "inc_wd": "",
        "exc_wd": "",
        "fields": "title",
        "cnum": "001",
        "sort": '{"infodatepx":"0"}',
        "ssort": "title",
        "cl": 200,
        "terminal": "",
        "condition": [],
        "time": [
            {
                "fieldName": "infodatepx",
                "startTime": that_day_3,
                "endTime": that_day,
            },
        ],
        "highlights": "title",
        "statistics": None,
        "unionCondition": None,
        "accuracy": "",
        "noParticiple": "1",
        "searchRange": None,
        "isBusiness": "1",
    }

    def start_requests(self):
        # print(self.json_data)
        yield scrapy.Request(
            url=self.start_urls,
            callback=self.parse_list,
            dont_filter=True,
            body=json.dumps(self.json_data),
            method="POST"
        )

    def parse_list(self, response):
        res = json.loads(response.text)
        totalcount = res.get("result").get("totalcount")
        # print(totalcount)
        count = math.ceil(int(totalcount / 20))
        # print(count)
        # logger.info(f"共{count}页")
        for i in range(1, count + 1):
            self.json_data["pn"] = self.pn
            self.pn += 20
            yield scrapy.Request(
                url=self.start_urls,
                callback=self.get_list_page,
                dont_filter=True,
                body=json.dumps(self.json_data),
            )

    def get_list_page(self, response):
        records = json.loads(response.text).get("result").get("records")
        for re in records:
            linkurl = self.source_url + re.get("linkurl")
            # print(linkurl)
            yield scrapy.Request(
                url=linkurl,
                callback=self.detail_page,
                cb_kwargs={"url": linkurl},
            )

    def detail_page(self, response, url):
        res = pq(response.text)
        id = res('a[id="catenum"]').text()
        bid_url = url
        bid_name = res('h2[class="ewb-trade-h"]').text()
        bid_public_time = res('div[class="ewb-trade-info"]').remove("a").text().split("：")[1].split("来源")[0]
        bid_category = res('div[class="ewb-page-wrap"] div a').text().split(" ")[2]
        bid_info_type = res('span[id="viewGuid"]').text()
        bid_content = res('div[class="ewb-trade-con clearfix"]').text()
        bid_html_con = res('div[class="ewb-trade-con clearfix"]').outer_html()
        if bid_category == "政府采购":
            item = GovernmentProcurementItem()
            item["po_id"] = get_md5(id)
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = bid_url
            item["po_province"] = "江苏省"
            item["po_category"] = bid_category
            item["po_info_type"] = bid_info_type
            item["bo_name"] = bid_name
            item["po_public_time"] = bid_public_time
            item["po_html_con"] = bid_html_con
            item["po_content"] = bid_content
            item["website_name"] = "全国公共资源交易平台(江苏省) 江苏省公共资源交易平台"
            item["website_url"] = self.source_url
            item["bid_orgin_url"] = self.start_urls
            # print(item)
            yield item
        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = get_md5(id)
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = bid_url
            item["bid_province"] = "江苏省"
            item["bid_category"] = bid_category
            item["bid_info_type"] = bid_info_type
            item["bid_name"] = bid_name
            item["bid_public_time"] = bid_public_time
            item["bid_html_con"] = bid_html_con
            item["bid_content"] = bid_content
            item["website_name"] = "全国公共资源交易平台(江苏省) 江苏省公共资源交易平台"
            item["website_url"] = self.source_url
            item["bid_orgin_url"] = self.start_urls
            # print(item)
            yield item
