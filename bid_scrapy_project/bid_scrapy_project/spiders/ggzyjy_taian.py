#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time : 28/6/2023 上午11:28
@Author : xushaowei
@File : ggzyjy_taian.py
@Desc :
@Software:PyCharm
"""
import re
import time

# import pandas as pd
import requests
import scrapy

from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem

from bid_scrapy_project.common.common import format_time


class GgzyjyNmgSpider(scrapy.Spider):
    name = "ggzyjy_taian"
    start_urls = "http://www.taggzyjy.com.cn/jydt/002007/notice_construction.html"
    website_name = "泰安市公共资源交易中心"
    website_url = "http://www.taggzyjy.com.cn"

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls, callback=self.parse_list_page, dont_filter=True)

    def parse_list_page(self, response):
        panel_list = response.xpath('//ul[@class="tree-sub"]/li')
        for panel in panel_list:
            one_title = panel.xpath('.//a[@class="wb-tree-tt"]/text()').extract_first()
            nav_links = panel.xpath('.//a[@class="text-overflow"]')
            if "政府采购" in one_title:
                for nav_link in nav_links:
                    for page_i in range(0, 60, 20):
                        two_title = nav_link.xpath("./text()").extract_first()
                        url = nav_link.xpath("./@href").extract_first()
                        post_url = (
                            "http://www.taggzyjy.com.cn/inteligentsearch/rest/esinteligentsearch/getFullTextDataNew"
                        )
                        data_rid = re.findall(".*/(.*?)/notice_.*", url)
                        if data_rid:
                            data_id = data_rid[0]
                        data = (
                            '{"token":"","pn":%s,"rn":15,"sdt":"","edt":"","wd":" ","inc_wd":"","exc_wd":"","fields":"title","cnum":"001","sort":"{\\"webdate\\":0}","ssort":"title","cl":200,"terminal":"","condition":[{"fieldName":"categorynum","equal":"%s","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2}],"time":[{"fieldName":"webdate","startTime":"","endTime":""}],"highlights":"title","statistics":null,"unionCondition":null,"accuracy":"","noParticiple":"0","searchRange":null,"isBusiness":"1"}'
                            % (page_i, data_id)
                        )
                        meta = {"one_title": one_title, "two_title": two_title}
                        headers = {
                            "Host": "www.taggzyjy.com.cn",
                            "Referer": f"http://www.taggzyjy.com.cn{url}",
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
                    for page_i in range(0, 60, 20):
                        two_title = nav_link.xpath("./text()").extract_first()
                        url = nav_link.xpath("./@href").extract_first()
                        post_url = (
                            "http://www.taggzyjy.com.cn/inteligentsearch/rest/esinteligentsearch/getFullTextDataNew"
                        )
                        data_rid = re.findall(".*/(.*?)/notice_.*", url)
                        if data_rid:
                            data_id = data_rid[0]
                        data = (
                            '{"token":"","pn":%s,"rn":15,"sdt":"","edt":"","wd":" ","inc_wd":"","exc_wd":"","fields":"title","cnum":"001","sort":"{\\"webdate\\":0}","ssort":"title","cl":200,"terminal":"","condition":[{"fieldName":"categorynum","equal":"%s","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2}],"time":[{"fieldName":"webdate","startTime":"","endTime":""}],"highlights":"title","statistics":null,"unionCondition":null,"accuracy":"","noParticiple":"0","searchRange":null,"isBusiness":"1"}'
                            % (page_i, data_id)
                        )
                        meta = {"one_title": one_title, "two_title": two_title}
                        headers = {
                            "Host": "www.taggzyjy.com.cn",
                            "Referer": f"http://www.taggzyjy.com.cn{url}",
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
        list_items = list_json_data.get("result").get("records")
        for list_item in list_items:
            areaname = list_item.get("areaname")
            webdate = list_item.get("webdate")
            title = list_item.get("title")
            linkurl = list_item.get("linkurl")
            url = self.website_url + linkurl
            meta = {
                "url": url,
                "title": title,
                "areaname": areaname,
                "webdate": webdate,
                "one_title": response.meta["one_title"],
                "two_title": response.meta["two_title"],
            }
            yield scrapy.Request(url, callback=self.parse_ztb_detail, meta=meta)

    def parse_zfcg_list(self, response):
        list_json_data = response.json()
        list_items = list_json_data.get("result").get("records")
        for list_item in list_items:
            areaname = list_item.get("areaname")
            webdate = list_item.get("webdate")
            title = list_item.get("title")
            linkurl = list_item.get("linkurl")
            url = self.website_url + linkurl
            meta = {
                "url": url,
                "title": title,
                "areaname": areaname,
                "webdate": webdate,
                "one_title": response.meta["one_title"],
                "two_title": response.meta["two_title"],
            }
            yield scrapy.Request(url, callback=self.parse_zfcg_detail, meta=meta)

    def parse_ztb_detail(self, response):
        detail_htlm = response.text
        # detail_text = " ".join(response.xpath("//text()").extract()).strip()
        detail_text = remove_node(detail_htlm, ["script"]).text
        bid_public_time = response.meta["webdate"]
        areaname = response.meta["areaname"]
        fields = areaname.split("·")
        bid_province = fields[0]
        try:
            bid_city = fields[1]
        except:
            bid_city = "泰安市"
        try:
            bid_county = fields[2]
        except:
            bid_county = ""
        po_public_time = format_time(bid_public_time)
        contentUrl = response.meta["url"]
        bid_id = get_md5(contentUrl)
        item = BidScrapyProjectItem()
        item["bid_id"] = bid_id
        item["bid_url"] = contentUrl
        item["bid_province"] = bid_province
        item["bid_city"] = bid_city
        item["bid_county"] = bid_county
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
        detail_htlm = response.text
        # detail_text = " ".join(response.xpath("//text()").extract()).strip()
        detail_text = remove_node(detail_htlm, ["script"]).text
        bid_public_time = response.meta["webdate"]
        areaname = response.meta["areaname"]
        fields = areaname.split("·")
        po_province = fields[0]
        try:
            po_city = fields[1]
        except:
            po_city = "泰安市"
        try:
            po_county = fields[2]
        except:
            po_county = ""
        po_public_time = format_time(bid_public_time)
        contentUrl = response.meta["url"]
        po_id = get_md5(contentUrl)
        item = GovernmentProcurementItem()
        item["po_id"] = po_id
        item["bid_url"] = contentUrl
        item["po_province"] = po_province
        item["po_city"] = po_city
        item["po_county"] = po_county
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

    # def normalize_datetime(self, time_str):
    #     try:
    #         datetime_obj = pd.to_datetime(time_str, format="%Y-%m-%d %H:%M:%S")
    #     except ValueError:
    #         try:
    #             datetime_obj = pd.to_datetime(time_str, format="%Y-%m-%d")
    #         except ValueError:
    #             try:
    #                 datetime_obj = pd.to_datetime(time_str, format="%m/%d/%Y %I:%M %p")
    #             except ValueError:
    #                 return None
    #
    #     normalized_time_str = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    #     return normalized_time_str
