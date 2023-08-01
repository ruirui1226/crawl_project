#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/19 15:00
# @Author  : xm
# @File    : shanxi_bid.py
# @Description :安徽省招标投标信息网   请求次数过多会不返回数据 状态码404  列表页会状态码403
import time

import scrapy
from scrapy.http import JsonRequest

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem
from bid_scrapy_project.settings import SPECIAL_CLOSESPIDER_TIMEOUT


class ShanxiBidSpider(scrapy.Spider):
    """
    测试 当天有68页数据 只可跑11页数据
    """

    name = "anhui_bid"
    custom_settings = {
        "RETRY_HTTP_CODES": [404],
        "CONCURRENT_REQUESTS": 1,
        "DOWNLOAD_DELAY": 0.5,
        "CLOSESPIDER_TIMEOUT": SPECIAL_CLOSESPIDER_TIMEOUT,
    }

    def __init__(self):
        self.apiUrl = "http://www.ahtba.org.cn/site/trade/affiche/pageList"
        self.website_name = "安徽省招标投标信息网"
        self.webUrl = "http://www.ahtba.org.cn"
        self.headers = {"Content-Type": "application/json"}

    def start_requests(self):
        # td 当天
        params = {
            "pubTime": "td",
            "tradeType": "",
            "regionCode": "",
            "afficheSourceType": "",
            "afficheTitle": "",
            "pageNum": 1,
            "pageSize": 1000,
        }

        yield JsonRequest(self.apiUrl, data=params, dont_filter=True, meta={"page": 1}, headers=self.headers)

    def parse(self, response, **kwargs):
        if "暂无数据" in response.text:
            return
        # print("这是第{}页".format(response.meta["page"]))
        lis = response.css("body > div > ul > li")
        for li in lis:
            href = li.css("a::attr(href)").get()
            href = response.urljoin(href)
            title = li.css("a::text").get()
            pubdate = li.css(".fr::text").get()
            # 类别
            typ_info = li.css(".detailCons > div")
            province = source = category = info_type = None
            for type in typ_info:
                type_ = type.css("span::text").get()
                typename = type.css("span::text")[1].get()
                if "项目区域" in type_:
                    province = typename
                elif "来源" in type_:
                    source = typename
                elif "交易信息分类" in type_:
                    category = typename
                elif "公告公示" in type_:
                    info_type = typename

            items = {
                "href": href,
                "title": title,
                "pubdate": pubdate,
                "province": province,
                "source": source,
                "category": category,
                "info_type": info_type,
            }
            try:
                contentId = href[href.index("detail/") + len("detail/") :]
            except:
                # print("非正常跳过")
                continue
            hrefApi = "http://www.ahtba.org.cn/htmlUrl/trade_/{}/{}.html".format(pubdate, contentId)
            yield scrapy.Request(url=hrefApi, callback=self.contentParse, meta={"items": items})
        # 下一页
        # page = response.meta["page"]
        # nextParam = {
        #     "pubTime": "td",
        #     "tradeType": "",
        #     "regionCode": "",
        #     "afficheSourceType": "",
        #     "afficheTitle": "",
        #     "pageNum": page + 1,
        #     "pageSize": 1000,
        # }
        # yield JsonRequest(
        #     url=self.apiUrl, data=nextParam, callback=self.parse, meta={"page": page + 1}, headers=self.headers
        # )

    def contentParse(self, response):
        item_info = response.meta["items"]
        content_html = response.css(".detailCon").get()
        contents = response.css(".detailCon *::text").extract()
        content = "".join(x.strip() for x in contents)
        items = {
            "bid_id": get_md5(item_info.get("href")),
            "bid_url": item_info.get("href"),
            "bid_category": item_info["category"],
            "bid_info_type": item_info["info_type"],
            "bid_source": item_info["source"],
            "bid_province": "安徽省",
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
        # print(item_info.get("href"))
        yield item_bid
