#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/6/15 15:35
@Author : zhangpf
@File : sichuan_ggzy.py
@Desc : 四川省
@Software: PyCharm
"""
import datetime
import json
import math
import re
import time

from pyquery import PyQuery as pq
import scrapy
# from loguru import logger

from bid_scrapy_project.common.common import urljoin_url, get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem

now_time = datetime.datetime.now()
that_day = now_time.strftime("%Y-%m-%d 23:59:59")
that_day_3 = (now_time + datetime.timedelta(days=-1)).strftime("%Y-%m-%d 00:00:00")


class sichuanSpider(scrapy.Spider):
    name = "sichuan_spider"
    source_url = "http://ggzyjy.sc.gov.cn"
    start_urls = "http://ggzyjy.sc.gov.cn/inteligentsearch/rest/inteligentSearch/getFullTextData"
    pn = 0

    data = '{"token":"","pn":0,"rn":12,"sdt":"","edt":"","wd":"","inc_wd":"","exc_wd":"","fields":"title","cnum":"","sort":"{\'webdate\':\'0\'}","ssort":"title","cl":500,"terminal":"","condition":[{"fieldName":"categorynum","equal":"002","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2}],"time":[{"fieldName":"webdate","startTime":"","endTime":""}],"highlights":"","statistics":null,"unionCondition":null,"accuracy":"","noParticiple":"0","searchRange":null,"isBusiness":"1"}'

    def start_requests(self):
        js_data = json.loads(self.data)
        js_data["time"][0]["startTime"] = that_day_3
        js_data["time"][0]["endTime"] = that_day
        data = json.dumps(js_data)
        yield scrapy.Request(
            url=self.start_urls,
            callback=self.parse_list,
            dont_filter=True,
            body=data,
        )

    def parse_list(self, response):
        count = math.ceil(int(json.loads(response.text).get("result").get("totalcount") / 12))
        # logger.info(f"共{count}页")
        for i in range(1, 6):
            js_data = json.loads(self.data)
            js_data["pn"] = self.pn
            js_data["time"][0]["startTime"] = that_day_3
            js_data["time"][0]["endTime"] = that_day
            data = json.dumps(js_data)
            # print(data)
            self.pn += 12
            yield scrapy.Request(
                url=self.start_urls,
                callback=self.get_list_page,
                body=data,
            )

    def get_list_page(self, response):
        records = json.loads(response.text).get("result").get("records")
        for re in records:
            # print(re)
            linkurl = self.source_url + re.get("linkurl")
            # print(linkurl)
            yield scrapy.Request(
                url=linkurl,
                callback=self.detail_page,
                cb_kwargs={"url": linkurl},
            )

    def detail_page(self, response, url):
        res = pq(response.text)
        id = res('input[id="souceinfoid"]').attr("value")
        bid_url = url
        bid_name = res('h2[id="title"]').text()
        bid_public_time = res('span[id="date"]').text()
        bid_source = res('p[class="detailed-desc"] span').eq(1).text()
        bid_category = res('div[class="container"] a').eq(2).text()
        bid_info_type = res('div[class="container"] a').eq(3).text()
        bid_content = res('div[class="container news-detailed"]').text()
        bid_html_con = res('div[class="container news-detailed"]').outer_html()
        if bid_category == "政府采购":
            item = GovernmentProcurementItem()
            item["po_id"] = get_md5(id)
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = bid_url
            item["po_source"] = bid_source
            item["po_province"] = "四川省"
            item["po_category"] = bid_category
            item["po_info_type"] = bid_info_type
            item["bo_name"] = bid_name
            item["po_public_time"] = bid_public_time
            item["po_html_con"] = bid_html_con
            item["po_content"] = bid_content
            item["website_name"] = "四川省公共资源交易信息网"
            item["website_url"] = self.source_url
            item["bid_orgin_url"] = self.start_urls
            # print(item)
            yield item

        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = get_md5(id)
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = bid_url
            item["bid_source"] = bid_source
            item["bid_province"] = "四川省"
            item["bid_category"] = bid_category
            item["bid_info_type"] = bid_info_type
            item["bid_name"] = bid_name
            item["bid_public_time"] = bid_public_time
            item["bid_html_con"] = bid_html_con
            item["bid_content"] = bid_content
            item["website_name"] = "四川省公共资源交易信息网"
            item["website_url"] = self.source_url
            item["bid_orgin_url"] = self.start_urls
            # print(item)
            yield item
