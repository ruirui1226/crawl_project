#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/1 16:51
# @Author  : xm
# @File    : youzhiceng_bid.py
# @Description :优质采云采购平台
import time

import pyDes
import scrapy

from bid_scrapy_project.common.aesDecode import Descryptor
from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem


class YouzhicaiBidSpider(scrapy.Spider):
    name = "youzhicai_bid"
    custom_settings = {"CONCURRENT_REQUESTS": 1}

    def __init__(self):
        self.categorys = {"招标": "1", "询比": "2", "招募": "3", "竞价": "4"}
        self.info_types = {"招标公告": "1", "澄清/变更公告": "5", "结果公示": "2", "交易见证书": "8", "招标项目计划": "9"}
        self.website_name = "优质采云采购平台"
        self.webUrl = "https://www.youzhicai.com/"
        self.headers = {
            "Host": "www.youzhicai.com",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Referer": "https://www.youzhicai.com/sn/1102.html",
            # 'Cookie': 'qddac=3-3-1.3tnzd2.8xhjnq.lkti0xc1; __root_domain_v=.youzhicai.com; _qddaz=QD.380190878440086; ASP.NET_SessionId=ziw1muj1tlrwhsxm4eoodiuo; _qdda=3-1.3tnzd2; _qddab=3-8xhjnq.lkti0xc1; Hm_lvt_9511d505b6dfa0c133ef4f9b744a16da=1689556614,1689578385,1690878440,1690966889; Hm_lpvt_9511d505b6dfa0c133ef4f9b744a16da=1690966889; vue_admin_template_token=false; spvrscode=8bb93171aa51f8de275b38b23dbba57c2e6231a2f672102e0a50b00f2ee91a7f1918e16d99138fb9109e5e083db64838bb6ea2607708f7dea385531ae3c168eba3281a59878538b584e15a67309958c0b9a08fe856e83810e6989104c1329eed48eadd5650f2459100dc151e8d8029c5e5032876e440703c66fb55bddc3c0e51f592b3c169dd91ec; ASP.NET_SessionId=zaqfxthcyrnhcpxmjwjce5dy'
        }

    def start_requests(self):
        for cates, cateid in self.categorys.items():
            for infoname, infoid in self.info_types.items():
                url = "https://www.youzhicai.com/sn/{}{}02.html".format(cateid, infoid)
                items = {"category": cates, "info_type": infoname}
                yield scrapy.Request(url, callback=self.getCookie, dont_filter=True, meta={"items": items})

    def getCookie(self, response):
        # 获取到key 和b des
        resText = response.text
        if "<title>" in resText:
            # 处理
            lis = response.css("div.projects > ul > li")
            for li in lis:
                if not li.css("a").get():
                    continue
                href = li.css("a::attr(href)").get()
                href = response.urljoin(href)
                title = li.css("a::attr(title)").get()
                pubdate = li.css(".pub-value0::text").get()

                source = li.css("a.pub-company0.el::text").get()
                items = {"href": href, "title": title, "pubdate": pubdate, "source": source}
                items.update(response.meta["items"])
                yield scrapy.Request(url=href, callback=self.getContentCookie, dont_filter=True, meta={"items": items})
        else:
            ##出现非授权问题  需要解决  list and content
            try:
                key = resText[resText.index("var a= '") + len("var a= '") : resText.index("';var b")]
            except:
                print("非授权了，记录一下")
                return
            value = resText[resText.index("var b = '") + len("var b = '") : resText.index("';var _0x754f")]
            cookie = None
            try:
                cookie = (Descryptor().des_encrypt(value, key, pyDes.ECB, pyDes.PAD_PKCS5)).toHexStr()
            except:
                print("cookie获取报错 原因不明，需测试")
            cookies = {"spvrscode": cookie}
            # print(cookies)
            yield scrapy.Request(
                response.url,
                callback=self.parse,
                dont_filter=True,
                meta={"items": response.meta["items"]},
                cookies=cookies,
            )

    def parse(self, response, **kwargs):
        """
        第一遍访问获取到第二遍访问需要的cookie
        des ecb pkcs7 加密 可用pkcs5
        """
        if "非授权验证" in response.text:
            print("列表页cookie问题")
            return
        lis = response.css("div.projects > ul > li")
        for li in lis:
            if not li.css("a").get():
                continue
            href = li.css("a::attr(href)").get()
            href = response.urljoin(href)
            title = li.css("a::attr(title)").get()
            pubdate = li.css(".pub-value0::text").get()
            source = li.css("a.pub-company0.el::text").get()
            items = {"href": href, "title": title, "pubdate": pubdate, "source": source}
            items.update(response.meta["items"])
            yield scrapy.Request(url=href, callback=self.getContentCookie, dont_filter=True, meta={"items": items})

    def getContentCookie(self, response):
        resText = response.text
        if "<title>" in resText:
            # 处理
            item_info = response.meta["items"]
            content_html = response.css('.tabContent > ul > li[style="display: block;"]').get()
            contents = response.css('.tabContent > ul > li[style="display: block;"] *::text').extract()
            content = "".join(contents)
            items = {
                "bid_id": get_md5(item_info["href"]),
                "bid_url": item_info["href"],
                "bid_category": item_info["category"],
                "bid_info_type": item_info["info_type"],
                "bid_public_time": item_info["pubdate"],
                "bid_name": item_info["title"],
                "bid_source": item_info["source"],
                "bid_html_con": content_html,
                "bid_content": content,
                "website_name": self.website_name,
                "website_url": self.webUrl,
                "create_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            }
            item_bid = BidScrapyProjectItem()
            item_bid.update(items)
            # print(items)
            yield item_bid
        else:
            try:
                key = resText[resText.index("var a= '") + len("var a= '") : resText.index("';var b")]
            except:
                print("非授权了，记录一下")
                return
            value = resText[resText.index("var b = '") + len("var b = '") : resText.index("';var _0x754f")]
            cookie = (Descryptor().des_encrypt(value, key, pyDes.ECB, pyDes.PAD_PKCS5)).toHexStr()
            cookies = {"spvrscode": cookie}
            # print("详情页cookie", cookies)
            yield scrapy.Request(
                response.url, callback=self.contentParse, meta={"items": response.meta["items"]}, cookies=cookies
            )

    def contentParse(self, response):
        if "非授权页" in response.text:
            print("详情页cookie问题")
            return
        item_info = response.meta["items"]
        content_html = response.css('.tabContent > ul > li[style="display: block;"]').get()
        contents = response.css('.tabContent > ul > li[style="display: block;"] *::text').extract()
        content = "".join(contents)
        items = {
            "bid_id": get_md5(item_info["href"]),
            "bid_url": item_info["href"],
            "bid_category": item_info["category"],
            "bid_info_type": item_info["info_type"],
            "bid_public_time": item_info["pubdate"],
            "bid_name": item_info["title"],
            "bid_source": item_info["source"],
            "bid_html_con": content_html,
            "bid_content": content,
            "website_name": self.website_name,
            "website_url": self.webUrl,
            "create_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        }
        item_bid = BidScrapyProjectItem()
        item_bid.update(items)
        # print(items)
        yield item_bid
