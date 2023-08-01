#!/usr/bin/conf python
# -*- coding: utf-8 -*-
"""
@desc: 招投标-山东省-德州
@version: python3
@author: qth
@time: 2023/06/09
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


def dezhou_info(url, headers, cookies, date, info_li):
    response = requests.get(url=url, headers=headers, cookies=cookies)
    sel = Selector(response)
    time_li = sel.xpath('//span[@class="ewb-list-date"]/text()').extract()
    items = []
    for i in range(len(date)):
        date = date[i].replace('-', '')
        link = info_li[i]
        infoid = re.search(r'infoid=([\w-]+)', link).group(1)
        url = 'http://ggzyjy.dezhou.gov.cn/TPFront/xmxx/' + infoid + date
        logger.debug(url)

        res = requests.get(url, headers=headers, cookies=cookies)
        sels = Selector(res)
        bid_html_con = str(sels.xpath('//div[@class="article-content"]').extract()).replace("'", '"')
        if not bid_html_con:
            pass
        bid_content = parse_news(res.text).get("content", "")
        bid_name = sels.xpath('//h2[@class="article-title"]//text()').extract_first()
        try:
            b_id = re.search(r'/([\w-]+\.html)$', url).group(1)[:-5]
        except:
            break
        category = sels.xpath("//div[@class='ewb-location']/span[1]//text()").extract_first()
        type = sels.xpath("//div[@class='ewb-location']/span[2]//text()").extract_first()
        souce = '德州市公共资源交易中心'
        bid_county = sels.xpath('//span[@id="viewGuid"]//text()').extract_first()
        bid_countys = bid_county if bid_county else 'None'
        item = {
            "bid_id": get_md5(str(b_id)),
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
            "bid_county": bid_countys
        }
        items.append(item)
    return items


def dezhou_list(tr_url, headers, cookies):
        res = requests.get(url=tr_url, headers=headers, cookies=cookies)
        sel2 = Selector(res)
        date = sel2.xpath('//span[@class="ewb-list-date"]//text()').extract()
        city_li = sel2.xpath('//a[@class="block-more"]/@href').extract()
        info_li = sel2.xpath('//li[@class="ewb-list-node clearfix"]/a/@href').extract()
        page = 2
        if city_li:
            for c in city_li:
                for p in range(1, page):
                    if p == 1:
                        url = urljoin(res.url, c)
                        return url
                    else:
                        link = re.search(r'/(\d+/\d+/\d+)/moreinfo2\.html', c).group(1)
                        url = 'http://ggzyjy.dezhou.gov.cn/TPFront/xmxx/' + link + '/{}.html'.format(p)
                        return url
        else:
            for p in range(1, page):
                # http://ggzyjy.dezhou.gov.cn/TPFront/xmxx/004001/004001002/004001002001/20230421/000dd25e-0dbe-4a53-86dd-e124b7c0dc50.html
                # http://ggzyjy.dezhou.gov.cn/TPFront/xmxx/004001/004001001/004001001001/20230613/fb47edf7-8e98-48f4-b440-06877e26fef8.html
                # http://ggzyjy.dezhou.gov.cn/TPFront/xmxx/004001/004001002/004001002001/20230421/000dd25e-0dbe-4a53-86dd-e124b7c0dc50.html
                #                                                                          infoid=000dd25e-0dbe-4a53-86dd-e124b7c0dc50
                url = res.url
                if p == 1:  # http://ggzyjy.dezhou.gov.cn/TPFront/xmxx/004001/004001001/moreinfo2_jsgc.html
                    dezhou_info(url, headers, cookies, date, info_li)
                else:  # http://ggzyjy.dezhou.gov.cn/TPFront/xmxx/004001/004001001/3.html
                    link = re.search(r'/(\d+/\d+)/', url).group(1)
                    url = 'http://ggzyjy.dezhou.gov.cn/TPFront/xmxx/' + link + '{}.html'.format(p)
                    return url

def main():
    cookies = {
        'userGuid': '-1177458307',
        'oauthClientId': 'demoClient',
        'oauthPath': 'http://10.2.129.27:8080/EpointWebBuilder',
        'oauthLoginUrl': 'http://10.2.129.27:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=',
        'oauthLogoutUrl': 'http://10.2.129.27:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=',
        'noOauthRefreshToken': '3f2148188634872555e5fdca9da1337f',
        'noOauthAccessToken': '4430ab8dcb9685404401e9c45f57f8f1',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        # 'Cookie': 'userGuid=-1177458307; oauthClientId=demoClient; oauthPath=http://10.2.129.27:8080/EpointWebBuilder; oauthLoginUrl=http://10.2.129.27:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://10.2.129.27:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=3f2148188634872555e5fdca9da1337f; noOauthAccessToken=4430ab8dcb9685404401e9c45f57f8f1',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }
    category = 'http://ggzyjy.dezhou.gov.cn/TPFront/xmxx/moreinfo2.html'
    response = requests.get(url=category, headers=headers, cookies=cookies)
    sel = Selector(response)
    type_li = sel.xpath('//a[@class="block-more"]/@href').extract()
    for type_url in type_li:
        type_url = urljoin(response.url, type_url)
        response = requests.get(type_url)
        sel = Selector(response)
        tr_li = sel.xpath("//a[@class='block-more']/@href").extract()
        for tr in tr_li:
            tr_url = urljoin(response.url, tr)
            url = dezhou_list(tr_url, headers, cookies)
            items = dezhou_info(url, headers, cookies)
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

