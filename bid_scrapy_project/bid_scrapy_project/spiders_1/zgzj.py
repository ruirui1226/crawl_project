# -*- coding: utf-8 -*-
"""
@desc: 中交集团供应链管理信息系统
@version: python3
@author: liuwx
@time: 2023/07/19
"""
import scrapy
import re
import time

from lxml import etree
from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import BidScrapyProjectItem


class ZgzjSpider(scrapy.Spider):
    name = 'zgzj'

    """
    二级类型 直接列出
    """
    def __init__(self):
        self.infoType = {
            "采购公告": "http://ec.ccccltd.cn/PMS/gysmore.shtml?id=sjN7r9ttBwLI2dpg4DQpQb68XreXjaqknBMygP8dAEQ57TILyRtTnCZX1hIiXHcc1Ra16D6TzZdblRFD/JXcCd5FP7Ek60ksxl9KkyODirY=",
            "评标结果公示": "http://ec.ccccltd.cn/PMS/gysmore.shtml?id=sjN7r9ttBwLI2dpg4DQpQb68XreXjaqknBMygP8dAEQ57TILyRtTnPr0y7nbc5lW1Ra16D6TzZdblRFD/JXcCd5FP7Ek60ksxl9KkyODirY="
        }

        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Referer': 'http://ec.ccccltd.cn/PMS/gysmore.shtml?id=sjN7r9ttBwLI2dpg4DQpQb68XreXjaqknBMygP8dAEQ57TILyRtTnCZX1hIiXHcc1Ra16D6TzZdblRFD/JXcCd5FP7Ek60ksxl9KkyODirY=',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }


    """
    二级分类遍历
    """
    def start_requests(self):
        for info_type, info_url in self.infoType.items():
            items = {
                "bid_info_type": info_type,  # 二级类型
            }
            param = "pid=&announcetstrtime_from=&announcetstrtime_to=&announcetitle=&dalei=&VENUS_PAGE_NO_KEY_INPUT=1&VENUS_PAGE_NO_KEY=1&VENUS_PAGE_SIZE_KEY=15"
            yield scrapy.Request(
                info_url,
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
        items_list = response.meta["items"]
        FLAG = True
        list = response.xpath('//table[@class="table_div_content2"]/tr/td/div/table/tr/td/table/tr')
        # 第一个为表头，去掉
        list.pop(0)
        for li in list:
            # 详情页链接 不是正常的url
            contentUrl = li.xpath("./td[2]/a/@href").extract_first()
            # 第一页第一条为置顶文章，不采
            if "sjN7r9ttBwLI2dpg4DQpQb68XreXjaqkS2JQxUxuL5i10fZTCLCagXX5B/CCLxrNujM2HfHDFD3V\\r\\nO/kUEEREl4mDvHhKUmXm+MUrSyN+vCR1RkP08s2ZebC6c+4EPKbbaiktqvbQ2PNWRFxeAJJDCVtX\\r\\nDy8n/F1o" in contentUrl:
                continue
            # 截取链接所需id
            contentId = re.search("\(\'(.*?)\'\);", contentUrl).group(1)
            if "\\r\\n" in contentId:
                contentId = contentId.replace("\\r\\n","")
            # 文章链接
            linkUrl = "http://ec.ccccltd.cn/PMS/moredetail.shtml?id=" + contentId
            # 文章标题
            title = li.xpath('./td[2]/a/text()').extract_first().strip()
            # 文章发布时间
            times = li.xpath('./td[3]/text()').extract_first().strip()
            # 获取当前年月日
            nowday = time.strftime("%Y-%m-%d")
            # 当发布时间不是当天时间时，跳出不采
            if times != nowday:
                FLAG = False
                # print(times + "不是当天最新文章，跳过")
                break
            items = {
                "bid_public_time": times,
                "bid_url": linkUrl,
                "bid_name": title,
                "bid_id": get_md5(linkUrl)
            }
            items.update(items_list)
            yield scrapy.Request(
                linkUrl,
                callback=self.getContentInfo,
                meta={"items": items}
            )
        if FLAG:
            param = response.meta['param']
            page = str(re.search('VENUS_PAGE_NO_KEY=(\d+)&VENUS_PAGE_SIZE_KEY', param).group(1))
            next_page = str(int(page) + 1)
            # param = param.replace(f'VENUS_PAGE_NO_KEY_INPUT={page}&VENUS_PAGE_NO_KEY', f'VENUS_PAGE_NO_KEY_INPUT={next_page}&VENUS_PAGE_NO_KEY')
            param = param.replace(f'VENUS_PAGE_NO_KEY={page}&VENUS_PAGE_SIZE_KEY', f'VENUS_PAGE_NO_KEY={next_page}&VENUS_PAGE_SIZE_KEY')
            yield scrapy.Request(
                url=response.url,
                callback=self.parse,
                method="POST",
                body=param,
                headers=self.headers,
                meta={"items": items_list, "param": param},
                dont_filter=True
            )

    """
    文章详情获取（发布内容）
    """
    def getContentInfo(self, response):
        items_info = response.meta["items"]
        # 带有html的文本
        str_html_content = etree.HTML(response.text).xpath('//table[@class="tab_content"]')
        if str_html_content:
            contentHtml = etree.tostring(str_html_content[0], encoding="utf-8").decode()
        else:
            print("未获取到html文本")
        # 纯净文本
        content = remove_node(contentHtml, ["style"]).text
        # 去掉换行、空格、制表符
        content = re.sub('\s|\t|\n', '', content)
        items_infos = BidScrapyProjectItem()
        items_infos['bid_category'] = "业务协同"
        items_infos['bid_info_type'] = items_info["bid_info_type"]
        items_infos['bid_public_time'] = items_info["bid_public_time"]
        items_infos['bid_name'] = items_info["bid_name"]
        items_infos['bid_html_con'] = contentHtml
        items_infos['bid_content'] = content
        items_infos['bid_url'] = items_info["bid_url"]
        items_infos["bid_id"] = items_info["bid_id"]
        items_infos['website_name'] = "中交集团供应链管理信息系统"
        items_infos['website_url'] = "http://ec.ccccltd.cn/PMS/jsp/business/web/index.jsp"
        items_infos['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        # print(
        #     items_infos["bid_info_type"],
        #     items_infos["bid_id"],
        #     items_infos["bid_url"],
        #     items_infos["bid_public_time"]
        # )
        yield items_infos