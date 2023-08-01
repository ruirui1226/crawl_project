# -*- coding: utf-8 -*-
"""
@desc: 陕西省政府采购网
@version: python3
@author: liuwx
@time: 2023/06/26
"""
import re
import scrapy
import json
import time

from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import GovernmentProcurementItem

class ShanxiCgwSpider(scrapy.Spider):
    name = 'shanxi_cgw'

    """
    公告类型 直接列出
    """
    def __init__(self):
        self.noticeType = {
            "采购公告": "001011,001012,001013,001014,001016,001019",
            "结果公告": "001021,001022,001023,001024,001025,001026,001029,001006",
            "更正公告": "001031,001032",
            "终止公告": "001004,001006",
            "其他": "001053,001052,00105B",
            "采购前公示": "001051,00105F",
            "意向公开": "59,5E",
            "合同公示": "001054,00100B",
            "履约验收信息": "00105A,001009,00100C",
            "中小企业预留份额执行情况公示": "001062",
        }

    """
    各个城市下的区县的id获取
    """
    def start_requests(self):
        # 所有城市id获取接口
        city_id_url = "http://www.ccgp-shaanxi.gov.cn/cms-sx/site/shanxi/resources/json/sxTree.json"
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
                po_city = catg['localCity']
                items = {
                    "po_city": po_city,
                    "po_info_type": info_type,
                }
                # 列表页接口
                link = f"http://www.ccgp-shaanxi.gov.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=a7a15d60-de5b-42f2-b35a-7e3efc34e54f&channel=1eb454a2-7ff7-4a3b-b12c-12acc2685bd1&currPage=1&pageSize=10&noticeType={notice_id}&regionCode={region_code}&purchaseManner=&title=&openTenderCode=&purchaseNature=&operationStartTime=&operationEndTime=&selectTimeName=noticeTime&cityOrArea=6"
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
        for data in data_list:
            # 获取发布时间
            pubtime = data['noticeTime']
            if not pubtime:
                print("未获取到时间")
                FLAG = False
                continue
            # 截取发布时间年月日
            pubday = pubtime.split(' ')[0]
            # 获取当前年月日
            nowday = time.strftime("%Y-%m-%d")
            # 当发布时间不是当天时间时，跳出不采
            if pubday != nowday:
                FLAG = False
                # print(item_info["po_city"]+"下的"+item_info["po_info_type"]+pubtime+"不是当天最新文章，跳过")
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
            items_infos['po_province'] = "陕西省"
            items_infos['po_city'] = item_info["po_city"]
            # items_infos['po_json_data'] = listjson
            items_infos['po_public_time'] = pubtime
            items_infos['bo_name'] = title
            items_infos['po_html_con'] = content_html
            items_infos['po_content'] = content
            items_infos['po_source'] = source
            items_infos['bid_url'] = url
            items_infos['website_name'] = "陕西省政府采购网"
            items_infos['website_url'] = "http://www.ccgp-shaanxi.gov.cn/"
            items_infos["po_id"] = get_md5(url)
            items_infos['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            items_infos['list_parse'] = url
            yield items_infos
        if FLAG == True:
            # 当前page
            pages = re.search('currPage=(\d+)&', response.url).groups()[0]
            if int(pages) <= 3:
                next_page_url = str(response.url).replace(f'currPage={str(pages)}&', f'currPage={str(int(pages)+1)}&')
                yield scrapy.Request(
                    next_page_url,
                    callback=self.getContentParse,
                    meta={"items": item_info},
                    dont_filter=True
                )

