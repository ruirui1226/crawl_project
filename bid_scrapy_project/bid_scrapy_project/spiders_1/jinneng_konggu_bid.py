#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/17 16:28
# @Author  : xm
# @File    : jinnegn_konggu_bid.py
# @Description :晋能控股招标采购网
import time

import scrapy

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem


class JinnengKongguBidSpider(scrapy.Spider):
    name = "jinneng_konggu_bid"

    def __init__(self):
        self.infotypes = {
            "招标公告": "1ywgg1qb",
            "资格预审公告": "1ywgg2qb",
            "控制价/二次及其他公告": "1ywgg3qb",
            "变更公告": "1ywgg4qb",
            "中标候选人公示": "1ywgg5qb",
            "中标结果公示": "1ywgg6qb",
        }
        self.website_name = "晋能控股招标采购网"
        self.webUrl = "https://dzzb.jnkgjtdzzbgs.com/"

    def start_requests(self):
        for type, typeid in self.infotypes.items():
            url = "https://dzzb.jnkgjtdzzbgs.com/cms/channel/{}/index.htm".format(typeid)
            items = {"info_type": type}
            yield scrapy.Request(url, callback=self.parse, dont_filter=True, meta={"items": items})

    def parse(self, response, **kwargs):
        lis = response.css("#list1 li")
        for li in lis:
            href = li.css("a::attr(href)").get()
            href = response.urljoin(href)
            title = li.css("a::attr(title)").get()
            pubdate = li.css("em::text").get().strip()
            items = {"title": title, "href": href, "pubdate": pubdate}
            items.update(response.meta["items"])
            yield scrapy.Request(href, callback=self.contentparse, meta={"items": items})

    def contentparse(self, response):
        item_info = response.meta['items']
        category = response.css("div.location > div > a:nth-child(8)::text").get().strip()
        content_html = response.css(".main-text").get()
        contents = response.css(".main-text *::text").extract()
        content = ''.join(x.strip() for x in contents)
        items = {
            "bid_id": get_md5(item_info.get("href")),
            "bid_province": "山西省",
            "bid_url": item_info.get("href"),
            "bid_category": category,
            "bid_info_type": item_info["info_type"],
            "bid_public_time": item_info["pubdate"],
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
