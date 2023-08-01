#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/7/18 16:02
@Author : zhangpf
@File : j1angx1.py
@Desc : 江西省招标投标网
@Software: PyCharm
"""
import time

import scrapy
from pyquery import PyQuery as pq

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem


class j1angx1Spider(scrapy.Spider):
    name = "j1angx1"
    source_url = "http://www.jxtb.org.cn/"
    list_url = [
        "http://www.jxtb.org.cn/gongshigg/zhaobiaogg/?p-1.html",
        "http://www.jxtb.org.cn/gongshigg/zhongbiaogongshi/?p-1.html",
    ]
    # list_url = ["http://www.jxtb.org.cn/gongshigg/zhaobiaogg/?p-1.html"]

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "If-Modified-Since": "Tue, 18 Jul 2023 09:07:06 GMT",
        "Referer": "http://www.jxtb.org.cn/gongshigg/zhaobiaogg/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
    }

    def start_requests(self):
        for url in self.list_url:
            yield scrapy.Request(
                url=url, headers=self.headers, callback=self.get_totals, dont_filter=True, cb_kwargs={"url": url}
            )

    def get_totals(self, response, url):
        res = pq(response.text)
        totals = res('div[id="pages"] b').text().split("/")[1]
        # for i in range(1, int(totals + 1)):
        for i in range(1, 2):
            if url == "http://www.jxtb.org.cn/gongshigg/zhaobiaogg/?p-1.html":
                yield scrapy.Request(
                    url=f"http://www.jxtb.org.cn/gongshigg/zhaobiaogg/?p-{i}.html",
                    headers=self.headers,
                    callback=self.get_list_page,
                    dont_filter=True,
                )
            else:
                yield scrapy.Request(
                    url=f"http://www.jxtb.org.cn/gongshigg/zhongbiaogongshi/?p-{i}.html",
                    headers=self.headers,
                    callback=self.get_list_page,
                    dont_filter=True,
                )

    def get_list_page(self, response):
        res = pq(response.text)
        url_list = res('div[class="newlist"] ul li a').items()
        for url in url_list:
            detail_url = url.attr("href")
            detail_url1 = self.source_url + detail_url
            yield scrapy.Request(
                url=detail_url1,
                headers=self.headers,
                callback=self.detail_page,
                cb_kwargs={"detail_url": detail_url},
            )

    def detail_page(self, response, detail_url):
        res = pq(response.text)
        title = res('div[class="title"]').text()
        bid_public_time = res('div[class="fbsj"] span').eq(0).text().split("：")[-1]
        bid_content = res('div[id="vsb_content_2"]').text()
        bid_html_con = res('div[id="vsb_content_2"]').outer_html()
        bid_category = res('div[class="nycolumn"]').text()
        item = BidScrapyProjectItem()
        item["bid_id"] = get_md5(detail_url)
        item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        item["bid_url"] = response.url
        item["bid_info_type"] = bid_category
        item["bid_province"] = "江西省"
        item["bid_category"] = "公告公示"
        item["bid_name"] = title
        item["bid_public_time"] = bid_public_time
        item["bid_html_con"] = bid_html_con
        item["bid_content"] = bid_content
        item["website_name"] = "江西省招标投标网"
        item["website_url"] = self.source_url
        # item["bid_orgin_url"] = detail_url
        # print(item)
        yield item
