# -*- coding: utf-8 -*-
"""
@desc: 陕西省公共资源交易服务平台
@version: python3
@author: liuwx
@time: 2023/06/20
"""

import scrapy
import re
import time

from bid_scrapy_project.common.common import get_md5
from lxml import etree
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem

class ShanxiGgzySpider(scrapy.Spider):
    name = "shanxi_ggzy"

    """
    初始链接请求
    """
    def start_requests(self):
        url = "http://www.sxggzyjy.cn/jydt/001001/001001001/subPage_jyxx.html"
        yield scrapy.Request(
            url,
            callback=self.parse,
            dont_filter=True
        )

    """
    大分类获取遍历
    """
    def parse(self, response):
        generalList = response.xpath('//ul[@class="wb-tree-sub"]/li')
        for li in generalList:
            general_href = li.xpath("./h3/a/@href").extract_first()  # 大分类url
            general_href = response.urljoin(general_href)  # 补齐url
            general_name = li.xpath("./h3/a/text()").extract_first().strip()  # 大分类名称
            items = {"bid_category": general_name}
            yield scrapy.Request(
                general_href,
                callback=self.data_Parse,
                meta={"items": items},
                dont_filter=True
            )

    """
    二级类别获取遍历
    """
    def data_Parse(self, response):
        secondaryList = response.xpath('//li[@class="wb-tree-item current"]/ul[@class="wb-four-sub"]/li')
        item = response.meta["items"]
        for li in secondaryList:
            # 翻页 1-3页
            for page in range(1, 4):
                secondary_href = li.xpath("./a/@href").extract_first()  # 二级分类url
                # 第二页的时候参数变化
                if page > 1:
                    secondary_href = secondary_href.replace("subPage_jyxx", "{}".format(page))
                secondary_href = response.urljoin(secondary_href)  # 补齐url
                secondary_name = li.xpath("./a/text()").extract_first().strip()  # 二级分类名称
                items = {"bid_info_type": secondary_name}
                items.update(item)
                yield scrapy.Request(
                    secondary_href,
                    callback=self.getContentParse,
                    meta={"items": items},
                    dont_filter=True
                )

    """
    列表详情获取（标题、发布时间、详情页链接）
    """
    def getContentParse(self, response):
        items_info = response.meta["items"]
        lis = response.xpath('//ul[@class="ewb-list"]/li')
        for li in lis:
            contentUrl = li.xpath("./a/@href").extract_first()  # 详情页链接
            contentUrl = response.urljoin(contentUrl)
            title = li.xpath("./a/@title").extract_first()  # 文章标题
            time = li.xpath('./span[@class="ewb-list-date"]/text()').extract_first()  # 文章发布时间
            # 当详情页没有时间的时候就将这个时间传到发布时间的字段中
            times = "".join(x.strip() for x in time)
            items = {
                "bid_public_time": times,
                "bid_url": contentUrl,
                "bid_name": title,
                "bid_id": get_md5(contentUrl),
            }
            items.update(items_info)
            yield scrapy.Request(contentUrl, callback=self.getContentInfo, meta={"items": items})

    """
    文章详情获取（文章内容、信息来源）
    """
    def getContentInfo(self, response):
        item_info = response.meta["items"]
        info_source = response.xpath('//div[@class="info-source"]').extract_first()
        # 这个网站有的文章打不开，没有url，一直跳转上一级的url，例如：路演窗口栏目下标题为“一种用于无人直升机的辅助着陆指示方法”这篇文章，所以做个判断
        if not info_source or info_source == "None":
            print(f"该请求的ur为{response.url}，链接出错，跳过")
            return
        # 发布时间
        if "信息时间" in info_source and "浏览次数" in info_source:
            pudate = re.search("信息时间：(\d{4}-\d{2}-\d{2})", response.text).groups()[0]
        if not pudate:
            pudate = item_info["bid_public_time"]
        # 信息来源
        author = re.search("信息来源：(.*?)】", response.text)
        if author:
            author = author.groups()[0]
        else:
            author = ""
        # 带有html的文本 有的文章div属性不同，例如：http://www.sxggzyjy.cn/jydt/001001/001001004/001001004009/20230621/8a69c41d88d6a1ff0188dbe971413cca.html
        str_html_content = etree.HTML(response.text).xpath(
            '//div[@class="epoint-article-content"]|//div[@class="epoint-article-content jynr news_content"]'
        )
        contentHtml = etree.tostring(str_html_content[0], encoding="utf-8").decode()
        # 纯净文本
        content = "".join(response.xpath('//div[@class="epoint-article-content"]//text()|//div[@class="epoint-article-content jynr news_content"]//text()').extract()).strip()
        if "政府采购" in item_info["bid_category"]:
            items_cg = GovernmentProcurementItem()
            items_cg["po_province"] = "陕西"
            items_cg["website_name"] = "陕西省公共资源交易服务平台"
            items_cg["website_url"] = "http://www.sxggzyjy.cn/"
            items_cg["po_source"] = author
            items_cg["bo_name"] = item_info.get("bid_name", None)
            items_cg["po_public_time"] = pudate
            items_cg["po_category"] = item_info.get("bid_category", None)
            items_cg["po_info_type"] = item_info.get("bid_info_type", None)
            items_cg["po_city"] = "陕西省"
            items_cg["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            items_cg["bid_url"] = response.request.url
            items_cg["po_id"] = get_md5(response.request.url)
            items_cg["po_html_con"] = contentHtml
            items_cg["po_content"] = content
            # print(
            #     items_cg["po_id"],
            #     items_cg["bid_url"],
            # )
            yield items_cg
        else:
            ##修改格式
            items_zy = BidScrapyProjectItem(
                bid_city="陕西省",
                website_name="陕西省公共资源交易服务平台",
                website_url="http://www.sxggzyjy.cn/",
                bid_province="陕西",
            )
            items_zy.update(item_info)
            items_zy["bid_public_time"] = pudate
            items_zy["bid_html_con"] = contentHtml
            items_zy["bid_content"] = content
            items_zy["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            items_zy["bid_source"] = author
            # print(
            #     items_zy["bid_id"],
            #     items_zy["bid_url"],
            # )
            yield items_zy
