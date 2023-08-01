# -*- coding: utf-8 -*-
"""
@desc: 四川政府采购网
@version: python3
@author: liuwx
@time: 2023/07/05
"""

import scrapy
import re
import json
import time

from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import GovernmentProcurementItem

class SichuanCgwSpider(scrapy.Spider):
    name = 'sichuan_cgw'

    """
    二级类型 直接列出
    """
    def __init__(self):
        self.noticeType = {
            "采购公告": "00101",
            "资格预审公告": "001052,001053,00105B",
            "中标（成交）公告": "00102",
            "更正公告": "00103",
            "废标（终止）公告": "001004,001006",
            "征集公告": "206011,206012",
            "入围结果公告": "206014",
            "汇总公告": "206019",
            "框架协议更正公告": "206015"
        }

    """
    各个市获取，市下边的区暂时不采
    """
    def start_requests(self):
        # 所有城市id获取接口
        city_id_url = "http://www.ccgp-sichuan.gov.cn/cms-sc/site/sichuan/resources/json/sc.json"
        yield scrapy.Request(
            city_id_url,
            callback=self.parse,
            dont_filter=True
        )

    """
    列表页接口获取
    """
    def parse(self, response):
        jsondata = json.loads(response.text)
        for catg in jsondata:
            # 没有children这个key值的是还未选城市，不采
            if 'children' not in str(catg):
                continue
            for info_type, notice_id in self.noticeType.items():
                # 各个城市的参数id
                region_code = catg['regionCode']
                # 市
                po_city = catg['name']
                items = {"po_city": po_city, "po_info_type": info_type}
                # 列表页接口
                link = f"http://www.ccgp-sichuan.gov.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=94c965cc-c55d-4f92-8469-d5875c68bd04&channel=c5bff13f-21ca-4dac-b158-cb40accd3035&currPage=1&pageSize=15&noticeType={notice_id}&regionCode={region_code}&purchaseManner=&title=&openTenderCode=&purchaser=&agency=&purchaseNature=&operationStartTime=&operationEndTime=&selectTimeName=noticeTime&cityOrArea=6"
                yield scrapy.Request(
                    link,
                    callback=self.getContentParse,
                    meta={"items": items},
                    dont_filter=True
                )

    """
    列表详情获取（因为文章内容也直接放在了列表页json中，所以直接一块获取）
    """
    def getContentParse(self, response):
        item_info = response.meta["items"]
        # 翻页判断参数
        FLAG = True
        # 获取详情页json数据
        listjson = json.loads(response.text)
        data_list = listjson['data']
        if data_list == []:
            print(item_info["po_city"]+"下没有"+item_info["po_info_type"])
            return
        for data in data_list:
            # 获取发布时间
            pubtime = data['noticeTime']
            # 截取发布时间年月日
            pubday = pubtime.split(' ')[0]
            # 获取当前年月日
            nowday = time.strftime("%Y-%m-%d")
            # 当发布时间不是当天时间时，跳出不采
            if pubday != nowday:
                FLAG = False
                # print("不是当天最新文章，跳过")
                break
            # 获取文章标题
            title = data['title']
            # 获取文章链接
            url = data['pageurl']
            url = response.urljoin(url)
            # 获取数据采购来源
            source = data['agency']
            # 获取网页内容
            content_html = data['content']
            # 获取采购详情
            content = remove_node(content_html, ["style"]).text
            items_infos = GovernmentProcurementItem()
            items_infos['po_category'] = "政府采购"
            items_infos['po_info_type'] = item_info["po_info_type"]
            items_infos['po_province'] = "四川省"
            items_infos['po_city'] = item_info["po_city"]
            items_infos['po_public_time'] = pubtime
            items_infos['bo_name'] = title
            items_infos['po_html_con'] = content_html
            items_infos['po_content'] = content
            items_infos['po_source'] = source
            items_infos['bid_url'] = url
            items_infos["po_id"] = get_md5(url)
            items_infos['website_name'] = "四川政府采购网"
            items_infos['website_url'] = "http://www.ccgp-sichuan.gov.cn/"
            items_infos['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            items_infos['list_parse'] = url
            # print(
            #     items_infos["po_id"],
            #     items_infos["bid_url"],
            #     items_infos["po_public_time"]
            # )
            yield items_infos
        if FLAG == True:
            # 当前page
            pages = re.search('currPage=(\d+)&', response.url).groups()[0]
            next_page_url = str(response.url).replace(f'currPage={str(pages)}&', f'currPage={str(int(pages) + 1)}&')
            yield scrapy.Request(
                next_page_url,
                callback=self.getContentParse,
                meta={"items": item_info},
                dont_filter=True
            )