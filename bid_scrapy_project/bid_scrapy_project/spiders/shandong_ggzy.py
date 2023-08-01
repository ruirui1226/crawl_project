#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/30 11:28
# @Author  : qth
# @File    : shandong_ggzy.py
# @Description : 山东省公共资源交易网
import re
import time

import scrapy
from Crypto.Cipher import AES
from gne import GeneralNewsExtractor

from bid_scrapy_project.common.aesDecode import AEScryptor
from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class ShandongGgzySpider(scrapy.Spider):
    name = "shandong_ggzy"

    def __init__(self):
        self.province = "山东省"
        self.cookies = {
            "_gscu_740847421": "85950495pev0tv87",
            "clientlanguage": "zh_CN",
            "_gscbrs_740847421": "1",
            "_gscs_740847421": "86033140gslpul87|pv:56",
            "JSESSIONID": "759BBDAA945BEF91CAB151502034A66C",
        }
        self.webName = "山东省公共资源交易网"
        self.webUrl = "http://www.sdggzyjy.gov.cn"
        # http://www.sdggzyjy.gov.cn/queryContent-jyxxgk.jspx
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "http://www.sdggzyjy.gov.cn",
            "Pragma": "no-cache",
            "Referer": "http://www.sdggzyjy.gov.cn/queryContent_2-jyxxgk.jspx",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        }
        self.key = b"qnbyzzwmdgghmcnm"
        self.aes = AEScryptor(
            self.key, AES.MODE_ECB, paddingMode="PKCS7Padding", characterSet="utf-8", isHeskey_iv=True
        )
        self.categorys = {
            "工程建设": 78,
            "土地使用权": 80,
            "矿业权出让": 81,
            "国有产权": 83,
            "政府采购": 79,
            "药械采购": 84,
            "国企采购": 167,
            "权益类": 179,
            "其他交易": 162,
        }
        self.page = 4

    def start_requests(self):
        for categoname, categoid in self.categorys.items():
            data = {
                "title": "",
                "origin": "省级",
                "inDates": "",
                "channelId": "{}".format(categoid),
                "ext": "",
            }
            for i in range(1, self.page):
                yield scrapy.FormRequest(
                    "http://www.sdggzyjy.gov.cn/queryContent_{}-jyxxgk.jspx".format(i),
                    formdata=data,
                    callback=self.parse,
                    headers=self.headers,
                    cookies=self.cookies,
                    meta={"items": {"bid_category": categoname}},
                    dont_filter=True
                )

    def parse(self, response, **kwargs):
        url_li = response.xpath("//div[@class='article-list3-t']/a/@href").extract()
        time_li = response.xpath("//div[@class='list-times']//text()").extract()
        category_li = response.xpath("//div[@class='article-list3-t2']//div[2]/text()").extract()
        type_li = response.xpath("//div[@class='article-list3-t2']//div[3]/text()").extract()
        souce_li = response.xpath("//div[@class='article-list3-t2']//div[1]/text()").extract()
        for i in range(len(url_li)):
            url = self.detail_url(url_li[i])
            b_id = re.search(r"http:\/\/.*\/(\d+)\.jhtml.*", url_li[i])
            items_info = {
                # "bid_category": category_li[i].split("：")[1],
                "bid_id": get_md5(str(b_id.group(1))),
                "bid_md5_url": get_md5(self.detail_url(url_li[i])),
                "bid_info_type": type_li[i].split("：")[1],
                "bid_source": souce_li[i].split("：")[1],
                "bid_public_time": time_li[i],
            }
            items_info.update(response.meta["items"])
            yield scrapy.Request(
                url, cookies=self.cookies, headers=self.headers, callback=self.contentParse, meta={"items": items_info}
            )
        ##翻页直到没有
        # print("下一页")
        # nextUrl = response.css("#nextPage::attr(data-url)").get()
        # if nextUrl:
        #     nextUrl = response.urljoin(nextUrl)
        #     yield scrapy.Request(
        #         nextUrl,
        #         callback=self.parse,
        #         headers=self.headers,
        #         cookies=self.cookies,
        #         meta=response.meta
        #     )

    def contentParse(self, response):
        item_info = response.meta["items"]
        bid_html_con = response.xpath("//table[@class='gycq-table']").extract_first()
        bid_content = self.parse_news(response.text).get("content", "")
        bid_name = response.xpath('//div[@class="div-title"]//text()').extract_first()
        item = {
            "bid_id": item_info.get("bid_id"),
            # "bid_md5_url": item_info.get("bid_md5_url"),
            "bid_name": bid_name.strip(),
            "create_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            "bid_url": response.request.url,
            "bid_category": item_info.get("bid_category"),
            "bid_info_type": item_info.get("bid_info_type"),
            "bid_source": item_info.get("bid_source"),
            "bid_public_time": item_info.get("bid_public_time"),
            "bid_html_con": bid_html_con,
            "bid_content": bid_content,
            "bid_province": self.province,
            "website_name": self.webName,
            "website_url": self.webUrl,
        }
        if "政府采购" in item_info.get("bid_category"):
            items = GovernmentProcurementItem()
            items["po_id"] = item_info.get("bid_id")
            items["bid_url"] = response.request.url
            items["po_province"] = self.province
            items["po_category"] = item_info.get("bid_category")
            items["po_info_type"] = item_info.get("bid_info_type")
            items["po_public_time"] = item_info.get("bid_public_time")
            items["bo_name"] = bid_name.strip()
            items["po_source"] = item_info.get("bid_source")
            items["po_html_con"] = bid_html_con
            items["po_content"] = bid_content
            items["website_name"] = self.webName
            items["website_url"] = self.webUrl
            items["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        else:
            items = BidScrapyProjectItem()
            items.update(item)
        # print(items)
        yield items

    # 工具
    def detail_url(self, d_url):
        """
        获取 信息详情页链接  aes
        """

        url_id = d_url[d_url.rindex(f"/") + len(f"/") : d_url.rindex(f".")]
        url_new_id = self.aes.encryptFromString(url_id).toBase64()
        url_new_id = url_new_id.replace(f"/", "^").replace("=", "")
        new_url = d_url[: d_url.rindex(f"/") + 1] + url_new_id + d_url[d_url.rindex(f".") :]
        return new_url

    def parse_news(self, html):
        extractor = GeneralNewsExtractor()
        result = extractor.extract(html)
        return result