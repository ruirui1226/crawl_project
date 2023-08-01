7  #!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/7/13 16:54
@Author : zhangpf
@File : zhaojicheng.py
@Desc : 招冀成
@Software: PyCharm
"""
import json
import math

import time

import scrapy
from pyquery import PyQuery as pq

from bid_scrapy_project.common.common import urljoin_url, get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class zhaojichengSpider(scrapy.Spider):
    name = "zhaojicheng"
    source_url = "http://www.hebeibidding.com"
    list_url = "http://www.hebeibidding.com/EpointWebBuilder/rest/GgSearchAction/getInfoMationList"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "userGuid=169054095; oauthClientId=hbej; oauthPath=http://127.0.0.1:8080/EpointWebBuilder; oauthLoginUrl=http://192.168.164.241:96/membercenter/login.html?redirect_uri=; oauthLogoutUrl=; noOauthRefreshToken=266ba0f34a94fb92dce2a12f7c9e5efb; noOauthAccessToken=f9d083f21bb426e1b502bc58e6923128",
        "Origin": "http://www.hebeibidding.com",
        "Referer": "http://www.hebeibidding.com/xmxx/project_info.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    data = {
        "siteGuid": "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a",
        "categoryNum": "0070",
        "xiaqucode": "",
        "pageIndex": "0",
        "pageSize": "12",
        "wd": "",
    }
    custom_settings = {"CONCURRENT_REQUESTS": 1, "DOWNLOAD_DELAY": 1}

    def start_requests(self):
        yield scrapy.FormRequest(
            url=self.list_url,
            headers=self.headers,
            callback=self.get_totals,
            formdata=self.data,
            dont_filter=True,
            method="POST",
        )

    def get_totals(self, response):
        response = json.loads(response.text)
        AllCount = response.get("AllCount")
        totals = math.ceil(int(AllCount) / 12)
        for i in range(0, 5):
            data = {
                "siteGuid": "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a",
                "categoryNum": "0070",
                "xiaqucode": "",
                "pageIndex": str(i),
                "pageSize": "12",
                "wd": "",
            }
            yield scrapy.FormRequest(
                url=self.list_url,
                headers=self.headers,
                callback=self.get_list_page,
                formdata=data,
                dont_filter=True,
                method="POST",
            )

    def get_list_page(self, response):
        # print(response.text)
        response = json.loads(response.text)
        customs = response.get("custom")
        for custom in customs:
            infourl = custom.get("infourl")
            detail_url = self.source_url + infourl

            yield scrapy.Request(
                url=detail_url,
                callback=self.detail_page,
                headers=self.headers,
                cb_kwargs={"detail_url": detail_url, "url": infourl},
            )

    def detail_page(self, response, **kwargs):
        res = pq(response.text)
        id = kwargs["url"].split("/")[-1].split(".")[0]
        bo_name = res('div[class="box"] h3').text()
        bid_public_time = res('div[class="source"] span').text().split("：")[1].split(" ")[0]
        po_category = res('ul[class="route-list l"] li').eq(2).text()
        po_info_type = res('ul[class="route-list l"] li').eq(3).text()
        bid_content = res('div[class="paragraph-box"]').text()
        po_html_con = res('div[class="paragraph-box"]').outer_html()
        if po_category == "政府采购":
            item = GovernmentProcurementItem()
            item["po_id"] = get_md5(id)
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = kwargs["detail_url"]
            item["po_province"] = "河北省"
            item["po_category"] = po_category
            item["po_info_type"] = po_info_type
            item["bo_name"] = bo_name
            item["po_public_time"] = bid_public_time
            item["po_html_con"] = po_html_con
            item["po_content"] = bid_content
            item["website_name"] = "招冀成"
            item["website_url"] = self.source_url
            item["bid_orgin_url"] = kwargs["detail_url"]
            # print(item)
            yield item
        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = get_md5(id)
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = kwargs["detail_url"]
            item["bid_province"] = "河北省"

            # item["po_province"] = po_province
            # item["po_city"] = po_city
            # item["po_zone"] = po_zone
            item["bid_category"] = po_category
            item["bid_info_type"] = po_info_type
            item["bid_name"] = bo_name
            item["bid_public_time"] = bid_public_time
            item["bid_html_con"] = po_html_con
            item["bid_content"] = bid_content
            item["website_name"] = "招冀成"
            item["website_url"] = self.source_url
            item["bid_orgin_url"] = kwargs["detail_url"]
            # print(item)
            yield item
