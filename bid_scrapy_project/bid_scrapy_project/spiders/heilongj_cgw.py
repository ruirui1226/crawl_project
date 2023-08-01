# -*- coding: utf-8 -*-
"""
@desc: 黑龙江省政府采购网
@version: python3
@author: liuwx
@time: 2023/06/27
"""
import scrapy
import json
import time

from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import GovernmentProcurementItem
from lxml import etree

class HeilongjCgwSpider(scrapy.Spider):
    name = 'heilongj_cgw'

    """
    公告类型、城市 直接列出
    """
    def __init__(self):
        self.announcement_name = {
            "项目采购公告": {
                # "全部": "00101,00103,00102,001032,001004,001006",
                "采购公告": "00101",
                "更正公告": "001031,001032",
                "中标（成交）公告": "00102",
                "中标（成交）更正公告": "001032",
                "废标（终止）公告": "001004,001006",
            },
            "电子卖场公告": {
                # "全部": "001072,001073",
                "采购需求公告": "001072",
                "采购成交公告": "001073",
            },
            "协议供货公告": {
                # "全部": "001076",
                "结果公告": "001076",
            },
            "定点采购公告": {
                # "全部": "00107D,201111,00107E,202111",
                "采购公告": "00107D,201111",
                "结果公告": "00107E,202111",
            },
            "服务工程超市公告": {
                # "全部": "00107A,00107B",
                "采购需求公告": "00107A",
                "采购成交公告": "00107B",
            }
        }
        self.city_name = {
            # ”全部“ "省本级" 不采
            "哈尔滨市": "230101","齐齐哈尔市": "230201", "鸡西市": "230301",
            "鹤岗市": "230401","双鸭山市": "230501", "大庆市": "230601", "伊春市": "230701",
            "佳木斯市": "230801", "七台河市": "230901", "牡丹江市": "231001",
            "黑河市": "231101", "绥化市": "231201", "大兴安岭": "232799"
        }

    """
    列表页接口获取
    """
    def start_requests(self):
        for category, info_types in self.announcement_name.items():
            for typeName, typeId in info_types.items():
                for cityName, cityId in self.city_name.items():
                    # 翻页 1-3页
                    for page in range(1, 3):
                        datas = {}
                        # 采购类别
                        # datas['po_category'] = category
                        items = {"po_info_type": typeName,
                                 "po_city": cityName,
                                 # 这个网站没有分区，所以“po_county”这个字段也传cityName的值
                                 "po_county": cityName,
                                 "po_province": "黑龙江省"
                                 }
                        # 列表页接口
                        link = f"http://hljcg.hlj.gov.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=94c965cc-c55d-4f92-8469-d5875c68bd04&channel=c5bff13f-21ca-4dac-b158-cb40accd3035&currPage={page}&pageSize=15&noticeType={typeId}&regionCode={cityId}&purchaseManner=&title=&openTenderCode=&purchaser=&agency=&purchaseNature=&operationStartTime=&operationEndTime=&selectTimeName=noticeTime"
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
        # 获取详情页json数据
        listjson = json.loads(response.text)
        data_list = listjson['data']
        for data in data_list:
            # 获取发布时间
            pubtime = data['noticeTime']
            # 截取发布时间年月日
            pubday = pubtime.split(' ')[0]
            # 获取当前年月日
            nowday = time.strftime("%Y-%m-%d")
            # 当发布时间不是当天时间时，跳出不采
            if pubday != nowday:
                # print(pubtime + "不是当天最新文章，跳过")
                break
            # 获取文章标题
            title = data['title']
            # 获取数据采购来源
            source = data['agency']
            # 获取网页内容
            content_html = data['content']
            # 有的网站链接会跳转，网页内容和来源为空，需要另写，例如：http://hljcg.hlj.gov.cn/mall-view/information/detail?noticeId=334273
            if not content_html and not source:
                # 这类文章没有来源，传空字符串
                source = ""
                # 获取文章id
                noticeId = data['noticeId']
                # 文章链接
                url = "https://hljcg.hlj.gov.cn/mall-view/information/detail?noticeId=" + noticeId
                items = {
                    "po_source": source,
                    "bid_url": url,
                    "bo_name": title,
                    "po_id": get_md5(url),
                    "po_public_time": pubtime
                }
                items.update(item_info)
                # 文章详情接口
                content_url = "http://hljcg.hlj.gov.cn/proxy/platform/platform/notice/queryMallNoticeById?id=" + noticeId
                yield scrapy.Request(
                    content_url,
                    callback=self.contentParse,
                    meta={"items": items}
                )
            else:
                # 获取文章链接
                url = data['pageurl']
                url = response.urljoin(url)
                # 获取采购详情
                content = remove_node(content_html, ["style"]).text
                items_infos = GovernmentProcurementItem()
                items_infos['po_category'] = "政府采购"
                items_infos['po_info_type'] = item_info["po_info_type"]
                items_infos['po_province'] = item_info["po_province"]
                items_infos['po_city'] = item_info["po_city"]
                items_infos['po_county'] = item_info["po_county"]
                # items_infos['po_json_data'] = listjson
                items_infos['po_public_time'] = pubtime
                items_infos['bo_name'] = title
                items_infos['po_source'] = source
                items_infos['bid_url'] = url
                items_infos['po_html_con'] = content_html
                items_infos['po_content'] = content
                items_infos['website_name'] = "黑龙江省政府采购网"
                items_infos['website_url'] = "http://hljcg.hlj.gov.cn/"
                items_infos["po_id"] = get_md5(url)
                items_infos['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
                items_infos['list_parse'] = url
                # print(
                #     items_infos["po_id"],
                #     items_infos["bid_url"],
                #     items_infos.get("po_info_type", None),
                #     items_infos["bo_name"],
                #     items_infos["po_city"],
                #     items_infos["po_county"],
                #     items_infos["po_source"],
                #     items_infos["po_public_time"],
                # )
                yield items_infos

    """
    针对”http://hljcg.hlj.gov.cn/mall-view/information/detail?noticeId=334273“这类文章的处理方法
    """
    def contentParse(self, response):
        item_info = response.meta["items"]
        datajson = json.loads(response.text)
        try:
            contentStr = datajson['data']['contentStr']
        except:
            print(item_info["bid_url"]+"该网站打不开")
            return
        # 采购详情
        content = remove_node(contentStr, ["style"]).text
        # 网页内容
        str_html_content = etree.HTML(contentStr).xpath('//div[@class="layui-fluid"]')
        if str_html_content:
            contentHtml = etree.tostring(str_html_content[0], encoding="utf-8").decode()
        items_infos = GovernmentProcurementItem()
        items_infos['po_category'] = "政府采购"
        items_infos['po_info_type'] = item_info["po_info_type"]
        items_infos['po_province'] = item_info["po_province"]
        items_infos['po_city'] = item_info["po_city"]
        items_infos['po_county'] = item_info["po_county"]
        # items_infos['po_json_data'] = listjson
        items_infos['po_public_time'] = item_info["po_public_time"]
        items_infos['bo_name'] = item_info["bo_name"]
        items_infos['po_source'] = item_info["po_source"]
        items_infos['bid_url'] = item_info["bid_url"]
        items_infos['po_html_con'] = contentHtml
        items_infos['po_content'] = content
        items_infos['website_name'] = "黑龙江省政府采购网"
        items_infos['website_url'] = "http://hljcg.hlj.gov.cn/"
        items_infos["po_id"] = item_info["po_id"]
        items_infos['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        # print(
        #     items_infos["po_id"],
        #     items_infos["bid_url"],
        #     items_infos.get("po_info_type", None),
        #     items_infos["bo_name"],
        #     items_infos["po_city"],
        #     items_infos["po_county"],
        #     items_infos["po_source"],
        #     items_infos["po_public_time"],
        # )
        yield items_infos
