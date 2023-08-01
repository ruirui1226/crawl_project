#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/6/30 15:37
@Author : zhangpf
@File : weifang_ggzy.py
@Desc : 潍坊
@Software: PyCharm
"""

import re
import time
from datetime import datetime

from pyquery import PyQuery as pq
import scrapy
# from loguru import logger

from bid_scrapy_project.common.common import urljoin_url, get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class weifangSpider(scrapy.Spider):
    name = "weifang"
    source_url = "http://ggzy.weifang.gov.cn"
    start_urls = "http://ggzy.weifang.gov.cn/wfggzy/xmxx/"

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls,
            callback=self.parse_list,
            dont_filter=True,
        )

    def parse_list(self, response):
        res = pq(response.text)
        for url in res('div[class="column-bd"] li a').items():
            url = url.attr("href")
            yield scrapy.Request(
                url=self.source_url + url,
                callback=self.parse_list1,
                dont_filter=True,
            )

    def parse_list1(self, response):
        res = pq(response.text)
        for url in res('div[class="s-block"] h4 a').items():
            url = url.attr("href")
            categorynum = str(url).split("/")[-1]
            yield scrapy.Request(
                url=f"http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_jh.aspx?address=&type=&categorynum={categorynum}",
                callback=self.parse_list2,
                dont_filter=True,
                cb_kwargs={"categorynum": categorynum},
            )

    def parse_list2(self, response, categorynum):
        res = pq(response.text)
        total = res('td[class="huifont"]').text().split("/")[-1]
        # print(total)
        for i in range(1, 2):
            yield scrapy.Request(
                url=f"http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_jh.aspx?address=&type=&categorynum={categorynum}&Paging={i}",
                callback=self.detail_list,
                dont_filter=True,
            )

    def detail_list(self, response):
        res = pq(response.text)
        for details_url in res('span[class="info-name"] a').items():
            detail_url = details_url.attr("href")
            # print("http://ggzy.weifang.gov.cn" + detail_url)
            yield scrapy.Request(
                url="http://ggzy.weifang.gov.cn" + detail_url,
                callback=self.parse_page,
                cb_kwargs={"detail_url": detail_url},
            )

    def parse_page(self, response, detail_url):
        # logger.warning("当前url={}".format("http://ggzy.weifang.gov.cn" + detail_url))
        res = pq(response.text)
        bid_name = res('h3[class="bigtitle"]').text()
        bid_html_con = str(res('div[class="substance"]').outer_html()).replace("'", '"')
        pre = re.compile(">(.*?)<")
        bid_content = "".join(pre.findall(str(bid_html_con)))
        bid_county = res('div[class="location"] span').text()
        # bid_source = res('p[class="sub-cp"]').text()
        bid_category = res('div[class="location"] a').eq(2).text()
        # print(bid_category)
        bid_info_type = res('div[class="location"] a').eq(3).text()
        try:
            information_time = str(res('p[class="sub-cp"]').text()).split("：")[2].split(" ")[0]
            dt_time = str(datetime.strptime(information_time, "%Y/%m/%d"))
        except:
            information_time = res('p[class="sub-cp"]').text().split("信息时间：")[1].split()[0]
            dt_time = str(datetime.strptime(information_time, "%Y/%m/%d"))
        if bid_category == "政府采购":
            item = GovernmentProcurementItem()
            item["po_id"] = get_md5(str(detail_url).split("/")[-1].split(".")[0])
            item["po_province"] = "山东省"
            item["po_city"] = "潍坊市"
            item["bid_url"] = "http://ggzy.weifang.gov.cn" + detail_url
            item["po_category"] = bid_category
            item["po_info_type"] = bid_info_type
            item["po_source"] = ""
            item["po_html_con"] = bid_html_con
            item["po_content"] = bid_content
            item["bo_name"] = bid_name
            item["po_public_time"] = dt_time
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["website_name"] = "潍坊市公共资源交易中心"
            item["website_url"] = self.source_url
            # print(item)
            yield item
        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = get_md5(str(detail_url).split("/")[-1].split(".")[0])
            item["bid_province"] = "山东省"
            item["bid_city"] = "潍坊市"
            item["bid_county"] = bid_county
            item["bid_url"] = "http://ggzy.weifang.gov.cn" + detail_url
            item["bid_category"] = bid_category
            item["bid_info_type"] = bid_info_type
            item["bid_source"] = ""
            item["bid_html_con"] = bid_html_con
            item["bid_content"] = bid_content
            item["bid_name"] = bid_name
            item["bid_public_time"] = dt_time
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["website_name"] = "潍坊市公共资源交易中心"
            item["website_url"] = self.source_url
            # print(item)
            yield item
