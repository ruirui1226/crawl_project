#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/19 9:21
# @Author  : xm
# @File    : army_bid.py
# @Description :贵州省招标投标服务平台
import json
import time

import scrapy
from bs4 import BeautifulSoup
from lxml import html

from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import BidScrapyProjectItem


class GuizhouBidSpider(scrapy.Spider):
    name = "guizhou_bid"

    def __init__(self):
        self.categorys = {"工程建设": "A", "土地使用和矿业权": "B", "国有产权": "C", "货物与服务": "D", "药品采购": "D4", "其他": "Z"}
        self.website_name = "贵州省招标投标服务平台"
        self.webUrl = "http://ztb.guizhou.gov.cn/"
        self.headers = {"Accept": "*/*"}

    def start_requests(self):
        for category, cateid in self.categorys.items():
            # http://ztb.guizhou.gov.cn/api/trade/search?pubDate=td&pubType=all&region=5200&industry=all&prjType=D&noticeType=all&noticeClassify=all&pageIndex=1&args=
            # http://ztb.guizhou.gov.cn/api/trade/search?pubDate=td&pubType=all&region=5200&industry=all&prjType=D&noticeType=all&noticeClassify=all&pageIndex=1&args=
            url = "http://ztb.guizhou.gov.cn/api/trade/search?pubDate=td&pubType=all&region=5200&industry=all&prjType={}&noticeType=all&noticeClassify=all&pageIndex={}&args=".format(
                cateid, 1
            )
            items = {"page": 1, "category": category}
            yield scrapy.Request(
                url=url, callback=self.parse, dont_filter=True, meta={"items": items}, headers=self.headers
            )

    def parse(self, response, **kwargs):
        jsonDict = json.loads(response.text)
        dataLists = jsonDict.get("data")
        if not dataLists:
            return
        for data in dataLists:
            title = data.get("Title")
            pubDate = data.get("PubDate")
            info_type = data.get("BTypeName")
            id = data.get("Id")
            href = "http://ztb.guizhou.gov.cn/trade/bulletin/?id={}".format(id)
            items = {"title": title, "pubDate": pubDate, "info_type": info_type, "href": href}
            items.update(response.meta["items"])
            content_api = "http://ztb.guizhou.gov.cn/api/trade/{}".format(id)
            yield scrapy.Request(content_api, callback=self.contentParse, meta={"items": items}, headers=self.headers)
        # 下一页
        page = response.meta["items"]["page"]
        nextUrl = response.url[: response.url.rindex("pageIndex=") + len("pageIndex=")] + str(page + 1) + "&args="
        items_next = {"category": response.meta["items"]["category"], "page": page + 1}
        yield scrapy.Request(
            nextUrl, callback=self.parse, dont_filter=True, meta={"items": items_next}, headers=self.headers
        )

    def contentParse(self, response):
        item_info = response.meta["items"]
        jsonDict = json.loads(response.text)
        source = jsonDict.get("Source")
        content_html = jsonDict.get("Content")
        content = remove_node(content_html, ["style"]).text
        items = {
            "bid_id": get_md5(item_info.get("href")),
            "bid_url": item_info.get("href"),
            "bid_category": item_info["category"],
            "bid_info_type": item_info["info_type"],
            "bid_public_time": item_info["pubDate"],
            "bid_name": item_info.get("title"),
            "bid_province": "贵州省",
            "bid_source": source,
            "bid_html_con": content_html,
            "bid_content": content,
            "website_name": self.website_name,
            "website_url": self.webUrl,
            "create_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        }
        item_bid = BidScrapyProjectItem()
        item_bid.update(items)
        # print(items)
        yield item_bid
