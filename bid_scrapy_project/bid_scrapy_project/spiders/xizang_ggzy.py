#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/7/3 9:30
@Author : zhangpf
@File : xizang_ggzy.py
@Desc : 西藏
@Software: PyCharm
"""
import datetime
import json
import math
import re
import time

from pyquery import PyQuery as pq
import scrapy
from loguru import logger

from bid_scrapy_project.common.common import urljoin_url, get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class sichuanSpider(scrapy.Spider):
    name = "xizang_ggzy"
    source_url = "http://ggzy.xizang.gov.cn"
    detail_url = "http://ggzy.xizang.gov.cn/personalitySearch/initDetailbyProjectCode"

    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": "JIDENTITY=9efc53c1-1c40-471e-8a2d-9d39f8393210; _site_id_cookie=22; arialoadData=true; SESSION=YjNmNzE2Y2UtNWZjOC00NWYwLWI4M2MtMjA1NTY4YmFmZmI1",
        "JEECMS-Auth-Token": "null",
        "Origin": "http://ggzy.xizang.gov.cn",
        "Redirect-Header": "false",
        "Referer": "http://ggzy.xizang.gov.cn/jyxxjg/1068715.jhtml",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    classify = ""

    url_list = {
        "工程建设": "http://ggzy.xizang.gov.cn/jyxxgc.jhtml",
        "政府采购": "http://ggzy.xizang.gov.cn/jyxxzc.jhtml",
        "土地使用权出让": "http://ggzy.xizang.gov.cn/jyxxtd.jhtml",
        "矿业权出让": "http://ggzy.xizang.gov.cn/jyxxky.jhtml",
        "药品采购": "http://ggzy.xizang.gov.cn/jyxxyp.jhtml",
    }

    def start_requests(self):
        for url in self.url_list.items():
            self.classify = url[0]
            yield scrapy.Request(
                url=url[1],
                callback=self.parse_list,
                dont_filter=True,
            )
            break

    def parse_list(self, response):
        response = response.text
        total = re.findall(",count: (.*?),", str(response), re.S)[0]
        # logger.info(f"共{int(total)}条")
        count = math.ceil(int(total) / 10)
        # logger.info(f"共{count}页")
        for i in range(2, count + 1):
            url = f"http://ggzy.xizang.gov.cn/jyxxgc_{i}.jhtml"
            yield scrapy.Request(
                url=url,
                callback=self.get_list_page,
                dont_filter=True,
            )
            break

    def get_list_page(self, response):
        response = response.text
        url_list = re.findall("<p onclick=\"window.open\('(.*?)'\)\">", str(response), re.S)
        for url in url_list:
            # logger.warning("当前url={}".format(self.source_url + url))
            yield scrapy.Request(
                url=self.source_url + url,
                callback=self.detail_page1,
                dont_filter=True,
                cb_kwargs={"url": self.source_url + url},
            )

    def detail_page1(self, response, url):
        response = response.text
        code = re.findall("<p>招标编号：(.*?)</p>", str(response), re.S)[0]
        code_2 = url.split("/")[-2]
        json_data = {
            "projectCode": code,
            "path": code_2,
            "sId": 22,
        }
        yield scrapy.Request(
            url=self.detail_url,
            headers=self.headers,
            callback=self.detail_page,
            dont_filter=True,
            body=json.dumps(json_data),
            cb_kwargs={"url": url, "code": code},
            method="POST",
        )

    def detail_page(self, response, **kwargs):
        url = kwargs["url"]
        code = kwargs["code"]
        res = json.loads(response.text)
        countData = res.get("data").get("countData")
        for code_2 in countData:
            json_data1 = {
                "projectCode": code,
                "path": code_2[0],
                "sId": 22,
            }
            yield scrapy.Request(
                url=self.detail_url,
                headers=self.headers,
                callback=self.detail_page2,
                body=json.dumps(json_data1),
                cb_kwargs={"url": url, "code": code},
                method="POST",
            )

    def detail_page2(self, response, **kwargs):
        # print(response.text)
        res = json.loads(response.text)
        listdata = res.get("data").get("listData")
        bid_public_time = res.get("timestamp")
        for dt in listdata:
            id = dt.get("id")
            bid_url = kwargs["url"]
            bid_name = dt.get("title")
            bid_category = self.classify
            bid_html_con = dt.get("txt")
            pre = re.compile(">(.*?)<")
            bid_content = "".join(pre.findall(str(bid_html_con)))
            if self.classify == "政府采购":
                item = GovernmentProcurementItem()
                item["po_id"] = get_md5(str(id))
                item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
                item["bid_url"] = bid_url
                item["po_province"] = "西藏自治区"
                item["po_category"] = bid_category
                item["bo_name"] = bid_name
                item["po_public_time"] = bid_public_time
                item["po_html_con"] = bid_html_con
                item["po_content"] = bid_content
                item["website_name"] = "全国公共资源交易平台(西藏自治区)西藏自治区公共资源交易网(试运行)"
                item["website_url"] = self.source_url
                item["bid_orgin_url"] = self.detail_url
                # print(item)
                yield item
            else:
                item = BidScrapyProjectItem()
                item["bid_id"] = get_md5(str(id))
                item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
                item["bid_url"] = bid_url
                item["bid_province"] = "西藏自治区"
                item["bid_category"] = bid_category
                item["bid_name"] = bid_name
                item["bid_public_time"] = bid_public_time
                item["bid_html_con"] = bid_html_con
                item["bid_content"] = bid_content
                item["website_name"] = "全国公共资源交易平台(西藏自治区)西藏自治区公共资源交易网(试运行)"
                item["website_url"] = self.source_url
                item["bid_orgin_url"] = self.detail_url
                # print(item)
                yield item
