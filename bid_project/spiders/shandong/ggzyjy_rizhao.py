#!/usr/bin/conf python
# -*- coding: utf-8 -*-
"""
@desc: 招投标-山东省-日照
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


def rizhao_info(headers, page, u):
        n = re.search(r"/(\d{9})$", u).group(1)
        for p in range(1, page):
            response = requests.get(
                url='http://ggzyjy.rizhao.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum={}&Paging={}'.format(n, p),
                headers=headers,
                verify=False,
            )
            sel = Selector(response)
            url_li = sel.xpath("//a[@class='news-link clearfix']/@href").extract()
            time_li = sel.xpath("//div[@class='news-date r']//text()").extract()
            items = []
            for i in range(len(url_li)):
                url = urljoin(response.url, url_li[i])
                res = requests.get(url=url, headers=headers)
                sels = Selector(res)
                bid_html_con = str(sels.xpath("//div[@class='article-content']").extract_first()).replace("'", '"'),
                bid_content = parse_news(res.text).get("content", "")
                bid_name = sels.xpath('//h3[@class="bigtitle"]//text()').extract_first()
                b_id = re.findall(r'InfoID=([a-zA-Z0-9-]+)', url)
                category = sels.xpath("//a[@class='bread-link'][2]//text()").extract_first()
                type = sels.xpath("//a[@class='bread-link'][3]//text()").extract_first()
                souce = 'None'
                bid_county = sels.xpath("//a[@class='bread-link bread-cur']//text()").extract_first()
                item = {
                    "bid_id": get_md5(str(b_id[0])),
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
                    "bid_city": '日照市',
                    "bid_county": bid_county
                }
                items.append(item)
            return items


def main():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'fontZoomState=0',
        'Pragma': 'no-cache',
        'Referer': 'http://ggzyjy.rizhao.gov.cn/rzwz/jyxx/071002/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }
    one_res = requests.get('http://ggzyjy.rizhao.gov.cn/rzwz/jyxx/', headers=headers)
    sel1 = Selector(one_res)
    url_li1 = sel1.xpath('//a[@class="news-more-bule r"]/@href').extract()
    for i in url_li1:
        url = urljoin(one_res.url, i)
        two_res = requests.get(url=url, headers=headers)
        sel2 = Selector(two_res)
        url_li2 = sel2.xpath("//a[@class='news-more-bule r']/@href").extract()
        for u in url_li2:
            page = 2
            items = rizhao_info(headers, page, u)
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

