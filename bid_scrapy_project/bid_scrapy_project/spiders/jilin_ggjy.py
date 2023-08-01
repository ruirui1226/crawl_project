# -*- coding: utf-8 -*-
# @Time : 2023/6/14
# @Author: mayj

"""
    吉林省公共资源交易服务平台
"""
import json
import re
import time
import scrapy
import logging


from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class JilinGgjySpider(scrapy.Spider):
    name = "jilin_ggjy"
    start_urls = "http://was.jl.gov.cn/was5/web/search?channelid=237687&page={}&prepage=17&searchword=modal%3C%3E3%20and%20gtitle%3C%3E%27%27%20and%20gtitle%3C%3E%27null%27%20%20&callback&callback=result"

    source_codes = [
        ["122201004232188615", "长春市政府采购中心"],
        ["12220000412759478T", "吉林省矿权中心"],
        ["1222010056393822XT", "长春市城乡土地交易中心"],
        ["73700954-4", "吉林省政府采购中心"],
        ["12220100423200207X", "吉林省产权中心"],
        ["12220200782609514F", "吉林市人民政府政务服务中心"],
        ["34004150-3", "辽源市公共资源交易中心"],
        ["112203007645929828", "四平市政务服务中心"],
        ["66011618-0", "松原市人民政府政务服务中心"],
        ["122200005740930828", "吉林省公共资源交易中心"],
        ["73256854-X", "延边朝鲜族自治州政府采购中心"],
        ["73256678-X", "通化市人民政府政务公开办公室"],
        ["66429601-9", "白城市人民政府政务服务中心"],
        ["12220600737041237Q", "白山市公共资源交易中心"],
        ["01382732-2", "长春市城乡建设委员会"],
        ["122030000105", "四平市政务服务中心"],
        ["41270618-1", "四平市政务服务中心"],
        ["112203000135292377", "四平市政务服务中心"],
        ["112203000135298353", "四平市政务服务中心"],
        ["11220300413126808N", "四平市政务服务中心"],
        ["12220100MB10780025", "长春市公共资源交易中心（新）"],
        ["12220800MB11528661", "白城市公共资源交易中心"],
        ["12220400412763282Y", "辽源市公共资源交易平台（新）"],
        ["12220500MB1143476B", "通化市公共资源交易中心 "],
        ["12220700MB1837064Y", "松原市公共资源交易中心"],
        ["12220300MB0125428T", "四平市公共资源交易平台"],
        ["11222400MB14602364", "延边州公共资源交易平台（新）"],
        ["112200007710693483", "长白山管委会"],
    ]
    area_codes = [
        ["122201004232188615", "长春市"],
        ["12220000412759478T", "省级"],
        ["1222010056393822XT", "长春市"],
        ["73700954-4", "省级"],
        ["12220100423200207X", "省级"],
        ["12220200782609514F", "吉林市"],
        ["34004150-3", "辽源市"],
        ["112203007645929828", "四平市"],
        ["66011618-0", "松原市"],
        ["122200005740930828", "省级"],
        ["73256854-X", "延边州"],
        ["73256678-X", "通化市"],
        ["66429601-9", "白城市"],
        ["12220600737041237Q", "白山市"],
        ["01382732-2", "长春市"],
        ["122030000105", "四平市"],
        ["41270618-1", "四平市"],
        ["112203000135292377", "四平市"],
        ["112203000135298353", "四平市"],
        ["11220300413126808N", "四平市"],
        ["112200007710693483", "长白山"],
        ["11222400MB14602364", "延边州"],
        ["12220100MB10780025", "长春市"],
        ["12220500MB1143476B", "通化市"],
        ["12220800MB11528661", "白城市"],
        ["12220400412763282Y", "辽源市"],
        ["12220700MB1837064Y", "松原市"],
        ["12220300MB0125428T", "四平市"],
    ]

    def start_requests(self):
        yield scrapy.Request(self.start_urls.format("1"), callback=self.parse_list, dont_filter=True)

    def parse_list(self, response):
        if "tType" in response.text:
            json_str_text = response.text[response.text.find("result(") + 7 : response.text.rfind(");")]
            json_datas = json.loads(json_str_text)["datas"]
            for data in json_datas:
                yield scrapy.Request(data["docpuburl"], meta=data, callback=self.parse_detail)
        page = re.search("&page=(\d+)&", response.url).group(1)
        if int(page) + 1 <= 17:
            yield scrapy.Request(self.start_urls.format(int(page) + 1), callback=self.parse_list, dont_filter=True)

    def parse_detail(self, response):
        bid_source = ""
        for source_code in self.source_codes:
            if source_code[0] == response.meta["area"]:
                bid_source = source_code[1]
                break

        bid_city = ""
        for area_code in self.area_codes:
            if area_code[0] == response.meta["area"]:
                bid_city = area_code[1]
                break

        response.meta["timestamp"] = response.meta["timestamp"].replace(".", "-")

        if response.meta["tType"] == "政府采购":
            item = GovernmentProcurementItem()
            item["po_id"] = get_md5(response.meta["docpuburl"])
            item["bid_url"] = response.meta["docpuburl"]
            item["po_province"] = "吉林省"
            item["po_city"] = bid_city
            item["po_category"] = response.meta["tType"]
            item["po_info_type"] = response.meta["iType"]
            item["po_public_time"] = response.meta["timestamp"]
            item["bo_name"] = response.meta["title"]
            item["po_html_con"] = response.xpath('//div[@class="ewb-article"]').extract_first().replace("'", "’")
            item["po_content"] = (
                response.xpath('string(//div[@class="ewb-article"])').extract_first().replace("'", "’").strip()
            )
            item["website_name"] = "吉林省公共资源交易服务平台"
            item["website_url"] = "http://www.jl.gov.cn/ggzy/"
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = get_md5(response.meta["docpuburl"])
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = response.meta["docpuburl"]
            item["bid_province"] = "吉林省"
            item["bid_city"] = bid_city
            item["bid_category"] = response.meta["tType"]
            item["bid_info_type"] = response.meta["iType"]
            item["bid_source"] = bid_source
            item["bid_name"] = response.meta["title"]
            item["bid_public_time"] = response.meta["timestamp"]
            item["bid_html_con"] = response.xpath('//div[@class="ewb-article"]').extract_first().replace("'", "’")
            item["bid_content"] = (
                response.xpath('string(//div[@class="ewb-article"])').extract_first().replace("'", "’").strip()
            )
            item["website_name"] = "吉林省公共资源交易服务平台"
            item["website_url"] = "http://www.jl.gov.cn/ggzy/"

        yield item
