# -*- coding: utf-8 -*-
# @Time : 2023/6/20
# @Author: mayj

"""
    海南省政府采购网
"""
import datetime
import re
import time

import scrapy

from bid_scrapy_project.common.common import urljoin_url, get_md5
from bid_scrapy_project.items import GovernmentProcurementItem


class HainanZfcgSpider(scrapy.Spider):
    name = "hainan_zfcg"
    start_url = "https://www.ccgp-hainan.gov.cn/cgw/cgw_list.jsp?currentPage={}&begindate=&enddate=&title=&bid_type=&proj_number=&zone=&ctype="

    def start_requests(self):
        page = '1'
        yield scrapy.Request(self.start_url.format(page), meta={'page':int(page)}, callback=self.parse_list, dont_filter=True)

    def parse_list(self, response):
        """处理列表信息"""
        # 获取li标签列表
        last_time = ""
        li_item_xpaths = response.xpath('//div[@class="index07_07_02"]/ul/li')
        for li_item_xpath in li_item_xpaths:
            meta = {}
            meta["city"] = li_item_xpath.xpath("./span[1]/p[1]/text()").extract_first().strip()
            meta["title"] = li_item_xpath.xpath("./span[1]/a[1]/text()").extract_first().strip()
            meta["pub_date"] = li_item_xpath.xpath("./span[1]/em[1]/text()").extract_first().strip()
            meta["category"] = li_item_xpath.xpath("./span[2]/p[1]/text()").extract_first().strip()
            href = li_item_xpath.xpath("./span[1]/a[1]/@href").extract_first().strip()
            meta["det_url"] = urljoin_url("https://www.ccgp-hainan.gov.cn", href)
            yield scrapy.Request(meta["det_url"], meta=meta, callback=self.parse_detail)
        data_now = datetime.datetime.now().strftime("%Y-%m-%d")
        if last_time == data_now and response.meta['page'] <= 7:
            page = response.meta['page']+1
            response.meta["page"] = page
            yield scrapy.Request(self.start_url.format(str(page)), meta=response.meta, dont_filter=True, callback=self.parse_list)

    def parse_detail(self, response):
        """处理详情信息"""

        item = GovernmentProcurementItem()
        item['po_id'] = get_md5(response.meta['det_url'])
        item['bid_url'] = response.meta['det_url']
        item['po_province'] = '海南省'
        item['po_city'] = response.meta['city']
        item['po_info_type'] = response.meta['category']
        item['po_public_time'] = response.meta['pub_date']
        item['bo_name'] = response.meta['title']
        try:
            source = re.search('信息来源：(.+)?</span>', response.text).group(1).strip()
        except:source = ''
        item['po_source'] = source
        item['po_html_con'] = response.xpath('//div[@class="cg20-gl"]').extract_first().strip()
        item['po_content'] = response.xpath('string(//div[@class="cg20-gl"])').extract_first().strip()
        item['website_name'] = '海南省政府采购网'
        item['website_url'] = 'https://www.ccgp-hainan.gov.cn/'
        item['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

        yield item