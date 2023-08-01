# -*- coding: utf-8 -*-
# @Time : 2023/7/3
# @Author: mayj

"""
    聊城市公共资源交易中心
"""
import datetime
import json
import re
import time
import scrapy
import logging

from lxml import etree

from bid_scrapy_project.common.common import get_md5, urljoin_url
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class SdliaoChengGgjySpider(scrapy.Spider):
    name = "sd_liaocheng_ggjy"
    start_urls = "http://ggzyjy.liaocheng.gov.cn/lcggzy/jyxx/003001/trade_info.html"
    base_url = "http://ggzyjy.liaocheng.gov.cn/"

    def start_requests(self):
        yield scrapy.Request(self.start_urls, dont_filter=True, callback=self.parse_category)

    def parse_category(self, response):
        """获取二级标签url"""
        item_xpaths = response.xpath('//ul[@class="tree"]/li')
        info_type_datas = []
        for item_xpath in item_xpaths:
            category = item_xpath.xpath("./h3/a/@title").extract_first()
            category_url = item_xpath.xpath("./h3/a/@href").extract_first()
            if category == "建设工程":
                item_sub_xpaths = item_xpath.xpath("./div/ul/li")
                for into_sub_xpath in item_sub_xpaths:
                    sub_category = into_sub_xpath.xpath("./h3/a/@title").extract_first()
                    sub_category_url = into_sub_xpath.xpath("./h3/a/@href").extract_first()
                    info_type_datas.append(
                        {
                            "url": urljoin_url(self.base_url, sub_category_url),
                            "category": category,
                            "sub_category": sub_category,
                        }
                    )
            else:
                info_type_datas.append(
                    {
                        "url": urljoin_url(self.base_url, category_url),
                        "category": category,
                    }
                )
        for info_type_data in info_type_datas:
            yield scrapy.Request(info_type_data["url"], meta=info_type_data, callback=self.parse_list, dont_filter=True)

    def parse_list(self, response):
        """处理列表页数据"""
        if "pan-hd" not in response.text:
            logging.error(f"{response['url']}:获取列表信息失败")
            return

        info_type_tree = response.xpath('//div[@class="context-box"]/div')
        for i, info_type_xpath in enumerate(info_type_tree):
            if (i + 1) % 2 == 1:
                info_type = info_type_xpath.xpath("./span/text()").extract_first().strip()
                # if response.meta.get("sub_category", ""):
                #     info_type = f'{response.meta["sub_category"]}:{info_type}'
                next_url = info_type_xpath.xpath("./a/@href").extract_first()
                category_id_str = re.search(r"jyxx(/.+/)trade", next_url).group(1)
            if (i + 1) % 2 == 0:
                trade_items = info_type_xpath.xpath('.//li[@class="trade-item"]')
                last_pub_time = ""
                for trade_item_xpath in trade_items:
                    href = trade_item_xpath.xpath("./a/@href").extract_first()
                    info_id = re.search(r"infoid=(.+?)&", href).group(1)
                    det_url = urljoin_url(self.base_url, href)

                    bid_name = trade_item_xpath.xpath("./a/@title").extract_first()
                    pub_date = trade_item_xpath.xpath('./span[@class="date r"]/text()').extract_first().strip()
                    last_pub_time = pub_date
                    categorynum_str = re.search("categorynum=(\d+)", href).group(1)
                    pub_date_str = pub_date.replace("-", "")
                    new_category_str = (
                        category_id_str
                        if categorynum_str in category_id_str
                        else category_id_str + categorynum_str + "/"
                    )
                    req_det_url = (
                        f"http://ggzyjy.liaocheng.gov.cn/lcggzy/jyxx{new_category_str}/{pub_date_str}/{info_id}.html"
                    )

                    ret_data = {
                        "url": det_url,
                        "req_det_url": req_det_url,
                        "pub_date": pub_date,
                        "bid_name": bid_name,
                        "id": get_md5(info_id),
                        "category": response.meta["category"],
                        "type": info_type,
                    }
                    yield scrapy.Request(req_det_url, meta=ret_data, callback=self.parse_detail)

                data_now = datetime.datetime.now().strftime("%Y-%m-%d")
                if last_pub_time == data_now:
                    new_next_url = urljoin_url(self.base_url, next_url)
                    next_meta = {
                        "category": response.meta["category"],
                        "info_type": info_type,
                        "url": new_next_url,
                    }
                    yield scrapy.Request(new_next_url, meta=next_meta, dont_filter=True, callback=self.parse_next_list)

    def parse_next_list(self, response):
        """获取列表页更多信息"""

        if "pan-hd" not in response.text:
            logging.error(f"{response.url}:获取列表更多信息失败")
            return
        item_tree = response.xpath('//div[@class="context-bd"]//li[@class="trade-item"]')
        for item_xpath in item_tree:
            href = item_xpath.xpath("./a/@href").extract_first()
            info_id = re.search(r"infoid=(.+?)&", href).group(1)
            det_url = urljoin_url(self.base_url, href)
            bid_name = item_xpath.xpath("./a/@title").extract_first()
            pub_date = item_xpath.xpath('./span[@class="date r"]/text()').extract_first().strip()
            categorynum_str = re.search("categorynum=(\d+)", href).group(1)
            pub_date_str = pub_date.replace("-", "")
            category_id_str = re.search(r"jyxx(/.+/)trade", response.meta["url"]).group(1)
            new_category_str = (
                category_id_str if categorynum_str in category_id_str else category_id_str + categorynum_str + "/"
            )
            req_det_url = f"http://ggzyjy.liaocheng.gov.cn/lcggzy/jyxx{new_category_str}/{pub_date_str}/{info_id}.html"
            ret_data = {
                "url": det_url,
                "req_det_url": req_det_url,
                "pub_date": pub_date,
                "bid_name": bid_name,
                "id": get_md5(info_id),
                "category": response.meta["category"],
                "type": response.meta["info_type"],
            }
            yield scrapy.Request(det_url, meta=ret_data, callback=self.parse_detail)

    def parse_detail(self, response):

        if "<!-- main -->" not in response.text:
            logging.error("未获取到详情信息内容")
            return

        bid_html_con = (
            re.search(r"<!-- main -->(.+)<!-- 页面脚本 -->", response.text, re.S).group(1).strip().replace("'", "’")
        )
        bid_html_con_tree = etree.HTML(bid_html_con)
        content = bid_html_con_tree.xpath("string(.)").replace("'", "’")

        id = response.meta["id"]
        url = response.meta["url"]
        category = response.meta["category"]
        info_type = response.meta["type"]
        if category == "政府采购":
            item = GovernmentProcurementItem()
            item["po_id"] = id
            item["bid_url"] = url
            item["po_province"] = "山东省"
            item["po_city"] = "聊城市"
            # item["po_county"] = county
            item["po_category"] = category
            item["po_info_type"] = info_type
            # item["bid_source"] = "济南公共资源交易中心"
            item["po_public_time"] = response.meta["pub_date"]
            item["bo_name"] = response.meta["bid_name"]
            item["po_html_con"] = bid_html_con
            item["po_content"] = content
            item["website_name"] = "聊城市公共资源交易中心"
            item["website_url"] = "http://ggzyjy.liaocheng.gov.cn/"
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = id
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = url
            item["bid_province"] = "山东省"
            item["bid_city"] = "聊城市"
            item["bid_category"] = category
            item["bid_info_type"] = info_type
            # item["bid_county"] = county
            # item["bid_source"] = bid_source
            item["bid_name"] = response.meta["bid_name"]
            item["bid_public_time"] = response.meta["pub_date"]
            item["bid_html_con"] = bid_html_con
            item["bid_content"] = content
            item["website_name"] = "聊城市公共资源交易中心"
            item["website_url"] = "http://ggzyjy.liaocheng.gov.cn/"
        # print(item)
        yield item
