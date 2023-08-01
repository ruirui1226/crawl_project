#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/7/20 15:08
@Author : zhangpf
@File : zhaobiaotong.py
@Desc : 招标通电子招投标交易平台
@Software: PyCharm
"""
import json
import math
import time

import scrapy
from pyquery import PyQuery

from bid_scrapy_project.common.common import urljoin_url, get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class zhaobiaotongiSpider(scrapy.Spider):
    name = "zhaobiaotong"
    source_url = "https://www.hebztb.com"
    list_url = "https://www.hebztb.com/zbxhcms/api/directive/contentList"

    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Cookie": "JSESSIONID=15A74F6F4E6983366477408AF8E6B226; acw_tc=3ccdc15e16898319765754442e2d11216475191846aaaf66c915746cb38642",
        "Referer": "https://www.hebztb.com/zbxhcms/category/bulletinList.html?dates=300&categoryId=88&tabName=%E6%8B%9B%E6%A0%87%E5%85%AC%E5%91%8A&page=1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
        "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    time = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))

    def start_requests(self):
        for categoryId in range(88, 90):
            yield scrapy.Request(
                url=f"https://www.hebztb.com/zbxhcms/api/directive/contentList?categoryId={categoryId}&pageIndex=1&blurSearch=&count=10&startPublishDate={self.time}&area=&signDate=&precise=",
                headers=self.headers,
                callback=self.get_totals,
                dont_filter=True,
                cb_kwargs={"categoryId": categoryId},
            )

    def get_totals(self, response, categoryId):
        res = json.loads(response.text)
        totalCount = res.get("page").get("totalCount")
        totals = math.ceil(int(totalCount) / 10)
        for i in range(1, totals + 1):
            url = f"https://www.hebztb.com/zbxhcms/api/directive/contentList?categoryId={categoryId}&pageIndex={i}&blurSearch=&count=10&startPublishDate={self.time}&area=&signDate=&precise="
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                callback=self.get_list_page,
                dont_filter=True,
                cb_kwargs={"categoryId": categoryId},
            )

    def get_list_page(self, response, categoryId):
        res = json.loads(response.text)
        lists = res.get("page").get("list")
        for data in lists:
            detail_url = data.get("url")
            time_one = time.localtime(int(str(data.get("publishDate"))[:-3]))
            bid_public_time = time.strftime("%Y-%m-%d", time_one)
            area = data.get("area")
            yield scrapy.Request(
                url=detail_url,
                callback=self.detail_page,
                headers=self.headers,
                cb_kwargs={
                    "detail_url": detail_url,
                    "bid_public_time": bid_public_time,
                    "area": area,
                    "categoryId": categoryId,
                },
            )

    def detail_page(self, response, **kwargs):
        res = PyQuery(response.text)
        title = res('div[class="container topTitle"] h3').text()
        bid_content = res('div[id="main"]').text()
        bid_html_con = res('div[id="main"]').outer_html()
        bid_info_type = res('table[class="blockContent"] tbody tr td').eq(0).text()
        if kwargs["categoryId"] == 88:
            bid_category = "招标公告"
        else:
            bid_category = "变更公告"
        if kwargs["area"] in ["石家庄市", "唐山市", "秦皇岛市", "邯郸市", "邢台市", "保定市", "张家口市", "承德市", "沧州市", "廊坊市", "衡水市"]:
            bid_province = "河北省"
        elif kwargs["area"] == None:
            bid_province = res('table[class="blockContent"] tbody tr td').eq(3).text()
        else:
            bid_province = "内蒙古自治区"
        item = BidScrapyProjectItem()
        item["bid_id"] = get_md5(kwargs["detail_url"])
        item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        item["bid_url"] = kwargs["detail_url"]
        item["bid_province"] = bid_province
        item["bid_city"] = kwargs["area"]
        item["bid_category"] = bid_category
        item["bid_info_type"] = bid_info_type
        item["bid_name"] = title
        item["bid_public_time"] = kwargs["bid_public_time"]
        item["bid_html_con"] = bid_html_con
        item["bid_content"] = bid_content
        item["website_name"] = "招标通电子招投标交易平台"
        item["website_url"] = self.source_url
        item["bid_orgin_url"] = kwargs["detail_url"]
        # print(item)
        yield item
