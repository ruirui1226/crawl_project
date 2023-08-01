#!/usr/bin/conf python
# -*- coding: utf-8 -*-
"""
@desc: 招投标-山东省
@version: python3
@author: qth
@time: 2023/06/08
"""
import time
import re
import requests
import execjs
from gne import GeneralNewsExtractor
from loguru import logger
from scrapy import Selector

from bid_project.conf import env_demo
from bid_project.untils.common import get_md5
from bid_project.untils.pysql import MysqlPipelinePublic


def detail_url(d_url):
    with open("cryptourl.js", "r", encoding="utf-8") as f:
        js = execjs.compile(f.read())
    p = js.call("getCryptoUrl", d_url)
    logger.debug(p)
    return p


def parse_news(html):
    extractor = GeneralNewsExtractor()
    result = extractor.extract(html)
    return result


def ggzyjy_list(cookies, headers, page):
        data = {
            'title': '',
            'origin': '省级',
            'inDates': '',
            'channelId': '152',
            'ext': '',
        }
        response = requests.post(
            'http://ggzyjy.shandong.gov.cn/queryContent_{}-jyxxgg.jspx'.format(page),
            cookies=cookies,
            headers=headers,
            data=data,
            verify=False,
        )
        sel = Selector(response)
        url_li = sel.xpath("//div[@class='article-list3-t']/a/@href").extract()
        time_li = sel.xpath("//div[@class='list-times']//text()").extract()
        category_li = sel.xpath("//div[@class='article-list3-t2']//div[2]/text()").extract()
        type_li = sel.xpath("//div[@class='article-list3-t2']//div[3]/text()").extract()
        souce_li = sel.xpath("//div[@class='article-list3-t2']//div[1]/text()").extract()
        items = []
        for i in range(len(url_li)):
            url = detail_url(url_li[i])
            res = requests.get(url=url, cookies=cookies, headers=headers,)
            sels = Selector(res)
            bid_html_con = sels.xpath("//table[@class='gycq-table']").extract_first()
            bid_content = parse_news(res.text).get("content", "")
            bid_name = sels.xpath('//div[@class="div-title"]//text()').extract_first()
            b_id = re.search(r'http:\/\/.*\/(\d+)\.jhtml.*', url_li[i])
            item = {
                "bid_id": get_md5(str(b_id.group(1))),
                "bid_md5_url": get_md5(detail_url(url_li[i])),
                "bid_name": bid_name.strip(),
                "create_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
                "bid_url": detail_url(url_li[i]),
                "bid_category": category_li[i].split('：')[1],
                "bid_info_type": type_li[i].split('：')[1],
                "bid_source": souce_li[i].split('：')[1],
                "bid_public_time": time_li[i],
                "bid_html_con": bid_html_con,
                "bid_content": bid_content
            }
            items.append(item)
        return items


def main():
    cookies = {
        '_gscu_740847421': '85950495pev0tv87',
        'clientlanguage': 'zh_CN',
        '_gscbrs_740847421': '1',
        '_gscs_740847421': '86033140gslpul87|pv:56',
        'JSESSIONID': '759BBDAA945BEF91CAB151502034A66C',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': '_gscu_740847421=85950495pev0tv87; clientlanguage=zh_CN; _gscbrs_740847421=1; _gscs_740847421=86033140gslpul87|pv:56; JSESSIONID=759BBDAA945BEF91CAB151502034A66C',
        'Origin': 'http://ggzyjy.shandong.gov.cn',
        'Pragma': 'no-cache',
        'Referer': 'http://ggzyjy.shandong.gov.cn/queryContent_2-jyxxgg.jspx',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }
    page = 2
    for i in range(1, page):
        items = ggzyjy_list(cookies, headers, i)
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

