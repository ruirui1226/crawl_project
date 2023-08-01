#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/7/12 15:11
@Author : zhangpf
@File : jizhaobiao.py
@Desc : 冀招标
@Software: PyCharm
"""
import time

import scrapy
from pyquery import PyQuery as pq

from bid_scrapy_project.common.common import urljoin_url, get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class jizhaobiaoSpider(scrapy.Spider):
    name = "jizhaobiao"
    source_url = "https://www.jizhaobiao.com"
    list_url = "https://www.jizhaobiao.com/HB/TradeCenter/colTableInfo.do"
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'JSESSIONID=EB2E4DCED1A339290FAFF91E114E9D4A',
        'Origin': 'https://www.jizhaobiao.com',
        'Referer': 'https://www.jizhaobiao.com/HB/TradeCenter/index.do',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    url_code_list = [
        "1",
        "WEB_JY_NOTICE",
        "2",
        "PUBLICITY",
        "RESULT_NOTICE",
        "ZBJH",
    ]
    custom_settings = {"CONCURRENT_REQUESTS": 1}
    def start_requests(self):
        for code in self.url_code_list:
            data = {
                'projectName': '',
                'date': '',
                'begin_time': '',
                'end_time': '',
                'date2': '',
                'projectType': 'gcjs',
                'dealType': '',
                'noticType': code,
                'area': '',
                'dataSource': '',
                'huanJie': 'NOTICE',
                'pageIndex': '1',
            }
            # time.sleep(3)
            yield scrapy.FormRequest(
                url=self.list_url,
                headers=self.headers,
                callback=self.get_totals,
                dont_filter=True,
                formdata=data,
                cb_kwargs={"code": code},
                method="POST"
            )

    def get_totals(self, response, code):
        res = pq(response.text)
        total = res('input[id="Page_TotalPage"]').attr("value")
        # totals = math.ceil(int(total) / 10)
        for i in range(1, 2):
            data = {
                'projectName': '',
                'date': '',
                'begin_time': '',
                'end_time': '',
                'date2': '',
                'projectType': 'gcjs',
                'dealType': '',
                'noticType': code,
                'area': '',
                'dataSource': '',
                'huanJie': 'NOTICE',
                'pageIndex': str(i),
            }
            time.sleep(3)
            yield scrapy.FormRequest(
                url=self.list_url,
                headers=self.headers,
                callback=self.get_list_page,
                dont_filter=True,
                formdata=data,
                cb_kwargs={"code": code},
                method="POST"
            )

    def get_list_page(self, response, code):
        res = pq(response.text)
        for label in res('dl dt a').items():
            href = label.attr("href")
            url = self.source_url + href
            time.sleep(1)
            yield scrapy.Request(
                url=url,
                callback=self.detail_page,
                cb_kwargs={"detail_url": url, "code": code},
            )

    def detail_page(self, response, **kwargs):
        res = pq(response.text)
        id = kwargs["detail_url"].split("=")[1].split("&")[0]
        bid_public_time = res('div[class="btime"]').text().split("：")[-1]
        bo_name = res('div[class="notice_title"]').text()
        Urban = res('input[id="REGION_CODE"]').attr("value").split("-")
        po_province = Urban[0]
        po_city = Urban[1]
        po_zone = Urban[2]
        po_category = res('div[class="cs-mianbaoxie"] span a').eq(2).text()
        po_info_type = res('div[class="cs-mianbaoxie"] span a').eq(3).text()
        bid_content = res('div[class="notice_content"]').text()
        po_html_con = res('div[class="notice_content"]').outer_html()
        item = BidScrapyProjectItem()
        item["bid_id"] = get_md5(id)
        item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        item["bid_url"] = kwargs["detail_url"]
        item["bid_province"] = po_province
        item["bid_city"] = po_city
        item["bid_zone"] = po_zone
        item["bid_category"] = po_category
        item["bid_info_type"] = po_info_type
        item["bid_name"] = bo_name
        item["bid_public_time"] = bid_public_time
        item["bid_html_con"] = po_html_con
        item["bid_content"] = bid_content
        item["website_name"] = "冀招标全流程电子交易平台"
        item["website_url"] = self.source_url
        item["bid_orgin_url"] = kwargs["detail_url"]
        # print(item)
        yield item
