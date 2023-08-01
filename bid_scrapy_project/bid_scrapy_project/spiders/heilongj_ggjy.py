# -*- coding: utf-8 -*-
# @Time : 2023/6/21
# @Author: mayj

"""
   全国公共资源交易平台(黑龙江省)
"""
import datetime
import time

import scrapy

from bid_scrapy_project.common.common import urljoin_url, get_md5
from bid_scrapy_project.items import GovernmentProcurementItem, BidScrapyProjectItem


class HeilongjGgjySpider(scrapy.Spider):
    name = "heilongj_ggjy"
    list_url = "https://ggzyjyw.hlj.gov.cn/EpointWebBuilder/rest/frontAppCustomAction/getPageInfoListNew?params=%7B%22siteGuid%22%3A%227eb5f7f1-9041-43ad-8e13-8fcb82ea831a%22%2C%22categoryNum%22%3A%22{}%22%2C%22xiaqucode%22%3A%22%22%2C%22pageIndex%22%3A{}%2C%22pageSize%22%3A15%7D"
    area_dicts = {
        "230000": "省本级",
        "230100": "哈尔滨市",
        "230200": "齐齐哈尔市",
        "230300": "鸡西市",
        "230400": "鹤岗市",
        "230500": "双鸭山市",
        "230600": "大庆市",
        "230700": "伊春市",
        "230800": "佳木斯市",
        "230900": "七台河市",
        "231000": "牡丹江市",
        "231100": "黑河市",
        "231200": "绥化市",
        "232700": "大兴安岭地区",
    }
    category_dicts = [
        {
            "category": "工程建设",
            "category_id": "003002001",
        },
        {
            "category": "政府采购",
            "category_id": "003002002",
        },
        {
            "category": "土地矿业权",
            "category_id": "003002003",
        },
        {
            "category": "国有产权",
            "category_id": "003002004",
        },
        {
            "category": "医疗卫生集中采购",
            "category_id": "003002005",
        },
        {
            "category": "碳汇、碳排放权交易",
            "category_id": "003002006",
        },
        # {
        #     "category": "限额标准以下项目",
        #     "category_id": "003002007",
        # },
        {
            "category": "医用耗材及检验试剂",
            "category_id": "003002008",
        },
    ]

    def start_requests(self):
        for category_dict in self.category_dicts:
            url = self.list_url.format(category_dict["category_id"], "0")
            category_dict["page"] = 0
            yield scrapy.Request(url, method="POST", meta=category_dict, dont_filter=True, callback=self.parse_list)

    def parse_list(self, response):
        """处理列表信息"""
        json_datas = response.json()["custom"]["infodata"]
        last_time = ""
        for json_data in json_datas:
            meta = response.meta
            meta["title"] = json_data.get("title", "")
            meta["area_code"] = json_data.get("code", "")
            meta["pub_date"] = json_data.get("infodate", "")
            meta["det_url"] = urljoin_url("https://ggzyjyw.hlj.gov.cn", json_data.get("infourl", ""))
            last_time = meta["pub_date"]
            yield scrapy.Request(meta["det_url"], meta=meta, callback=self.parse_detail)

        data_now = datetime.datetime.now().strftime("%Y-%m-%d")
        if last_time == data_now and response.meta["page"] <= 5:
            page = response.meta["page"] + 1
            meta_data = response.meta
            meta_data["page"] = page
            url = self.list_url.format(response.meta["category_id"], str(page))
            yield scrapy.Request(url, method="POST", meta=meta_data, dont_filter=True, callback=self.parse_list)

    def parse_detail(self, response):
        """处理详情数据"""

        title = response.meta["title"]
        province = "黑龙江省"
        area_code = response.meta["area_code"]
        city = self.area_dicts.get(area_code, "")
        bid_url = response.meta["det_url"]
        bid_id = get_md5(bid_url)
        create_datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

        category = response.meta["category"]
        try:
            into_type = response.xpath('//span[@class="ewb-cur"]/text()').extract_first().strip()
        except:
            into_type = ""
        public_time = response.meta["pub_date"]
        html_con = response.xpath('//div[@class="ewb-art-bd"]').extract_first().strip()
        content = response.xpath('string(//div[@class="ewb-art-bd"])').extract_first().strip()
        website_name = "全国公共资源交易平台(黑龙江省)"  # 网站
        website_url = "https://ggzyjyw.hlj.gov.cn/"
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
