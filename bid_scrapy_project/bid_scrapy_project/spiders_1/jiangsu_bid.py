#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/19 16:42
# @Author  : xm
# @File    : jiangsu_bid.py
# @Description :江苏省招标投标协会网站
import datetime
import json
import time

import scrapy
from bs4 import BeautifulSoup

from bid_scrapy_project.common.common import gettime_day, get_md5
from bid_scrapy_project.items import BidScrapyProjectItem


class JiangsuBidSpider(scrapy.Spider):
    name = "jiangsu_bid"

    def __init__(self):
        self.info_type = {
            "招标公告": "Tender",
            "资格预审公告": "Qulify",
            "中标结果公示": "WinBid",
            "中标候选人公示": "WinCandidate",
            "更正公告公示": "Amend",
        }
        self.category = {
            "F3200001801": "江苏水利",
            "E3200001807": "江苏住建",
            "D3200001802": "江苏交通",
            "E3201000023": "南京货物",
            "C3209001801": "江苏悦达集团",
            "B3200001805": "徐矿集团",
            "C3209001802": "e平台交易",
            "E3200001806": "中招联合(江苏)",
            "D3200001803": "江苏交通控股",
            "E3201000024": "易建采",
            "E3200001810": "迅招交易平台",
            "E3200001811": "龙标电招",
            "D3200001804": "铁路工程",
            "E3200001812": "蜘蛛招标通",
            "E3200001809": "鑫智链电子交易平台",
            "D3200001805": "苏州轨道交通",
            "K3200001801": "江苏招标JSTCC",
            "E3201000025": "江苏港口",
            "D3200001806": "易智采",
            "D3200001807": "南京水务集团",
            "E3200001814": "招采进宝",
            "I3200001801": "新点交易平台",
            "I3200001804": "云出智慧交易",
        }
        self.page = 4
        self.website_name = "江苏省招标投标协会网站"
        self.webUrl = "http://www.jstba.org.cn/"

    def start_requests(self):
        # 获取当天的日期
        getData_before = gettime_day(days=1, cut=True)
        getData_last = gettime_day(tomorrow=1, cut=True)
        for infoname, infoid in self.info_type.items():
            # https://api.jszbtb.com/DataSyncApi/HomeTenderBulletin?PageSize=1000&CurrentPage=1&StartDateTime=2023-07-19%2000:00:00&EndDateTime=2023-07-20%2000:00:00&Keyword=
            # https://api.jszbtb.com/DataSyncApi/Home{}Bulletin?PageSize=1000&CurrentPage={}&StartDateTime={}&EndDateTime={}&Keyword=
            # https://api.jszbtb.com/DataSyncApi/AmendBulletin?PageSize=20&CurrentPage=1&StartDateTime=2023-07-19%2000:00:00&EndDateTime=2023-07-20%2000:00:00&Keyword=
            if "更正" in infoname:
                url = "https://api.jszbtb.com/DataSyncApi/{}Bulletin?PageSize=1000&CurrentPage={}&StartDateTime={}&EndDateTime={}&Keyword=".format(
                    infoid, 1, getData_before[1] + "%2000:00:00", getData_last[1] + "%2023:59:59"
                )
            else:
                url = "https://api.jszbtb.com/DataSyncApi/Home{}Bulletin?PageSize=1000&CurrentPage={}&StartDateTime={}&EndDateTime={}&Keyword=".format(
                    infoid, 1, getData_before[1] + "%2000:00:00", getData_last[1] + "%2023:59:59"
                )
            items = {"infoname": infoname}
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={"items": items})

    def parse(self, response, **kwargs):
        jsonDict = json.loads(response.text)
        datas = jsonDict.get("data").get("data")
        if not datas:
            return
        for data in datas:
            title = data.get("publicityName")
            if not title:
                title = data.get('bulletinName')
            create_time = data.get("create_time")  # 2023-07-18T03:23:40.000+0000
            pubdate = str(datetime.datetime.strptime(
                create_time.replace("T", " ").replace(".000+0000", ""), "%Y-%m-%d %H:%M:%S"
            ) + datetime.timedelta(hours=8))
            cid = data.get("id")
            info_ = response.meta["items"]["infoname"]
            info_id = self.info_type[info_]
            # https://www.jszbtb.com/#/bulletindetail/WinBidBulletin/306463
            href = "https://www.jszbtb.com/#/bulletindetail/{}Bulletin/{}".format(info_id, cid)
            # https://api.jszbtb.com/DataSyncApi/WinBidBulletin/id/306463
            apiUrl = "https://api.jszbtb.com/DataSyncApi/{}Bulletin/id/{}".format(info_id, cid)
            items = {"title": title, "pubdate": pubdate, "href": href}
            items.update(response.meta['items'])
            yield scrapy.Request(url=apiUrl, callback=self.contentParse, meta={"items": items})

    def contentParse(self, response):
        item_info = response.meta['items']
        jsonDict = json.loads(response.text)
        try:
            data = jsonDict.get("data").get("data")[0]
        except:
            return
        content_html = data.get("amendcontent")
        if not content_html:
            content_html = data.get('publicitycontent')
        if not content_html:
            content_html = data.get('bulletincontent')
        if not content_html:
            print("无内容")
            return
        content = data.get("htmlInnerText")
        if not content:
            content = BeautifulSoup(content_html, 'lxml').text
        source = data.get("bulletinmedia")
        platformcode = data.get("platformcode")  ## 大类型id
        category = self.category[platformcode]
        items = {
            "bid_id": get_md5(item_info.get("href")),
            "bid_url": item_info.get("href"),
            "bid_category": category,
            "bid_info_type": item_info["infoname"],
            "bid_public_time": item_info["pubdate"],
            "bid_name": item_info.get("title"),
            "bid_province": "江苏省",
            "bid_source": source,
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