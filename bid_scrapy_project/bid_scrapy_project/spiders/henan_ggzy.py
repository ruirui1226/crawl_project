#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/6/14 13:36
@Author : zhangpf
@File : henan_ggzy.py
@Desc : 河南省
@Software: PyCharm
"""
import json
import math
import re
import time

from pyquery import PyQuery as pq
import scrapy

from bid_scrapy_project.common.common import urljoin_url, get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class henanSpider(scrapy.Spider):
    name = "henan_spider"
    start_urls = "http://www.hnggzy.com/EpointWebBuilder/rest/frontAppCustomAction/getPageInfoListNewYzm"

    data = {
        "siteGuid": "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a",
        "categoryNum": "",
        "kw": "",
        "startDate": "",
        "endDate": "",
        "pageIndex": "0",
        "pageSize": "8",
        "jytype": "",
        "xiaqucode": "4100",
    }

    def start_requests(self):
        for i in range(1, 6):
            self.data["categoryNum"] = "00200" + str(i)
            yield scrapy.FormRequest(
                url=self.start_urls,
                callback=self.parse_list,
                dont_filter=True,
                formdata=self.data,
            )

    def parse_list(self, response):
        count = math.ceil(int(json.loads(response.text).get("custom").get("count") / 8))
        # logger.info(f"共{count}页")
        # for i in range(0, count + 1):
        for i in range(0, 5):
            # logger.warning(f"当前第{i}页")
            self.data["pageIndex"] = str(i)
            yield scrapy.FormRequest(
                url=self.start_urls,
                callback=self.get_list_page,
                dont_filter=True,
                formdata=self.data,
            )

    def get_list_page(self, response):
        infodata = json.loads(response.text).get("custom").get("infodata")
        for info in infodata:
            infourl = info.get("infourl")
            if infourl[0:5] == "https":
                id = info.get("infourl").split("=")[-1]
                url = f"https://biz.hnprec.com/cqjyapi/api/AnncApi/AnncBrowse?id={id}"
                yield scrapy.Request(
                    url=url,
                    callback=self.detail_page1,
                    cb_kwargs={"url": url, "bid_orgin_url": infourl},
                )
            else:
                # print("http://www.hnggzy.com" + infourl)
                yield scrapy.Request(
                    url="http://www.hnggzy.com" + infourl,
                    callback=self.detail_page,
                    cb_kwargs={"url": "http://www.hnggzy.com" + infourl},
                )

    def detail_page(self, response, url):
        res = pq(response.text)
        id = url.split("/")[-1].split(".")[0]
        bid_url = url
        bid_name = res('meta[name="ArticleTitle"]').attr("content")
        bid_public_time = res('meta[name="PubDate"]').attr("content")
        bid_category = res('div[class="location"] a').eq(2).text()
        bid_info_type = res('div[class="location"] a').eq(3).text()
        bid_province = res('div[class="title-text"] font').eq(0).text()
        bid_content = res('div[class="text detail-list"]').text()
        bid_html_con = res('div[class="text detail-list"]').outer_html()
        if bid_category == "政府采购":
            item = GovernmentProcurementItem()
            item["po_id"] = get_md5(id)
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = bid_url
            item["po_province"] = bid_province
            item["po_category"] = bid_category
            item["po_info_type"] = bid_info_type
            item["bo_name"] = bid_name
            item["po_public_time"] = bid_public_time
            item["po_html_con"] = bid_html_con
            item["po_content"] = bid_content
            item["website_name"] = "河南省公共资源交易中心"
            item["website_url"] = "http://www.hnggzy.com/"
            item["bid_orgin_url"] = self.start_urls
            yield item
        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = get_md5(id)
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = bid_url
            item["bid_province"] = bid_province
            item["bid_category"] = bid_category
            item["bid_info_type"] = bid_info_type
            item["bid_name"] = bid_name
            item["bid_public_time"] = bid_public_time
            item["bid_html_con"] = bid_html_con
            item["bid_content"] = bid_content
            item["website_name"] = "河南省公共资源交易中心"
            item["website_url"] = "http://www.hnggzy.com/"
            item["bid_orgin_url"] = self.start_urls
            yield item
        # print(item)

    def detail_page1(self, response, **kwargs):
        url = kwargs["url"]
        id = url.split("/")[-1].split(".")[0]
        bid_orgin_url = kwargs["bid_orgin_url"]
        res = json.loads(response.text)
        try:
            Content = res.get("Data").get("AnncContentModel").get("Content")
        except:
            # print(kwargs["url"])
            Content = res.get("Data")[0].get("Content")
        pre = re.compile(">(.*?)<")
        bid_content = "".join(pre.findall(str(Content)))
        item = BidScrapyProjectItem()
        item["bid_id"] = get_md5(id)
        item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        item["bid_url"] = url
        item["bid_province"] = res.get("Data").get("ProvinceName", "")
        item["bid_city"] = res.get("Data").get("CityName", "")
        item["bid_county"] = res.get("Data").get("CountyName", "")
        item["bid_name"] = res.get("Data").get("AnncName", "")
        item["bid_public_time"] = res.get("Data").get("CreateTime", "")
        item["bid_html_con"] = res.get("Data").get("AnncContentModel").get("Content")
        item["bid_content"] = bid_content
        item["website_url"] = "http://www.hnggzy.com/"
        item["website_name"] = "河南省公共资源交易中心"
        item["bid_orgin_url"] = self.start_urls
        # print(item)
        yield item
