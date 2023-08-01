#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/6/16 9:21
@Author : zhangpf
@File : guangxi_ggzy.py
@Desc : 广西省
@Software: PyCharm
"""
import json
import math
import re
import time

import datetime
from pyquery import PyQuery as pq
import scrapy
# from loguru import logger

from bid_scrapy_project.common.common import urljoin_url, get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem

now_time = datetime.datetime.now()

that_day = now_time.strftime("%Y-%m-%d 23:59:59")
that_day_3 = (now_time + datetime.timedelta(days=-3)).strftime("%Y-%m-%d 00:00:00")


class guangxiSpider(scrapy.Spider):
    name = "guangxi_spider"
    source_url = "http://ggzy.jgswj.gxzf.gov.cn"
    start_urls = "http://ggzy.jgswj.gxzf.gov.cn/inteligentsearchgxes/rest/esinteligentsearch/getFullTextDataNew"
    pn = 0

    data = '{"token":"","pn":0,"rn":15,"sdt":"","edt":"","wd":"","inc_wd":"","exc_wd":"","fields":"title","cnum":"001","sort":"{\\"infodatepx\\":\\"0\\"}","ssort":"title","cl":200,"terminal":"","condition":[{"fieldName":"categorynum","equal":"001","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2}],"time":[{"fieldName":"infodatepx","startTime":"","endTime":""}],"highlights":"","statistics":null,"unionCondition":null,"accuracy":"","noParticiple":"0","searchRange":null,"isBusiness":"1"}'

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
        count = math.ceil(int(json.loads(response.text).get("result").get("totalcount") / 15))
        # print(count)
        # logger.info(f"共{count}页")
        for i in range(1, count + 1):
            js_data = json.loads(self.data)
            js_data["pn"] = self.pn
            js_data["time"][0]["startTime"] = that_day_3
            js_data["time"][0]["endTime"] = that_day
            data = json.dumps(js_data)
            self.pn += 15
            yield scrapy.Request(
                url=self.start_urls,
                callback=self.get_list_page,
                dont_filter=True,
                body=data,
            )

    def get_list_page(self, response):
        records = json.loads(response.text).get("result").get("records")
        for re in records:
            linkurl = self.source_url + re.get("linkurl")
            yield scrapy.Request(
                url=linkurl,
                callback=self.detail_page,
                cb_kwargs={"url": linkurl},
            )

    def detail_page(self, response, url):
        res = pq(response.text)
        id = res('span[id="viewGuid"]').attr("value")
        bid_url = url
        bid_name = res('div[class="ewb-details-title"]').text()
        bid_public_time = res('div[class="ewb-details-sub"]').text().split("：")[1].split("】")[0]
        bid_category = res('div[class="ewb-route"] a').eq(2).text()
        bid_info_type = res('span[id="viewGuid"]').text()
        bid_content = res('div[class="ewb-tabview"]').text()
        bid_html_con = res('div[class="ewb-tabview"]').outer_html()
        if bid_category == "政府采购":
            item = GovernmentProcurementItem()
            item["po_id"] = get_md5(id)
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = bid_url
            item["po_source"] = ""
            item["po_province"] = "广西省"
            item["po_zone"] = "交易信息"
            item["po_category"] = bid_category
            item["po_info_type"] = bid_info_type
            item["bo_name"] = bid_name
            item["po_public_time"] = bid_public_time
            item["po_html_con"] = bid_html_con
            item["po_content"] = bid_content
            item["website_name"] = "全国公共资源交易平台(广西壮族自治区)"
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
            item["bid_zone"] = "交易信息"
            item["bid_province"] = "广西省"
            item["bid_category"] = bid_category
            item["bid_info_type"] = bid_info_type
            item["bid_name"] = bid_name
            item["bid_public_time"] = bid_public_time
            item["bid_html_con"] = bid_html_con
            item["bid_content"] = bid_content
            item["website_name"] = "全国公共资源交易平台(广西壮族自治区)"
            item["website_url"] = self.source_url
            item["bid_orgin_url"] = self.start_urls
            # print(item)
            yield item
