# -*- coding: utf-8 -*-
"""
@desc: 阳光采购服务平台
@version: python3
@author: shenr
@time: 2023/06/16
"""
import json
import logging
import re
import time

import scrapy
from pyquery import PyQuery as pq

from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import BidScrapyProjectItem


class ExampleSpider(scrapy.Spider):
    name = "ygcg_ggjy"
    # allowed_domains = ["http://www.ygcgfw.com/gggs/001001/subpage-gggs.html?cate=001001"]
    start_urls = "http://www.ygcgfw.com/inteligentsearchnew/rest/esinteligentsearch/getFullTextDataNew"
    page = 1
    page_all = 1
    current_time = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
    page_time = ""

    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "http://www.ygcgfw.com",
        "Referer": "http://www.ygcgfw.com/gggs/001001/subpage-gggs.html?cate=001001",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    url = "http://www.ygcgfw.com/inteligentsearchnew/rest/esinteligentsearch/getFullTextDataNew"
    data_ = {
        "token": "",
        "pn": 0,
        "rn": 10,
        "sdt": "",
        "edt": "",
        "wd": "apple",
        "inc_wd": "",
        "exc_wd": "",
        "fields": "gudingname",
        "cnum": "004",
        "sort": '{"webdate":0}',
        "ssort": "gudingname",
        "cl": 500,
        "terminal": "",
        "condition": [
            {
                "fieldName": "categorynum",
                "equal": "001001",
                "notEqual": None,
                "equalList": None,
                "notEqualList": None,
                "isLike": True,
                "likeType": "2",
            }
        ],
        "time": [],
        "highlights": "gudingname",
        "statistics": None,
        "unionCondition": None,
        "accuracy": "",
        "noParticiple": "0",
        "searchRange": None,
    }
    data = json.dumps(data_, separators=(",", ":"))

    def start_requests(self):
        yield scrapy.FormRequest(
            url=self.start_urls,
            headers=self.headers,
            body=self.data,
            callback=self.parse_list,
            dont_filter=True,
            method="post",
        )

    def parse_list(self, response, **kwargs):
        if int(response.status) == 200:
            logging.debug(f"============当前爬取{self.page}页==========")
            res = response.text
            js_res = json.loads(res)
            records = js_res.get("result").get("records")
            for each in records:
                detail_url = "http://www.ygcgfw.com/" + each.get("linkurl", "")
                title = each.get("title", "")
                id_ = each.get("id", "")
                release_time = each.get("webdate", "")
                infodate = each.get("infodate", "")
                zhuanzai = each.get("zhuanzai", "")
                cglb = each.get("cglb", "")
                self.page_time = release_time[:10]
                yield scrapy.Request(
                    url=detail_url,
                    headers=self.headers,
                    callback=self.detail_parse,
                    # dont_filter=True,
                    meta={
                        "title": title,
                        "id_": id_,
                        "infodate": infodate,
                        "zhuanzai": zhuanzai,
                        "cglb": cglb,
                    },
                )
            # if self.page == 1:
            #     self.page_all = js_res.get("categorys").get("count")
            # if self.page > self.page_all:
            self.page += 1
            if self.current_time == self.page_time:
                next_data_ = {
                    "token": "",
                    "pn": self.page * 10,
                    "rn": 10,
                    "sdt": "",
                    "edt": "",
                    "wd": "apple",
                    "inc_wd": "",
                    "exc_wd": "",
                    "fields": "gudingname",
                    "cnum": "004",
                    "sort": '{"webdate":0}',
                    "ssort": "gudingname",
                    "cl": 500,
                    "terminal": "",
                    "condition": [
                        {
                            "fieldName": "categorynum",
                            "equal": "001001",
                            "notEqual": None,
                            "equalList": None,
                            "notEqualList": None,
                            "isLike": True,
                            "likeType": "2",
                        }
                    ],
                    "time": [],
                    "highlights": "gudingname",
                    "statistics": None,
                    "unionCondition": None,
                    "accuracy": "",
                    "noParticiple": "0",
                    "searchRange": None,
                }
                next_data = json.dumps(next_data_, separators=(",", ":"))
                yield scrapy.FormRequest(
                    url=self.start_urls,
                    headers=self.headers,
                    body=next_data,
                    callback=self.parse_list,
                    dont_filter=True,
                    method="post",
                )
            else:
                logging.debug("=============当天已爬取完毕==============")
        else:
            logging.debug(f"============爬取结束==========")

    def detail_parse(self, response, **kwargs):
        res = pq(response.text)
        meta = response.meta
        coutent = res('div[class="col-md-20"]')
        # print(coutent.contents())
        category = res('div[class="hidden"] a').eq(2).text()
        bid_info_type = res('div[class="hidden"] span').text()
        item = BidScrapyProjectItem()
        item["bid_id"] = get_md5(meta.get("id_"))
        item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        item["bid_url"] = response.url
        item["bid_md5_url"] = ""
        item["bid_province"] = "山东省"
        item["bid_city"] = ""
        item["bid_county"] = ""
        item["bid_category"] = category
        item["bid_info_type"] = bid_info_type
        item["bid_source"] = meta.get("zhuanzai", "")
        item["bid_name"] = meta.get("title", "")
        item["bid_public_time"] = meta.get("infodate", "")
        item["bid_html_con"] = coutent.html().replace("'", '"')
        # item["bid_content"] = coutent.text().replace("'", '"')
        item["bid_content"] = remove_node(coutent.html(), ["script"]).text
        item["description"] = ""
        item["website_name"] = "阳光采购服务平台"
        item["website_url"] = "http://www.ygcgfw.com/gggs/001001/subpage-gggs.html?cate=001001"
        yield item
