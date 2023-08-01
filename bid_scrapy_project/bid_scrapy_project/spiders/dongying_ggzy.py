#!/usr/bin/conf python
# -*- coding: utf-8 -*-
"""
@desc: 招投标-山东省-东营市公共资源交易中心
@version: python3
@author: shenr
@time: 2023/06/07
"""
import logging
import re
import time

import requests
import scrapy
from pyquery import PyQuery as pq

from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class ExampleSpider(scrapy.Spider):
    name = "dongying_ggjy"
    # allowed_domains = ["http://ggzy.dongying.gov.cn/jyxx/about.html"]
    start_urls = "http://ggzy.dongying.gov.cn/jyxx/about.html"
    page = 1
    current_time = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
    page_time = ""

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls,
            dont_filter=True,
            callback=self.parse_1,
        )

    def parse_1(self, response, **kwargs):
        logging.debug(f"===========当前爬取{self.page}页===========")
        res = pq(response.text)
        results = res('div[id="static"]')
        for each in results('ul[class="ewb-look-items"] li').items():
            time.sleep(1)
            detail_url = "http://ggzy.dongying.gov.cn/" + each("h2 a").attr("href")
            bid_public_time = each("div div").eq(1).text()
            infoid = re.findall(".*/(.*?).html", str(detail_url), re.S)[0]
            self.page_time = each('div[class="look-sta03 r"]').text()
            # 详情页
            yield scrapy.Request(
                url=detail_url,
                callback=self.parse_detail,
                meta={
                    "bid_public_time": bid_public_time,
                    "infoid": infoid,
                }
            )
        # 下一页
        total = re.findall('total: (.*?),', str(res), re.S)[0]
        # if int(total)/10 + 1 > self.page and self.page < 10:
        if self.page_time == self.current_time:
            self.page += 1
            yield scrapy.Request(
                url=f"http://ggzy.dongying.gov.cn/jyxx/{self.page}.html",
                dont_filter=True,
                callback=self.parse_1,
            )

    def parse_detail(self, response, **kwargs):
        res_t = pq(response.text)
        meta = response.meta
        # 区县
        region = res_t('span[class="go-tt"] font').eq(0).text()
        # 层级
        bid_category = res_t('div[class="ewb-route"] p a').eq(2).text()
        bid_info_type = res_t('span[id="viewGuid"]').text()
        # 详情
        content = res_t('div[class="cm-wpr"]').text()
        html_content = res_t('div[class="cm-wpr"]').outerHtml()
        region_ = re.findall("·(.*?)]", str(region), re.S)[0] if re.findall("·(.*?)]", str(region), re.S) else ""
        if bid_info_type == "政府采购":
            item = GovernmentProcurementItem()
            item["po_id"] = get_md5(meta.get("infoid"))
            item["po_province"] = "山东省"
            item["po_city"] = "东营市"
            item["po_county"] = region_
            item["bid_url"] = response.url
            item["po_category"] = bid_category
            item["po_info_type"] = bid_info_type
            item["po_source"] = ""
            item["po_html_con"] = str(html_content).replace("'", '"')
            item["po_content"] = remove_node(html_content, ["script"]).text
            item["bid_name"] = res_t('span[class="go-tt"]').remove("font").text()
            item["po_public_time"] = meta.get("bid_public_time")
            item["website_name"] = "东营市公共资源交易中心"
            item["website_url"] = "http://ggzy.dongying.gov.cn/jyxx/about.html"
            item["bid_orgin_url"] = "http://ggzy.dongying.gov.cn/jyxx/about.html"
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            yield item
        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = get_md5(meta.get("infoid"))
            item["bid_md5_url"] = ""
            item["bid_province"] = "山东省"
            item["bid_city"] = "东营市"
            item["bid_county"] = region_
            item["bid_url"] = response.url
            item["bid_category"] = bid_category
            item["bid_info_type"] = bid_info_type
            item["bid_source"] = ""
            item["bid_html_con"] = str(html_content).replace("'", '"')
            item["bid_content"] = remove_node(html_content, ["script"]).text
            item["bid_name"] = res_t('span[class="go-tt"]').remove("font").text()
            item["bid_public_time"] = meta.get("bid_public_time")
            item["website_name"] = "东营市公共资源交易中心"
            item["website_url"] = "http://ggzy.dongying.gov.cn/jyxx/about.html"
            item["bid_orgin_url"] = "http://ggzy.dongying.gov.cn/jyxx/about.html"
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            yield item
            # break

