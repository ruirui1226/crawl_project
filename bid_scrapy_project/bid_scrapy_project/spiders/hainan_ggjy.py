# -*- coding: utf-8 -*-
# @Time : 2023/6/16
# @Author: mayj

"""
   全国公共资源交易平台(海南省)
"""
import datetime
import re
import time

import scrapy
from lxml import etree

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import GovernmentProcurementItem, BidScrapyProjectItem


class HainanGgjySpider(scrapy.Spider):
    name = "hainan_ggjy"
    start_url = "https://zw.hainan.gov.cn/ggzy/ggzy/jgzbgg/index.jhtml"

    def start_requests(self):
        yield scrapy.Request(self.start_url, callback=self.parse_nav_list, dont_filter=True)

    def parse_nav_list(self, response):
        sub_nav_list = response.xpath('//ul[@class="navContent"]')
        number = 1
        url_dict_list = []
        # category = ''
        # into_type = ''
        # into_type_url = ''
        while True:
            try:
                tag = sub_nav_list.xpath(f"./*[position()={number}]")
                if not tag:
                    break
            except:
                break

            try:
                category = tag.xpath("./text()").extract()[0]
            except:
                pass
            try:
                data = {
                    "category": category,
                }
                into_type = tag.xpath("./a/span/text()").extract()[0]
                into_type_url = tag.xpath("./a/@href").extract()[0]
                data["into_type"] = into_type
                data["into_type_url"] = into_type_url
                url_dict_list.append(data)
            except:
                pass

            number += 1

        for url_dict in url_dict_list:
            url_dict["page"] = 1
            yield scrapy.Request(url_dict["into_type_url"], meta=url_dict, dont_filter=True, callback=self.parse_list)

    def parse_list(self, response):
        category = response.meta["category"]
        into_type = response.meta["into_type"]
        page = response.meta["page"]
        info_list = response.xpath('//table[@class="newtable"]/tbody/tr')
        last_time = ""
        for info_xpath in info_list:
            meta_data = {}
            meta_data["city"] = info_xpath.xpath("./td[2]/text()").extract_first()
            meta_data["title"] = info_xpath.xpath("./td[3]/a/@title").extract_first()
            if not meta_data["title"]:
                continue
            meta_data["det_url"] = info_xpath.xpath("./td[3]/a/@href").extract_first()
            meta_data["pub_date"] = info_xpath.xpath("./td[4]/text()").extract_first()
            last_time = meta_data["pub_date"]
            meta_data["category"] = category
            meta_data["into_type"] = into_type

            yield scrapy.Request(meta_data["det_url"], meta=meta_data, callback=self.parse_detail)

        data_now = datetime.datetime.now().strftime("%Y-%m-%d")
        if last_time == data_now and page <= 7:
            page += 1
            response.meta["page"] = page
            next_url = re.sub(r"(index.)jhtml", f"index_{str(page)}.jhtml", response.url)
            yield scrapy.Request(next_url, meta=response.meta, dont_filter=True, callback=self.parse_list)

    def parse_detail(self, response):
        title = response.meta["title"]
        province = "海南省"
        city = response.meta["city"]
        bid_id = get_md5(response.url)
        create_datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        bid_url = response.url
        category = response.meta["category"]
        into_type = response.meta["into_type"]
        public_time = response.meta["pub_date"]
        html_con = re.search('<!-- 左栏_begin -->(.+)<div id="video"', response.text, re.S).group(1).replace("'", "’")
        content = etree.HTML(html_con).xpath("string(.)").replace("'", "’")
        website_name = "全国公共资源交易平台(海南省)"  # 网站
        website_url = "https://zw.hainan.gov.cn/ggzy/"

        if response.meta["category"] == "政府采购":
            item = GovernmentProcurementItem()
            item["po_id"] = bid_id
            item["bid_url"] = bid_url
            item["po_province"] = province
            item["po_city"] = city
            item["po_category"] = category
            item["po_info_type"] = into_type
            item["po_public_time"] = public_time
            item["bo_name"] = title
            item["po_html_con"] = html_con
            item["po_content"] = content
            item["website_name"] = website_name
            item["website_url"] = website_url
            item["create_datetime"] = create_datetime

        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = bid_id
            item["create_datetime"] = create_datetime
            item["bid_url"] = bid_url
            item["bid_province"] = province
            item["bid_city"] = city
            item["bid_category"] = category
            item["bid_info_type"] = into_type
            item["bid_name"] = title
            item["bid_public_time"] = public_time
            item["bid_html_con"] = html_con
            item["bid_content"] = content
            item["website_name"] = website_name
            item["website_url"] = website_url

        yield item
