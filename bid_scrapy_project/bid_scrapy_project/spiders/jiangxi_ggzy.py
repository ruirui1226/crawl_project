#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/6/15 10:27
@Author : zhangpf
@File : jiangxi_ggzy.py
@Desc : 江西省
@Software: PyCharm
"""

import json
import math
import re
import time
from datetime import datetime
import datetime as da

from pyquery import PyQuery as pq
import scrapy
# from loguru import logger

from bid_scrapy_project.common.common import urljoin_url, get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem

now_time = da.datetime.now()
that_day = now_time.strftime("%Y-%m-%d 23:59:59")
that_day_3 = (now_time + da.timedelta(days=0)).strftime("%Y-%m-%d 00:00:00")


class jiangxiSpider(scrapy.Spider):
    name = "jiangxi_spider"
    source_url = "https://www.jxsggzy.cn"
    start_urls = "https://www.jxsggzy.cn/XZinterface/rest/esinteligentsearch/getFullTextDataNew"
    pn = 0

    data = '{"token":"","pn":0,"rn":10,"sdt":"","edt":"","wd":"","inc_wd":"","exc_wd":"","fields":"","cnum":"","sort":"{\\"webdate\\":\\"0\\",\\"id\\":\\"0\\"}","ssort":"","cl":10000,"terminal":"","condition":[{"fieldName":"categorynum","equal":"002","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2}],"time":[{"fieldName":"webdate","startTime":"%s","endTime":"%s"}],"highlights":"","statistics":null,"unionCondition":[],"accuracy":"","noParticiple":"1","searchRange":null,"noWd":true}' %(that_day_3, that_day)
    def start_requests(self):
        # print(self.data)
        yield scrapy.Request(
            url=self.start_urls,
            callback=self.parse_list,
            dont_filter=True,
            body=self.data,
            method="POST"
        )

    def parse_list(self, response):
        # print(json.loads(response.text).get("result").get("totalcount"))
        count = math.ceil(int(json.loads(response.text).get("result").get("totalcount") / 10))
        # logger.info(f"共{count}页")
        for i in range(1, count + 1):
            # logger.warning(f"当前第{i}页")
            js_data = json.loads(self.data)
            js_data["pn"] = self.pn
            data = json.dumps(js_data)
            self.pn += 10
            yield scrapy.Request(
                url=self.start_urls,
                callback=self.get_list_page,
                dont_filter=True,
                body=data,
                method="POST"
            )

    def get_list_page(self, response):
        records = json.loads(response.text).get("result").get("records")
        for re in records:
            linkurl = self.source_url + re.get("linkurl")
            # logger.warning("当前url={}".format(linkurl))
            yield scrapy.Request(
                url=linkurl,
                callback=self.detail_page,
                cb_kwargs={"url": linkurl},
            )

    def detail_page(self, response, url):
        # print(response)
        res = pq(response.text)
        id = res('input[id="souceinfoid"]').attr("value")
        bid_url = url
        bid_name = res('p[class="title"]').text()
        bid_public_time = res('ul[class="infor"] li').text().split("： ")[1].split("】")[0]
        dt_time = str(datetime.strptime(bid_public_time, "%Y-%m-%d"))
        bid_category = res('div[class="local"] a').eq(2).text().split(">")[0]
        bid_info_type = res('div[class="local"] a').eq(3).text()
        bid_content = res('div[class="content"]').text()
        bid_html_con = res('div[class="content"]').outer_html()
        if bid_category == "政府采购":
            item = GovernmentProcurementItem()
            item["po_id"] = get_md5(id)
            item["po_province"] = "江西省"
            item["bid_url"] = bid_url
            item["po_category"] = bid_category
            item["po_info_type"] = bid_info_type
            item["po_source"] = ""
            item["po_html_con"] = bid_html_con
            item["po_content"] = bid_content
            item["bo_name"] = bid_name
            item["po_public_time"] = dt_time
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["website_name"] = "江西省公共资源交易中心"
            item["website_url"] = self.source_url
            item["bid_orgin_url"] = self.start_urls
            # print(item)
            yield item
        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = get_md5(id)
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = bid_url
            item["bid_source"] = ""
            item["bid_province"] = "江西省"
            item["bid_category"] = bid_category
            item["bid_info_type"] = bid_info_type
            item["bid_name"] = bid_name
            item["bid_public_time"] = dt_time
            item["bid_html_con"] = bid_html_con
            item["bid_content"] = bid_content
            item["website_name"] = "江西省公共资源交易中心"
            item["website_url"] = self.source_url
            item["bid_orgin_url"] = self.start_urls
            # print(item)
            yield item
