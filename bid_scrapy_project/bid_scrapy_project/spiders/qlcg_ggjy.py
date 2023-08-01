# -*- coding: utf-8 -*-
"""
@desc: 齐鲁采购与招标网
@version: python3
@author: shenr
@time: 2023/06/16
"""
import logging
import re
import time

import scrapy
from pyquery import PyQuery as pq

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class ExampleSpider(scrapy.Spider):
    name = "qlcg_ggjy"
    # allowed_domains = ["http://www.qlebid.com/cms/index.htm"]
    # start_urls = "http://www.qlebid.com/cms/channel/2ywgg1qb/index.htm"
    start_urls = "http://www.qlebid.com/cms/index.htm"
    page = 1
    page_all = 1
    current_time = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
    page_time = ""

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Referer": "http://www.qlebid.com/cms/index.htm",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }
    more_url_list = []
    more1_url_list = []
    more2_url_list = []

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls,
            headers=self.headers,
            callback=self.parse_1,
            dont_filter=True,
        )

    def parse_1(self, response, **kwargs):
        res = pq(response.text)
        # 招标专区
        zb_res = res('div[class="m-hd"]').eq(1)
        # 非招标专区
        fzb_res = res('div[class="m-hd"]').eq(2)
        # 履约专区
        # ly_res = res('div[class="m-hd"]').eq(3)
        page_ = 1
        for each in zb_res("div ul li").items():
            more1_url = "http://www.qlebid.com" + each('div[class="more"] a').attr("href")
            yield scrapy.Request(
                url=more1_url,
                headers=self.headers,
                callback=self.parse_list,
                dont_filter=True,
                meta={"url_gg": more1_url, "page_": page_},
            )
        page_ = 1
        for each in fzb_res("div ul li").items():
            more2_url = "http://www.qlebid.com" + each('div[class="more"] a').attr("href")
            yield scrapy.Request(
                url=more2_url,
                headers=self.headers,
                callback=self.parse_list,
                dont_filter=True,
                meta={"url_gg": more2_url, "page_": page_},
            )

    def parse_list(self, response, **kwargs):
        if int(response.status) == 200:
            meta = response.meta
            url_gg = meta.get("url_gg")
            page_ = meta.get("page_")
            res = pq(response.text)
            list1 = res('ul[id="list1"]')
            logging.debug(f"============当前爬取{url_gg} 的 {page_}页==========")
            for each in list1("li").items():
                detail_url = "http://www.qlebid.com/" + each("a").attr("href")
                title = each("a").attr("title")
                time_ = each("a em").text()
                self.page_time = time_[:10]
                yield scrapy.Request(
                    url=detail_url,
                    headers=self.headers,
                    callback=self.parse_detail,
                    # dont_filter=True,
                    meta={"title": title, "time_": time_, "url_gg": url_gg},
                )
            page_ += 1
            if self.page_time == self.current_time:
            # if page_ < 8:
                yield scrapy.Request(
                    url=f"{url_gg}?pageNo={page_}",
                    headers=self.headers,
                    callback=self.parse_list,
                    # dont_filter=True,
                    meta={"url_gg": url_gg, "page_": page_},
                )
        else:
            logging.debug("===============爬取结束=============")

    def parse_detail(self, response, **kwargs):
        res = pq(response.text)
        meta = response.meta
        url_gg = meta.get("url_gg")
        title = meta.get("title")
        time_ = meta.get("time_").replace("电子全流程", "").replace("[", "").replace("]", "").replace(" ", "")
        id_ = re.findall(".*/(.*?).htm", str(response.url), re.S)[0]
        if res('div[class="loc-link"] a').eq(2).text() == "采购公告":
            item = GovernmentProcurementItem()
            item["po_id"] = get_md5(id_)
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = response.url
            item["po_province"] = "山东省"
            item["po_city"] = ""
            item["po_county"] = ""
            item["po_zone"] = res('div[class="loc-link"] a').eq(1).text()
            item["po_category"] = res('div[class="loc-link"] a').eq(3).text()
            item["po_info_type"] = res('div[class="loc-link"] a').eq(2).text()
            item["po_source"] = ""
            item["bo_name"] = title
            item["po_public_time"] = time_
            item["po_html_con"] = res('div[class="article-content"]').html().replace("'", '"')
            item["po_content"] = res('div[class="article-content"]').text().replace("'", '"')
            item["description"] = ""
            item["website_name"] = "齐鲁采购与招标网"
            item["website_url"] = url_gg
        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = get_md5(id_)
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = response.url
            item["bid_md5_url"] = ""
            item["bid_province"] = "山东省"
            item["bid_city"] = ""
            item["bid_county"] = ""
            item["bid_zone"] = res('div[class="loc-link"] a').eq(1).text()
            item["bid_category"] = res('div[class="loc-link"] a').eq(3).text()
            item["bid_info_type"] = res('div[class="loc-link"] a').eq(2).text()
            item["bid_source"] = ""
            item["bid_name"] = title
            item["bid_public_time"] = time_
            item["bid_html_con"] = res('div[class="article-content"]').html().replace("'", '"')
            item["bid_content"] = res('div[class="article-content"]').text().replace("'", '"')
            item["description"] = ""
            item["website_name"] = "齐鲁采购与招标网"
            item["website_url"] = url_gg
        yield item
