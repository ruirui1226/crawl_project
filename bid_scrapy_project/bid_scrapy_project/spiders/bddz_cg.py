# -*- coding: utf-8 -*-
"""
@desc: 比德电子采购平台
@version: python3
@author: liuwx
@time: 2023/07/12
"""
import re
import scrapy
import json
import time

from lxml import etree
from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import BidScrapyProjectItem

class BddzCgSpider(scrapy.Spider):
    name = 'bddz_cg'

    """
    二级类型 直接列出
    """
    def __init__(self):
        self.infoType = {
            "采购公告": "003001",
            "变更公告": "003002",
            "候选人公示": "003003",
            "采购结果公示": "003004"
        }

        # 31个省份
        self.cityName = {
            "北京市": "110000",
            "天津市": "120000",
            "河北省": "130000",
            "山西省": "140000",
            "内蒙古自治区": "150000",
            "辽宁省": "210000",
            "吉林省": "220000",
            "黑龙江省": "230000",
            "上海市": "310000",
            "江苏省": "320000",
            "浙江省": "330000",
            "安徽省": "340000",
            "福建省": "350000",
            "江西省": "360000",
            "山东省": "370000",
            "河南省": "410000",
            "湖北省": "420000",
            "湖南省": "430000",
            "广东省": "440000",
            "广西壮族自治区": "450000",
            "海南省": "460000",
            "重庆市": "500000",
            "四川省": "510000",
            "贵州省": "520000",
            "云南省": "530000",
            "西藏自治区": "540000",
            "陕西省": "610000",
            "甘肃省": "620000",
            "青海省": "630000",
            "宁夏回族自治区": "640000",
            "新疆维吾尔自治区": "650000",
        }

    """
    列表页链接请求
    """
    def start_requests(self):
        for info_type, categorynum in self.infoType.items():
            for city_name, city_id in self.cityName.items():
                items = {
                    "bid_info_type": info_type, # 二级类型
                    "bid_province": city_name, # 省份
                }
                # 列表页接口获取
                link = "https://www.bdebid.com/EpointWebBuilder5_1/rest/commonSearch/getInfoList"
                param = 'params={"categorynum":"'+categorynum+'","title":"","datetime":"","codearea":"'+city_id+'","hangye":"","pageIndex":0,"pageSize":60}'
                headers = {
                    "Authorization": "Bearer 908aecfce20208fec9dd6ea943a99ea5",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Host": "www.bdebid.com",
                    "Referer": f"https://www.bdebid.com/gggs/{categorynum}/detailpage.html",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                }
                yield scrapy.Request(
                    url=link,
                    callback=self.parse,
                    method="POST",
                    body=param,
                    headers=headers,
                    meta={"items": items},
                    dont_filter=True
                )

    """
    列表页详情获取（标题、发布时间、详情页链接）
    """
    def parse(self, response):
        item_info = response.meta["items"]
        # 获取详情页json数据
        listjson = json.loads(response.text)
        data_list = listjson['infodata']
        for data in data_list:
            # 获取发布时间
            pubtime = data["infodate"]
            # 获取当前年月日
            nowday = time.strftime("%Y-%m-%d")
            # 当发布时间不是当天时间时，跳出不采
            if pubtime != nowday:
                # print(pubtime + "不是当天最新文章，跳过")
                break
            # 获取文章标题
            title = data['title']
            # 获取文章链接
            url = data['infourl']
            url = response.urljoin(url)
            items = {
                "bid_public_time": pubtime,
                "bid_url": url,
                "bid_name": title,
                "bid_id": get_md5(url),
            }
            items.update(item_info)
            yield scrapy.Request(
                url,
                callback=self.getContentInfo,
                meta={"items": items}
            )

    """
    文章详情获取（发布内容）
    """
    def getContentInfo(self, response):
        items_info = response.meta["items"]
        # 带有html的文本
        str_html_content = etree.HTML(response.text).xpath('//div[@class="ewb-trade-info"]')
        if str_html_content:
            contentHtml = etree.tostring(str_html_content[0], encoding="utf-8").decode()
        else:
            print("未获取到html文本")
        # 纯净文本
        content = remove_node(contentHtml, ["style"]).text
        # 去掉换行、空格、制表符
        content = re.sub('\s|\t|\n','',content)
        items_infos = BidScrapyProjectItem()
        items_infos['bid_category'] = "公告公示"
        items_infos['bid_info_type'] = items_info["bid_info_type"]
        items_infos['bid_province'] = items_info["bid_province"]
        items_infos['bid_public_time'] = items_info["bid_public_time"]
        items_infos['bid_name'] = items_info["bid_name"]
        items_infos['bid_html_con'] = contentHtml
        items_infos['bid_content'] = content
        items_infos['bid_url'] = items_info["bid_url"]
        items_infos["bid_id"] = items_info["bid_id"]
        items_infos['website_name'] = "比德电子采购平台"
        items_infos['website_url'] = "https://www.bdebid.com/gggs/subpage.html"
        items_infos['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        # print(
        #     items_infos["bid_id"],
        #     items_infos["bid_url"],
        #     items_infos["bid_public_time"]
        # )
        yield items_infos