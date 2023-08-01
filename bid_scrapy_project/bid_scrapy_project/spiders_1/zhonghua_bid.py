#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/13 9:51
# @Author  : xm
# @File    : zhonghua_bid.py
# @Description : 中化招标电子招投标平台
import datetime
import time

import scrapy

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import GovernmentProcurementItem, BidScrapyProjectItem


class ZhonghuaBidSpider(scrapy.Spider):
    name = "zhonghua_bid"

    def __init__(self):
        self.types = {
            "招标/预审/变更": "ywgg1qb", "评标结果/中标结果": "ywgg2qb",
                      "非招标采购公告": "ywgg3qb"}
        self.website_name = "中化招标电子招投标平台"
        self.webUrl = "https://e.sinochemitc.com/cms/index.htm"
        self.cates = {
            "ywgg3hw": "货物",
            "ywgg3gc": "工程",
            "ywgg3fw": "服务",
            "ywgg2hw": "货物",
            "ywgg2gc": "工程",
            "ywgg2fw": "服务",
            "ywgg1hw": "货物",
            "ywgg1gc": "工程",
            "ywgg1fw": "服务",
        }

    def start_requests(self):
        for typename, typeid in self.types.items():
            url = "http://e.sinochemitc.com/cms/channel/{}/index.htm?pageNo={}".format(typeid, 1)
            items = {
                "type": typename,
            }
            yield scrapy.Request(url, callback=self.parse, dont_filter=True, meta={"items": items, "page": 1})

    def parse(self, response, **kwargs):
        lis = response.css(".tab-pane > ul > li")
        flag = True
        for li in lis:
            href = li.css("a::attr(href)").get()
            href = response.urljoin(href)
            title = li.css("a::text").get().strip()
            pubdate = li.css(".time::text").get()
            pubdate = pubdate[pubdate.index("发布时间：") + len("发布时间：") :].strip()
            # 判断是否在一天以内  在就继续获取下一页
            timeNow = datetime.datetime.now()  ###现在的时间
            pdate = datetime.datetime.strptime(pubdate, "%Y-%m-%d")
            if abs((timeNow - pdate).days) > 1:  # 判断时间间隔天数
                flag = False
            items = {"href": href, "title": title}
            items.update(response.meta["items"])
            yield scrapy.Request(href, callback=self.content_parse, meta={"items": items})
        if flag:
            page = response.meta.get("page")
            nextPage = page + 1
            nextUrl = response.url[: response.url.index("pageNo=") + len("pageNo=")] + str(nextPage)
            yield scrapy.Request(
                nextUrl, callback=self.parse, dont_filter=True, meta={"items": response.meta["items"], "page": nextPage}
            )

    def content_parse(self, response):
        item_info = response.meta["items"]
        times = response.css(".a-time > span::text").get()
        pubdate = times[times.index("发布时间：") + len("发布时间：") :]
        content_html = response.css("div.a-content").get()
        contents = response.css("div.a-content *::text").extract()
        category = response.css("li.active > a:nth-child(2)::attr(ref)").get()
        category = self.cates[category]
        content = "".join(x.strip() for x in contents)
        items = {
            "bid_id": get_md5(item_info.get("href")),
            "bid_url": item_info.get("href"),
            "bid_category": category,
            "bid_info_type": item_info["type"],
            "bid_public_time": pubdate,
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
