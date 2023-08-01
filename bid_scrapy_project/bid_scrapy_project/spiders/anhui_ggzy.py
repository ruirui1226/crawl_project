#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/6/20 10:52
@Author : zhangpf
@File : anhui_ggzy.py
@Desc : 安徽省
@Software: PyCharm
"""
import json
import math
import re
import time
from datetime import datetime

from pyquery import PyQuery as pq
import scrapy
from loguru import logger

from bid_scrapy_project.common.common import urljoin_url, get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class anhuiSpider(scrapy.Spider):
    name = "anhui_spider"
    source_url = "https://ggzy.ah.gov.cn"

    start_urls = "https://ggzy.ah.gov.cn/{}/list"

    details_url = "https://ggzy.ah.gov.cn/{}/newDetailSub"

    # classify = ["jsgc","zfcg","cqjy","qtjy"]
    classify = ["jsgc","zfcg"]
    # classify = ["jsgc"]


    data = {
        "currentPage": "",
        "tenderProjectType": "",
        "bulletinNature": "1",
        "jyptId": "",
        "region": "",
    }
    detail_data = {
        "type": "",
        "bulletinNature": "1",
        "guid": "",
        "statusGuid": "",
    }

    def start_requests(self):
        for i in self.classify:
            if i == "jsgc":
                yield scrapy.Request(
                    url=self.start_urls.format(i),
                    callback=self.get_list_jsgc,
                    dont_filter=True,
                    cb_kwargs={"logotype":i}
                )
            else:
                yield scrapy.Request(
                    url=self.start_urls.format(i),
                    callback=self.get_list_other,
                    dont_filter=True,
                    cb_kwargs={"logotype": i}
                )

    def get_list_jsgc(self, response, logotype):
        res = pq(response.text)
        url_list = res('ul[class="tran-info-list-list"] a').items()
        for url in url_list:
            url = self.source_url + url.attr("href")
            url_id = url.split("=")[-1]
            yield scrapy.Request(
                url=url, callback=self.get_list_page_jsgc, dont_filter=True, cb_kwargs={"url_id": url_id,"logotype":logotype}
            )

    def get_list_page_jsgc(self, response, **kwargs):
        res = response.text
        page_number = re.findall('return false;">(.*?)</a>', str(res), re.S)[4]
        # print(page_number)
        for i in range(1, 8):
            self.data["currentPage"] = str(i)
            self.data["tenderProjectType"] = kwargs["url_id"]
            # print(self.data)
            yield scrapy.FormRequest(
                url=self.start_urls.format(kwargs["logotype"]),
                callback=self.detail_page,
                dont_filter=True,
                formdata=self.data,
                method="POST",
                cb_kwargs={"logotype":kwargs["logotype"]}
            )

    def get_list_other(self, response,logotype):
        res = response.text
        page_number = re.findall('return false;">(.*?)</a>', str(res), re.S)[4]
        # print(page_number)
        for i in range(1, 8):
            self.data["currentPage"] = str(i)
            yield scrapy.FormRequest(
                url=self.start_urls.format(logotype),
                callback=self.detail_page,
                dont_filter=True,
                formdata=self.data,
                method="POST",
                cb_kwargs={"logotype":logotype}
            )

    def detail_page(self, response, logotype):
        res = pq(response.text)
        url_list = res('div[class="list clear"] li a').items()
        for detail_url in url_list:
            url = self.source_url + detail_url.attr("href")
            id = detail_url.attr("href").split("&")[0].split("=")[-1]
            self.detail_data["guid"] = id
            if logotype == "zfcg":
                self.detail_data["type"] = "bulletin"
            elif logotype == "jsgc":
                self.detail_data["type"] = "tender"
            yield scrapy.FormRequest(
                url=self.details_url.format(logotype),
                callback=self.get_detail_page,
                formdata=self.detail_data,
                method="POST",
                cb_kwargs={"url": url, "id": id, "logotype":logotype},
            )
            # if self.logotype == "zfcg" or self.logotype == "jsgc":
            #     yield scrapy.FormRequest(
            #         url=self.details_url.format(self.logotype),
            #         callback=self.get_detail_page,
            #         formdata=self.detail_data,
            #         method="POST",
            #         cb_kwargs={"url": url, "id": id},
            #     )
            # else:
            #     yield scrapy.Request(
            #         url=url,
            #         callback=self.get_detail_page1,
            #         cb_kwargs={"url": url, "id": id},
            #     )

    def get_detail_page(self, response, **kwargs):
        res = pq(response.text)
        if res('p[class="article-title clamp-3 m-b-15"]').text() is None:
            bid_name = res('p[class="article-title clamp-1 m-b-15"]').text()
        else:
            bid_name = res('p[class="article-title clamp-3 m-b-15"]').text()
        source_url = res('div[class="article-mid-title m-b-40"] a').attr("href")
        try:
            bid_public_time = res('div[class="m-l-5 m-r-5"] span').text()
            tim = bid_public_time.split("\r")[0].replace(" ", "")
            dt_time = str(datetime.strptime(tim, "%Y%m%d"))
        except:
            bid_public_time = res('div[class="m-l-5 m-r-5"] span').text()
            dt_time = str(datetime.strptime(bid_public_time, "%Y-%m-%d"))
        bid_category = res('div[class="ewb-route"] a').eq(2).text()
        bid_info_type = res('span[id="viewGuid"]').text()
        bid_content = res('div[class="article-text-box m-b-50 m-t-50"]').text()
        bid_html_con = res('div[class="article-text-box m-b-50 m-t-50"]').outer_html()
        if kwargs["logotype"] == "zfcg":
            item = GovernmentProcurementItem()
            item["po_id"] = get_md5(kwargs["id"])
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = kwargs["url"]
            item["po_source"] = source_url
            item["po_province"] = "安徽省"
            item["po_category"] = "政府采购"
            item["po_info_type"] = bid_info_type
            item["bo_name"] = bid_name
            item["po_public_time"] = dt_time
            item["po_html_con"] = bid_html_con
            item["po_content"] = bid_content
            item["website_name"] = "全国公共资源交易平台(安徽省) 安徽省公共资源交易监管网"
            item["website_url"] = self.source_url
            item["bid_orgin_url"] = self.details_url.format(kwargs["logotype"])
            # print(item)

            yield item
        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = get_md5(kwargs["id"])
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = kwargs["url"]
            item["bid_source"] = source_url
            item["bid_province"] = "安徽省"
            item["bid_category"] = bid_category
            item["bid_info_type"] = bid_info_type
            item["bid_name"] = bid_name
            item["bid_public_time"] = dt_time
            item["bid_html_con"] = bid_html_con
            item["bid_content"] = bid_content
            item["website_name"] = "全国公共资源交易平台(安徽省) 安徽省公共资源交易监管网"
            item["website_url"] = self.source_url
            item["bid_orgin_url"] = self.details_url.format(kwargs["logotype"])
            # print(item)
            yield item

    # def get_detail_page1(self, response, **kwargs):
    #     res = pq(response.text)
    #     bid_name = res('p[class="article-title clamp-1 m-b-15"]').text()
    #     source_url = res('div[class="article-mid-title m-b-40"] a').attr("href")
    #     bid_public_time = res('div[class="m-l-5 m-r-5"] span').text()
    #     dt_time = str(datetime.strptime(bid_public_time, "%Y-%m-%d"))
    #     bid_category = res('div[class="bread-crumb"] a').eq(3).text()
    #     bid_content = res('div[class="contentDiv tran-info-detail-content-article"]').text()
    #     bid_html_con = res('div[class="contentDiv tran-info-detail-content-article"]').outer_html()
    #     item = BidScrapyProjectItem()
    #     item["bid_id"] = get_md5(kwargs["id"])
    #     item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
    #     item["bid_url"] = kwargs["url"]
    #     item["bid_source"] = source_url
    #     item["bid_province"] = "安徽省"
    #     item["bid_category"] = bid_category
    #     item["bid_info_type"] = ""
    #     item["bid_name"] = bid_name
    #     item["bid_public_time"] = dt_time
    #     item["bid_html_con"] = bid_html_con
    #     item["bid_content"] = bid_content
    #     item["website_name"] = "全国公共资源交易平台(安徽省) 安徽省公共资源交易监管网"
    #     item["website_url"] = self.source_url
    #     item["bid_orgin_url"] = self.details_url.format(self.logotype)
    #     yield item
    #     # print(item)
