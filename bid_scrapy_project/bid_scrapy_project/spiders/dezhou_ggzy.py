#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/30 13:29
# @Author  : xm
# @File    : dezhou_ggzy.py
# @Description : 德州市公共资源交易中心
import json
import re
import time

import scrapy
from bs4 import BeautifulSoup
from gne import GeneralNewsExtractor

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class DezhouGgzySpider(scrapy.Spider):
    name = "dezhou_ggzy"

    def __init__(self):
        self.cookies = {
            "userGuid": "-1177458307",
            "oauthClientId": "demoClient",
            "oauthPath": "http://10.2.129.27:8080/EpointWebBuilder",
            "oauthLoginUrl": "http://10.2.129.27:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=",
            "oauthLogoutUrl": "http://10.2.129.27:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=",
            "noOauthRefreshToken": "3f2148188634872555e5fdca9da1337f",
            "noOauthAccessToken": "4430ab8dcb9685404401e9c45f57f8f1",
        }

        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            # 'Cookie': 'userGuid=-1177458307; oauthClientId=demoClient; oauthPath=http://10.2.129.27:8080/EpointWebBuilder; oauthLoginUrl=http://10.2.129.27:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://10.2.129.27:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=3f2148188634872555e5fdca9da1337f; noOauthAccessToken=4430ab8dcb9685404401e9c45f57f8f1',
            "Pragma": "no-cache",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        }
        self.province = "山东省"
        self.apiUrl = "http://ggzyjy.dezhou.gov.cn/EpointWebBuilder/rest/frontAppCustomAction/getInfoUrlByInfoid"
        self.page = 3

    def start_requests(self):
        category = "http://ggzyjy.dezhou.gov.cn/TPFront/xmxx/moreinfo2.html"
        yield scrapy.Request(category, callback=self.parse, headers=self.headers, cookies=self.cookies,dont_filter=True)

    def parse(self, response, **kwargs):
        """
        一级分类
        """
        type_li = response.xpath('//a[@class="block-link"]')
        for type in type_li:
            type_url = type.css("a::attr(href)").get()
            category = type.css("a::text").get()
            if "综合交易" in category:
                continue
            type_url = response.urljoin(type_url)
            yield scrapy.Request(type_url, callback=self.listParse, meta={"items": {"category": category}},dont_filter=True)

    def listParse(self, response):
        """
        二级分类
        """

        tr_li = response.xpath("//a[@class='block-link']")
        for tr in tr_li:
            trUrl = tr.css("a::attr(href)").get()
            tr_url = response.urljoin(trUrl)
            info_type = tr.css("a::text").get()
            items = {"info_type": info_type}
            items.update(response.meta["items"])
            yield scrapy.Request(
                tr_url, headers=self.headers, cookies=self.cookies, callback=self.dezhou_list, meta={"items": items},dont_filter=True
            )

    def dezhou_list(self, response):
        city_li = response.css("a.block-link")
        itme_info = response.meta["items"]
        if city_li:
            for c in city_li:
                cityName = c.css("a::text").get()
                city_href = c.css("a::attr(href)").get()
                for p in range(1, self.page):
                    if p == 1:
                        url = response.urljoin(city_href)
                        items = {"bid_county": cityName}
                        items.update(itme_info)
                        yield scrapy.Request(
                            url,
                            headers=self.headers,
                            cookies=self.cookies,
                            callback=self.dezhou_info,
                            meta={"items": items},
                            dont_filter=True
                        )
                    else:
                        try:
                            link = re.search(r"/(\d+/\d+/\d+)/moreinfo2", city_href).group(1)
                        except:
                            print("")
                            continue
                        url = "http://ggzyjy.dezhou.gov.cn/TPFront/xmxx/" + link + "/{}.html".format(p)
                        items = {"bid_county": cityName}
                        items.update(itme_info)
                        yield scrapy.Request(
                            url,
                            headers=self.headers,
                            cookies=self.cookies,
                            callback=self.dezhou_info,
                            meta={"items": items},
                            dont_filter=True
                        )
        else:
            for p in range(1, self.page):
                # http://ggzyjy.dezhou.gov.cn/TPFront/xmxx/004001/004001002/004001002001/20230421/000dd25e-0dbe-4a53-86dd-e124b7c0dc50.html
                # http://ggzyjy.dezhou.gov.cn/TPFront/xmxx/004001/004001001/004001001001/20230613/fb47edf7-8e98-48f4-b440-06877e26fef8.html
                # http://ggzyjy.dezhou.gov.cn/TPFront/xmxx/004001/004001002/004001002001/20230421/000dd25e-0dbe-4a53-86dd-e124b7c0dc50.html
                #                                                                          infoid=000dd25e-0dbe-4a53-86dd-e124b7c0dc50
                url = response.request.url
                if p == 1:  # http://ggzyjy.dezhou.gov.cn/TPFront/xmxx/004001/004001001/moreinfo2_jsgc.html
                    yield scrapy.Request(
                        url,
                        headers=self.headers,
                        cookies=self.cookies,
                        callback=self.dezhou_info,
                        meta={"items": itme_info},
                        dont_filter=True
                    )
                else:  # http://ggzyjy.dezhou.gov.cn/TPFront/xmxx/004001/004001001/3.html
                    link = re.search(r"/(\d+/\d+)/", url).group(1)
                    url = "http://ggzyjy.dezhou.gov.cn/TPFront/xmxx/" + link + "{}.html".format(p)
                    yield scrapy.Request(
                        url,
                        headers=self.headers,
                        cookies=self.cookies,
                        callback=self.dezhou_info,
                        meta={"items": itme_info},
                        dont_filter=True
                    )

    def dezhou_info(self, response):
        items_info = response.meta["items"]
        info_li = response.xpath('//li[@class="ewb-list-node clearfix"]/a').extract()
        time_li = response.xpath('//span[@class="ewb-list-date"]/text()').extract()
        if not time_li:
            print()
            return
        for i in range(len(time_li)):
            date_info = time_li[i].replace("-", "")
            title = BeautifulSoup(info_li[i], "lxml").text
            link = BeautifulSoup(info_li[i], "lxml").select("a")[0].attrs["href"]
            # link = info_li[i]
            if "infoid" in link:
                ##有加密的链接的情况   链接在post中
                infoid = None
                try:
                    infoid = re.search(r"infoid=([\w-]+)", link).group(1)
                except:
                    print("正则获取失败", link)
                ##/xmxx/004003/004003001/004003001001/20230523/ad634cd1-8788-4179-9901-ca59e7f53277.html
                # http://ggzyjy.dezhou.gov.cn/TPFront/ZtbDyDetail_tdcr.html?infoid=ad634cd1-8788-4179-9901-ca59e7f53277&categorynum=004003001001&relationguid=46e7bece-d141-46b6-99d9-88ee975730c4%3B45522e65-3fe3-4215-8ca4-0e6db2bca071%3B
                # http://ggzyjy.dezhou.gov.cn/TPFront/xmxx/004003/004003003/004003003009/moreinfo2_tdcr.html
                ##处理 response.url
                ## 获取 接口 url
                # http://ggzyjy.dezhou.gov.cn/EpointWebBuilder/rest/frontAppCustomAction/getInfoUrlByInfoid
                # params={"siteGuid":"7eb5f7f1-9041-43ad-8e13-8fcb82ea831a","infoid":"f989a557-cefe-4a6e-b9da-44b82dc4b85f","categorynum":"004006004006001"}
                list_ids = response.url[(response.url).index(r"xmxx/") + len(r"xmxx/") : (response.url).rindex(r"/")]
                cidid = list_ids[list_ids.rindex(r"/") + len(r"/") :]
                params = {
                    "params": '{"siteGuid":"7eb5f7f1-9041-43ad-8e13-8fcb82ea831a","infoid":"'
                    + infoid
                    + '","categorynum":"'
                    + cidid
                    + '"}'
                }
                url = "http://ggzyjy.dezhou.gov.cn/TPFront/xmxx/" + list_ids + "r/" + date_info + r"/" + infoid
                headerApi = {"Content-Type": "application/x-www-form-urlencoded"}
                items = {"title": title}
                items.update(items_info)
                yield scrapy.FormRequest(
                    url=self.apiUrl,
                    formdata=params,
                    callback=self.apiParse,
                    headers=headerApi,
                    meta={"time_li": time_li[i], "items": items},
                    cookies=self.cookies,
                    dont_filter=True
                )
            else:
                items = {"title": title}
                items.update(items_info)
                url = response.urljoin(link)
                yield scrapy.Request(
                    url=url,
                    headers=self.headers,
                    cookies=self.cookies,
                    callback=self.getContent,
                    meta={"time_li": time_li[i], "items": items},
                )

    def apiParse(self, response):
        time_li = response.meta["time_li"]
        jsonDict = json.loads(response.text)
        try:
            infourl = jsonDict.get("custom").get("infourl")
        except:
            return
        if not infourl:
            return
        infourl = "http://ggzyjy.dezhou.gov.cn/TPFront" + infourl
        yield scrapy.Request(
            infourl,
            headers=self.headers,
            cookies=self.cookies,
            callback=self.getContent,
            meta={"time_li": time_li, "items": response.meta["items"]},
        )

    def getContent(self, response):
        items_info = response.meta["items"]
        time_li = response.meta["time_li"]
        bid_html_con = str(response.xpath('//div[@class="article-content"]').get()).replace("'", '"')
        if not bid_html_con:
            pass
        bid_content = self.parse_news(response.text).get("content", "")
        bid_name = response.xpath('//h2[@class="article-title"]//text()').extract_first()
        if not bid_name:
            print("")
        try:
            b_id = re.search(r"/([\w-]+\.html)$", response.request.url).group(1)[:-5]
        except:
            return
        category = response.xpath("//div[@class='ewb-location']/span[1]//text()").extract_first()
        type = response.xpath("//div[@class='ewb-location']/span[2]//text()").extract_first()
        souce = "德州市公共资源交易中心"
        bid_county = response.xpath('//span[@id="viewGuid"]//text()').extract_first()
        bid_countys = bid_county if bid_county else "None"
        item = {
            "bid_id": get_md5(str(b_id)),
            "bid_md5_url": get_md5(response.request.url),
            "bid_name": items_info["title"],
            "create_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            "bid_url": response.request.url,
            "bid_category": items_info.get("category"),
            "bid_info_type": items_info.get("info_type"),
            "bid_source": souce,
            "bid_public_time": time_li.strip(),
            "bid_html_con": bid_html_con,
            "bid_content": bid_content,
            "bid_city": "德州市",
            "bid_county": items_info.get("bid_county"),
            "bid_province": self.province,
            "website_name": "德州市公共资源交易中心",
            "website_url": "http://ggzyjy.dezhou.gov.cn/",
        }
        if "政府采购" in items_info.get("category"):
            items = GovernmentProcurementItem()
            items["po_id"] = get_md5(str(b_id))
            items["bid_url"] = response.request.url
            items["po_province"] = self.province
            items["po_city"] = "德州市"
            items["po_category"] = items_info.get("category")
            items["po_info_type"] = items_info.get("info_type")
            items["po_public_time"] = time_li.strip()
            items["bo_name"] = items_info["title"]
            items["po_source"] = souce
            items["po_html_con"] = bid_html_con
            items["po_content"] = bid_content
            items["po_county"] = items_info.get("bid_county")
            items["website_name"] = "德州市公共资源交易中心"
            items["website_url"] = "http://ggzyjy.dezhou.gov.cn/"
            items["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        else:
            items = BidScrapyProjectItem()
            items.update(item)
        # print(item["bid_id"])
        yield items

    def parse_news(self, html):
        extractor = GeneralNewsExtractor()
        result = extractor.extract(html)
        return result
