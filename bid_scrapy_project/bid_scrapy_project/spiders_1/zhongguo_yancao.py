# -*- coding: utf-8 -*-
"""
@desc: 中国烟草
@version: python3
@author: shenr
@time: 2023/07/17
"""
import base64
import datetime
import json
import random
import re
import time
import logging
import urllib

import requests
import scrapy
from urllib.parse import quote
from pyquery import PyQuery as pq

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import GovernmentProcurementItem, BidScrapyProjectItem


class ExampleSpider(scrapy.Spider):
    name = "zhonguo_yancao"
    # allowed_domains = ["http://www.ccgp-guangxi.gov.cn/"]
    start_urls = "http://www.tobacco.gov.cn/gjyc/zfcg/list.shtml"
    page = 1
    page_all = 1
    page_time = ""
    current_time = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
    info_types = ['招标公告','中标候选人公示','中标结果公示','中标结果公告','流标公告','变更公告','中标公告','成交候选人公示']
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }
    cookies = {
        "Secure": "",
        "_yfxfst10000001": "1689561790630",
        "_yfxlst10000001": "1689561790630",
        "_yfxvst10000001": "1689561790630",
        "_yfxcookie10000001": "20230717104310631697171562138864",
        "JSESSIONID": "fwAAARroZLSqvoS52UouUEGRqLVSKNS496IA",
    }

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls,
            headers=self.headers,
            cookies=self.cookies,
            dont_filter=True,
            callback=self.parse_1,
        )

    def parse_1(self, response, **kwargs):
        res = pq(response.text)
        # print("kkkk", res)
        time_ = ""
        inlist = res('ul[class="inTyList"] li')
        for each in inlist.items():
            title = each("a").text()
            detail_url = "http://www.tobacco.gov.cn/" + each("a").attr("href")
            time_ = each("span").text()
            # print(title, detail_url, time_)
            yield scrapy.Request(
                url=detail_url,
                headers=self.headers,
                cookies=self.cookies,
                callback=self.detail_parse,
            )
        if self.current_time == time_[:10]:
            self.page += 1
            yield scrapy.Request(
                url=f"http://www.tobacco.gov.cn/gjyc/zfcg/list_{self.page}.shtml",
                headers=self.headers,
                cookies=self.cookies,
                dont_filter=True,
                callback=self.parse_1,
            )

    def detail_parse(self, response, **kwargs):
        res = pq(response.text)
        title = res('meta[name="ArticleTitle"]').attr("content")
        time_ = res('meta[name="PubDate"]').attr("content")
        source = res('meta[name="ContentSource"]').attr("content")
        bid_html_con = str(res('div[class="tyContent"]').html()).replace("'", '"')
        bid_content = str(res('div[class="tyContent"]').text()).replace("'", '"')
        item = GovernmentProcurementItem()
        item["po_id"] = get_md5(response.url)
        item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        item["bid_url"] = response.url
        item["po_province"] = ""
        item["po_city"] = ""
        item["po_county"] = ""
        item["po_category"] = "采购信息"
        item["po_info_type"] = ""
        for info_type in self.info_types:
            if info_type in title:
                item["po_info_type"] = info_type
                break
        item["po_source"] = source
        item["bo_name"] = title
        item["po_public_time"] = time_
        item["po_html_con"] = bid_html_con
        item["po_content"] = bid_content
        item["description"] = ""
        item["website_name"] = "中国烟草"
        item["website_url"] = "http://www.tobacco.gov.cn/gjyc/zfcg/list.shtml"
        yield item
