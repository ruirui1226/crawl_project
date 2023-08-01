#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/7/18 13:31
@Author : zhangpf
@File : 365jiaoyi.py
@Desc : 交易365招标采购平台
@Software: PyCharm
"""
import json
import math
import re

import time

import scrapy
from pyquery import PyQuery as pq

from bid_scrapy_project.common.common import urljoin_url, get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class jiaoyi365Spider(scrapy.Spider):
    name = "365jiaoyi"
    source_url = "https://sx.jiaoyi365.com/"
    list_url = "https://sx.jiaoyi365.com/home-web-shanxi/cgxxRest/pageList"
    code = [1, 2, 3, 4, 6]

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://sx.jiaoyi365.com",
        "Pragma": "no-cache",
        "Referer": "https://sx.jiaoyi365.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
        "authorization": "",
        "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    def start_requests(self):
        for id in self.code:
            json_data = {
                "xmLeiXing": "",
                "ggXingZhi": id,
                "zbFangShi": "1,2",
                "keyWords": None,
                "currentPage": 1,
                "rows": 10,
                "isShiShuGuoQi": None,
                "isZhanLueYingJiWuZi": None,
            }
            yield scrapy.Request(
                url=self.list_url,
                headers=self.headers,
                callback=self.get_totals,
                dont_filter=True,
                body=json.dumps(json_data),
                method="POST",
                cb_kwargs={"id": id},
            )

    def get_totals(self, response, id):
        res = json.loads(response.text)
        totalPages = res.get("data").get("totalPages")
        for i in range(1, 3):
            json_data = {
                "xmLeiXing": "",
                "ggXingZhi": id,
                "zbFangShi": "1,2",
                "keyWords": None,
                "currentPage": i,
                "rows": 10,
                "isShiShuGuoQi": None,
                "isZhanLueYingJiWuZi": None,
            }
            yield scrapy.Request(
                url=self.list_url,
                headers=self.headers,
                callback=self.get_list_page,
                dont_filter=True,
                body=json.dumps(json_data),
                method="POST",
                cb_kwargs={"id": id},
            )

    def get_list_page(self, response, id):
        res = json.loads(response.text)
        data_list = res.get("data").get("list")
        for data in data_list:
            guid1 = data.get("guid1")
            guid2 = data.get("guid2")
            ggXingZhi = data.get("ggXingZhi")
            shiXiangGuid = data.get("shiXiangGuid")
            detail_url = "https://sx.jiaoyi365.com/home-web-shanxi/cgxxRest/detail"
            url = f"https://sx.jiaoyi365.com/#/transaction-information/{guid2}?ggBdGuid={guid1}&ggXingZhi={ggXingZhi}&shiXiangGuid={shiXiangGuid}&type=1"
            json_data = {
                "guid1": guid1,
                "guid2": guid2,
                "ggXingZhi": "1",
                "shiXiangGuid": shiXiangGuid,
            }
            yield scrapy.Request(
                url=detail_url,
                headers=self.headers,
                callback=self.detail_page,
                body=json.dumps(json_data),
                method="POST",
                cb_kwargs={"detail_url": detail_url, "url": url, "id": id},
            )

    def detail_page(self, response, **kwargs):
        info_type = ""
        res = json.loads(response.text)
        data = res.get("data").get("gg")
        ggName = data.get("ggName")
        if data.get("ggStartTime") == 0:
            ggStartTime = data.get("modifyTime")
        else:
            ggStartTime = data.get("ggStartTime")
        timeStamp = str(ggStartTime)[:-3]
        timeArray = time.localtime(int(timeStamp))
        otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
        ggNeiRong = data.get("ggNeiRong")
        pre = re.compile(">(.*?)<")
        bid_content = "".join(pre.findall(str(ggNeiRong)))
        if kwargs["id"] == 1:
            info_type = "招标公告"
        elif kwargs["id"] == 6:
            info_type = "招标控制价公示"
        elif kwargs["id"] == 2:
            info_type = "表更公告"
        elif kwargs["id"] == 3:
            info_type = "中标候选人公示"
        elif kwargs["id"] == 4:
            info_type = "中标结果公示"
        item = BidScrapyProjectItem()
        item["bid_id"] = get_md5(kwargs["url"])
        item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        item["bid_url"] = kwargs["url"]
        item["bid_json_data"] = response.text
        # item["bid_province"] = province
        # item["bid_city"] = city
        # item["bid_county"] = area
        item["bid_category"] = "交易信息"
        item["bid_info_type"] = info_type
        item["bid_name"] = ggName
        item["bid_public_time"] = otherStyleTime
        item["bid_html_con"] = ggNeiRong
        item["bid_content"] = bid_content
        item["website_name"] = "交易365招标采购平台"
        item["website_url"] = self.source_url
        item["bid_orgin_url"] = kwargs["detail_url"]
        # print(item)
        yield item
