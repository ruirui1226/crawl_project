# -*- coding: utf-8 -*-
"""
@desc: 铁建云采
@version: python3
@author: liuwx
@time: 2023/07/12
"""
import scrapy
import re
import json
import time

from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import BidScrapyProjectItem


class TjycSpider(scrapy.Spider):
    name = 'tjyc'

    """
    二级类型 直接列出
    """
    def __init__(self):
        self.infoType = {
            "招标公告": '"noticeType":"1,2","sourcingModeID":"ZBCG",',
            "竞争性谈判": '"noticeType":"1,2","sourcingModeID":"TPCG",',
            "询价公告": '"noticeType":"1,2","sourcingModeID":"XJCG",',
            "补遗公告": '"noticeType":"4,6","sourcingModeID":null,',
            "中标公示": '"noticeType":"5,3","sourcingModeID":null,'
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
            link = "https://www.crccep.com/crcc-purportal-manage/portal/specialtopic/findNoticesBynotices"
            param = '{"pageNum":1,"pageSize":80,'+ categorynum +'"likeKey":"","purCompanyName":"","orgLevel":"","publishTimeBegin":"","publishTimeEnd":""}'
            headers = {
                'Content-Type': 'application/json',
                'Referer': 'https://www.crccep.com/findNoticesList?index=LetterOfAcceptance',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
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
        data_list = listjson['list']
        for data in data_list:
            # 获取发布时间
            pubtime = data["publishTime"]
            # 截取发布时间年月日
            pubday = pubtime.split(' ')[0]
            # 获取当前年月日
            nowday = time.strftime("%Y-%m-%d")
            # 当发布时间不是当天时间时，跳出不采
            if pubday != nowday:
                # print(pubtime + "不是当天最新文章，跳过")
                break
            # 获取文章标题
            title = data['noticeTitle']
            # 获取文章id
            id = data['id']
            # 获取文章链接
            url = "https://www.crccep.com/findNotices?noticeId=" + id
            # 获取文章接口
            link = "https://www.crccep.com/crcc-purportal-manage/portal/specialtopic/findNoticesDetails?id=" + id
            items = {
                "bid_public_time": pubtime,
                "bid_url": url,
                "bid_name": title,
                "bid_id": get_md5(url),
            }
            items.update(item_info)
            yield scrapy.Request(
                link,
                callback=self.getContentInfo,
                meta={"items": items}
            )

    """
    文章详情获取（发布内容）
    """
    def getContentInfo(self, response):
        items_info = response.meta["items"]
        # 获取详情页json数据
        contentjson = json.loads(response.text)
        # 带有html的文本
        contentHtml = contentjson['noticeContent']
        # 纯净文本
        content = remove_node(contentHtml, ["style"]).text
        # 去掉换行、空格、制表符
        content = re.sub('\s|\t|\n', '', content)
        items_infos = BidScrapyProjectItem()
        items_infos['bid_category'] = "采购信息"
        items_infos['bid_info_type'] = items_info["bid_info_type"]
        items_infos['bid_public_time'] = items_info["bid_public_time"]
        items_infos['bid_name'] = items_info["bid_name"]
        items_infos['bid_html_con'] = contentHtml
        items_infos['bid_content'] = content
        items_infos['bid_url'] = items_info["bid_url"]
        items_infos["bid_id"] = items_info["bid_id"]
        items_infos['website_name'] = "中国铁建"
        items_infos['website_url'] = "https://www.crccep.com/homeIndex"
        items_infos['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        # print(
        #     items_infos["bid_id"],
        #     items_infos["bid_url"],
        #     items_infos["bid_public_time"]
        # )
        yield items_infos
