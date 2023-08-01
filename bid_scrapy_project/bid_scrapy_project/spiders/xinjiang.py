# -*- coding: utf-8 -*-
"""
@desc: 新疆公共资源交易平台
@version: python
@author: qth
@time: 2023/6/20
"""
import json
import time

import scrapy
import requests
from scrapy import Selector

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class XinjiangSpider(scrapy.Spider):
    name = "Xinjiang"
    start_url = "http://ggzy.xjbt.gov.cn/jygk/004001/construction_project.html"
    # custom_settings = {"CONCURRENT_REQUESTS": 2, "DOWNLOAD_DELAY": 1}
    cookies = {
        "userGuid": "-1177458307",
        "oauthClientId": "xjbt",
        "oauthPath": "http://10.239.19.93:8080/EpointWebBuilder",
        "oauthLoginUrl": "http://127.0.0.1:1112/membercenter/login.html?redirect_uri=",
        "oauthLogoutUrl": "",
        "noOauthRefreshToken": "d2adae5943f256c9a7b12f1ddbe2a856",
        "noOauthAccessToken": "57c0b40e395dd84883653c8b95ce8f34",
    }

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        # 'Cookie': 'userGuid=-1177458307; oauthClientId=xjbt; oauthPath=http://10.239.19.93:8080/EpointWebBuilder; oauthLoginUrl=http://127.0.0.1:1112/membercenter/login.html?redirect_uri=; oauthLogoutUrl=; noOauthRefreshToken=d2adae5943f256c9a7b12f1ddbe2a856; noOauthAccessToken=57c0b40e395dd84883653c8b95ce8f34',
        "Origin": "http://ggzy.xjbt.gov.cn",
        "Pragma": "no-cache",
        "Referer": "http://ggzy.xjbt.gov.cn//jygk/004001/construction_project.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    lists = ["004001", "004002", "004003", "004004", "004005", "004008", "004009"]
    category = ["工程建设", "政府采购", "矿权交易", "国有产权", "土地交易", "补充耕地", "其他交易"]
    page = 15
    data = '{"token":"","pn":15,"rn":15,"sdt":"1970-01-01 00:00:00","edt":"2999-12-31 23:59:59","wd":"","inc_wd":"","exc_wd":"","fields":"title","cnum":"001","sort":"{\\"webdate\\":\\"0\\"}","ssort":"title","cl":500,"terminal":"","condition":[{"fieldName":"categorynum","equal":"004001","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2}],"time":"","highlights":"","statistics":null,"unionCondition":null,"accuracy":"100","noParticiple":"1","searchRange":null,"isBusiness":"1"}'

    info_types = [{'categorynum': '004001', 'categoryname': '全部', 'emactive': 'em-active'}, {'categorynum': '004001001', 'categoryname': '全部', 'emactive': 'em-active'}, {'categorynum': '004001001001', 'categoryname': '招标公告'}, {'categorynum': '004001001002', 'categoryname': '答疑澄清'}, {'categorynum': '004001001003', 'categoryname': '中标候选人公示'}, {'categorynum': '004001001004', 'categoryname': '中标结果公告'}, {'categorynum': '004001001005', 'categoryname': '资格预审结果公示'}, {'categorynum': '004001001006', 'categoryname': '变更公告'}, {'categorynum': '004001001007', 'categoryname': '定标候选人公示'}, {'categorynum': '004001001008', 'categoryname': '合同公示'}, {'categorynum': '004001002', 'categoryname': '全部', 'emactive': 'em-active'}, {'categorynum': '004001002009', 'categoryname': '招标计划'}, {'categorynum': '004001002001', 'categoryname': '招标公告'}, {'categorynum': '004001002002', 'categoryname': '答疑澄清'}, {'categorynum': '004001002003', 'categoryname': '中标候选人公示'}, {'categorynum': '004001002004', 'categoryname': '中标结果公告'}, {'categorynum': '004001002005', 'categoryname': '资格预审结果公示'}, {'categorynum': '004001002006', 'categoryname': '变更公告'}, {'categorynum': '004001002007', 'categoryname': '定标候选人公示'}, {'categorynum': '004001002008', 'categoryname': '合同公示'}, {'categorynum': '004001003', 'categoryname': '全部', 'emactive': 'em-active'}, {'categorynum': '004001003001', 'categoryname': '招标公告'}, {'categorynum': '004001003002', 'categoryname': '答疑澄清'}, {'categorynum': '004001003003', 'categoryname': '中标候选人公示'}, {'categorynum': '004001003004', 'categoryname': '中标结果公告'}, {'categorynum': '004001003005', 'categoryname': '资格预审结果公示'}, {'categorynum': '004001003006', 'categoryname': '变更公告'}, {'categorynum': '004001003007', 'categoryname': '定标候选人公示'}, {'categorynum': '004001003008', 'categoryname': '合同公示'}, {'categorynum': '004001004', 'categoryname': '全部', 'emactive': 'em-active'}, {'categorynum': '004001004001', 'categoryname': '招标公告'}, {'categorynum': '004001004002', 'categoryname': '答疑澄清'}, {'categorynum': '004001004003', 'categoryname': '中标候选人公示'}, {'categorynum': '004001004004', 'categoryname': '中标结果公告'}, {'categorynum': '004001004005', 'categoryname': '资格预审结果公示'}, {'categorynum': '004001004006', 'categoryname': '变更公告'}, {'categorynum': '004001004007', 'categoryname': '定标候选人公示'}, {'categorynum': '004001004008', 'categoryname': '合同公示'}, {'categorynum': '004001005', 'categoryname': '全部', 'emactive': 'em-active'}, {'categorynum': '004001005001', 'categoryname': '招标公告'}, {'categorynum': '004001005002', 'categoryname': '答疑澄清'}, {'categorynum': '004001005003', 'categoryname': '中标候选人公示'}, {'categorynum': '004001005004', 'categoryname': '中标结果公告'}, {'categorynum': '004001005005', 'categoryname': '资格预审结果公示'}, {'categorynum': '004001005006', 'categoryname': '变更公告'}, {'categorynum': '004001005007', 'categoryname': '定标候选人公示'}, {'categorynum': '004001005008', 'categoryname': '合同公示'}, {'categorynum': '004002', 'categoryname': '全部', 'emactive': 'em-active'}, {'categorynum': '004002001', 'categoryname': '全部', 'emactive': 'em-active'}, {'categorynum': '004002001001', 'categoryname': '单一来源公示'}, {'categorynum': '004002001002', 'categoryname': '采购公告'}, {'categorynum': '004002001003', 'categoryname': '变更公告'}, {'categorynum': '004002001004', 'categoryname': '答疑澄清'}, {'categorynum': '004002001005', 'categoryname': '结果公示'}, {'categorynum': '004002001006', 'categoryname': '合同公示'}, {'categorynum': '004002002', 'categoryname': '全部', 'emactive': 'em-active'}, {'categorynum': '004002002001', 'categoryname': '采购公告'}, {'categorynum': '004002002002', 'categoryname': '变更公告'}, {'categorynum': '004002002003', 'categoryname': '答疑澄清'}, {'categorynum': '004002002004', 'categoryname': '结果公示'}, {'categorynum': '004002002005', 'categoryname': '合同公示'}, {'categorynum': '004002003', 'categoryname': '全部', 'emactive': 'em-active'}, {'categorynum': '004002003001', 'categoryname': '采购公告'}, {'categorynum': '004002003002', 'categoryname': '变更公告'}, {'categorynum': '004002003003', 'categoryname': '答疑澄清'}, {'categorynum': '004002003004', 'categoryname': '结果公示'}, {'categorynum': '004002003005', 'categoryname': '合同公示'}, {'categorynum': '004002004', 'categoryname': '全部', 'emactive': 'em-active'}, {'categorynum': '004002004001', 'categoryname': '采购公告'}, {'categorynum': '004002004002', 'categoryname': '变更公告'}, {'categorynum': '004002004003', 'categoryname': '答疑澄清'}, {'categorynum': '004002004004', 'categoryname': '结果公示'}, {'categorynum': '004002004005', 'categoryname': '合同公示'}, {'categorynum': '004003', 'categoryname': '全部', 'emactive': 'em-active'}, {'categorynum': '004003001', 'categoryname': '交易公告'}, {'categorynum': '004003002', 'categoryname': '答疑澄清'}, {'categorynum': '004003003', 'categoryname': '成交公示'}, {'categorynum': '004004', 'categoryname': '全部', 'emactive': 'em-active'}, {'categorynum': '004004001', 'categoryname': '交易公告'}, {'categorynum': '004004002', 'categoryname': '答疑澄清'}, {'categorynum': '004004003', 'categoryname': '成交公示'}, {'categorynum': '004005', 'categoryname': '全部', 'emactive': 'em-active'}, {'categorynum': '004005001', 'categoryname': '交易公告'}, {'categorynum': '004005002', 'categoryname': '答疑澄清'}, {'categorynum': '004005003', 'categoryname': '成交公示'}, {'categorynum': '004005', 'categoryname': '全部', 'emactive': 'em-active'}, {'categorynum': '004005', 'categoryname': '全部', 'emactive': 'em-active'}, {'categorynum': '004008', 'categoryname': '全部', 'emactive': 'em-active'}, {'categorynum': '004008001', 'categoryname': '交易公告'}, {'categorynum': '004008002', 'categoryname': '答疑澄清'}, {'categorynum': '004008003', 'categoryname': '成交公示'}, {'categorynum': '004009', 'categoryname': '全部', 'emactive': 'em-active'}, {'categorynum': '004009001', 'categoryname': '交易公告'}, {'categorynum': '004009002', 'categoryname': '答疑澄清'}, {'categorynum': '004009003', 'categoryname': '成交公示'}]

    def start_requests(self):
        for c in range(len(self.category)):
            for i in range(0, self.page, 15):
                data = json.loads(self.data)
                data["pn"] = i
                data["condition"][0]["equal"] = self.lists[c]
                bid_category = self.category[c]
                response = requests.post(
                    "http://ggzy.xjbt.gov.cn/inteligentsearch/rest/esinteligentsearch/getFullTextDataNew",
                    # cookies=self.cookies,
                    headers=self.headers,
                    data=json.dumps(data),
                    verify=False,
                )
                date_josn = json.loads(response.text)
                categorys = date_josn["result"]["records"]
                for ca in categorys:
                    infoid = ca.get("infoid", "")
                    bid_public_time = ca.get("webdate", "")
                    bid_name = ca.get("bdname", "title")
                    bid_category = bid_category
                    categorynum = ca.get("categorynum")
                    source = ca.get("xxly", "")
                    # http://ggzy.xjbt.gov.cn/jygk/004001/004001005/004001005004/20230620/6f9202be-0c14-4823-b4a5-79245138cac5.html
                    linkurl = "http://ggzy.xjbt.gov.cn" + ca.get("linkurl")
                    yield scrapy.Request(
                        url=linkurl,
                        cookies=self.cookies,
                        headers=self.headers,
                        callback=self.parse,
                        meta={
                            "infoid": infoid,
                            "bid_public_time": bid_public_time,
                            "bid_name": bid_name,
                            "bid_category": bid_category,
                            "categorynum": categorynum,
                            "source": source,
                        },
                    )

    def parse(self, response, **kwargs):
        sel = Selector(response)
        categorynum = response.meta['categorynum']
        bid_type = ''
        for info_type in self.info_types:
            if info_type['categorynum'] == str(categorynum):
                bid_type = info_type['categoryname']
                break

        source = response.meta["source"]
        if sel.xpath('//div[@class="ewb-article-info"]').extract():
            bid_html_con = sel.xpath('//div[@class="ewb-article-info"]')
        elif sel.xpath('//div[@class="ewb-article-sources"]').extract():
            bid_html_con = sel.xpath('//div[@class="ewb-article-sources"]')
        else:
            bid_html_con = ""
        # if sel.xpath('//div[@class="ewb-artice-info"]//text()').extract():
        #     bid_content = ' '.join(sel.xpath('//div[@class="ewb-article-info"]//text()').extract()).strip()
        # elif sel.xpath('//div[@class="ewb-article-sources"]//text()').extract():
        #     bid_content = ' '.join(sel.xpath('//div[@class="ewb-article-sources"]//text()').extract()).strip()
        # else:
        #     bid_content = ''
        try:
            bid_content = bid_html_con.xpath("string(.)").extract_first()
        except:
            bid_content = ""
        if bid_html_con:
            bid_html_con = bid_html_con.extract_first()
        category = response.meta["bid_category"]
        id = get_md5(response.meta["infoid"])
        province = "新疆"
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        if category == "政府采购":
            items = BidScrapyProjectItem()
            items["bid_id"] = id
            items["bid_name"] = response.meta["bid_name"]
            items["create_datetime"] = create_time
            items["bid_url"] = response.url
            items["bid_category"] = category
            items["bid_source"] = source
            items["bid_public_time"] = response.meta["bid_public_time"]
            items["bid_html_con"] = str(bid_html_con).replace("'", '"')
            items["bid_content"] = bid_content
            items["website_name"] = "新疆生产建设兵团公共资源服务平台"
            items["website_url"] = "http://ggzy.xjbt.gov.cn/"
            items["bid_province"] = province
            items["bid_info_type"] = bid_type

        else:
            items = GovernmentProcurementItem()
            items["po_id"] = id
            items["bid_url"] = response.url
            items["po_province"] = province
            items["po_category"] = category
            items["po_public_time"] = response.meta["bid_public_time"]
            items["bo_name"] = response.meta["bid_name"]
            items["po_source"] = source
            items["po_html_con"] = bid_html_con
            items["po_content"] = bid_content
            items["website_name"] = "新疆生产建设兵团公共资源服务平台"
            items["website_url"] = "http://ggzy.xjbt.gov.cn/"
            items["create_datetime"] = create_time
            items["po_info_type"] = bid_type
        yield items
