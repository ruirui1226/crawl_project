#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/6/16 13:35
@Author : zhangpf
@File : shanx1_ggzy.py
@Desc : 山西省
@Software: PyCharm
"""
import json
import math
import re
import time

import attr
from pyquery import PyQuery as pq
import scrapy
from loguru import logger

from bid_scrapy_project.common.common import urljoin_url, get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class xinjiangSpider(scrapy.Spider):
    name = "shanxi_spider"
    start_urls = "http://prec.sxzwfw.gov.cn/jyxxgc/index.jhtml"
    source_url = "https://prec.sxzwfw.gov.cn/"

    data = {
        "title": "",
        "channelId": "11",
        "origin": "",
        "inDates": "4000",
        "beginTime": "",
        "endTime": "",
        "ext": "",
    }
    title = ""

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls,
            callback=self.parse_list,
            dont_filter=True,
        )

    def parse_list(self, response):
        res = pq(response.text)
        for url_list in res('ul[class="nav_second nav_special"] li a').items():
            url = url_list.attr("href")
            self.title = url_list.text()
            yield scrapy.Request(
                url=url,
                callback=self.get_list_page,
                dont_filter=True,
            )

    def get_list_page(self, response):
        res = response.text
        count = re.findall(",count: (.*?),limit", str(res), re.S)[0].strip("\n\t\t")
        page = math.ceil(int(count) / 10)
        # print(page)
        for i in range(1, 8):
            list_url = f"http://prec.sxzwfw.gov.cn/queryContent_{i}-jyxx.jspx"
            yield scrapy.FormRequest(
                url=list_url, callback=self.get_detail_page, formdata=self.data, method="POST"
            )
            # break

    def get_detail_page(self, response):
        res = pq(response.text)
        detail_url = res('a[class="cs_two_c_2"]').items()
        for url in detail_url:
            url = url.attr("href")
            # print(url)
            yield scrapy.Request(url=url, callback=self.parse_detail, cb_kwargs={"url": url})
            # break

    def parse_detail(self, response, url):
        res = pq(response.text)
        id = url.split("/")[-1].split(".")[0]
        bid_name = res('p[class="cs_title_P1"]').text()
        bid_public_time = res('p[class="cs_title_P3"]').text().split("：")[-1]
        # bid_category = res('div[class="local"] a').eq(2).text()
        # bid_info_type = res('div[class="local"] a').eq(3).text()
        if res('div[style="font-size:15pt;width: 100%;"]').outer_html() is None:
            bid_html_con = res('div[class="div-article2"]').outer_html()
            bid_content = res('div[class="div-article2"]').text()
        else:
            bid_html_con = res('div[style="font-size:15pt;width: 100%;"]').outer_html()
            bid_content = res('div[style="font-size:15pt;width: 100%;"]').text()
        if self.title == "政府采购":
            item = GovernmentProcurementItem()
            item["po_id"] = get_md5(id)
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = url
            item["po_province"] = "山西省"
            item["bid_category"] = self.title
            # item["bid_info_type"] = bid_info_type
            item["bo_name"] = bid_name
            item["po_public_time"] = bid_public_time
            item["po_html_con"] = bid_html_con
            item["po_content"] = bid_content
            item["website_name"] = "全国公共资源交易平台(山西省)"
            item["website_url"] = self.source_url
            item["bid_orgin_url"] = self.start_urls
            # print(item)
            yield item
        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = get_md5(id)
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = url
            item["bid_province"] = "山西省"
            item["bid_category"] = self.title
            # item["bid_info_type"] = bid_info_type
            item["bid_name"] = bid_name
            item["bid_public_time"] = bid_public_time
            item["bid_html_con"] = bid_html_con
            item["bid_content"] = bid_content
            item["website_name"] = "全国公共资源交易平台(山西省)"
            item["website_url"] = self.source_url
            item["bid_orgin_url"] = self.start_urls
            # print(item)
            yield item
