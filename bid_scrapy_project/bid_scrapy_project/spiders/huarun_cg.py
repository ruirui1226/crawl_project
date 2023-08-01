#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/12 16:14
# @Author  : xm
# @File    : huarun_cg.py
# @Description : 华润集团守正电子招标采购平台
import datetime
import time

import scrapy
from bs4 import BeautifulSoup
from lxml import html

from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class HuarunCgSpider(scrapy.Spider):
    name = "huarun_cg"

    def __init__(self):
        self.types = {
            "招标专区": {
                "招标（预审）公告": "http://szecp.crc.com.cn/zbxx/006001/006001001/secondpagejy.html",
                "变更公告": "http://szecp.crc.com.cn/zbxx/006001/006001002/secondpagejy.html",
                "中标候选人公示": "http://szecp.crc.com.cn/zbxx/006001/006001003/secondpagejyNoStatuw.html",
                "中标公告": "http://szecp.crc.com.cn/zbxx/006001/006001004/secondpagejyNoStatuw.html",
                "终止公告": "http://szecp.crc.com.cn/zbxx/006001/006001005/secondpagejyNoStatuw.html",
                "开标日程": "http://szecp.crc.com.cn/zbxx/006001/006001006/weekInfo.html",
            },
            "非招标专区": {
                "采购公告": "http://szecp.crc.com.cn/zbxx/006002/006002001/secondpagejy.html",
                "变更公告": "http://szecp.crc.com.cn/zbxx/006002/006002002/secondpagejy.html",
                "结果公告": "http://szecp.crc.com.cn/zbxx/006002/006002003/secondpagejyNoStatuw.html",
            },
        }
        self.website_name = "华润集团守正电子招标采购平台"
        self.webUrl = "http://szecp.crc.com.cn/"
        self.cates = {"FZ": "服务", "SZ": "货物", "GZ": "工程", "QT": "其他"}

    def start_requests(self):
        for zonename, zongtype in self.types.items():
            for typename, typeUrl in zongtype.items():
                items = {"bid_zone": zonename, "info_type": typename}
                yield scrapy.Request(typeUrl, callback=self.parse, dont_filter=True, meta={"items": items})

    def parse(self, response, **kwargs):
        trs = response.css("#infocontent > tr")
        flag = True
        for tr in trs:
            href = tr.css("td>a::attr(href)").get()
            href = response.urljoin(href)
            title = tr.css("td>a::text").get().strip()
            category = tr.css(".zclx_lw::text").get()
            if category in self.cates.keys():
                category = self.cates[category]
            pubdate = tr.css("td:nth-child(5)::text").get()
            if not pubdate:
                pubdate = tr.css("td:nth-child(4)::text").get()
            if not pubdate:
                continue
            # 判断时间 判断是否进下一页
            timeNow = datetime.datetime.now()  ###现在的时间
            pdate = datetime.datetime.strptime(pubdate, "%Y-%m-%d")
            if abs((timeNow - pdate).days) > 1:  # 判断时间间隔天数
                flag = False
            items = {"title": title, "href": href, "category": category, "pubdate": pubdate}
            items.update(response.meta["items"])
            yield scrapy.Request(href, callback=self.content_parse, meta={"items": items})
        if flag:
            page = response.meta.get("page")
            if not page:
                page = 1
            nextPage = page + 1
            nextUrl = response.url[: response.url.rindex("/") + 1] + str(nextPage) + r".html"
            yield scrapy.Request(
                nextUrl, callback=self.parse, dont_filter=True, meta={"items": response.meta["items"], "page": nextPage}
            )

    def content_parse(self, response):
        item_info = response.meta["items"]
        content_html = response.css(".ewb-con-bd").get()
        content = remove_node(content_html, ["style", "script"]).text.strip()
        if item_info["bid_zone"] == "招标专区":
            items = {
                "bid_id": get_md5(item_info.get("href")),
                "bid_url": item_info.get("href"),
                "bid_category": item_info.get("category"),
                "bid_info_type": item_info.get("info_type"),
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
        else:
            items = {
                "po_id": get_md5(item_info.get("href")),
                "bid_url": item_info.get("href"),
                "po_category": "政府采购",
                "po_info_type": item_info.get("info_type"),
                "po_public_time": item_info.get("pubdate"),
                "bo_name": item_info.get("title"),
                "po_html_con": content_html,
                "po_content": content,
                "website_name": self.website_name,
                "website_url": self.webUrl,
                "create_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            }
            item_po = GovernmentProcurementItem()
            item_po.update(items)
            # print(items)
            yield item_po

