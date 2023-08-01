# -*- coding: utf-8 -*-
"""
@desc: 招商局集团电子招标采购交易平台
@version: python3
@author: liuwx
@time: 2023/07/13
"""
import re
import scrapy
import time

from lxml import etree
from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import BidScrapyProjectItem

class ZhjjtCgSpider(scrapy.Spider):
    name = 'zhjjt_cg'
    # 网站有封控，需要降低请求频率
    custom_settings = {"CONCURRENT_REQUESTS": 1, 'DOWNLOAD_DELAY': 3}

    """
    二级类型 直接列出
    """
    def __init__(self):
        self.infoType = {
            "招标": '10',
            "询价采购": '1',
            "单一来源": '5',
            "竞争性谈判": '6',
            "竞价采购": '3',
            "网上竞买": '4',
            "电子竞价": '9',
            "市场询价": '2',
        }

    """
    列表页链接请求
    """
    def start_requests(self):
        for info_type, categorynum in self.infoType.items():
            # 翻页 1-4
            for page in range(1, 5):
                items = {
                    "bid_info_type": info_type,  # 二级类型
                }
                # 列表页接口获取
                link = "https://dzzb.ciesco.com.cn/gg/cgggList"
                # param = '{"pageNum":1,"pageSize":80,' + categorynum + '"likeKey":"","purCompanyName":"","orgLevel":"","publishTimeBegin":"","publishTimeEnd":""}'
                param = "currentPage="+str(page)+"&xmLeiXing=&zbFangShi="+categorynum+"&jiTuanId=&danWei=&xm_BH=&ggName=&zbr=&danWeiName=&keyWord="
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Referer': 'https://dzzb.ciesco.com.cn/gg/cgggList',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                    'Cookie': 'SF_cookie_199=27817826'
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
        items_list = response.meta["items"]
        list = response.xpath('//div[@class="list-content-between"][1]')
        for li in list:
            # 详情页链接
            contentUrl = li.xpath("./span/span/a/@href").extract_first()
            contentUrl = response.urljoin(contentUrl)
            # 截取文章id
            if "guid=" in contentUrl and "&xinXiLaiYuan" in contentUrl:
                newsId = re.search("guid=(.*?)&xinXiLaiYuan", contentUrl).group(1)
            # 文章标题
            title = li.xpath('./span/span/a/@title').extract_first().strip()
            # 文章发布时间
            pubtime = li.xpath('./span[@class="list-content-end"]/text()').extract_first().strip()
            # 获取当前年月日
            nowday = time.strftime("%Y-%m-%d")
            # 当发布时间不是当天时间时，跳出不采
            if pubtime != nowday:
                # print(pubtime + "不是当天最新文章，跳过")
                break
            # 详情页获取链接
            link = "https://node.dzzb.ciesco.com.cn/xunjia-mh/gonggaoxinxi/gongGao_view_3.html?guid="+ newsId +"&callBackUrl=https://dzzb.ciesco.com.cn/html/crossDomainForFeiZhaoBiao.html"
            items = {
                "bid_public_time": pubtime,
                "bid_url": contentUrl,
                "bid_name": title,
                "bid_id": get_md5(contentUrl),
            }
            items.update(items_list)
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
        # 带有html的文本
        str_html_content = etree.HTML(response.text).xpath('//div[@class="divMainContent"]')
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
        items_infos['website_name'] = "招商局集团电子招标采购交易平台"
        items_infos['website_url'] = "https://dzzb.ciesco.com.cn/"
        items_infos['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        # print(
        #     items_infos["bid_id"],
        #     items_infos["bid_url"],
        #     items_infos["bid_public_time"]
        # )
        yield items_infos