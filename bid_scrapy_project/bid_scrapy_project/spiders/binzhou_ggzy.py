# -*- coding: utf-8 -*-
"""
@desc: 滨州公共资源交易中心
@version: python3
@author: liuwx
@time: 2023/07/03
"""
import scrapy
import time
import re

from bid_scrapy_project.common.common import get_md5, remove_node
from lxml import etree
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem

class BinzhouGgzySpider(scrapy.Spider):
    name = 'binzhou_ggzy'

    """
    一级、二级类别直接列出
    """
    def __init__(self):
        self.category_list = {
            "工程建设": {
                "招标计划公示": "http://jypt.bzggzyjy.cn/bzweb/jyxx/012001/012001007/list1.html",
                "招标公告": "http://jypt.bzggzyjy.cn/bzweb/jyxx/012001/012001001/list1.html",
                "变更公告": "http://jypt.bzggzyjy.cn/bzweb/jyxx/012001/012001002/list1.html",
                "中标候选人公示": "http://jypt.bzggzyjy.cn/bzweb/jyxx/012001/012001003/list1.html",
                "中标(废标)公示": "http://jypt.bzggzyjy.cn/bzweb/jyxx/012001/012001004/list1.html",
                "中标变更": "http://jypt.bzggzyjy.cn/bzweb/jyxx/012001/012001005/list1.html",
                "合同（变更）公示": "http://jypt.bzggzyjy.cn/bzweb/jyxx/012001/012001006/list1.html",
                "项目负责人变更信息": "http://jypt.bzggzyjy.cn/bzweb/jyxx/012001/012001008/list2.html",
            },
            "政府采购": {
                "需求(意向)公开": "http://jypt.bzggzyjy.cn/bzweb/jyxx/012002/012002001/list1.html",
                "招标公告": "http://jypt.bzggzyjy.cn/bzweb/jyxx/012002/012002002/list1.html",
                "中标公告": "http://jypt.bzggzyjy.cn/bzweb/jyxx/012002/012002003/list1.html",
                "信息更正": "http://jypt.bzggzyjy.cn/bzweb/jyxx/012002/012002004/list1.html",
                "废标公告": "http://jypt.bzggzyjy.cn/bzweb/jyxx/012002/012002005/list1.html",
                "合同公开": "http://jypt.bzggzyjy.cn/bzweb/jyxx/012002/012002006/list1.html",
                "验收公开": "http://jypt.bzggzyjy.cn/bzweb/jyxx/012002/012002007/list1.html",
            },
            "产权（要素）交易": {
                "处置公告": "http://jypt.bzggzyjy.cn/bzweb/jyxx/012003/012003001/list1.html",
                "结果公示": "http://jypt.bzggzyjy.cn/bzweb/jyxx/012003/012003002/list1.html",
                "其他": "http://jypt.bzggzyjy.cn/bzweb/jyxx/012003/012003003/list1.html",
            },
            "土地矿业交易": {
                "出让公告": "http://jypt.bzggzyjy.cn/bzweb/jyxx/012004/012004001/list1.html",
                "结果公示": "http://jypt.bzggzyjy.cn/bzweb/jyxx/012004/012004002/list1.html",
                "其他": "http://jypt.bzggzyjy.cn/bzweb/jyxx/012004/012004003/list1.html",
            }
        }

    """
    列表页请求，通过列表页获取城市
    """
    def start_requests(self):
        for category, info_types in self.category_list.items():
            for typeName, typeUrl in info_types.items():
                items = {
                    # 一级分类
                    "bid_category": category,
                    # 二级分类
                    "bid_info_type": typeName
                }
                yield scrapy.Request(
                    typeUrl,
                    callback=self.city_requests,
                    meta={"items": items},
                    dont_filter=True
                )

    """
    各个城市获取，再请求每个城市下的列表页
    """
    def city_requests(self, response):
        items_list = response.meta["items"]
        city_list = response.xpath('//h3[@class="list-hd clearfix"]')
        for city_info in city_list:
            # 区
            county = city_info.xpath('.//text()').extract_first().strip()
            if county == "市本级":
                county = ""
            else:
                county = county
            # 获取区的url
            city_url = city_info.xpath("./a/@href").extract_first()
            city_url = response.urljoin(city_url)
            items = {"bid_county": county}
            items.update(items_list)
            # 该网站数据不多且每页展示条数足够，所以不再翻页
            yield scrapy.Request(
                city_url,
                callback=self.parse,
                meta={"items": items},
                dont_filter=True
            )

    """
    城市列表页详情获取（标题、发布时间、详情页链接）
    """
    def parse(self, response):
        items_list = response.meta["items"]
        list = response.xpath('//li[@class="list-item"]')
        for li in list:
            # 详情页链接
            contentUrl = li.xpath("./a/@href").extract_first()
            contentUrl = response.urljoin(contentUrl)
            # 文章标题
            title = li.xpath('./a/text()').extract_first().strip()
            # 文章发布时间
            times = li.xpath('./a/span[@class="list-time"]/text()').extract_first().strip()
            # 获取当前年月日
            nowday = time.strftime("%Y-%m-%d")
            # 当发布时间不是当天时间时，跳出不采
            if times != nowday:
                # print(pubtime + "不是当天最新文章，跳过")
                break
            print(times)
            items = {
                "bid_public_time": times,
                "bid_url": contentUrl,
                "bid_name": title,
                "bid_id": get_md5(contentUrl)
            }
            items.update(items_list)
            yield scrapy.Request(
                contentUrl,
                callback=self.getContentInfo,
                meta={"items": items}
            )
            break
    """
    文章详情获取（发布内容）
    """
    def getContentInfo(self, response):
        item_info = response.meta["items"]
        # 带有html的文本
        str_html_content = etree.HTML(response.text).xpath('//div[@class="article-info"]')
        if str_html_content:
            contentHtml = etree.tostring(str_html_content[0], encoding="utf-8").decode()
        else:
            print("未获取到html文本，可能是网站疯了")
        # 纯净文本
        content = remove_node(contentHtml, ["style"]).text
        # 去掉换行、空格、制表符
        content = re.sub('\s|\t|\n', '', content)
        if "政府采购" in item_info["bid_category"]:
            items_cg = GovernmentProcurementItem()
            items_cg["po_province"] = "山东省"
            items_cg["po_city"] = "滨州市"
            items_cg["po_county"] = item_info.get("bid_county") #区
            items_cg["website_name"] = "滨州公共资源交易中心"
            items_cg["website_url"] = "http://jypt.bzggzyjy.cn/bzweb/"
            # items_cg["po_source"] = author 该网站没有来源
            items_cg["bo_name"] = item_info.get("bid_name", None)
            items_cg["po_public_time"] = item_info.get("bid_public_time")
            items_cg["po_category"] = item_info.get("bid_category", None)
            items_cg["po_info_type"] = item_info.get("bid_info_type", None)
            items_cg["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            items_cg["bid_url"] = item_info.get("bid_url")
            items_cg["po_id"] = item_info.get("bid_id")
            items_cg["po_html_con"] = contentHtml
            items_cg["po_content"] = content
            # print(
            #     items_cg["po_id"],
            #     items_cg["bid_url"],
            #     items_cg["po_public_time"]
            # )
            yield items_cg
        else:
            ##修改格式
            items_zy = BidScrapyProjectItem(
                bid_city="滨州市",
                website_name="滨州公共资源交易中心",
                website_url="http://jypt.bzggzyjy.cn/bzweb/",
                bid_province="山东省",
            )
            items_zy.update(item_info)
            items_zy["bid_html_con"] = contentHtml
            items_zy["bid_content"] = content
            items_zy["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            # items_zy["bid_source"] = author 该网站没有来源
            # print(
            #     items_zy["bid_id"],
            #     items_zy["bid_url"],
            #     items_zy["bid_public_time"],
            # )
            yield items_zy
