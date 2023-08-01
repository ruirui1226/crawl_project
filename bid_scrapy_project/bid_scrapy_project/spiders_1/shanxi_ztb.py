#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/7/19 17:26
@Author : zhangpf
@File : shanxi_ztb.py
@Desc : 山西省招标投标公共服务平台
@Software: PyCharm
"""
import json
import math
import re
from pyquery import PyQuery as pq
import time

import scrapy

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem


class shanxi_ztbSpider(scrapy.Spider):
    name = "shanxi_ztb"
    source_url = "https://www.sxbid.com.cn"

    url_list = [
        "https://www.sxbid.com.cn/f/new/notice/list/10",
        "https://www.sxbid.com.cn/f/new/notice/list/11",
        "https://www.sxbid.com.cn/f/new/notice/list/12",
        "https://www.sxbid.com.cn/f/new/notice/list/13",
        "https://www.sxbid.com.cn/f/new/notice/list/14",
        "https://www.sxbid.com.cn/f/new/notice/list/15",
        "https://www.sxbid.com.cn/f/new/notice/list/16",
    ]

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": "JSESSIONID=2A448A3D0CA0B8F8DCC6A4708F23506B; psp.session.id=f5183358eae84387bfdf8a18f40838d4",
        "Origin": "https://www.sxbid.com.cn",
        "Referer": "https://www.sxbid.com.cn/f/new/notice/list/16",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
        "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    data = {
        "pageNo": "1",
        "pageSize": "",
        "title": "",
        "recentType": "1",
    }

    def start_requests(self):
        for url in self.url_list:
            yield scrapy.FormRequest(
                url=url,
                headers=self.headers,
                formdata=self.data,
                callback=self.get_totals,
                dont_filter=True,
                cb_kwargs={"url": url},
            )

    def get_totals(self, response, url):
        res = pq(response.text)
        urls_list = res('div[class="list_pages"] form span').text().split(" ")[0]
        pages = re.sub("[\u4e00-\u9fa5]", "", urls_list)
        for i in range(1, int(pages) + 1):
            data = {
                "pageNo": str(i),
                "pageSize": "15",
                "title": "",
                "recentType": "1",
            }
            yield scrapy.FormRequest(
                url=url,
                headers=self.headers,
                formdata=data,
                callback=self.get_list_page,
                dont_filter=True,
            )

    def get_list_page(self, response):
        res = pq(response.text)
        urls_list = res('table[class="content_table"] tbody tr td').items()
        po_info_type = res('div[class="bid_title nav_leftTitle pull_left"]').text()
        for urls in urls_list:
            href = urls("a").attr("href")
            city = urls("span").text().replace("[", "").replace("]", "")
            detail_url = self.source_url + str(href)
            yield scrapy.Request(
                url=detail_url,
                callback=self.detail_page,
                headers=self.headers,
                cb_kwargs={"detail_url": detail_url, "city": city, "po_info_type": po_info_type},
            )

    def detail_page(self, response, **kwargs):
        res = pq(response.text)
        title = res('div[class="page_name"]').text()
        bid_public_time = res('div[class="page_msg"] span').eq(0).text().split("：")[1]
        bid_content = res('div[class="page_panel noticeInfoDiv"]').text()
        bid_html_con = res('div[class="page_panel noticeInfoDiv"]').outer_html()
        item = BidScrapyProjectItem()
        item["bid_id"] = get_md5(kwargs["detail_url"])
        item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        item["bid_url"] = kwargs["detail_url"]
        item["bid_province"] = "山西省"
        item["bid_city"] = kwargs["city"]
        item["bid_category"] = "招标信息"
        item["bid_info_type"] = kwargs["po_info_type"]
        item["bid_name"] = title
        item["bid_public_time"] = bid_public_time
        item["bid_html_con"] = bid_html_con
        item["bid_content"] = bid_content
        item["website_name"] = "山西省招标投标公共服务平台"
        item["website_url"] = self.source_url
        item["bid_orgin_url"] = kwargs["detail_url"]
        # print(item)
        yield item
