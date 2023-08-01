#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 28/6/2023 下午5:14
@Author : xushaowei
@File : ggzyjy_weihai.py
@Desc :
@Software:PyCharm
"""
import re
import time

import pandas as pd
import requests
import scrapy
from pyquery import PyQuery as pq
from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class GgzyjyNmgSpider(scrapy.Spider):
    name = "ggzyjy_weihai"
    start_urls = "http://ggzyjy.weihai.cn/jyxx/003001/transInfo.html"
    website_name = "威海市公共资源交易网"
    website_url = "http://ggzyjy.weihai.cn"

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls, callback=self.parse_list_page, dont_filter=True)

    def parse_list_page(self, response):
        panel_list = response.xpath('//ul[@id="firstpane"]/li')
        for panel in panel_list:
            re_one_title = panel.xpath(".//h3//text()").extract()
            if re_one_title:
                one_title = re_one_title[1].replace("\r\n", "").replace("\t", "")
            nav_links = panel.xpath(".//a")
            if "政府采购" in one_title:
                for nav_link in nav_links:
                    for page_i in range(0, 3):
                        two_title = nav_link.xpath("./text()").extract_first()
                        url = nav_link.xpath("./@href").extract_first()
                        post_url = (
                            "http://ggzyjy.weihai.cn/EpointWebBuilder/rest/frontAppCustomAction/getPageInfoListNew"
                        )
                        data_rid = re.findall(".*/(.*?)/transInfo", url)
                        if data_rid:
                            data_id = data_rid[0]
                        data = f"params=%7B%22siteGuid%22%3A%227eb5f7f1-9041-43ad-8e13-8fcb82ea831a%22%2C%22categoryNum%22%3A%22{data_id}%22%2C%22kw%22%3A%22%22%2C%22startDate%22%3A%22%22%2C%22endDate%22%3A%22%22%2C%22pageIndex%22%3A{page_i}%2C%22pageSize%22%3A12%2C%22area%22%3A%22%22%7D"
                        meta = {"one_title": one_title, "two_title": two_title}
                        headers = {
                            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                            "Host": "ggzyjy.weihai.cn",
                            "Referer": f"http://ggzyjy.weihai.cn{url}",
                        }
                        yield scrapy.Request(
                            post_url,
                            method="POST",
                            body=data,
                            headers=headers,
                            callback=self.parse_zfcg_list,
                            meta=meta,
                            dont_filter=True,
                        )
            else:
                for nav_link in nav_links:
                    for page_i in range(0, 3):
                        two_title = nav_link.xpath("./text()").extract_first()
                        url = nav_link.xpath("./@href").extract_first()
                        post_url = (
                            "http://ggzyjy.weihai.cn/EpointWebBuilder/rest/frontAppCustomAction/getPageInfoListNew"
                        )
                        data_rid = re.findall(".*/(.*?)/transInfo", url)
                        if data_rid:
                            data_id = data_rid[0]
                        data = f"params=%7B%22siteGuid%22%3A%227eb5f7f1-9041-43ad-8e13-8fcb82ea831a%22%2C%22categoryNum%22%3A%22{data_id}%22%2C%22kw%22%3A%22%22%2C%22startDate%22%3A%22%22%2C%22endDate%22%3A%22%22%2C%22pageIndex%22%3A{page_i}%2C%22pageSize%22%3A12%2C%22area%22%3A%22%22%7D"
                        meta = {"one_title": one_title, "two_title": two_title}
                        headers = {
                            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                            "Host": "ggzyjy.weihai.cn",
                            "Referer": f"http://ggzyjy.weihai.cn{url}",
                        }
                        yield scrapy.Request(
                            post_url,
                            method="POST",
                            body=data,
                            headers=headers,
                            callback=self.parse_ztb_list,
                            meta=meta,
                            dont_filter=True,
                        )

    def parse_ztb_list(self, response):
        list_json_data = response.json()
        list_items = list_json_data.get("custom").get("infodata")
        for list_item in list_items:
            categorynum = list_item.get("categorynum")
            infodate = list_item.get("infodate")
            title = list_item.get("title")
            infourl = list_item.get("infourl")
            url = self.website_url + infourl
            meta = {
                "url": url,
                "title": title,
                "categorynum": categorynum,
                "infodate": infodate,
                "one_title": response.meta["one_title"],
                "two_title": response.meta["two_title"],
            }
            yield scrapy.Request(url, callback=self.parse_ztb_detail, meta=meta)

    def parse_zfcg_list(self, response):
        list_json_data = response.json()
        list_items = list_json_data.get("custom").get("infodata")
        for list_item in list_items:
            categorynum = list_item.get("categorynum")
            infodate = list_item.get("infodate")
            title = list_item.get("title")
            infourl = list_item.get("infourl")
            url = self.website_url + infourl
            meta = {
                "url": url,
                "title": title,
                "categorynum": categorynum,
                "infodate": infodate,
                "one_title": response.meta["one_title"],
                "two_title": response.meta["two_title"],
            }
            yield scrapy.Request(url, callback=self.parse_zfcg_detail, meta=meta)

    def parse_ztb_detail(self, response):
        resp_html = pq(response.text)
        detail_htlm = response.xpath('//div[@class="content"]').get()
        # detail_text = ' '.join(response.xpath('//div[@class="content"]//text()').extract()).strip()
        detail_text = remove_node(resp_html('div[class="content"]').html(), ["script"]).text
        bid_public_time = response.meta["infodate"]
        po_public_time = self.normalize_datetime(bid_public_time)
        contentUrl = response.meta["url"]
        bid_id = get_md5(contentUrl)
        item = BidScrapyProjectItem()
        item["bid_id"] = bid_id
        item["bid_url"] = contentUrl
        item["bid_province"] = "山东省"
        item["bid_city"] = "威海市"
        item["bid_category"] = response.meta["one_title"]
        item["bid_info_type"] = response.meta["two_title"]
        item["bid_name"] = response.meta["title"]
        item["bid_public_time"] = po_public_time
        item["bid_html_con"] = detail_htlm
        item["bid_content"] = detail_text
        item["website_name"] = self.website_name
        item["website_url"] = self.website_url
        item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        yield item

    def parse_zfcg_detail(self, response):
        resp_html = pq(response.text)
        detail_htlm = response.xpath('//div[@class="content"]').get()
        # detail_text = " ".join(response.xpath('//div[@class="content"]//text()').extract()).strip()
        detail_text = remove_node(resp_html('div[class="content"]').html(), ["script"]).text
        bid_public_time = response.meta["infodate"]
        po_public_time = self.normalize_datetime(bid_public_time)
        contentUrl = response.meta["url"]
        po_id = get_md5(contentUrl)
        item = GovernmentProcurementItem()
        item["po_id"] = po_id
        item["bid_url"] = contentUrl
        item["po_province"] = "山东省"
        item["po_city"] = "威海市"
        item["po_category"] = response.meta["one_title"]
        item["po_info_type"] = response.meta["two_title"]
        item["po_public_time"] = po_public_time
        item["bo_name"] = response.meta["title"]
        item["po_html_con"] = detail_htlm
        item["po_content"] = detail_text
        item["website_name"] = self.website_name
        item["website_url"] = self.website_url
        item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        yield item

    def normalize_datetime(self, time_str):
        try:
            datetime_obj = pd.to_datetime(time_str, format="%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                datetime_obj = pd.to_datetime(time_str, format="%Y-%m-%d")
            except ValueError:
                try:
                    datetime_obj = pd.to_datetime(time_str, format="%m/%d/%Y %I:%M %p")
                except ValueError:
                    return None

        normalized_time_str = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
        return normalized_time_str
