#!/usr/bin/conf python
# -*- coding: utf-8 -*-
"""
@desc: 招投标-山东省-滨州
@version: python3
@author: qth
@time: 2023/06/08
"""

import time
import re
from urllib.parse import urljoin

import requests
import execjs
from gne import GeneralNewsExtractor
from loguru import logger
from scrapy import Selector

from bid_project.conf import env_demo
from bid_project.untils.common import get_md5
from bid_project.untils.pysql import MysqlPipelinePublic


def parse_news(html):
    extractor = GeneralNewsExtractor()
    result = extractor.extract(html)
    return result


def binzhou_list(headers, cookies, res):
        sel = Selector(res)
        url_li = sel.xpath("//li[@class='list-item']//a/@href").extract()
        time_li = sel.xpath("//li[@class='list-item']//a/span//text()").extract()
        items = []
        for i in range(len(url_li)):
            url = urljoin(res.url, url_li[i])
            res = requests.get(url=url, headers=headers, cookies=cookies)
            sels = Selector(res)
            bid_html_con = str(sels.xpath("//div[@class='article-info']").extract_first()).replace("'", '"'),
            bid_content = parse_news(res.text).get("content", "")
            bid_name = sels.xpath('//div[@class="article"]/h3//text()').extract_first()
            b_id = re.search(r"/(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})\.html$", url)
            category = sels.xpath("//div[@class='location mt12']/a[2]//text()").extract_first()
            type = sels.xpath("//div[@class='location mt12']/a[3]//text()").extract_first()
            souce = 'None'
            bid_county = sels.xpath("//a[@class='current']//text()").extract_first()
            item = {
                "bid_id": get_md5(str(b_id.group(1))),
                "bid_md5_url": get_md5(url),
                "bid_name": bid_name,
                "create_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
                "bid_url": url,
                "bid_category": category,
                "bid_info_type": type,
                "bid_source": souce,
                "bid_public_time": time_li[i].strip(),
                "bid_html_con": bid_html_con,
                "bid_content": bid_content,
                "bid_city": '滨州市',
                "bid_county": bid_county
            }
            items.append(item)
        return items


def main():

    cookies = {
        'userGuid': '-1177458307',
        'oauthClientId': '58617b43-2d97-4734-8718-1215fce30dd5',
        'oauthPath': 'http://jypt.bzggzyjy.cn/TPFrame',
        'oauthLoginUrl': 'http://127.0.0.1:1112/membercenter/login.html?redirect_uri=',
        'oauthLogoutUrl': '',
        'noOauthRefreshToken': 'a5e12a2dc94301805462bfab6079c893',
        'noOauthAccessToken': 'c4fb6fa7395af46ca1953bb5f9dd2bc0',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        # 'Cookie': 'userGuid=-1177458307; oauthClientId=58617b43-2d97-4734-8718-1215fce30dd5; oauthPath=http://jypt.bzggzyjy.cn/TPFrame; oauthLoginUrl=http://127.0.0.1:1112/membercenter/login.html?redirect_uri=; oauthLogoutUrl=; noOauthRefreshToken=a5e12a2dc94301805462bfab6079c893; noOauthAccessToken=c4fb6fa7395af46ca1953bb5f9dd2bc0',
        'Pragma': 'no-cache',
        'Referer': 'http://jypt.bzggzyjy.cn/bzweb/jyxx/012002/012002003/list1.html',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }
    one_res = requests.get('http://jypt.bzggzyjy.cn/bzweb/jyxx/list1.html', headers=headers, cookies=cookies)
    sel1 = Selector(one_res)
    url_li1 = sel1.xpath('//a[@class="info-more r"]//@href').extract()
    for i in url_li1:
        url = urljoin(one_res.url, i)
        two_res = requests.get(url=url, headers=headers, cookies=cookies)
        sel2 = Selector(two_res)
        url_li2 = sel2.xpath("//a[@class='info-more r']//@href").extract()
        for u in url_li2:
            url2 = urljoin(one_res.url, u)
            response = requests.get(
                url=url2,
                cookies=cookies,
                headers=headers,
                verify=False,
            )
            sel = Selector(response)
            city_li = sel.xpath("//a[@class='info-more r']/@href").extract()
            for c in city_li:
                urls = urljoin(response.url, c)
                res = requests.get(url=urls, cookies=cookies, headers=headers)
                items = binzhou_list(headers, cookies, res)

                try:
                    mq = MysqlPipelinePublic()
                    for item in items:
                        mq.insert_sql("t_zx_bid_crawl_info", item)
                        logger.info("数据%s 插入成功" % item)
                    mq.close()

                except Exception as e:
                    logger.debug(e)


if __name__ == '__main__':
    main()

