# -*- coding: utf-8 -*-
# @Time : 2023/7/3
# @Author: mayj

"""
    青岛市公共资源交易电子服务系统
"""
import datetime
import re
import time
import scrapy
import logging

from bid_scrapy_project.common.common import get_md5, urljoin_url
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem


class SdQingDaoGgjySpider(scrapy.Spider):
    name = "sd_qingdao_ggjy"
    start_urls = "https://ggzy.qingdao.gov.cn/Tradeinfo-GGGSList/0-0-4"
    base_url = "https://ggzy.qingdao.gov.cn"
    data_now = datetime.datetime.now().strftime("%Y-%m-%d")
    def start_requests(self):
        yield scrapy.Request(self.start_urls, dont_filter=True, callback=self.parse_category)

    def parse_category(self, response):
        """获取二级标签url"""
        expmenu_list = response.xpath('//div[@class="expmenu"]/div')
        datas = []
        for i, expmenu_xph in enumerate(expmenu_list):
            try:
                vtitle = expmenu_xph.xpath(f'../div[{i + 1}][@class="vtitle"]/text()').extract_first()

                if vtitle:
                    vcons = expmenu_xph.xpath(f'../div[{i + 2}][@class="vcon"]/ul/li')
                    for vcon in vcons:
                        data_dict = {
                            "category": vtitle,
                        }
                        vcon_name = vcon.xpath("./a/text()").extract_first()
                        vcon_href = vcon.xpath("./a/@href").extract_first()
                        data_dict["type"] = vcon_name
                        data_dict["href"] = vcon_href
                        datas.append(data_dict)

            except:
                pass

        for data in datas:
            if 'colcode=13' in data["href"]:
                data_url = data["href"]
            else:
                data_url = data["href"] + '?ProjectName=&ArryCode=&Time=03&ClassId=&ZBFlag='

            url = urljoin_url(self.base_url, data_url)
            yield scrapy.Request(url, meta=data, callback=self.parse_list, dont_filter=True)

    def parse_list(self, response):
        """处理列表页数据"""
        if '暂无信息' in response.text:
            logging.debug(f'{response.url}：无新数据')
            return
        if "list_info" not in response.text:
            logging.error(f"{response.url}:获取列表信息失败")

            return

        li_list = response.xpath('//div[@class="info_con"]//tr')
        for li_xph in li_list:
            try:
                herf = li_xph.xpath("./td[1]/a/@href").extract_first()
            except:
                logging.debug(f'{response.meta["href"]}没有数据')
                continue
            det_url = urljoin_url(self.base_url, herf)

            try:
                county = li_xph.xpath("./td[1]/a/text()").extract_first()
                county = re.search(r"\[(.+?)\]", county).group(1)
            except Exception as e:
                county = ""
            bid_name = li_xph.xpath("./td[1]/a/@title").extract_first().strip()
            pub_date = li_xph.xpath("./td[2]/text()").extract_first()
            if pub_date is None:
                continue
            if '/' in pub_date:
                pub_date = pub_date.replace(' ','').replace('/','-').strip()
            try:
                pub_date = pub_date.split(' ')[0]
            except:
                pass
            if pub_date > self.data_now:
                logging.warning(f'日期错误：{pub_date}')
                continue
            ret_data = {
                "url": det_url,
                "county": county,
                "pub_date": pub_date,
                "bid_name": bid_name,
                "id": get_md5(det_url),
                "category": response.meta["category"],
                "type": response.meta["type"],
            }
            yield scrapy.Request(det_url, meta=ret_data, callback=self.parse_detail)

    def parse_detail(self, response):
        if "ewb_location" not in response.text:
            logging.error("未获取到详情信息内容")
            return
        try:
            bid_html_con = response.xpath('//div[@class="box_bg"]').extract_first()
            content = response.xpath('string(//div[@class="box_bg"])').extract_first()
        except:
            bid_html_con = response.xpath('.//div[@class="ewb-main"]').extract_first()
            content = response.xpath('string(//div[@class="ewb-main"])').extract_first()

        url = response.meta["url"]
        id = get_md5(url)
        category = response.meta["category"]
        info_type = response.meta["type"]
        city = "青岛市"
        county = response.meta["county"]
        if category == "政府采购":
            item = GovernmentProcurementItem()
            item["po_id"] = id
            item["bid_url"] = url
            item["po_province"] = "山东省"
            item["po_city"] = city
            # item["po_county"] = county
            item["po_category"] = category
            item["po_info_type"] = info_type
            # item["bid_source"] = "济南公共资源交易中心"
            item["po_public_time"] = response.meta["pub_date"]
            item["bo_name"] = response.meta["bid_name"]
            item["po_html_con"] = bid_html_con
            item["po_content"] = content
            item["website_name"] = "青岛市公共资源交易中心"
            item["website_url"] = "https://ggzy.qingdao.gov.cn/"
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

        else:
            item = BidScrapyProjectItem()
            item["bid_id"] = id
            item["create_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            item["bid_url"] = url
            item["bid_province"] = "山东省"
            item["bid_city"] = city
            item["bid_category"] = category
            item["bid_info_type"] = info_type
            # item["bid_county"] = county
            # item["bid_source"] = bid_source
            item["bid_name"] = response.meta["bid_name"]
            item["bid_public_time"] = response.meta["pub_date"]
            item["bid_html_con"] = bid_html_con
            item["bid_content"] = content
            item["website_name"] = "青岛市公共资源交易中心"
            item["website_url"] = "https://ggzy.qingdao.gov.cn/"

        yield item

    # def parse_next_list(self, response):
    #     """获取列表页更多信息"""
    #
    #     if "pan-hd" not in response.text:
    #         logging.error(f"{response.url}:获取列表更多信息失败")
    #         return
    #     item_tree = response.xpath('//div[@class="context-bd"]//li[@class="trade-item"]')
    #     for item_xpath in item_tree:
    #         href = item_xpath.xpath("./a/@href").extract_first()
    #         info_id = re.search(r"infoid=(.+?)&", href).group(1)
    #         det_url = urljoin_url(self.base_url, href)
    #         bid_name = item_xpath.xpath("./a/@title").extract_first()
    #         pub_date = item_xpath.xpath('./span[@class="date r"]/text()').extract_first().strip()
    #         categorynum_str = re.search("categorynum=(\d+)", href).group(1)
    #         pub_date_str = pub_date.replace("-", "")
    #         category_id_str = re.search(r"jyxx(/.+/)trade", response.meta["url"]).group(1)
    #         new_category_str = (
    #             category_id_str if categorynum_str in category_id_str else category_id_str + categorynum_str + "/"
    #         )
    #         req_det_url = f"http://ggzyjy.liaocheng.gov.cn/lcggzy/jyxx{new_category_str}/{pub_date_str}/{info_id}.html"
    #         ret_data = {
    #             "url": det_url,
    #             "req_det_url": req_det_url,
    #             "pub_date": pub_date,
    #             "bid_name": bid_name,
    #             "id": get_md5(info_id),
    #             "category": response.meta["category"],
    #             "type": response.meta["info_type"],
    #         }
    #         yield scrapy.Request(det_url, meta=ret_data, callback=self.parse_detail)
