#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/12 9:56
# @Author  : xm
# @File    : baowu_cg.py
# @Description : 宝华智慧招标共享平台 华北专区
import datetime
import time

import scrapy

from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import BidScrapyProjectItem


class BaowuCgSpider(scrapy.Spider):
    name = "baowu_cg"

    def __init__(self):
        self.ids = ["007001", "007002", "007003"]
        self.website_name = "宝华智慧招标共享平台(华北专区)"
        self.webUrl = "https://bid.tisco.com.cn/"

    def start_requests(self):
        for id in self.ids:
            listUrl = "https://bid.tisco.com.cn/jyxx/{}/level4.html".format(id)
            yield scrapy.Request(listUrl, callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        flag = True
        lis = response.css("#info > li")
        for li in lis:
            href = li.css("a::attr(href)").get()
            href = response.urljoin(href)
            title = li.css("a::text").get().strip()
            pubdate = li.css(".em-time::text").get()
            ##判断不是当天就不再进入下一页
            timeNow = datetime.datetime.now()  ###现在的时间
            pdate = datetime.datetime.strptime(pubdate, "%Y-%m-%d")
            if abs((timeNow - pdate).days) > 1:  # 判断时间间隔天数
                flag = False
            items = {"title": title, "contentUrl": href, "pubdate": pubdate}
            yield scrapy.Request(href, callback=self.contentParse, meta={"items": items})
        # 下一页
        if flag:
            page = response.meta.get("page")
            if not page:
                page = 1
                nextPage = page + 1
                nextUrl = response.request.url.replace("level4", str(nextPage))
            else:
                nextPage = page + 1
                nextUrl = response.request.url.replace(rf"/{page}.html", rf"/{nextPage}.html")
            yield scrapy.Request(nextUrl, callback=self.parse, meta={"page": nextPage})

    def contentParse(self, response):
        item_info = response.meta["items"]
        content_html = response.css(".news_content").get()
        if content_html:
            contents = response.css(".news_content *::text").extract()
        else:
            content_html = response.css("#content").get()
            contents = response.css("#content *::text").extract()
        if not content_html:
            content_html = response.css(".ewb-article").get()
            contents = response.css(".ewb-article *::text").extract()
        content = remove_node(content_html, ["style", "script"]).text
        catogory = response.css(".em-location >a::text")[2].get()
        info_type = response.css("#viewGuid::text").get()
        items = {
            "bid_id": get_md5(item_info.get("contentUrl")),
            "bid_url": item_info.get("contentUrl"),
            "bid_category": catogory,
            "bid_info_type": info_type,
            "bid_public_time": item_info.get("pubdate"),
            "bid_name": item_info.get("title"),
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