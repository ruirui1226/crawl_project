# -*- coding: utf-8 -*-
"""
@desc: 河南省政府采购网
@version: python3
@author: liuwx
@time: 2023/07/07
"""

import re
import scrapy
import time

from lxml import etree
from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import GovernmentProcurementItem

class HenanCgwSpider(scrapy.Spider):
    name = 'henan_cgw'

    """
    公告类型 直接列出
    """
    def __init__(self):
        self.noticeType = {
            "采购意向": "http://www.ccgp-henan.gov.cn/henan/list2?channelCode=9102&pageNo=1&pageSize=16&bz=1&gglx=0",
            "采购公告": "http://www.ccgp-henan.gov.cn/henan/list2?channelCode=0101&pageNo=1&pageSize=16&bz=1&gglx=0",
            "更正公告": "http://www.ccgp-henan.gov.cn/henan/list2?channelCode=0103&pageNo=1&pageSize=16&bz=1&gglx=0",
            "结果公告": "http://www.ccgp-henan.gov.cn/henan/list2?channelCode=0102&pageNo=1&pageSize=16&bz=1&gglx=0",
            "废标公告": "http://www.ccgp-henan.gov.cn/henan/list2?channelCode=0190&pageNo=1&pageSize=16&bz=1&gglx=0",
            "合同公告": "http://www.ccgp-henan.gov.cn/henan/list2?channelCode=1401&pageNo=1&pageSize=16&bz=1&gglx=0",
            "验收结果公告": "http://www.ccgp-henan.gov.cn/henan/list2?channelCode=1402&pageNo=1&pageSize=16&bz=1&gglx=0",
            "单一来源公示": "http://www.ccgp-henan.gov.cn/henan/list2?channelCode=1301&pageNo=1&pageSize=16&bz=1&gglx=0",
            "非政府采购": "http://www.ccgp-henan.gov.cn/henan/list2?channelCode=9101&pageNo=1&pageSize=16&bz=1&gglx=0",
            "其他": "http://www.ccgp-henan.gov.cn/henan/list2?channelCode=1304&pageNo=1&pageSize=16&bz=1&gglx=0",
        }

    def start_requests(self):
        for info_type, info_url in self.noticeType.items():
            items = {"po_info_type": info_type}
            if info_type == "采购意向":
                type_id = "cgxx/cgyx"
            elif info_type == "采购公告":
                type_id = "cgxx/cggg"
            elif info_type == "更正公告":
                type_id = "cgxx/bggg"
            elif info_type == "结果公告":
                type_id = "cgxx/jggg"
            elif info_type == "废标公告":
                type_id = "cgxx/henan/cgxx/fbgg"
            elif info_type == "合同公告":
                type_id = "htysgg/htgg"
            elif info_type == "验收结果公告":
                type_id = "htysgg/ysgg"
            elif info_type == "单一来源公示":
                type_id = "qtgg/dgly"
            elif info_type == "非政府采购":
                type_id = "cgxx/fzfcggg"
            else:
                type_id = "cgxx/zxyj" # 其他
            yield scrapy.Request(
                info_url,
                callback=self.parse,
                meta={"items": items, "type_id": type_id},
                dont_filter=True
            )

    """
    列表详情获取（标题、发布时间、详情页链接）
    """
    def parse(self, response):
        items_list = response.meta["items"]
        type_id = response.meta["type_id"]
        list = response.xpath('//div[@class="List2"]/ul/li')
        for li in list:
            # 详情页链接
            contentUrl = li.xpath("./a/@href").extract_first()
            contentUrl = response.urljoin(contentUrl)
            # 截取文章id
            contentId = re.search("infoId=(.*?)&channel", contentUrl).group(1)
            # 标题
            title = li.xpath('./a/text()').extract_first().strip()
            # 文章发布时间
            pubtime = li.xpath('./p/span[@class="Gray Right"]/text()').extract_first().strip()
            # 截取时间
            pubday = pubtime.split(' ')[0]
            # 获取发布年月
            ym = pubday[:pubday.rindex("-")]
            time1 = ym.replace("-","/")
            # 获取发布年月日
            time2 = pubday.replace("-", "/")
            # 信息来源
            author = li.xpath('./p/span[1]/span[@class="Blue"]/text()').extract_first().strip()
            if not author:
                print("未获取到来源")
                author = ""
            items = {
                "po_public_time": pubtime,
                "bid_url": contentUrl,
                "bo_name": title,
                "po_id": get_md5(contentUrl),
                "po_source": author
            }
            items.update(items_list)
            # “采购公告”、“更正公告”、“结果公告”、“其他”下的详情链接都需要年月日参数，剩下的类型只需要年月参数
            # 文章详情链接
            if "cgxx/cggg" == type_id or "cgxx/bggg" == type_id or "cgxx/jggg" == type_id or "cgxx/zxyj" == type_id:
                link = f"http://www.ccgp-henan.gov.cn/webfile/henan/{type_id}/webinfo/{time2}/{contentId}.htm"
            else:
                link = f"http://www.ccgp-henan.gov.cn/webfile/henan/{type_id}/webinfo/{time1}/{contentId}.htm"
            yield scrapy.Request(
                link,
                callback=self.getContentInfo,
                meta={"items": items, "type_id": type_id}
            )

    """
    文章详情获取（发布内容、信息来源）
    """
    def getContentInfo(self, response):
        item_info = response.meta["items"]
        type_id = response.meta["type_id"]
        # "非政府采购"、"其他"下的文章内容获取规则不同
        # 带有html的文本
        if type_id == "cgxx/fzfcggg" or type_id == "cgxx/zxyj":
            str_html_content = etree.HTML(response.text).xpath('//body')
        else:
            str_html_content = etree.HTML(response.text).xpath('//table[@class="Content"]')
        if str_html_content:
            contentHtml = etree.tostring(str_html_content[0], encoding="utf-8").decode()
        # 纯净文本
        content = remove_node(contentHtml, ["style"]).text
        items_infos = GovernmentProcurementItem()
        items_infos['po_category'] = "政府采购"
        items_infos['po_info_type'] = item_info["po_info_type"]
        items_infos['po_province'] = "河南省"
        # items_infos['po_json_data'] = listjson
        items_infos['po_public_time'] = item_info["po_public_time"]
        items_infos['bo_name'] = item_info["bo_name"]
        items_infos['po_html_con'] = contentHtml
        items_infos['po_content'] = content
        items_infos['po_source'] = item_info["po_source"]
        items_infos['bid_url'] = item_info["bid_url"]
        items_infos['website_name'] = "河南省政府采购网"
        items_infos['website_url'] = "http://www.ccgp-henan.gov.cn/"
        items_infos["po_id"] = item_info["po_id"]
        items_infos['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        # print(
        #     items_infos["po_id"],
        #     items_infos["bid_url"],
        #     items_infos["po_public_time"],
        #     items_infos["bo_name"],
        #     items_infos["po_info_type"],
        # )
        yield items_infos