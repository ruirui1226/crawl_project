# -*- coding: utf-8 -*-
"""
@desc: 河北省公共资源交易平台
@version: python
@author: zhangpf
@time: 2023/6/15
"""
import json
import re
import time

from loguru import logger

import requests
import scrapy
from pyquery import PyQuery as pq

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class HebeiSpider(scrapy.Spider):
    name = "Hebei"
    source_url = "http://ggzy.hebei.gov.cn"
    start_url = "http://ggzy.hebei.gov.cn/inteligentsearchfw/rest/inteligentSearch/getFullTextData"

    data = '{"token":"","pn":0,"rn":10,"sdt":"","edt":"","wd":" ","inc_wd":"","exc_wd":"","fields":"title","cnum":"001","sort":"{\\"webdate\\":0}","ssort":"title","cl":200,"terminal":"","condition":[{"fieldName":"categorynum","equal":"003","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2},{"fieldName":"infoc","equal":"1300","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2}],"time":null,"highlights":"title","statistics":null,"unionCondition":null,"accuracy":"","noParticiple":"0","searchRange":null,"isBusiness":"1"}'
    pn = 0

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, body=self.data, callback=self.get_list_page, method="POST")

    def get_list_page(self, response):
        date_json = json.loads(response.text)
        totalcount = date_json.get("result").get("totalcount")
        # print("总数：", totalcount)
        # for i in range(1, totalcount +1):
        for i in range(1, 11):
            js_data = json.loads(self.data)
            js_data["pn"] = self.pn
            data = json.dumps(js_data)
            self.pn += 10
            yield scrapy.Request(url=self.start_url, body=data, callback=self.get_page, method="POST")

    def get_page(self, response):
        date_json = json.loads(response.text)
        records = date_json.get("result").get("records")
        for record in records:
            link = "http://ggzy.hebei.gov.cn/hbggfwpt" + record.get("linkurl")
            # logger.debug(link)
            yield scrapy.Request(url=link, callback=self.parse, cb_kwargs={"url": link})

    def parse(self, response, **kwargs):
        res = pq(response.text)
        bid_url = kwargs["url"]
        id = bid_url.split("/")[-1].split(".")[0]
        bid_name = res('h2[id="titlecontent"]').text()
        bid_public_time = res('div[class="ewb-info-intro"] span').eq(0).text().split("：")[1]
        bid_category = res('div[class="ewb-location"] a').eq(3).text()
        bid_info_type = res('div[class="ewb-location"] a').eq(3).text()
        bid_city = res('span[id="infod"]').text()
        bid_content = res('div[class="ewb-copy"]').text()
        bid_html_con = res('div[class="ewb-copy"]').outer_html()
        if bid_category == "政府采购":
            items = GovernmentProcurementItem()
            items["po_id"] = get_md5(id)
            items["bo_name"] = bid_name
            items["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            items["bid_url"] = bid_url
            items["po_category"] = bid_category
            items["po_info_type"] = bid_info_type
            items["po_public_time"] = bid_public_time
            items["po_city"] = bid_city
            items["po_html_con"] = bid_html_con
            items["po_content"] = bid_content
            items["website_name"] = "河北省公共资源交易平台"
            items["website_url"] = self.source_url
            items["po_province"] = "河北省"
            yield items
        else:
            items = BidScrapyProjectItem()
            items["bid_id"] = get_md5(id)
            items["bid_name"] = bid_name
            items["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            items["bid_url"] = bid_url
            items["bid_category"] = bid_category
            items["bid_info_type"] = bid_info_type
            items["bid_public_time"] = bid_public_time
            items["bid_city"] = bid_city
            items["bid_html_con"] = bid_html_con
            items["bid_content"] = bid_content
            items["website_name"] = "河北省公共资源交易平台"
            items["website_url"] = self.source_url
            items["bid_province"] = "河北省"
            yield items
