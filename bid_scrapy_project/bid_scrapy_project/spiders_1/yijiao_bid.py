#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/18 10:07
# @Author  : xm
# @File    : yijiao_bid.py
# @Description :易交在线电子招标头条交易平台
import datetime
import time

import scrapy

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem


class YijiaoBidSpider(scrapy.Spider):
    name = "yijiao_bid"

    def __init__(self):
        self.categorys = {
            "货物公告": ["huowu", "hwgg", "ghwgg"],
            "工程公告": ["gongcheng", "ggcg", "ggcgg"],
            "服务公告": ["fuwu", "fwgg", "gfwgg"],
        }
        self.website_name = "易交在线电子招标头条交易平台"
        self.webUrl = "http://www.sxyjcg.com/"

    def start_requests(self):
        for category, infos in self.categorys.items():
            for info in infos:
                url = "http://www.sxyjcg.com/{}/index_{}.jhtml".format(info, 1)
                items = {"page": 1, "category": category}
                yield scrapy.Request(url, callback=self.parse, dont_filter=True, meta={"items": items})

    def parse(self, response, **kwargs):
        flag = True
        lis = response.css("li.PaddingLR15")
        for li in lis:
            href = li.css("a::attr(href)").get()
            title = li.css("a::text").get()
            pubdate = li.css(".Right::text").get()
            if "发布时间" in pubdate:
                pubdate = pubdate[pubdate.index("发布时间：") + len("发布时间：") :]
            timeNow = datetime.datetime.now()  ###现在的时间
            pdate = datetime.datetime.strptime(pubdate, "%Y-%m-%d %H:%M:%S")
            if abs((timeNow - pdate).days) > 1:  # 判断时间间隔天数
                flag = False
                break
            items = {"href": href, "title": title, "pubdate": pubdate}
            items.update(response.meta["items"])
            yield scrapy.Request(href, callback=self.contparse, meta={"items": items})
        if flag:
            page = response.meta["items"]['page']
            nextPage = page + 1
            nextUrl = (
                response.request.url[: response.request.url.rindex("index_") + len("index_")]
                + str(nextPage)
                + r".jhtml"
            )
            items_next = {"category": response.meta["items"]["category"], "page": nextPage}
            yield scrapy.Request(nextUrl, callback=self.parse, dont_filter=True, meta={"items": items_next})

    def contparse(self, response):
        item_info = response.meta["items"]
        info_type = response.css("div.Title02 > span::text").get()
        content_html = response.css(".Content").get()
        contents = response.css(".Content *::text").extract()
        content = "".join(x.strip() for x in contents)
        items = {
            "bid_id": get_md5(item_info.get("href")),
            "bid_url": item_info.get("href"),
            "bid_category": item_info["category"],
            "bid_info_type": info_type,
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
