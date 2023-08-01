# -*- coding: utf-8 -*-
# @Time : 2023/7/3
# @Author: mayj

"""
    济南公共资源交易中心
"""
import re
import time
import scrapy
import logging

from lxml import etree

from bid_scrapy_project.common.common import get_md5, urljoin_url, remove_node
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class SdJiNanGgjySpider(scrapy.Spider):
    name = "sd_jinan_ggjy"
    start_urls = "http://jnggzy.jinan.gov.cn/jnggzyztb/front/newChangeHomePageList.do"
    base_url = "http://jnggzy.jinan.gov.cn/"
    type_number_list = [0, 1, 2, 3, 4, 5, 6, 7]

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }

    def start_requests(self):
        for type_number in self.type_number_list:
            if type_number == 7:
                data = {
                    "area": "",
                    "type": str(type_number),
                    "pagenum": "1",
                    "subheading": "城乡绿化",
                }
            else:
                data = {
                    "area": "",
                    "type": str(type_number),
                    "pagenum": "1",
                }

            yield scrapy.FormRequest(
                self.start_urls,
                meta={"page": 1, "data": data},
                headers=self.headers,
                formdata=data,
                dont_filter=True,
                method="POST",
                callback=self.parse_list,
            )

    def parse_list(self, response):
        json_data = response.json()
        if "<li>" not in str(json_data.get("params", {})):
            logging.error("获取列表信息失败")
            return False
        data_params = json_data.get("params", {})
        data_str = ""
        for data_v in data_params.values():
            if isinstance(data_v, int):
                continue
            data_str += data_v
        data_tree = etree.HTML(data_str)
        li_list = data_tree.xpath("//li")
        for li_xph in li_list:
            herf = li_xph.xpath("./a/@href")[0]
            id = re.search(r"=(\w+)", herf).group(1)

            try:
                county = li_xph.xpath('./span[@class="bt-left dq"]/@title')[0]
            except:
                county = ""
            bid_name = li_xph.xpath("./a/@title")[0].strip()
            pub_date = li_xph.xpath("./span[last()]/text()")[0]
            det_url = urljoin_url(self.base_url, herf)
            ret_data = {"url": det_url, "county": county, "pub_date": pub_date, "bid_name": bid_name, "id": id}

            yield scrapy.Request(det_url, meta=ret_data, callback=self.parse_detail)

        page = response.meta["page"]

        page = int(page)
        if page + 1 <= 3:
            page += 1
            data = response.meta["data"]
            data["pagenum"] = str(page)
            meta_data = {"page": page, "data": data}
            yield scrapy.FormRequest(
                self.start_urls,
                meta=meta_data,
                headers=self.headers,
                formdata=data,
                dont_filter=True,
                method="POST",
                callback=self.parse_list,
            )

    def parse_detail(self, response):
        if 'class="list"' not in response.text:
            logging.error("未获取到详情信息内容")
            return

        id = re.search(r"=(\w+)", response.meta["url"]).group(1)
        try:
            info_type = response.xpath('//div[@class="bread"]/span[3]/text()').extract_first()
            category = response.xpath('//div[@class="bread"]/span[2]/text()').extract_first()
        except:
            category = response.xpath("//title/text()").extract_first().strip("详情")
            info_type = ""
        if category:
            category = category.replace(">", "").strip()
        if info_type:
            info_type = info_type.replace(">", "").strip()
            info_type = info_type if len(info_type) > 2 else ""
        if info_type is None:
            info_type = ""
        if category and not info_type:
            info_type = category
            category = ''

        bid_html_con = response.xpath('//div[@class="list"]').extract_first()
        # content = response.xpath('string(//div[@class="list"])').extract_first()
        content = remove_node(response.text, ["style"]).text
        county = response.meta["county"]
        if "区" in county:
            county = response.meta["county"].replace("市本级", "")
        if category == "政府采购":
            item = GovernmentProcurementItem()
            item["po_id"] = get_md5(id)
            item["bid_url"] = response.url
            item["po_province"] = "山东省"
            item["po_city"] = "济南市"
            item["po_county"] = county
            item["po_category"] = category
            item["po_info_type"] = info_type
            # item["bid_source"] = "济南公共资源交易中心"
            item["po_public_time"] = response.meta["pub_date"]
            item["bo_name"] = response.meta["bid_name"]
            item["po_html_con"] = bid_html_con
            item["po_content"] = content
            item["website_name"] = "济南公共资源交易中心"
            item["website_url"] = "http://jnggzy.jinan.gov.cn/"
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = get_md5(id)
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = response.url
            item["bid_province"] = "山东省"
            item["bid_city"] = "济南市"
            item["bid_category"] = category
            item["bid_info_type"] = info_type
            item["bid_county"] = county
            # item["bid_source"] = bid_source
            item["bid_name"] = response.meta["bid_name"]
            item["bid_public_time"] = response.meta["pub_date"]
            item["bid_html_con"] = bid_html_con
            item["bid_content"] = content
            item["website_name"] = "济南公共资源交易中心"
            item["website_url"] = "http://jnggzy.jinan.gov.cn/"

        # yield item
        print(item)
