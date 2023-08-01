# -*- coding: utf-8 -*-
"""
@desc: 青海省公共资源交易交易网
@version: python3
@author: liuwx
@time: 2023/06/21
"""

import scrapy
import re
import time
import json

from bid_scrapy_project.common.common import get_md5, remove_node
from lxml import etree
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem

class QinghaiGgzySpider(scrapy.Spider):
    name = "qinghai_ggzy"

    def __init__(self):
        # 大分类直接列出
        self.urlList = {
            "工程建设": "http://www.qhggzyjy.gov.cn/ggzy/jyxx/001001/transinfo_list.html",
            "政府采购": "http://www.qhggzyjy.gov.cn/ggzy/jyxx/001002/transinfo_list.html",
            "产权交易": "http://www.qhggzyjy.gov.cn/ggzy/jyxx/001004/transinfo_list.html",
            "土地及矿权": "http://www.qhggzyjy.gov.cn/ggzy/jyxx/001005/transinfo_list.html",
            "药品采购": "http://www.qhggzyjy.gov.cn/ggzy/jyxx/001003/transinfo_list.html",
        }

    """
    大分类遍历
    """
    def start_requests(self):
        for i, v in self.urlList.items():
            # 大分类名称
            items = {"bid_category": i}
            # 大分类链接
            url = v
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={"items": items},
                dont_filter=True
            )

    """
    二级类别获取遍历
    """
    def parse(self, response):
        secondaryList = response.xpath('//li[@class="wb-tree-items hasChild current"]/div[@class="wb-tree-subs"]/ul/li')
        second_items = response.meta["items"]
        for li in secondaryList:
            # 二级类别名称
            secondary_name = li.xpath("./a/span/text()").extract_first().strip()
            # ”产权交易-公车拍卖“这个栏目打不开，不采；”产权交易-挂牌竞价“不属于招标内容，不采
            if "公车拍卖" == secondary_name or "挂牌竞价" == secondary_name:
                print(secondary_name+"不采")
                continue
            items = {"bid_info_type": secondary_name}
            items.update(second_items)
            # 二级类别url
            secondary_href = li.xpath("./a/@href").extract_first()
            # 列表链接未在源码中，需请求接口，post请求
            # 截取接口所需参数
            equal_list = secondary_href.split('/')
            equal = equal_list[-2]
            # 列表页接口
            link = "http://www.qhggzyjy.gov.cn/inteligentsearch/rest/inteligentSearch/getFullTextData"
            param = "{\"token\":\"\",\"pn\":0,\"rn\":10,\"sdt\":\"\",\"edt\":\"\",\"wd\":\"\",\"inc_wd\":\"\",\"exc_wd\":\"\",\"fields\":\"title\",\"cnum\":\"001;002;003;004;005;006;007;008;009;010\",\"sort\":\"{\\\"showdate\\\":\\\"0\\\"}\",\"ssort\":\"title\",\"cl\":200,\"terminal\":\"\",\"condition\":[{\"fieldName\":\"categorynum\",\"isLike\":true,\"likeType\":2,\"equal\":\""+equal+"\"}],\"time\":null,\"highlights\":\"title\",\"statistics\":null,\"unionCondition\":null,\"accuracy\":\"100\",\"noParticiple\":\"0\",\"searchRange\":null,\"isBusiness\":1}"
            yield scrapy.Request(
                url=link,
                callback=self.getContentParse,
                method="POST",
                body=param,
                meta={"items": items, 'param': param, 'equal': equal},
                dont_filter=True
            )

    """
    列表详情获取（标题、发布时间、详情页链接）
    """
    def getContentParse(self, response):
        print(f"当前{json.loads(response.meta['param'])['pn']}页")
        # 翻页判断参数
        FLAG = True
        list_info_items = response.meta["items"]
        jsondata = json.loads(response.text)
        records_list = jsondata['result']['records']
        if not records_list:
            print(list_info_items['bid_info_type'] +":该栏目下没有文章")
            return
        for records in records_list:
            # 文章标题
            title = records['title']
            # 详情页链接
            linkurl = records['linkurl']
            # 补齐url
            linkurl = response.urljoin(linkurl)
            # 当详情页没有时间的时候就将这个时间传到发布时间的字段中
            times = records['infodate']
            # 截取发布时间年月日
            pubday = times.split(' ')[0]
            # 获取当前年月日
            nowday = time.strftime("%Y-%m-%d")
            # 当发布时间不是当天时间时，跳出不采
            if pubday != nowday:
                FLAG = False
                # print("不是当天最新文章，跳过")
                break
            items = {
                "bid_public_time": times,
                "bid_url": linkurl,
                "bid_name": title,
                "bid_id": get_md5(linkurl),
            }
            items.update(list_info_items)
            yield scrapy.Request(
                linkurl,
                callback=self.getContentInfo,
                meta={"items": items}
            )
        if FLAG:
            param = json.loads(response.meta['param'])
            equal = response.meta['equal']
            page = int(param['pn']) + 10
            link = "http://www.qhggzyjy.gov.cn/inteligentsearch/rest/inteligentSearch/getFullTextData"
            param = "{\"token\":\"\",\"pn\": "+str(page)+",\"rn\":10,\"sdt\":\"\",\"edt\":\"\",\"wd\":\"\",\"inc_wd\":\"\",\"exc_wd\":\"\",\"fields\":\"title\",\"cnum\":\"001;002;003;004;005;006;007;008;009;010\",\"sort\":\"{\\\"showdate\\\":\\\"0\\\"}\",\"ssort\":\"title\",\"cl\":200,\"terminal\":\"\",\"condition\":[{\"fieldName\":\"categorynum\",\"isLike\":true,\"likeType\":2,\"equal\":\"" + equal + "\"}],\"time\":null,\"highlights\":\"title\",\"statistics\":null,\"unionCondition\":null,\"accuracy\":\"100\",\"noParticiple\":\"0\",\"searchRange\":null,\"isBusiness\":1}"
            yield scrapy.Request(
                url=link,
                callback=self.getContentParse,
                method="POST",
                body=param,
                meta={"items": list_info_items, 'param': param, 'equal': equal},
                dont_filter=True
            )

    """
    文章详情获取（文章内容、信息来源）
    """
    def getContentInfo(self, response):
        items_info = response.meta["items"]
        info_source = response.xpath('//div[@class="detail-source"]/span|//div[@class="xiangxidate"]').extract_first()
        # 有的文章没有发布时间的标签，例如：http://www.qhggzyjy.gov.cn/ggzy/jyxx/001001/001001007/20230620/47b855e1-5427-456b-ba9f-cc6cbf3d2b81.html 这篇文章
        # 如果没有时间标签，发布时间就使用列表页采到的时间
        if not info_source:
            pudate = items_info["bid_public_time"]
        # 发布时间
        else:
            if "信息时间" in info_source:
                pudate = re.search("信息时间：(\d{4}/\d{2}/\d{2})", response.text).groups()[0]
        if "/" in pudate:
            pudate = pudate.replace("/","-")
        # 带有html的文本
        str_html_content = etree.HTML(response.text).xpath('//div[@class="info make"]|//div[@class="info"]|//div[@class="ewb-ca-detail"]|//div[@class="info xiangxiyekuang"]')
        contentHtml = etree.tostring(str_html_content[0], encoding="utf-8").decode()
        # 纯净文本
        content = remove_node(contentHtml, ["style"]).text
        if "政府采购" in items_info["bid_category"]:
            items_cg = GovernmentProcurementItem()
            items_cg["po_province"] = "青海"
            items_cg["website_name"] = "青海省公共资源交易服务平台"
            items_cg["website_url"] = "http://www.qhggzyjy.gov.cn/ggzy/"
            items_cg["bo_name"] = items_info.get("bid_name", None)
            items_cg["po_public_time"] = pudate
            items_cg["po_category"] = items_info.get("bid_category", None)
            items_cg["po_info_type"] = items_info.get("bid_info_type", None)
            items_cg["po_city"] = "青海省"
            items_cg["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            items_cg["bid_url"] = items_info.get("bid_url", None)
            items_cg["po_id"] = items_info.get("bid_id", None)
            items_cg["po_html_con"] = contentHtml
            items_cg["po_content"] = content
            # print(
            #     items_cg["po_id"],
            #     items_cg["bid_url"],
            #     items_cg["po_category"],
            #     items_cg.get("po_info_type", None),
            #     items_cg["bo_name"],
            #     items_cg["po_public_time"],
            # )
            yield items_cg
        else:
            ##修改格式
            items_zy = BidScrapyProjectItem(
                bid_city="青海省",
                website_name="青海省公共资源交易服务平台",
                website_url="http://www.qhggzyjy.gov.cn/ggzy/",
                bid_province="青海",
            )
            items_zy.update(items_info)
            items_zy["bid_public_time"] = pudate
            items_zy["bid_html_con"] = contentHtml
            items_zy["bid_content"] = content
            items_zy["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            # print(
            #     items_zy["bid_id"],
            #     items_zy["bid_url"],
            #     items_zy["bid_category"],
            #     items_zy.get("bid_info_type", None),
            #     items_zy["bid_name"],
            #     items_zy["bid_public_time"],
            # )
            yield items_zy