#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/31 16:34
# @Author  : xm
# @File    : ejiaoyi_bid.py
# @Description :e交易-产权交易与招标采购的非标资产电子商务平台
import time

import scrapy

from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import BidScrapyProjectItem


class EjiaoyiBidSpder(scrapy.Spider):
    name = "ejiaoyi_bid"

    def __init__(self):
        self.website_name = "e交易-产权交易与招标采购的非标资产电子商务平台"
        self.webUrl = "https://www.ejy365.com/"
        self.cates = {"GC": "工程", "HW": "货物", "FW": "服务", "QT": "其他"}

    def start_requests(self):
        for cateid, catename in self.cates.items():
            for page in range(1, 10):
                url = "https://www.ejy365.com/purchase/list?morejg=0&orderType={}&page={}".format(cateid, page)
                items = {"category": catename}
                yield scrapy.Request(url, dont_filter=True, callback=self.parse, meta={"items": items})

    def parse(self, response, **kwargs):
        lis = response.css("div.waterfall-list.clearfix > div > div > ul > li")
        for li in lis:
            href = li.css("a::attr(href)").get()
            info_type = li.css("a .fr > em::text").get()
            title = li.css(".title-cg > h3::attr(title)").get()
            items = {"href": href, "title": title, "info_type": info_type}
            items.update(response.meta["items"])
            yield scrapy.Request(href, callback=self.contentParse, meta={"items": items})

    def contentParse(self, response):
        item_info = response.meta["items"]
        # .layui-show > div > div > div > div.time
        pubdate = response.css(".layui-show > div > div > div > div.time::text").get()
        if not pubdate:
            print()
            return
        #处理 发布时间 2023-08-01 10:16:26
        pubdate = pubdate[pubdate.index("发布时间 ") + len("发布时间 "):].strip()
        content_html = response.css(".layui-show  > div > div > div").get()
        content = remove_node(content_html, ["style", "script"]).text
        items = {
            "bid_id": get_md5(item_info["href"]),
            "bid_url": item_info["href"],
            "bid_category": item_info["category"],
            "bid_info_type": item_info["info_type"],
            "bid_public_time": pubdate,
            "bid_name": item_info["title"],
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
