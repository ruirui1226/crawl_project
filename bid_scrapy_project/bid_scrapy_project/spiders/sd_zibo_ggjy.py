# -*- coding: utf-8 -*-
# @Time : 2023/7/3
# @Author: mayj

"""
    淄博公共资源交易网
"""
import re
import time
import scrapy
import logging

from lxml import etree

from bid_scrapy_project.common.common import get_md5, urljoin_url, remove_node
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class SdZiBoGgjySpider(scrapy.Spider):
    name = "sd_zibo_ggjy"
    start_urls = "http://ggzyjy.zibo.gov.cn:8082/EpointWebBuilder_zbggzy/rest/frontAppCustomAction/getPageInfoListNew?params=%7B%22siteGuid%22%3A%227eb5f7f1-9041-43ad-8e13-8fcb82ea831a%22%2C%22categoryNum%22%3A%22002%22%2C%22kw%22%3A%22%22%2C%22startDate%22%3A%22%22%2C%22endDate%22%3A%22%22%2C%22jystauts%22%3A%22%22%2C%22areacode%22%3A%22%22%2C%22pageIndex%22%3A{}%2C%22pageSize%22%3A14%7D"
    base_url = "http://ggzyjy.zibo.gov.cn:8082/gonggongziyuan-content.html?"
    type_number_list = [0, 1, 2, 3, 4, 5, 6, 7]

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    category_num_dict = {
        "002001001": "建设工程:招标公告",
        "002001002": "建设工程:变更公告",
        "002001003": "建设工程:中标候选人公示",
        "002001004": "建设工程:中标结果公示",
        "002001005": "建设工程:异常公告",
        "002001006": "建设工程:合同公示及变更",
        "002001007": "建设工程:招标项目计划",
        "002001009": "建设工程:提问回复",
        "002002001": "政府采购:需求（意向）公示",
        "002002002": "政府采购:采购公告",
        "002002003": "政府采购:更正公告",
        "002002004": "政府采购:中标（成交）公告",
        "002002005": "政府采购:终止公告",
        "002002006": "政府采购:合同公告",
        "002002007": "政府采购:验收公告",
        "002011001": "自然资源:土地矿产",
        "002011001001": "土地矿产:出让公告",
        "002011001002": "土地矿产:结果公示",
        "002011001003": "土地矿产:变更公告",
        "002011001004": "土地矿产:终止公告",
        "002011001005": "土地矿产:中止公告",
        "002011002": "自然资源:集体用地",
        "002011002001": "集体用地:出让公告",
        "002011002002": "集体用地:结果公示",
        "002011002003": "集体用地:变更公告",
        "002011002004": "集体用地:终止公告",
        "002004001": "产权交易:出让公告",
        "002004002": "产权交易:结果公示",
        "002004003": "产权交易:变更公告",
        "002004004": "产权交易:终止公告",
        "002009001": "国企采购:需求（意向）公示",
        "002009002": "国企采购:采购公告",
        "002009003": "国企采购:更正公告",
        "002009004": "国企采购:中标（成交）公告",
        "002009005": "国企采购:终止公告",
        "002009006": "国企采购:合同公告",
        "002009007": "国企采购:验收公告",
        "002007001": "药械采购:需求（意向）公示",
        "002007002": "药械采购:采购公告",
        "002007003": "药械采购:更正公告",
        "002007004": "药械采购:中标（成交）公告",
        "002007005": "药械采购:终止公告",
        "002007006": "药械采购:合同公告",
        "002007007": "药械采购:验收公告",
        "002008001": "其他交易:需求（意向）公示",
        "002008002": "其他交易:采购公告",
        "002008003": "其他交易:更正公告",
        "002008004": "其他交易:中标（成交）公告",
        "002008005": "其他交易:终止公告",
        "002008006": "其他交易:合同公告",
        "002008007": "其他交易:验收公告",
    }

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls.format("0"), meta={"page": 0}, method="POST", dont_filter=True, callback=self.parse_list
        )

    def parse_list(self, response):
        json_data = response.json()
        if json_data.get("status", {}).get("text", "") != "操作成功":
            logging.error("获取列表信息失败")
            return
        datas = json_data.get("custom").get("infodata")

        for data_dict in datas:
            herf = data_dict.get("infourl")
            id = data_dict.get("infoid")
            county = data_dict.get("areacode")
            bid_name = data_dict.get("realtitle")
            pub_date = data_dict.get("infodate")
            det_url = urljoin_url(self.base_url, herf)
            relationguid = data_dict.get("relationguid")
            categorynum = data_dict.get("categorynum")
            try:
                category_str = self.category_num_dict.get(str(categorynum))
                category, info_type = category_str.split(":")
            except:
                category = ""
                info_type = ""

            url = f"http://ggzyjy.zibo.gov.cn:8082/gonggongziyuan-content.html?infoid={id}&relationguid={relationguid}&categorynum={categorynum}"
            ret_data = {
                "det_url": det_url,
                "county": county,
                "pub_date": pub_date,
                "bid_name": bid_name,
                "id": id,
                "url": url,
                "category": category,
                "info_type": info_type,
            }

            yield scrapy.Request(det_url, meta=ret_data, callback=self.parse_detail)

        page = response.meta["page"] + 1
        if page <= 4:
            yield scrapy.Request(
                self.start_urls.format(str(page)),
                meta={"page": page},
                method="POST",
                dont_filter=True,
                callback=self.parse_list,
            )

    def parse_detail(self, response):
        html_con = response.text
        # content = response.xpath("string(.)").extract_first()
        content = remove_node(html_con, ["script"]).text

        id = response.meta["id"]
        category = response.meta["category"]
        url = response.meta["url"]
        county = response.meta["county"]
        info_type = response.meta["info_type"]
        if category == "政府采购":
            item = GovernmentProcurementItem()
            item["po_id"] = get_md5(id)
            item["bid_url"] = url
            item["po_province"] = "山东省"
            item["po_city"] = "淄博市"
            item["po_county"] = county
            item["po_category"] = category
            item["po_info_type"] = info_type
            # item["bid_source"] = "济南公共资源交易中心"
            item["po_public_time"] = response.meta["pub_date"]
            item["bo_name"] = response.meta["bid_name"]
            item["po_html_con"] = html_con
            item["po_content"] = content
            item["website_name"] = "淄博公共资源交易网"
            item["website_url"] = "http://ggzyjy.zibo.gov.cn:8082/"
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = get_md5(id)
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = url
            item["bid_province"] = "山东省"
            item["bid_city"] = "淄博市"
            item["bid_category"] = category
            item["bid_info_type"] = info_type
            item["bid_county"] = county
            # item["bid_source"] = bid_source
            item["bid_name"] = response.meta["bid_name"]
            item["bid_public_time"] = response.meta["pub_date"]
            item["bid_html_con"] = html_con
            item["bid_content"] = content
            item["website_name"] = "淄博公共资源交易网"
            item["website_url"] = "http://ggzyjy.zibo.gov.cn:8082/"

        yield item
