#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/7/19 9:39
@Author : zhangpf
@File : guangda.py
@Desc : 光大环境招标采购电子交易平台
@Software: PyCharm
"""
import time

import scrapy
from pyquery import PyQuery as pq

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem


class guangdaSpider(scrapy.Spider):
    name = "guangda"
    source_url = "https://zcpt.cebenvironment.com.cn/"
    list_url = "https://zcpt.cebenvironment.com.cn/cms/category/iframe.html"

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": "JSESSIONID=2D5459D011A888B604ACF01899994516; JSESSIONID=2D5459D011A888B604ACF01899994516",
        "Referer": "https://zcpt.cebenvironment.com.cn/cms/category/iframe.html?dates=300&categoryId=2&tabName=%E6%8B%9B%E6%A0%87%E5%85%AC%E5%91%8A&page=1",
        "Sec-Fetch-Dest": "iframe",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    classify_list = [
        {"categoryId": 2, "tabName": "招标公告"},
        {"categoryId": 3, "tabName": "变更公告"},
        {"categoryId": 4, "tabName": "中标候选人公示"},
        {"categoryId": 5, "tabName": "采购结果公示"},
        {"categoryId": 6, "tabName": "废标公告"},
        {"categoryId": 17, "tabName": "废旧物资处置公告"},
    ]

    def start_requests(self):
        for classify in self.classify_list:
            categoryId = classify.get("categoryId")
            tabName = classify.get("tabName")
            searchDate = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
            yield scrapy.Request(
                url=f"https://zcpt.cebenvironment.com.cn/cms/category/iframe.html?searchDate={searchDate}&dates=0&categoryId={categoryId}&tabName={tabName}&precise=&status=&tenderno=&goSearch=&tenderMethod=",
                headers=self.headers,
                callback=self.get_totals,
                dont_filter=True,
                cb_kwargs={"categoryId": categoryId, "tabName": tabName, "searchDate": searchDate},
            )

    def get_totals(self, response, **kwargs):
        categoryId = kwargs["categoryId"]
        tabName = kwargs["tabName"]
        searchDate = kwargs["searchDate"]
        res = pq(response.text)
        pages = res('div[class="pages"] label').eq(0).text()
        for i in range(1, int(pages) + 1):
            yield scrapy.Request(
                url=f"https://zcpt.cebenvironment.com.cn/cms/category/iframe.html?searchDate={searchDate}&dates=0&categoryId={categoryId}&tabName={tabName}&precise=&status=&tenderno=&goSearch=&tenderMethod=&page={i}",
                headers=self.headers,
                callback=self.get_list_page,
                dont_filter=True,
            )

    def get_list_page(self, response):
        res = pq(response.text)
        details_url = res('ul[class="newslist"] li a').items()
        for detail_url in details_url:
            href = detail_url.attr("href")
            yield scrapy.Request(
                url=href,
                callback=self.detail_page,
                headers=self.headers,
                cb_kwargs={"detail_url": href},
            )

    def detail_page(self, response, detail_url):
        res = pq(response.text)
        if res('div[class=" topTitle"]').text() == "":
            title = res('div[class="load "] div span').eq(0).text()
        else:
            title = res('div[class=" topTitle"]').text()
        if res('div[id="main"]').text() == "":
            bid_content = res('div[class="container"]').eq(2).text()
            bid_html_con = res('div[class="container"]').eq(2).outer_html()
        else:
            bid_content = res('div[id="main"]').text()
            bid_html_con = res('div[id="main"]').outer_html()
        po_info_type = res('div[class="load "] div a').eq(1).text()
        item = BidScrapyProjectItem()
        item["bid_id"] = get_md5(detail_url)
        item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        item["bid_url"] = detail_url
        # item["bid_province"] = province
        # item["bid_city"] = city
        # item["bid_county"] = area
        item["bid_category"] = "采购项目信息"
        item["bid_info_type"] = po_info_type
        item["bid_name"] = title
        item["bid_public_time"] = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
        item["bid_html_con"] = bid_html_con
        item["bid_content"] = bid_content
        item["website_name"] = "光大环境招标采购电子交易平台"
        item["website_url"] = self.source_url
        item["bid_orgin_url"] = detail_url
        # print(item)
        yield item
