#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/31 14:55
# @Author  : xm
# @File    : sinounited.py
# @Description : 圣诺联合电子招投标平台   数据量少  7.31 16：26 当天获取到了两条数据
import json
import time

import scrapy
from bs4 import BeautifulSoup

from bid_scrapy_project.common.common import timestamp_to_str, get_md5
from bid_scrapy_project.items import BidScrapyProjectItem


class SinounitedBidSpider(scrapy.Spider):
    name = "sinounited_bid"

    def __init__(self):
        self.info_types = {
            "tender_bulletin": "招标公告",
            "change_bulletin": "变更公告",
            "clarify_bulletin": "答疑澄清",
            "win_candidate_bulletin": "中标候选人公示",
            "winbid_bulletin": "中标公告",
            "abolish_bid_bulletin": "废标公告",
        }
        self.website_name = "圣诺联合电子招投标平台"
        self.webUrl = "https://www.okzhaobiao.com/#/homeMain"

    def start_requests(self):
        for info_id, info_name in self.info_types.items():
            url = "https://www.okzhaobiao.com/api/cms/openwebsite/pageFindChannelItem?page=0&size=10&channelShortName={}&itemTitle=&timeRange=1".format(
                info_id
            )
            yield scrapy.Request(url, dont_filter=True, callback=self.parse, meta={"items": {"info_name": info_name}})

    def parse(self, response, **kwargs):
        item_info = response.meta["items"]
        jsonDict = json.loads(response.text)
        dataList = jsonDict.get("data")
        if not dataList:
            return
        for data in dataList:
            bizTypeName = data.get("bizTypeName")
            itemTitle = data.get("itemTitle")
            itemDistrict = data.get("itemDistrict")
            pulishDate = data.get("pulishDate")
            pulishDate = timestamp_to_str(pulishDate)
            itemContent_html = data.get("itemContent")
            content = BeautifulSoup(itemContent_html, "lxml").text
            itemId = data.get("itemId")
            link = "https://www.okzhaobiao.com/#/dealDetails?id={}".format(itemId)
            items = {
                "list_parse": link,
                "bid_id": get_md5(link),
                "bid_url": link,
                "bid_category": bizTypeName,
                "bid_info_type": item_info["info_name"],
                "bid_public_time": pulishDate,
                "bid_name": itemTitle,
                "bid_html_con": itemContent_html,
                "bid_content": content,
                "website_name": self.website_name,
                "bid_province": "河北省",
                "website_url": self.webUrl,
                "create_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            }
            item_bid = BidScrapyProjectItem()
            item_bid.update(items)
            # print(items)
            yield item_bid
