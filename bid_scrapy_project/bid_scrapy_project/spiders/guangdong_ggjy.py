# -*- coding: utf-8 -*-
"""
@desc: 广东公共资源交易平台-加速乐
@version: python3
@author: shenr
@time: 2023/06/14
"""
import base64
import json
import logging
import re
import time

import requests
import scrapy
from pyquery import PyQuery as pq

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem


class ExampleSpider(scrapy.Spider):
    name = "guangdong_ggjy"
    allowed_domains = ["http://bs.gdggzy.org.cn/osh-web/project/projectbulletin/bulletinList"]
    start_urls = "http://bs.gdggzy.org.cn/osh-web/project/projectbulletin/bulletinList"
    page = 1
    page_all = 1

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "http://bs.gdggzy.org.cn",
        "Referer": "http://bs.gdggzy.org.cn/osh-web/project/projectbulletin/bulletinList",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }
    cookies = {
        "Hm_lvt_e69ca51933e85f436518122b1647992e": "1686719334,1686813003,1686878859",
        "Hm_lpvt_e69ca51933e85f436518122b1647992e": "1686878920",
        "JSESSIONID": "F5DA2E51597989162B776394C6AC74A1",
        "__jsluid_h": "4c221cb9626e8ed8cb7c6299d3146385",
        "__jsl_clearance": "1686878859.096|1|8EsTnK10cEbAmGqRsgMe%2FOrSckc%3D",
    }

    def start_requests(self):
        data = {
            "orgCode": "",
            "tradeTypeId": "GovernmentProcurement",
            "queryType": "1",
            "tradeItemId": "zf_res_bulletin",
            "bulletinName": "",
            "startTime": "",
            "endTime": "",
            "pageNum": "1",
        }
        yield scrapy.FormRequest(
            self.start_urls,
            headers=self.headers,
            cookies=self.cookies,
            formdata=data,
            dont_filter=True,
            callback=self.parse_1,
            method="POST",
        )

    def parse_1(self, response, **kwargs):
        if int(response.status) == 200:
            res = pq(response.text)
            table = res('table[class="table"] tbody tr')
            logging.debug(f"============当前爬取{self.page}页==========")
            for each in table.items():
                detail_url = "http://bs.gdggzy.org.cn" + each("td a").attr("href")
                bid_city = each("td").eq(2).text()
                yield scrapy.Request(
                    url=detail_url,
                    headers=self.headers,
                    meta={"bid_city": bid_city},
                    dont_filter=True,
                    callback=self.detail_parse,
                )
            # if self.page == 1:
            #     count = re.findall('pageCount = parseInt\("(.*?)"\);', str(res), re.S)[0]
            #     self.page_all = int(count)
            self.page += 1
            # if self.page < self.page_all:
            data = {
                "orgCode": "",
                "tradeTypeId": "GovernmentProcurement",
                "queryType": "1",
                "tradeItemId": "zf_res_bulletin",
                "bulletinName": "",
                "startTime": "",
                "endTime": "",
                "pageNum": str(self.page),
            }
            yield scrapy.FormRequest(
                self.start_urls,
                headers=self.headers,
                cookies=self.cookies,
                formdata=data,
                dont_filter=True,
                callback=self.parse_1,
                method="POST",
            )
        else:
            logging.debug("==========爬取结束============")

    def detail_parse(self, response, **kwargs):
        res = pq(response.text)
        meta = response.meta
        bid_city = meta.get("bid_city")
        category = res('div[class="f_left mt5"] span a').eq(1).text()
        bid_info_type = res('div[class="f_left mt5"] span a').eq(2).text()
        bid_id = re.findall("bulletinId=(.*?)&", str(response.url), re.S)[0]
        title = res('div[id="bulletinName"]').text()
        bid_public_time = res('span[id="bulletinCreateTime"]').text()
        data = res('div[class="tab-content-ds"]')
        # for each in data.items():
        item = BidScrapyProjectItem()
        item["bid_id"] = get_md5(bid_id)
        item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        item["bid_url"] = response.url
        item["bid_md5_url"] = ""
        item["bid_province"] = "广东省"
        item["bid_city"] = bid_city
        item["bid_county"] = ""
        item["bid_category"] = category
        item["bid_info_type"] = bid_info_type
        item["bid_source"] = ""
        item["bid_name"] = title
        item["bid_public_time"] = bid_public_time
        item["bid_html_con"] = res.html().replace("'", '"')
        item["bid_content"] = res.text().replace("'", '"')
        item["description"] = ""
        item["website_name"] = "广东公共资源交易平台"
        item["website_url"] = "https://pzxx.ggzyjy.gansu.gov.cn/"
        yield item
