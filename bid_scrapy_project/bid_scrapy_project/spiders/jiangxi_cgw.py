# -*- coding: utf-8 -*-
"""
@desc: 江西省政府采购网
@version: python3
@author: liuwx
@time: 2023/07/03
"""
import scrapy
import json
import time

from lxml import etree
from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import GovernmentProcurementItem
from bs4 import BeautifulSoup

class JiangxiCgwSpider(scrapy.Spider):
    name = 'jiangxi_cgw'

    def __init__(self):
        self.info_types = {
            "采购意向": "002006007",
            "采购公告": "002006001",
            "变更公告": "002006002",
            "答疑澄清": "002006003",
            "结果公示": "002006004",
            "单一来源公示": "002006005",
            "合同公示": "002006006"
        }
        self.cityName = {
            "江西省", "南昌市", "景德镇市", "萍乡市", "九江市", "新余市", "鹰潭市",
            "吉安市", "宜春市", "抚州市", "上饶市", "赣州市", "赣江新区"
        }

    """
    二级分类切换城市遍历
    """
    def start_requests(self):
        for info_type, info_id in self.info_types.items():
            for city_name in self.cityName:
                if city_name == "江西省":
                    po_city = ""
                else:
                    po_city = city_name
                items = {"po_info_type": info_type, "po_city": po_city}
                # 列表页接口
                link = f"http://www.ccgp-jiangxi.gov.cn/jxzfcg/services/JyxxWebservice/getList?response=application/json&pageIndex=1&pageSize=22&area=d{city_name}&prepostDate=&nxtpostDate=&xxTitle=&categorynum={info_id}"
                yield scrapy.Request(
                    link,
                    callback=self.parse,
                    meta={"items": items, "info_id": info_id},
                    dont_filter=True
                )

    """
    列表详情获取（标题、发布时间、详情页链接）
    """
    def parse(self, response):
        list_info_items = response.meta["items"]
        jsondata = json.loads(response.text)["return"]
        jsonlist = json.loads(jsondata)['Table']
        for table in jsonlist:
            # 文章标题
            title = table['title']
            if "<font" in title:
                soup = BeautifulSoup(title, 'html.parser')
                title = soup.get_text()
            # 发布时间
            pubtimes = table['postdate']
            # 详情页链接拼接
            # 类型id
            info_id = response.meta["info_id"]
            # 处理发布时间
            if "-" in pubtimes:
                times = pubtimes.replace("-", "")
            # 文章id
            content_id = table['infoid']
            # if content_id == "b734364d-e2de-4d55-ab71-7a07bdb5363c":
            #     print(list_info_items["po_city"])
            linkurl = f"http://www.ccgp-jiangxi.gov.cn/web/jyxx/002006/{info_id}/{times}/{content_id}.html"
            items = {
                "po_public_time": pubtimes,
                "bid_url": linkurl,
                "bo_name": title,
                "po_id": get_md5(linkurl),
            }
            items.update(list_info_items)
            yield scrapy.Request(
                linkurl,
                callback=self.getContentInfo,
                meta={"items": items}
            )

    """
    文章详情获取（发布内容）
    """
    def getContentInfo(self, response):
        item_info = response.meta["items"]
        # 带有html的文本
        str_html_content = etree.HTML(response.text).xpath('//div[@class="con"]')
        if str_html_content:
            contentHtml = etree.tostring(str_html_content[0], encoding="utf-8").decode()
        else:
            print("未获取到html文本")
        # 纯净文本
        content = remove_node(contentHtml, ["style"]).text
        items_info = GovernmentProcurementItem()
        items_info['po_category'] = "政府采购"
        items_info['po_info_type'] = item_info["po_info_type"]
        items_info['po_province'] = "江西省"
        items_info['po_city'] = item_info["po_city"]
        # items_info['po_county'] = response.meta["po_county"]
        items_info['po_public_time'] = item_info["po_public_time"]
        items_info['bo_name'] = item_info["bo_name"]
        # items_info['po_source'] = source 该网站没有来源
        items_info['bid_url'] = item_info["bid_url"]
        items_info['po_id'] = item_info["po_id"]
        items_info['po_html_con'] = contentHtml
        items_info['po_content'] = content
        items_info['website_name'] = "江西省政府采购网"
        items_info['website_url'] = "http://www.ccgp-jiangxi.gov.cn/web/"
        items_info['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        # print(
        #     items_info["po_id"],
        #     items_info["bid_url"],
        #     items_info.get("po_info_type", None),
        #     items_info["bo_name"],
        #     items_info["po_public_time"],
        #     items_info["po_city"],
        # )
        yield items_info