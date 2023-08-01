# -*- coding: utf-8 -*-
"""
@desc: 烟台公共交易资源网
@version: python3
@author: shenr
@time: 2023/07/04
"""
import base64
import json
import re
import time
import urllib
from datetime import datetime

import requests
import scrapy
from urllib.parse import quote
from pyquery import PyQuery as pq

from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import GovernmentProcurementItem, BidScrapyProjectItem


class ExampleSpider(scrapy.Spider):
    name = "yantai_ggjy"
    start_urls = "http://ggzyjy.yantai.gov.cn/{}/index_1.jhtml"
    page = 1
    page_all = 1
    page_time = ""
    current_time = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Referer": "http://ggzyjy.yantai.gov.cn/jyxxgc/index.jhtml",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }
    cookies = {
        "_gscu_31623267": "861010745g3vav21",
        "clientlanguage": "zh_CN",
        "_gscbrs_31623267": "1",
        "_gscs_31623267": "86279097icb2x521|pv:17",
    }
    city_data = ["jyxxgc", "jyxxzc", "jyxxgt", "jyxxcq"]

    def start_requests(self):
        for city_ in self.city_data:
            yield scrapy.Request(
                url=self.start_urls.format(city_),
                headers=self.headers,
                cookies=self.cookies,
                meta={"city_": city_},
                dont_filter=True,
                callback=self.parse_1,
            )

    def parse_1(self, response, **kwargs):
        res_t = pq(response.text)
        meta = response.meta
        city_ = meta.get("city_")
        results = res_t('ul[class="article-list2"]')
        for each in results('li[class="jygk-li"]').items():
            po_county = each("div span").eq(0).text().replace("[", "").replace("]", "").replace(" ", "")
            detail_url = each("div a").attr("href")
            title = each("div a").attr("title")
            po_public_time_ = each('div[class="list-times"]').text() or each('p[class="bmZhong"]').text().replace("-", ".")
            po_public_time_ = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(po_public_time_[:10], "%Y.%m.%d"))
            self.current_time = po_public_time_ or self.page_time
            bid_id = re.findall(".*/(.*?).jhtml", str(detail_url), re.S)[0]
            yield scrapy.Request(
                url=detail_url,
                callback=self.detail_parse,
                meta={
                    "bid_id": bid_id,
                    "po_county": po_county,
                    "title": title,
                    "meta": meta,
                    "po_public_time": po_public_time_,
                },
            )
        if self.page_time == self.current_time:
            self.page += 1
            yield scrapy.Request(
                url=f"http://ggzyjy.yantai.gov.cn/{city_}/index_{self.page}.jhtml",
                headers=self.headers,
                cookies=self.cookies,
                meta={"city_": city_},
                dont_filter=True,
                callback=self.parse_1,
            )

    def detail_parse(self, response, **kwargs):
        res_t = pq(response.text)
        meta = response.meta
        bid_source = res_t('div[class="content-title2"] span').eq(2).text()
        # 层级
        bid_category = res_t('div[class="sitemap"] a').eq(2).text()
        bid_info_type = res_t('div[class="sitemap"] a').eq(3).text()
        # 详情
        content = res_t('div[class="content-warp"]').text()
        html_content = res_t('div[class="content-warp"]').outerHtml()
        if bid_category == "政府采购":
            item = GovernmentProcurementItem()
            item["po_id"] = get_md5(meta.get("bid_id"))
            item["po_province"] = "山东省"
            item["po_city"] = "烟台市"
            item["po_county"] = meta.get("po_county")
            item["bid_url"] = response.url
            item["po_category"] = bid_category
            item["po_info_type"] = bid_info_type
            item["po_source"] = bid_source
            item["po_html_con"] = str(html_content).replace("'", '"')
            item["po_content"] = remove_node(html_content, ["script"]).text
            item["bo_name"] = meta.get("title")
            item["po_public_time"] = meta.get("po_public_time")
            item["website_name"] = "烟台市公共交易资源网"
            item["website_url"] = "http://ggzyjy.yantai.gov.cn/jyxxgc/index_1.jhtml"
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            yield item
        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = get_md5(meta.get("bid_id"))
            item["bid_md5_url"] = ""
            item["bid_province"] = "山东省"
            item["bid_city"] = "烟台市"
            item["bid_county"] = meta.get("po_county")
            item["bid_url"] = response.url
            item["bid_category"] = bid_category
            item["bid_info_type"] = bid_info_type
            item["bid_source"] = bid_source
            item["bid_html_con"] = str(html_content).replace("'", '"')
            item["bid_content"] = remove_node(html_content, ["script"]).text
            item["bid_name"] = meta.get("title")
            item["bid_public_time"] = meta.get("po_public_time")
            item["website_name"] = "烟台市公共交易资源网"
            item["website_url"] = "http://ggzyjy.yantai.gov.cn/jyxxgc/index_1.jhtml"
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            yield item
