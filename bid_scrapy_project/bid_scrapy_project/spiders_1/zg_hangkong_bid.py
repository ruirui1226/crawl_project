#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/13 16:52
# @Author  : xm
# @File    : zg_hangkong_bid.py
# @Description : 中国航空油料集团有限公司采购管理平台
import datetime
import time

import scrapy
from bs4 import BeautifulSoup
from lxml import html

from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import BidScrapyProjectItem


class ZgHangkongBidSpider(scrapy.Spider):
    name = "zg_hangkang_bid"

    def __init__(self):
        self.cates = {
            "公开招标": {
                "value": "003001",
                "child": {
                    "招标公告": "003001001",
                    "变更公告": "003001002",
                    "中标候选人公示": "003001003",
                    "中标结果公示": "003001004",
                    "异常公示": "003001005",
                },
            },
            "邀请招标": {
                "value": "003002",
                "child": {"中标候选人公示": "003002001", "中标结果公示": "003002002", "异常公示": "003002003"},
            },
            "竞争性谈判": {
                "value": "003003",
                "child": {
                    "采购公告": "003003001",
                    "变更公告": "003003002",
                    "成交候选人公示": "003003003",
                    "成交结果公示": "003003004",
                    "异常公示": "003003005",
                },
            },
            "竞争性磋商": {
                "value": "003004",
                "child": {"采购公告": "003004001", "变更公告": "003004002", "成交候选人公示": "003004003", "成交结果公示": "003004004"},
            },
            "询比采购": {
                "value": "003006",
                "child": {"采购公告": "003006001", "变更公告": "003006002", "成交候选人公示": "003006003", "成交结果公示": "003006004"},
            },
            # "竞价采购": "003005"
            # "直接采购":"003007",
        }
        self.website_name = "中国航空油料集团有限公司采购管理平台"
        self.webUrl = "http://zc.cnaf.com/"

    def start_requests(self):
        for category, cate in self.cates.items():
            value = cate["value"]
            child = cate["child"]
            for typename, typeid in child.items():
                url = "http://zc.cnaf.com/003/{}/{}/subPageGKZBlist.html".format(value, typeid)
                items = {"category": category, "info_type": typename}
                yield scrapy.Request(url, callback=self.parse, dont_filter=True, meta={"items": items})

    def parse(self, response, **kwargs):
        lis = response.css("ul.content-list > li")
        for li in lis:
            href = li.css("a::attr(href)").get()
            href = response.urljoin(href)
            title = li.css("a::text").get()
            pubdate = li.css(".column-date::text").get()
            timeNow = datetime.datetime.now()  ###现在的时间
            pdate = datetime.datetime.strptime(pubdate, "%Y-%m-%d")
            if abs((timeNow - pdate).days) > 2:  # 判断时间间隔天数
                continue
            items = {"href": href, "title": title, "pubdate": pubdate}
            items.update(response.meta["items"])
            yield scrapy.Request(url=href, callback=self.contentParse, meta={"items": items})

    def contentParse(self, response):
        item_info = response.meta["items"]
        content_html = response.css(".ewb-article-info").get()
        content = remove_node(content_html, ["script"]).text
        items = {
            "bid_id": get_md5(item_info.get("href")),
            "bid_url": item_info.get("href"),
            "bid_category": item_info["category"],
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
