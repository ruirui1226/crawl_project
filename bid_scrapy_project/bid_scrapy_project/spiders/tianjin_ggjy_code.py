# -*- coding: utf-8 -*-
"""
@desc: 天津市公共资源交易平台-方法调用
@version: python3
@author: shenr
@time: 2023/07/11
"""
import base64
import json
import os
import re
import time
import logging
from Crypto.Cipher import AES
import execjs
import requests
import scrapy
from pyquery import PyQuery as pq

from bid_scrapy_project.common.aesDecode import AEScryptor
from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


# def get_detail_url(d_url):
#     with open(rf"{os.getcwd()}\bid_scrapy_project\js_file\cryptourl_tianjin.js", "r", encoding="utf-8") as f:
#         js = execjs.compile(f.read())
#     p = js.call("getCryptoUrl", d_url)
#     logger.debug(p)
#     return p


def get_detail_url(aes, d_url):
    """
    获取 信息详情页链接  aes
    """

    url_id = d_url[d_url.rindex(f"/") + len(f"/"): d_url.rindex(f".")]
    url_new_id = aes.encryptFromString(url_id).toBase64()
    url_new_id = url_new_id.replace(f"/", "^").replace("=", "")
    new_url = d_url[: d_url.rindex(f"/") + 1] + url_new_id + d_url[d_url.rindex(f"."):]
    return new_url


class ExampleSpider(scrapy.Spider):
    name = "tianjin_ggjy_1"
    # allowed_domains = ["http://ggzy.zwfwb.tj.gov.cn/jyxx/index.jhtml"]
    start_urls = [
        "http://ggzy.zwfwb.tj.gov.cn/jyxx/index.jhtml",
        "http://ggzy.zwfwb.tj.gov.cn/jyxxgcjs/index.jhtml",
        "http://ggzy.zwfwb.tj.gov.cn/jyxxky/index.jhtml",
        "http://ggzy.zwfwb.tj.gov.cn/jyxxcq/index.jhtml",
        "http://ggzy.zwfwb.tj.gov.cn/jygknccq/index.jhtml",
        "http://ggzy.zwfwb.tj.gov.cn/jyxxkyq/index.jhtml",
        "http://ggzy.zwfwb.tj.gov.cn/jyxxel/index.jhtml",
        "http://ggzy.zwfwb.tj.gov.cn/jyxxyy/index.jhtml",
        "http://ggzy.zwfwb.tj.gov.cn/jyxxtp/index.jhtml",
        "http://ggzy.zwfwb.tj.gov.cn/jyxxpw/index.jhtml",
        "http://ggzy.zwfwb.tj.gov.cn/jyxxlq/index.jhtml",
        "http://ggzy.zwfwb.tj.gov.cn/jyxxzs/index.jhtml",
        "http://ggzy.zwfwb.tj.gov.cn/jyxxqt/index.jhtml",
    ]
    page = 1
    page_all = 1
    current_time = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
    key_ = b"qnbyzzwmdgghmcnm"
    aes = AEScryptor(
        key_, AES.MODE_ECB, paddingMode="PKCS7Padding", characterSet="utf-8", isHeskey_iv=True
    )

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Referer": "http://ggzy.zwfwb.tj.gov.cn/jyxx/index.jhtml",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }
    cookies = {"JSESSIONID": "CF99B77962BF73838F84A32CD369397E", "clientlanguage": "zh_CN"}

    def start_requests(self):
        for url_ in self.start_urls:
            yield scrapy.Request(
                url=url_,
                headers=self.headers,
                # cookies=self.cookies,
                dont_filter=True,
                callback=self.parse_1,
                meta={"url_start": url_}
            )
            # break

    def parse_1(self, response, **kwargs):
        if int(response.status) == 200:
            res = pq(response.text)
            logging.debug(f"============当前爬取{self.page}页==========")
            data_res = res('ul[class="article-list2"] li')
            meta = response.meta
            for each in data_res.items():
                detail_url = each('div a').attr("url")
                detail_url_ = get_detail_url(self.aes, detail_url)
                title = each('div a').text()
                release_time = each('div div').text().replace(" ", "")
                self.page_time = release_time[:10]
                yield scrapy.Request(
                    url=detail_url_,
                    headers=self.headers,
                    cookies=self.cookies,
                    callback=self.detail_parse,
                    meta={
                        "id_": "id_",
                        "md5_url": detail_url,
                        "url_start": meta.get("url_start"),
                    }
                )
            if self.current_time == self.page_time:
                self.page += 1
                yield scrapy.Request(
                    url=f"http://ggzy.zwfwb.tj.gov.cn/jyxx/index_{self.page}.jhtml",
                    headers=self.headers,
                    # cookies=self.cookies,
                    dont_filter=True,
                    callback=self.parse_1,
                    meta={"url_start": meta.get("url_start")},
                )
        else:
            logging.debug("=====================爬取结束==================")

    def detail_parse(self, response, **kwargs):
        logging.debug("进入详情页=================")
        res = pq(response.text)
        meta = response.meta
        url_start = meta.get("url_start")
        title = res('div[class="content-title"]').text()
        bid_source = res('div[class="content-title2"] span').eq(1).text()
        time_ = res('div[class="content-title2"] span').eq(0).text()
        content = res('div[class="content-article"]').text().replace("'", '"')
        html_content = res('div[class="content-article"]').html().replace("'", '"')
        if res('div[class="sitemap"] a').eq(2).text() == "政府采购":
            item = GovernmentProcurementItem()
            item["po_id"] = get_md5(re.findall('.*/(.*?).jhtml', meta.get("md5_url"), re.S)[0])
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = response.url
            # item["bid_md5_url"] = meta.get("md5_url")
            item["po_province"] = "天津市"
            item["po_city"] = ""
            item["po_county"] = ""
            item["po_category"] = res('div[class="sitemap"] a').eq(2).text()
            item["po_info_type"] = res('div[class="sitemap"] a').eq(3).text()
            item["po_source"] = bid_source
            item["bo_name"] = title
            item["po_public_time"] = time_
            item["po_html_con"] = html_content
            item["po_content"] = content
            item["description"] = ""
            item["website_name"] = "天津市公共资源交易平台"
            item["website_url"] = url_start
            yield item
        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = get_md5(re.findall('.*/(.*?).jhtml', meta.get("md5_url"), re.S)[0])
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = response.url
            item["bid_md5_url"] = meta.get("md5_url")
            item["bid_province"] = "天津市"
            item["bid_city"] = ""
            item["bid_county"] = ""
            item["bid_category"] = res('div[class="sitemap"] a').eq(2).text()
            item["bid_info_type"] = res('div[class="sitemap"] a').eq(3).text()
            item["bid_source"] = bid_source
            item["bid_name"] = title
            item["bid_public_time"] = time_
            item["bid_html_con"] = html_content
            item["bid_content"] = content
            item["description"] = ""
            item["website_name"] = "天津市公共资源交易平台"
            item["website_url"] = url_start
            yield item
            logging.debug("========", item)

