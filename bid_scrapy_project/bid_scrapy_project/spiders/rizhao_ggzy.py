# -*- coding: utf-8 -*-
"""
@desc: 日照公共资源交易网
@version: python3
@author: liuwx
@time: 2023/06/30
"""
import scrapy
import re
import time
import datetime as dt
from bid_scrapy_project.common.common import get_md5, remove_node
from lxml import etree
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem

class RizhaoGgzySpider(scrapy.Spider):
    name = 'rizhao_ggzy'
    # 网站有封控，需要降低请求频率
    custom_settings = {"CONCURRENT_REQUESTS": 1}

    """
    一级、二级类别直接列出
    """
    def __init__(self):
        self.category_list = {
            "工程建设": {
                "招标计划": "http://ggzyjy.rizhao.gov.cn/rzwz/jyxx/071001/071001006/",
                "招标公告": "http://ggzyjy.rizhao.gov.cn/rzwz/jyxx/071001/071001001/",
                "变更公告": "http://ggzyjy.rizhao.gov.cn/rzwz/jyxx/071001/071001002/",
                "中标公示": "http://ggzyjy.rizhao.gov.cn/rzwz/jyxx/071001/071001003/",
                "废标公告": "http://ggzyjy.rizhao.gov.cn/rzwz/jyxx/071001/071001004/",
                "合同公示": "http://ggzyjy.rizhao.gov.cn/rzwz/jyxx/071001/071001005/",
                "合同变更": "http://ggzyjy.rizhao.gov.cn/rzwz/jyxx/071001/071001007/",
            },
            "政府采购": {
                "意向、需求公示": "http://ggzyjy.rizhao.gov.cn/rzwz/jyxx/071002/071002001/",
                "采购公告": "http://ggzyjy.rizhao.gov.cn/rzwz/jyxx/071002/071002002/",
                "变更公告": "http://ggzyjy.rizhao.gov.cn/rzwz/jyxx/071002/071002003/",
                "中标(结果)公告": "http://ggzyjy.rizhao.gov.cn/rzwz/jyxx/071002/071002004/",
                "合同公开": "http://ggzyjy.rizhao.gov.cn/rzwz/jyxx/071002/071002005/",
                "验收公开": "http://ggzyjy.rizhao.gov.cn/rzwz/jyxx/071002/071002006/",
            },
            "土地及矿业权": {
                "出让公告": "http://ggzyjy.rizhao.gov.cn/rzwz/jyxx/071003/071003001/",
                "结果公示": "http://ggzyjy.rizhao.gov.cn/rzwz/jyxx/071003/071003002/",
            },
            "农村集体产权及其他交易": {
                "招标(出让)公告": "http://ggzyjy.rizhao.gov.cn/rzwz/jyxx/071004/071004001/",
                "变更公告": "http://ggzyjy.rizhao.gov.cn/rzwz/jyxx/071004/071004003/",
                "中标(结果)公告": "http://ggzyjy.rizhao.gov.cn/rzwz/jyxx/071004/071004002/",
            },
        }

    """
    列表页请求
    """
    def start_requests(self):
        for category, info_types in self.category_list.items():
            for typeName, typeUrl in info_types.items():
                # 翻页 1-2页
                # for page in range(1, 3):
                items = {
                    # 一级分类
                    "bid_category": category,
                    # 二级分类
                    "bid_info_type": typeName
                }
                # 二级分类id获取
                type_info = typeUrl.split('/')
                type_id = type_info[-2]
                # 列表页请求链接
                link = f"http://ggzyjy.rizhao.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum={type_id}&Paging=1"
                yield scrapy.Request(
                    link,
                    callback=self.parse,
                    meta={"items": items},
                    dont_filter=True
                )

    """
    列表详情获取（标题、发布时间、详情页链接）
    """
    def parse(self, response):
        linkUrl = response.url
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Referer': linkUrl,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
        items_list = response.meta["items"]
        list = response.xpath('//li[@class="news-item"]')
        for li in list:
            # 详情页链接
            contentUrl = li.xpath("./a/@href").extract_first()
            contentUrl = response.urljoin(contentUrl)
            # 文章标题
            title = li.xpath('./a/div[@class="news-txt l"]/text()').extract_first().strip()
            # 文章发布时间
            times = li.xpath('./a/div[@class="news-date r"]/text()').extract_first().strip()
            if "." in times:
                a = dt.datetime.strptime(times, '%Y.%m.%d')
                pubtime = dt.datetime.strftime(a, '%Y-%m-%d')
            # 获取当前年月日
            nowday = time.strftime("%Y-%m-%d")
            # 当发布时间不是当天时间时，跳出不采
            if pubtime != nowday:
                # print(pubtime + "不是当天最新文章，跳过")
                break
            items = {
                "bid_public_time": pubtime,
                "bid_url": contentUrl,
                "bid_name": title,
                "bid_id": get_md5(contentUrl),
            }
            items.update(items_list)
            yield scrapy.Request(
                contentUrl,
                headers=headers,
                callback=self.getContentInfo,
                meta={"items": items}
            )

    """
    文章详情获取（发布内容、信息来源）
    """
    def getContentInfo(self, response):
        item_info = response.meta["items"]
        # 信息来源
        author = re.search("信息来源：(.*?)】", response.text)
        if author:
            author = author.groups()[0]
        else:
            author = ""
        # 带有html的文本
        str_html_content = etree.HTML(response.text).xpath('//div[@class="article-content"]')
        if str_html_content:
            contentHtml = etree.tostring(str_html_content[0], encoding="utf-8").decode()
        else:
            print("未获取到html文本，可能是网站疯了")
        # 纯净文本
        content = remove_node(contentHtml, ["style", "title"]).text
        # 去掉换行、空格、制表符
        content = re.sub('\s|\t|\n', '', content)
        if "政府采购" in item_info["bid_category"]:
            items_cg = GovernmentProcurementItem()
            items_cg["po_province"] = "山东省"
            items_cg["website_name"] = "日照公共资源交易网"
            items_cg["website_url"] = "http://ggzyjy.rizhao.gov.cn/rzwz/"
            items_cg["po_source"] = author
            items_cg["bo_name"] = item_info.get("bid_name", None)
            items_cg["po_public_time"] = item_info.get("bid_public_time")
            items_cg["po_category"] = item_info.get("bid_category", None)
            items_cg["po_info_type"] = item_info.get("bid_info_type", None)
            items_cg["po_city"] = "日照市"
            items_cg["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            items_cg["bid_url"] = item_info.get("bid_url")
            items_cg["po_id"] = item_info.get("bid_id")
            items_cg["po_html_con"] = contentHtml
            items_cg["po_content"] = content
            # print(
            #     items_cg["po_id"],
            #     items_cg["bid_url"],
            #     items_cg["po_public_time"],
            # )
            yield items_cg
        else:
            ##修改格式
            items_zy = BidScrapyProjectItem(
                bid_city="日照市",
                website_name="日照公共资源交易网",
                website_url="http://ggzyjy.rizhao.gov.cn/rzwz/",
                bid_province="山东省",
            )
            items_zy.update(item_info)
            items_zy["bid_html_con"] = contentHtml
            items_zy["bid_content"] = content
            items_zy["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            items_zy["bid_source"] = author
            # print(
            #     items_zy["bid_id"],
            #     items_zy["bid_url"],
            #     items_zy["bid_public_time"],
            # )
            yield items_zy
