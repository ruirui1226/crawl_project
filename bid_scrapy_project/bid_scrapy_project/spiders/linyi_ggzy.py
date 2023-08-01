#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2023/6/30 10:20
@Author : zhangpf
@File : linyi_ggzy.py
@Desc : 临沂
@Software: PyCharm
"""
import json
import math
import re
import time

import scrapy
# from loguru import logger
from pyquery import PyQuery as pq

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class linyiSpider(scrapy.Spider):
    name = "linyi"
    source_url = "http://ggzyjy.linyi.gov.cn"
    start_urls = "http://ggzyjy.linyi.gov.cn/linyi/jyxx/jylist.html"
    start_url_7_ = "http://ggzyjy.linyi.gov.cn/EpointWebBuilder/rest/frontAppNotNeedLoginAction/getPageInfoList"

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls,
            callback=self.parse_list,
            dont_filter=True,
        )

    def parse_list(self, response):
        response = response.text
        total = re.findall("total: (.*?),", str(response), re.S)[0]
        totals = math.ceil(int(total) / 15)
        print(totals)
        for i in range(1, 6):
            if i >= 7:
                data = {
                    "params": '{"siteGuid":"7eb5f7f1-9041-43ad-8e13-8fcb82ea831a","categoryNum":"012","pageIndex":"%s","controlname":"subpagelist"}'
                    % i,
                }
                yield scrapy.FormRequest(
                    url=self.start_url_7_, callback=self.detail_list1, dont_filter=True, method="POST", formdata=data
                )
            elif i == 1:
                yield scrapy.Request(
                    url=self.start_urls,
                    callback=self.detail_list,
                    dont_filter=True,
                )
            else:
                yield scrapy.Request(
                    url=f"http://ggzyjy.linyi.gov.cn/linyi/jyxx/{i}.html",
                    callback=self.detail_list,
                    dont_filter=True,
                )

    def detail_list(self, response):
        res_t = pq(response.text)
        for url in res_t('ul[class="news-items"] li a').items():
            detail_url = url.attr("href")
            # logger.warning("当前url={}".format("http://ggzyjy.linyi.gov.cn" + detail_url))
            yield scrapy.Request(
                url="http://ggzyjy.linyi.gov.cn" + detail_url,
                callback=self.parse_page,
                cb_kwargs={"detail_url": detail_url},
            )

    def detail_list1(self, response):
        response = json.loads(response.text)
        infodata = response.get("custom").get("infodata")
        for i in infodata:
            detail_url = i.get("infourl")
            # logger.warning("当前url={}".format("http://ggzyjy.linyi.gov.cn" + detail_url))
            url = self.source_url + i.get("infourl")
            yield scrapy.Request(url=url, callback=self.parse_page, cb_kwargs={"detail_url": detail_url})

    def parse_page(self, response, detail_url):
        res_t = pq(response.text)
        bid_name = res_t('div[class="ewb-article"] h3').text()
        bid_html_con = str(res_t('div[class="ewb-article-info"]').outer_html()).replace("'", '"')
        bid_source = res_t('div[class="ewb-article-sources"] p').eq(3).text()
        bid_category = res_t('div[class="ewb-location"] a').eq(2).text()
        bid_info_type = res_t('span[id="viewGuid"]').text()
        pre = re.compile(">(.*?)<")
        bid_content = "".join(pre.findall(str(bid_html_con)))
        information_time = res_t('div[class="ewb-article-sources"] p').eq(0).text().split("：")[-1].split("】")[0]
        if bid_category == "政府采购":
            item = GovernmentProcurementItem()
            item["po_id"] = get_md5(str(detail_url).split("/")[-1].split(".")[0])
            item["po_province"] = "山东省"
            item["po_city"] = "临沂市"
            item["bid_url"] = "http://ggzyjy.linyi.gov.cn" + detail_url
            item["po_category"] = bid_category
            item["po_info_type"] = bid_info_type
            item["po_source"] = bid_source
            item["po_html_con"] = bid_html_con
            item["po_content"] = bid_content
            item["bo_name"] = bid_name
            item["po_public_time"] = information_time
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["website_name"] = "全国公共资源交易平台（山东省·临沂市）临沂市公共资源交易中心"
            item["website_url"] = self.source_url
            # print(item)
            yield item
        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = get_md5(str(detail_url).split("/")[-1].split(".")[0])
            item["bid_province"] = "山东省"
            item["bid_city"] = "临沂市"
            item["bid_county"] = ""
            item["bid_url"] = "http://ggzyjy.linyi.gov.cn" + detail_url
            item["bid_category"] = bid_category
            item["bid_info_type"] = bid_info_type
            item["bid_source"] = bid_source
            item["bid_html_con"] = bid_html_con
            item["bid_content"] = bid_content
            item["bid_name"] = bid_name
            item["bid_public_time"] = information_time
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["website_name"] = "全国公共资源交易平台（山东省·临沂市）临沂市公共资源交易中心"
            item["website_url"] = self.source_url
            # print(item)
            yield item
