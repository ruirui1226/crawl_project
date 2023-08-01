#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/7/12 13:59
@Author : zhangpf
@File : xinJ1ang_cgw.py
@Desc : 新疆兵团政府采购网
@Software: PyCharm
"""
import json
import math
import re
import time

import scrapy
from loguru import logger

from bid_scrapy_project.common.common import urljoin_url, get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class xinJ1ang_cgSpider(scrapy.Spider):
    name = "xinJ1ang_cg"
    source_url = "http://ccgp-bingtuan.gov.cn/"
    list_url = "http://ccgp-bingtuan.gov.cn/portal/category"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Cookie": "_zcy_log_client_uuid=582d1e00-098b-11ee-b053-d178feb2c1d3; acw_tc=ac11000116885420165033946e247e9a8fcf471edf3ee1e0a8afa84c7928bb",
        "Origin": "http://www.ccgp-qinghai.gov.cn",
        "Referer": "http://www.ccgp-qinghai.gov.cn/luban/category?parentId=4149&childrenCode=ZcyAnnouncement&utm=luban.luban-PC-43172.959-pc-websitegroup-navBar-front.3.efbffe001a1011eea9af2da466ba416f",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    url_code_list = [
        "ZcyAnnouncement10016",
        "ZcyAnnouncement3001",
        "ZcyAnnouncement3002",
        "ZcyAnnouncement3003",
        "ZcyAnnouncement3008",
        "ZcyAnnouncement3011",
        "ZcyAnnouncement3012",
        "ZcyAnnouncement3004",
        "ZcyAnnouncement3015",
        "ZcyAnnouncement3017",
        "ZcyAnnouncement4004",
        "ZcyAnnouncement3010",
        "ZcyAnnouncement3005",
        "ZcyAnnouncement3006",
        "ZcyAnnouncement3007",
        "ZcyAnnouncement8014",
        "ZcyAnnouncement8013",
        "ZcyAnnouncement5001",
        "ZcyAnnouncement7001",
        "ZcyAnnouncement8001",
        "ZcyAnnouncement9001",
        "ZcyAnnouncement9005",
        "ZcyAnnouncement10008",
        "ZcyAnnouncement10009",
        "ZcyAnnouncement10010",
        "ZcyAnnouncement10007",
        "ZcyAnnouncement10011",

    ]

    def start_requests(self):
        for code in self.url_code_list:
            json_data = {
                "pageNo": 1,
                "pageSize": 15,
                "categoryCode": code,
            }
            yield scrapy.Request(
                url=self.list_url,
                headers=self.headers,
                callback=self.get_totals,
                dont_filter=True,
                body=json.dumps(json_data),
                method="POST",
                cb_kwargs={"code": code},
            )

    def get_totals(self, response, code):
        response = json.loads(response.text)
        total = response.get("result").get("data").get("total")
        totals = math.ceil(int(total) / 15)
        for i in range(1, 3):
            json_data = {
                "pageNo": i,
                "pageSize": 15,
                "categoryCode": code,
            }
            yield scrapy.Request(
                url=self.list_url,
                headers=self.headers,
                callback=self.get_list_page,
                dont_filter=True,
                body=json.dumps(json_data),
                method="POST",
            )

    def get_list_page(self, response):
        response = json.loads(response.text)
        data_list = response.get("result").get("data").get("data")
        for d in data_list:
            timeStamp = str(time.mktime(time.localtime())).split(".")[0]
            articleId = d.get("articleId")
            url = f"http://ccgp-bingtuan.gov.cn/portal/detail?articleId={articleId}&parentId=4149"
            detail_url = f"http://ccgp-bingtuan.gov.cn/luban/detail?parentId=189170&articleId={articleId}"
            yield scrapy.Request(
                url=url.replace("+", "%2B"),
                callback=self.detail_page,
                # headers=self.headers,
                cb_kwargs={"detail_url": detail_url, "url": url},
            )

    def detail_page(self, response, **kwargs):
        # logger.warning("当前url={}".format(kwargs["detail_url"]))
        res = json.loads(response.text)
        data = res.get("result").get("data")
        bid_public_time = str(data.get("publishDate"))[:-3]
        timeArray = time.localtime(int(bid_public_time))
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        title = data.get("title")
        try:
            po_category = data.get("categoryNames")[1]
            po_info_type = data.get("categoryNames")[2]
        except:
            po_category = data.get("categoryNames")[1]
            po_info_type = ""
        id = data.get("articleId")
        bid_html_con = data.get("content")
        pre = re.compile(">(.*?)<")
        bid_content = "".join(pre.findall(str(bid_html_con)))

        item = GovernmentProcurementItem()
        item["po_id"] = get_md5(str(id))
        item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        item["bid_url"] = kwargs["detail_url"]
        item["po_province"] = "新疆"
        item["po_category"] = po_category
        item["po_info_type"] = po_info_type
        item["bo_name"] = title
        item["po_public_time"] = otherStyleTime
        item["po_html_con"] = bid_html_con
        item["po_content"] = bid_content
        item["website_name"] = "新疆兵团政府采购网"
        item["website_url"] = self.source_url
        item["bid_orgin_url"] = kwargs["url"]
        # print(item)
        yield item
