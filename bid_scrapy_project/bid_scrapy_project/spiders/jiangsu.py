# -*- coding: utf-8 -*-
"""
@desc: 江苏省公共资源交易平台
@version: python
@author: qth
@time: 2023/6/16
"""
import datetime
import json
import re
import time

# from loguru import logger

import bid_scrapy_project.settings
import requests
from scrapy import Selector, Request, FormRequest
import scrapy
from gne import GeneralNewsExtractor


from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem


def parse_news(html):
    extractor = GeneralNewsExtractor()
    result = extractor.extract(html)
    return result


class JiangsuSpider(scrapy.Spider):
    name = "Jiangsu"
    start_url = 'http://jsggzy.jszwfw.gov.cn/inteligentsearch/rest/esinteligentsearch/getFullTextDataNew'
    # custom_settings = {"CONCURRENT_REQUESTS": 2, "DOWNLOAD_DELAY": 1}
    cookies = {
        '_gscu_2113302982': '86878538jxjmh150',
        '_gscbrs_2113302982': '1',
        '_gscs_2113302982': 't86882922s8vjn812|pv:5',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        # 'Cookie': '_gscu_2113302982=86878538jxjmh150; _gscbrs_2113302982=1; _gscs_2113302982=86878538j48dts50|pv:2',
        'Origin': 'http://jsggzy.jszwfw.gov.cn',
        'Pragma': 'no-cache',
        'Referer': 'http://jsggzy.jszwfw.gov.cn/jyxx/tradeInfonew.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    def start_requests(self):
        now = datetime.datetime.now()
        time_str = now.strftime('%Y-%m-%d')
        page = 20
        json_data = {
            'token': '',
            'pn': 0,
            'rn': 20,
            'sdt': '',
            'edt': '',
            'wd': '',
            'inc_wd': '',
            'exc_wd': '',
            'fields': 'title',
            'cnum': '001',
            'sort': '{"infodatepx":"0"}',
            'ssort': 'title',
            'cl': 200,
            'terminal': '',
            'condition': [],
            'time': [
                {
                    'fieldName': 'infodatepx',
                    'startTime': str(time_str) + " " + '00:00:00',
                    'endTime': str(time_str) + " " + '23:59:59',
                },
            ],
            'highlights': 'title',
            'statistics': None,
            'unionCondition': None,
            'accuracy': '',
            'noParticiple': '1',
            'searchRange': None,
            'isBusiness': '1',
        }
        for i in range(0, page, 10):
            json_data['pn'] = i
            response = requests.post(
                url=self.start_url,
                cookies=self.cookies,
                headers=self.headers,
                json=json_data,
                verify=False,
            )

            date_josn = json.loads(response.text)
            categorys = date_josn["result"]["records"]
            for ca in categorys:
                link = "http://jsggzy.jszwfw.gov.cn/" + ca["linkurl"]
                infoid = ca.get('infoid', 'id')
                bid_public_time = ca.get('infodatepx', '')
                bid_name = ca.get('title')
                bid_info_type = ca.get('categoryname')
                yield scrapy.Request(
                    url=link,
                    callback=self.parse,
                    meta={'infoid': infoid, 'bid_public_time': bid_public_time, 'bid_name': bid_name,
                          'bid_info_type': bid_info_type},
                    dont_filter=True)

    def parse(self, response, **kwargs):
        sel = Selector(response)
        bid_category = sel.xpath('//div[@class="ewb-bread"]/a[3]//text()').extract_first()
        source = sel.xpath('//div[@class="ewb-trade-info"]//text()[2]').extract_first().strip()
        try:
            bid_source = re.search(r'(?<=来源：).+', source).group()
        except:
            bid_source = '江苏省公共资源交易平台'
        bid_info_type = response.meta['bid_info_type']
        if bid_info_type == '招标公告' or '中标结果公告':
            bid_html_con = sel.xpath('//div[@class="ewb-trade-right l"]').extract()
            bid_content = ' '.join(sel.xpath('//div[@class="ewb-trade-right l"]//text()').extract()).strip()

        elif bid_info_type == '中标候选人公示':
            bid_html_con = sel.xpath('//div[@class="ewb-trade-con clearfix"]').extract()
            bid_content = sel.xpath('//div[@class="ewb-trade-con clearfix"]//text()').extract()
        else:
            bid_html_con = ""
            bid_content = ""
        items = BidScrapyProjectItem()
        items["bid_id"] = get_md5(response.meta['infoid'])
        items["bid_md5_url"] = ""
        items["bid_name"] = response.meta['bid_name']
        items["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        items["bid_url"] = response.url
        items["bid_category"] = bid_category
        items["bid_info_type"] = bid_info_type
        items["bid_source"] = bid_source
        items["bid_public_time"] = response.meta['bid_public_time']
        items["bid_html_con"] = str(bid_html_con).replace("'", '"')
        items["bid_content"] = bid_content
        items["bid_city"] = "",
        items["bid_county"] = "",
        items["website_name"] = "江苏省公共资源交易平台",
        items["website_url"] = "http://jsggzy.jszwfw.gov.cn/",
        items["bid_province"] = "江苏省",
        # logger.debug('插入成功')

        yield items
