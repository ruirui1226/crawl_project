# -*- coding: utf-8 -*-
"""
@desc: 冀中能源
@version: python3
@author: liuwx
@time: 2023/07/14
"""
import scrapy
import re
import json
import time

from lxml import etree
from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import BidScrapyProjectItem
from datetime import datetime

class JznyZtbSpider(scrapy.Spider):
    name = 'jzny_ztb'

    """
    二级类型 直接列出
    """
    def __init__(self):
        self.infoType = {
            "招标公告": "5030",
            "采购公告": "5035",
            "变更公告": "5032",
            "计划公告": "5031",
            "中标公示": "5033",
            "中标公告": "5034",
            "成交公告": "5036",
            "其他公告": "5037",
        }

    """
    列表页链接请求
    """
    def start_requests(self):
        for info_type, categorynum in self.infoType.items():
            items = {
                "bid_info_type": info_type,  # 二级类型
            }
            # 列表页接口获取
            link = "https://www.jzbidding.com/cms/api/dynamicData/queryContentPage"
            param = '{\"pageSize\":\"70\",\"dto\":{\"siteId\":\"747\",\"categoryId\":\"'+categorynum+'\",\"bidType\":\"\",\"province\":\"\",\"city\":\"\",\"county\":\"\",\"publishDays\":\"\"}}'
            headers = {
                "Content-Type": "application/json; charset=UTF-8",
                "Referer": "https://www.jzbidding.com/cms/jzny/webfile/zd20=jsgcgg/index.html",
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
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
        data_list = listjson['res']['rows']
        for data in data_list:
            # 获取发布时间
            pubtime = data["publishDate"]
            # 处理时间
            _date = datetime.strptime(pubtime, "%Y-%m-%dT%H:%M:%S.%f+0800")
            times = _date.strftime("%Y-%m-%d %H:%M:%S")
            # 获取当前年月日
            nowday = time.strftime("%Y-%m-%d")
            # 截取发布时间年月日
            pubday = times.split(' ')[0]
            # 当发布时间不是当天时间时，跳出不采
            if pubday != nowday:
                # print(pubtime + "不是当天最新文章，跳过")
                break
            # 获取文章标题
            title = data['title']
            # 获取文章链接
            url = "https://www.jzbidding.com/cms/jzny/webfile" + data['url']
            items = {
                "bid_public_time": times,
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
        str_html_content = etree.HTML(response.text).xpath('//div[@class="text-part-text"]')
        if str_html_content:
            contentHtml = etree.tostring(str_html_content[0], encoding="utf-8").decode()
        else:
            print("未获取到html文本")
        # 纯净文本
        content = remove_node(contentHtml, ["style"]).text
        # 去掉换行、空格、制表符
        content = re.sub('\s|\t|\n', '', content)
        items_infos = BidScrapyProjectItem()
        items_infos['bid_category'] = "交易信息"
        items_infos['bid_info_type'] = items_info["bid_info_type"]
        items_infos['bid_public_time'] = items_info["bid_public_time"]
        items_infos['bid_name'] = items_info["bid_name"]
        items_infos['bid_html_con'] = contentHtml
        items_infos['bid_content'] = content
        items_infos['bid_url'] = items_info["bid_url"]
        items_infos["bid_id"] = items_info["bid_id"]
        items_infos['website_name'] = "冀中能源"
        items_infos['website_url'] = "https://www.jzbidding.com/cms/jzny/webfile/index.html"
        items_infos['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        # print(
        #     items_infos["bid_id"],
        #     items_infos["bid_url"],
        #     items_infos["bid_public_time"]
        # )
        yield items_infos
