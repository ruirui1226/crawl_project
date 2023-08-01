# -*- coding: utf-8 -*-
"""
@desc: 河北省招标投标公共服务平台
@version: python3
@author: liuwx
@time: 2023/07/18
"""

import scrapy
import re
import time

from lxml import etree
from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import BidScrapyProjectItem
from bid_scrapy_project.settings import SPECIAL_CLOSESPIDER_TIMEOUT

class HebeiZtbSpider(scrapy.Spider):
    name = 'hebei_ztb'
    # 封ip
    custom_settings = {"CONCURRENT_REQUESTS": 1, 'DOWNLOAD_DELAY': 4, 'CLOSESPIDER_TIMEOUT':SPECIAL_CLOSESPIDER_TIMEOUT}

    """
    二级类型 直接列出
    """
    def __init__(self):
        self.infoType = {
            "招标计划公告": "http://www.hebeieb.com/tender/xxgk/zbjhgg.do",
            "招标公告": "http://www.hebeieb.com/tender/xxgk/zbgg.do",
            "变更公告": "http://www.hebeieb.com/tender/xxgk/bggg.do",
            "答疑澄清": "http://www.hebeieb.com/tender/xxgk/dygs.do",
            "开标记录": "http://www.hebeieb.com/tender/xxgk/kbjl.do",
            "中标候选人公示": "http://www.hebeieb.com/tender/xxgk/pbgs.do",
            "中标结果公示": "http://www.hebeieb.com/tender/xxgk/zhongbgg.do",
            "合同履行公示": "http://www.hebeieb.com/tender/xxgk/qylx.do",
        }
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": " Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

    """
    列表页链接请求
    """
    def start_requests(self):
        for info_type, info_url in self.infoType.items():
            items = {
                "bid_info_type": info_type,  # 二级类型
            }
            param = "page=0&TimeStr=&allDq=&allHy=reset1&AllPtName=&KeyStr=&KeyType=ggname"
            yield scrapy.Request(
                url=info_url,
                callback=self.parse,
                method="POST",
                body=param,
                headers=self.headers,
                meta={"items": items, "param": param},
                dont_filter=True
            )

    """
    列表页详情获取（标题、发布时间、详情页链接）
    """
    def parse(self, response):
        FLAG = True
        item_info = response.meta["items"]
        list = response.xpath('//div[@class="publicont"]/div/h4')
        for li in list:
            # 详情页链接
            contentUrl = li.xpath("./a/@href").extract_first()
            contentUrl = response.urljoin(contentUrl)
            # 文章标题
            title = li.xpath('./a/text()').extract_first().strip()
            # 文章发布时间
            times = li.xpath('./span[@class="span_o"]/text()').extract_first().strip()
            # 获取当前年月日
            nowday = time.strftime("%Y-%m-%d")
            # 当发布时间不是当天时间时，跳出不采
            if times != nowday:
                FLAG = False
                # print(times + "不是当天最新文章，跳过")
                break
            items = {
                "bid_public_time": times,
                "bid_url": contentUrl,
                "bid_name": title,
                "bid_id": get_md5(contentUrl)
            }
            items.update(item_info)
            # 该网站有的文章为静态，有的文章为接口请求。需要分两种情况写
            # 截取infoid 作为判断依据
            infoid = re.search("infoid=(.*?)&bdcodes", contentUrl).group(1)
            if len(infoid) > 10:
            # if "infoid=I13" in contentUrl:
                # 截取接口所需参数
                linkId = re.search("detail.do\?(.*?)&bdcodes", contentUrl).group(1)
                linkUrl = "http://www.hebeieb.com/infogk/newDetail.do?" + linkId + "&laiyuan=[%E5%B9%B3%E5%8F%B0%E5%86%85]"
                yield scrapy.Request(
                    url=linkUrl,
                    callback=self.getContentInfo,
                    method="POST",
                    meta={"items": items}
                )
            else:
                yield scrapy.Request(
                    contentUrl,
                    callback=self.getContentInfo,
                    meta={"items": items}
                )
        if FLAG:
            param = response.meta['param']
            page = str(re.search('page=(\d+)&', param).group(1))
            next_page = str(int(page) + 1)
            param = param.replace(f'page={page}&', f'page={next_page}&')
            yield scrapy.Request(
                url=response.url,
                callback=self.parse,
                method="POST",
                body=param,
                headers=self.headers,
                meta={"items": item_info, 'param': param},
                dont_filter=True
            )


    """
    文章详情获取（发布内容）
    """
    def getContentInfo(self, response):
        items_info = response.meta["items"]
        # 带有html的文本
        str_html_content = etree.HTML(response.text).xpath('//div[@class="article_con"]')
        if str_html_content:
            contentHtml = etree.tostring(str_html_content[0], encoding="utf-8").decode()
        else:
            contentHtml = ""
            print("未获取到html文本")
        # 纯净文本
        content = remove_node(contentHtml, ["style"]).text
        # 去掉换行、空格、制表符
        content = re.sub('\s|\t|\n', '', content)
        items_infos = BidScrapyProjectItem()
        items_infos['bid_category'] = "公告公示"
        items_infos['bid_province'] = "河北省"
        items_infos['bid_info_type'] = items_info["bid_info_type"]
        items_infos['bid_public_time'] = items_info["bid_public_time"]
        items_infos['bid_name'] = items_info["bid_name"]
        items_infos['bid_html_con'] = contentHtml
        items_infos['bid_content'] = content
        items_infos['bid_url'] = items_info["bid_url"]
        items_infos["bid_id"] = items_info["bid_id"]
        items_infos['website_name'] = "河北省招标投标公共服务平台"
        items_infos['website_url'] = "http://www.hebeieb.com/"
        items_infos['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        print(
            items_infos["bid_info_type"],
            items_infos["bid_id"],
            items_infos["bid_url"],
            items_infos["bid_public_time"]
        )
        # yield items_infos

