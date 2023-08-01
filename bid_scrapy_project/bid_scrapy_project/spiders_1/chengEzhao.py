# -*- coding: utf-8 -*-
"""
@desc: 诚E招
@version: python3
@author: liuwx
@time: 2023/07/20
"""
import scrapy
import re
import time

from lxml import etree
from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import BidScrapyProjectItem


class ChengEzhaoSpider(scrapy.Spider):
    name = 'chengEzhao'

    """
    二级类型 直接列出
    """
    def __init__(self):
        self.infoType = {
            "项目公告": "https://www.chengezhao.com/cms/categories/%E4%B8%9A%E5%8A%A1%E5%85%AC%E5%91%8A/%E9%A1%B9%E7%9B%AE%E5%85%AC%E5%91%8A/",
            "变更公告": "https://www.chengezhao.com/cms/categories/%E4%B8%9A%E5%8A%A1%E5%85%AC%E5%91%8A/%E5%8F%98%E6%9B%B4%E5%85%AC%E5%91%8A/",
            "中标公示": "https://www.chengezhao.com/cms/categories/%E4%B8%9A%E5%8A%A1%E5%85%AC%E5%91%8A/%E4%B8%AD%E6%A0%87%E5%85%AC%E7%A4%BA/",
            "结果公告": "https://www.chengezhao.com/cms/categories/%E4%B8%9A%E5%8A%A1%E5%85%AC%E5%91%8A/%E7%BB%93%E6%9E%9C%E5%85%AC%E5%91%8A/",
        }

    """
    二级分类遍历
    """
    def start_requests(self):
        for info_type, info_url in self.infoType.items():
            # 翻页 1-3
            for page in range(1, 4):
                items = {
                    "bid_info_type": info_type,  # 二级类型
                }
                if page > 1:
                    link = info_url + "page/" + str(page)
                else:
                    link = info_url
                yield scrapy.Request(
                    link,
                    callback=self.parse,
                    meta={"items": items},
                    dont_filter=True
                )

    """
    列表页详情获取（标题、发布时间、详情页链接）
    """
    def parse(self, response):
        items_list = response.meta["items"]
        list = response.xpath('//div[@class="cez-business-main__news-item cez-business-main__news-item--active"]')
        for li in list:
            # 详情页链接
            contentUrl = li.xpath("./a/@href").extract_first()
            contentUrl = response.urljoin(contentUrl)
            # 文章标题
            title = li.xpath('./div/h3/a/text()').extract_first().strip()
            # 文章发布时间
            # 年月
            time1 = li.xpath('./a/span[1]/text()').extract_first().strip()
            time2 = li.xpath('./a/span[2]/text()').extract_first().strip()
            # 最终时间
            times = time2 + "-" + time1
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
        str_html_content = etree.HTML(response.text).xpath('//div[@class="cez-business-details-main__middle-content cez-custom-content"]')
        if str_html_content:
            contentHtml = etree.tostring(str_html_content[0], encoding="utf-8").decode()
        else:
            print("未获取到html文本")
        # 纯净文本
        content = remove_node(contentHtml, ["style"]).text
        # 去掉换行、空格、制表符
        content = re.sub('\s|\t|\n', '', content)
        items_infos = BidScrapyProjectItem()
        items_infos['bid_category'] = "业务公告"
        items_infos['bid_info_type'] = items_info["bid_info_type"]
        items_infos['bid_public_time'] = items_info["bid_public_time"]
        items_infos['bid_name'] = items_info["bid_name"]
        items_infos['bid_html_con'] = contentHtml
        items_infos['bid_content'] = content
        items_infos['bid_url'] = items_info["bid_url"]
        items_infos["bid_id"] = items_info["bid_id"]
        items_infos['website_name'] = "诚E招"
        items_infos['website_url'] = "https://www.chengezhao.com/cms/"
        items_infos['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        # print(
        #     items_infos["bid_info_type"],
        #     items_infos["bid_id"],
        #     items_infos["bid_url"],
        #     items_infos["bid_public_time"]
        # )
        yield items_infos
