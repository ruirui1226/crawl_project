# -*- coding: utf-8 -*-
"""
@desc: 中国三峡电子采购平台
@version: python3
@author: liuwx
@time: 2023/08/02
"""
import scrapy
import re
import time

from lxml import etree
from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import BidScrapyProjectItem

class ZgsxCgSpider(scrapy.Spider):
    name = 'zgsx_cg'

    """
    一级、二级类别直接列出
    """
    def __init__(self):
        self.category_list = {
            "招标专区": {
                "招标公告": "https://eps.ctg.com.cn/cms/channel/1ywgg1/index.htm?pageNo=1",
                "澄清变更公告": "https://eps.ctg.com.cn/cms/channel/1ywgg2/index.htm?pageNo=1",
                "中标候选人公示": "https://eps.ctg.com.cn/cms/channel/1ywgg3/index.htm?pageNo=1",
                "中标结果公告": "https://eps.ctg.com.cn/cms/channel/1ywgg4/index.htm?pageNo=1",
            },
            "采购专区": {
                "采购公告": "https://eps.ctg.com.cn/cms/channel/2ywgg1/index.htm?pageNo=1",
                "变更公告": "https://eps.ctg.com.cn/cms/channel/2ywgg2/index.htm?pageNo=1",
                "采购结果公告": "https://eps.ctg.com.cn/cms/channel/2ywgg3/index.htm?pageNo=1",
            }
        }

    """
    二级分类遍历
    """
    def start_requests(self):
        for category, info_types in self.category_list.items():
            for info_type, info_url in info_types.items():
                # 翻页 1-2
                for page in range(1, 3):
                    items = {
                        # 一级分类
                        "bid_category": category,
                        # 二级分类
                        "bid_info_type": info_type
                    }
                    if page > 1:
                        next_url = info_url.replace("pageNo=1", "pageNo=" + str(page))
                    else:
                        next_url = info_url
                    yield scrapy.Request(
                        next_url,
                        callback=self.parse,
                        meta={"items": items},
                        dont_filter=True
                    )

    """
    列表页详情获取（标题、发布时间、详情页链接）
    """
    def parse(self, response):
        items_list = response.meta["items"]
        list = response.xpath('//li[@name="li_name"]')
        for li in list:
            # 详情页链接
            contentUrl = li.xpath("./a/@href").extract_first()
            contentUrl = response.urljoin(contentUrl)
            # 文章标题
            title = li.xpath('./a/@title').extract_first().strip()
            # 文章发布时间
            times = li.xpath('./a/em/text()').extract_first().strip()
            # 获取当前年月日
            nowday = time.strftime("%Y-%m-%d")
            # 当发布时间不是当天时间时，跳出不采
            if times != nowday:
                # print(times + "不是当天最新文章，跳过")
                break
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

    """
    文章详情获取（发布内容）
    """
    def getContentInfo(self, response):
        items_info = response.meta["items"]
        # 带有html的文本
        str_html_content = etree.HTML(response.text).xpath('//div[@class="main-text"]')
        if str_html_content:
            contentHtml = etree.tostring(str_html_content[0], encoding="utf-8").decode()
        else:
            print("未获取到html文本")
        # 纯净文本
        content = remove_node(contentHtml, ["style"]).text
        # 去掉换行、空格、制表符
        content = re.sub('\s|\t|\n', '', content)
        items_infos = BidScrapyProjectItem()
        items_infos['bid_category'] = items_info["bid_category"]
        items_infos['bid_info_type'] = items_info["bid_info_type"]
        items_infos['bid_public_time'] = items_info["bid_public_time"]
        items_infos['bid_name'] = items_info["bid_name"]
        items_infos['bid_html_con'] = contentHtml
        items_infos['bid_content'] = content
        items_infos['bid_url'] = items_info["bid_url"]
        items_infos["bid_id"] = items_info["bid_id"]
        items_infos['website_name'] = "中国三峡电子采购平台"
        items_infos['website_url'] = "https://eps.ctg.com.cn/cms/index.htm"
        items_infos['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        # print(
        #     items_infos["bid_info_type"],
        #     items_infos["bid_id"],
        #     items_infos["bid_url"],
        #     items_infos["bid_public_time"]
        # )
        yield items_infos