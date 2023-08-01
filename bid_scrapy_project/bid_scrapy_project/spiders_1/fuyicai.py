#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/7/14 13:40
@Author : zhangpf
@File : fuyicai.py
@Desc : 福易采电子交易平台
@Software: PyCharm
"""
import json
import math
import re

import time

import scrapy

from bid_scrapy_project.common.common import urljoin_url, get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class fuyicaiSpider(scrapy.Spider):
    name = "fuyicai"
    source_url = "http://www.fycbid.cn/"
    list_url = "http://www.fycbid.cn/fyc/fyc-cms/index/home/notice"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": "__bid_n=1894df8540e4368422718f; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221894df8541b4ea-076c5eaca219248-26031d51-2073600-1894df8541c1a8b%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTg5NGRmODU0MWI0ZWEtMDc2YzVlYWNhMjE5MjQ4LTI2MDMxZDUxLTIwNzM2MDAtMTg5NGRmODU0MWMxYThiIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%221894df8541b4ea-076c5eaca219248-26031d51-2073600-1894df8541c1a8b%22%7D",
        "Origin": "http://www.fycbid.cn",
        "Referer": "http://www.fycbid.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }

    def start_requests(self):
        for i in range(0, 2):
            json_data = {
                "projName": "",
                "bultype": "",
                "projType": "",
                "bulProperties": "",
                "pageNumh": 1,
                "pageSizeh": 10,
                "purchaseType": str(i),
                "days": 1,
                "projectType": "",
                "areaCode": "0",
            }
            yield scrapy.Request(
                url=self.list_url,
                headers=self.headers,
                callback=self.get_totals,
                dont_filter=True,
                body=json.dumps(json_data),
                method="POST",
                cb_kwargs={"purchaseType": i},
            )

    def get_totals(self, response, purchaseType):
        res = json.loads(response.text)
        total = res.get("total")
        totals = math.ceil(int(total) / 10)
        for i in range(1, totals + 1):
            json_data = {
                "projName": "",
                "bultype": "",
                "projType": "",
                "bulProperties": "",
                "pageNumh": i,
                "pageSizeh": 10,
                "purchaseType": str(purchaseType),
                "days": 1,
                "projectType": "",
                "areaCode": "0",
            }
            yield scrapy.Request(
                url=self.list_url,
                headers=self.headers,
                callback=self.get_list_page,
                dont_filter=True,
                body=json.dumps(json_data),
                method="POST",
                cb_kwargs={"purchaseType": purchaseType},
            )

    def get_list_page(self, response, purchaseType):
        res = json.loads(response.text)
        rows = res.get("rows")
        for row in rows:
            id = row.get("id")
            projId = row.get("projId")
            announceType = row.get("announceType")
            detail_url = f"http://www.fycbid.cn/#/notice/detail?id={projId}&noticeId={id}"
            url = f"http://www.fycbid.cn/fyc/fyc-statistics/home/announceInfo?id={id}"
            yield scrapy.Request(
                url=url,
                callback=self.detail_page,
                headers=self.headers,
                cb_kwargs={
                    "detail_url": detail_url,
                    "url": url,
                    "id": id,
                    "announceType": announceType,
                    "purchaseType": purchaseType,
                },
            )

    def detail_page(self, response, **kwargs):
        res = json.loads(response.text)
        if res.get("total") == 0:
            yield scrapy.Request(
                url=f"http://www.fycbid.cn/fyc/fyc-statistics/home/bulletinInfo?id={kwargs['id']}",
                callback=self.detail_page,
                headers=self.headers,
                cb_kwargs={
                    "detail_url": kwargs["detail_url"],
                    "url": kwargs["url"],
                    "announceType": kwargs["announceType"],
                    "purchaseType": kwargs["purchaseType"],
                },
            )
        else:
            if kwargs["purchaseType"] == "1":
                bid_category = "委托招采"
            else:
                bid_category = "自主采购"
            if kwargs["announceType"] == "zbgg":
                bid_info_type = "招标公告"
            elif kwargs["announceType"] == "zgysgg":
                bid_info_type = "资格预审公告"
            elif kwargs["announceType"] == "bggg":
                bid_info_type = "变更公告"
            elif kwargs["announceType"] == "jggs":
                bid_info_type = "结果公示"
            else:
                bid_info_type = ""
            res = json.loads(response.text)
            data = res.get("rows")[0]
            title = data.get("title")
            bid_html_con = data.get("content")
            province = data.get("province")
            city = data.get("city")
            area = data.get("area")
            pre = re.compile(">(.*?)<")
            bid_content = "".join(pre.findall(str(bid_html_con)))
            item = BidScrapyProjectItem()
            item["bid_id"] = get_md5(kwargs["url"])
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = kwargs["detail_url"]
            item["bid_province"] = province
            item["bid_city"] = city
            item["bid_county"] = area
            item["bid_category"] = bid_category
            item["bid_info_type"] = bid_info_type
            item["bid_name"] = title
            item["bid_public_time"] = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
            item["bid_html_con"] = bid_html_con
            item["bid_content"] = bid_content
            item["website_name"] = "福易采电子交易平台"
            item["website_url"] = self.source_url
            item["bid_orgin_url"] = kwargs["detail_url"]
            # print(item)
            yield item
