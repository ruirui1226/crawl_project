#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/13 14:32
# @Author  : xm
# @File    : zhongmei_bid.py
# @Description : 中煤招标与采购网
import datetime
import time

import scrapy

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem


class ZhongmeiBidSpider(scrapy.Spider):
    name = "zhongmei_bid"

    def __init__(self):
        self.website_name = "中煤招标与采购网"
        self.webUrl = "http://www.zmzb.com/cms/index.htm"
        self.types = {"ywgg1": "招标公告", "ywgg2": "非招标公告", "ywgg3": "变更公告", "ywgg4": "候选人公示", "ywgg5": "中标公告"}
        self.cates = {"gc": "工程", "hw": "货物", "fw": "服务"}

    def start_requests(self):
        for tyid, tyname in self.types.items():
            for caid, caname in self.cates.items():
                url = "http://www.zmzb.com/cms/channel/{}/index.htm?pageNo=1".format(tyid + caid)
                items = {"type": tyname, "category": caname}
                yield scrapy.Request(url, callback=self.parse, dont_filter=True, meta={"items": items, "page": 1})

    def parse(self, response, **kwargs):
        flag = True
        lis = response.css(".infolist-main > #list1 > li")
        for li in lis:
            href = li.css("a::attr(href)").get()
            href = response.urljoin(href)
            title = li.css("a::attr(title)").get().strip()
            pubdate = li.css("em::text")[2].get().strip()
            timeNow = datetime.datetime.now()  ###现在的时间
            pdate = datetime.datetime.strptime(pubdate, "%Y-%m-%d")
            if abs((timeNow - pdate).days) > 1:  # 判断时间间隔天数
                flag = False
            items = {"href": href, "title": title, "pubdate": pubdate}
            items.update(response.meta["items"])
            yield scrapy.Request(href, callback=self.contentparse, meta={"items": items})
        if flag:
            # 下一页
            page = response.meta["page"]
            nextPage = page + 1
            nextUrl = response.url[: response.url.index("pageNo=") + len("pageNo=")] + str(nextPage)
            yield scrapy.Request(
                nextUrl, callback=self.parse, dont_filter=True, meta={"items": response.meta["items"], "page": nextPage}
            )

    def contentparse(self, response):
        item_info = response.meta["items"]
        content_html = response.css("div.main-text").get()
        contents = response.css("div.main-text *::text").extract()
        content = "".join(x.strip() for x in contents)
        items = {
            "bid_id": get_md5(item_info.get("href")),
            "bid_url": item_info.get("href"),
            "bid_category": item_info["category"],
            "bid_info_type": item_info["type"],
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
