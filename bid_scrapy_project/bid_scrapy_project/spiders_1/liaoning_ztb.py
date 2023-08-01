# -*- coding: utf-8 -*-
"""
@desc: 辽宁省招标投标监管网
@version: python3
@author: liuwx
@time: 2023/07/20
"""
import scrapy
import time
import json

from bid_scrapy_project.common.common import get_md5
from bid_scrapy_project.items import BidScrapyProjectItem
from datetime import datetime

class LiaoningZtbSpider(scrapy.Spider):
    name = 'liaoning_ztb'
    # 请求频率过快会不出数据，不会封ip
    custom_settings = {"CONCURRENT_REQUESTS": 1, 'DOWNLOAD_DELAY': 3}
    """
    二级类型 直接列出
    """
    def __init__(self):
        self.infoType = {
            "特殊事项公告": "c_bid_exception_report",
            "资格预审": "c_tender_notice_p",
            "招标公告": "c_tender_notice",
            "补充公告": "c_tender_doc",
            "澄清与修改文件": "clarification",
            "中标候选人公示": "c_win_candidate_publicity",
            "中标结果公告": "c_wid_bidder_publicity",
            "书面报告": "c_written_exception_record",
        }
        self.headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

    """
    列表页链接请求
    """
    def start_requests(self):
        for info_type, noticeType in self.infoType.items():
            items = {
                "bid_info_type": info_type,  # 二级类型
            }
            if info_type == "特殊事项公告":
                info_id = "CBidExceptionReport"
                link_id = "CBidExceptionReport/getDetail"
            elif info_type == "资格预审":
                info_id = "prequalificationResult"
                link_id = "cPrequalificationResult/getDetail"
            elif info_type == "招标公告":
                info_id = "notice"
                link_id = "cTenderNoticeController/getDetail"
            elif info_type == "补充公告":
                info_id = "tenderNoticeSupplement"
                link_id = "cTenderNoticeController/getSupplementDetail"
            elif info_type == "澄清与修改文件":
                info_id = "clarifyUpdate"
                link_id = "tenderDoc/getClarifyUpdateDetail"
            elif info_type == "中标候选人公示":
                info_id = "cWinCandidatePublicity"
                link_id = "CWinCandidatePublicity/getDetail"
            elif info_type == "中标结果公告":
                info_id = "bidderPublicity"
                link_id = "CWinBidderPublicity/selectCWinBidderPublicityDetail"
            elif info_type == "书面报告":
                info_id = "writtenExceptionRecord"
                link_id = "CWrittenExceptionRecord/getDetail"
            # 列表页接口获取
            link = "https://www.lntb.gov.cn/mhback/api/cTenderProjectNode/checkList"
            param = '{"keyword":"","regionLevel":"","regionCode":"","tradeCode":"","classificationCode":"","noticeType":"'+noticeType+'","noticeIndex":"","time":"","creditShow":"","number":1,"size":60,"total":0}'
            yield scrapy.Request(
                url=link,
                callback=self.parse,
                method="POST",
                body=param,
                headers=self.headers,
                meta={"items": items, "info_id": info_id, "link_id": link_id},
                dont_filter=True
            )

    """
    列表页详情获取（标题、发布时间、详情页链接）
    """
    def parse(self, response):
        item_info = response.meta["items"]
        info_id = response.meta["info_id"]
        link_id = response.meta["link_id"]
        listjson = json.loads(response.text)
        data_list = listjson['data']['list']
        for data in data_list:
            # 获取发布时间
            pubtime = data["time"]
            # 处理时间
            _date = datetime.strptime(pubtime, "%Y-%m-%dT%H:%M:%S.%f+0000")
            times = _date.strftime("%Y-%m-%d %H:%M:%S")
            # 截取发布时间年月日
            pubday = times.split(' ')[0]
            # 获取当前年月日
            nowday = time.strftime("%Y-%m-%d")
            # 当发布时间不是当天时间时，跳出不采
            if pubday != nowday:
                # print(times + "不是当天最新文章，跳过")
                break
            # 获取文章标题
            title = data['title']
            # 获取文章id
            newsId = data['id']
            # 文章url
            url = "https://www.lntb.gov.cn/#/"+info_id+"?id="+newsId
            # 文章接口
            link = "https://www.lntb.gov.cn/mhback/api/"+link_id+"/"+newsId
            items = {
                "bid_public_time": times,
                "bid_url": url,
                "bid_name": title,
                "bid_id": get_md5(url),
            }
            items.update(item_info)
            yield scrapy.Request(
                url=link,
                callback=self.getContentInfo,
                method="POST",
                headers=self.headers,
                meta={"items": items}
            )

    """
    文章详情获取（发布内容 json字符串拼接）
    """
    def getContentInfo(self, response):
        items_info = response.meta["items"]
        # 获取详情页json数据
        datajson = json.loads(response.text)
        data = response.json()['data']
        if data == None:
            print("操作过于频繁")
            return
        else:
            content = ','.join([str_data for str_data in list(response.json()['data'].values()) if type(str_data) == str]).replace(',,,', ',').replace(',,', ',')
        # 采集联系人、联系电话
        # content_list = []
        # for str_data in list(response.json()['data'].values()):
        #     if type(str_data) == str or type(str_data) == int:
        #         content_list.append(str(str_data))
        #     else:
        #         if str_data != None:
        #             for str_data_next in list(str_data.values()):
        #                 if type(str_data_next) == str or type(str_data) == int:
        #                     content_list.append(str(str_data_next))
        #                 else:
        #                     if str_data_next != None:
        #                         for str_data_next_next in list(str_data_next.values()):
        #                             if type(str_data_next_next) == str or type(str_data) == int:
        #                                 content_list.append(str(str_data_next_next))
        #                             else:
        #                                 pass
        # content = ','.join(content_list).replace(',,,',',').replace(',,', ',')
        items_infos = BidScrapyProjectItem()
        items_infos['bid_category'] = "交易公开"
        items_infos['bid_province'] = "辽宁省"
        items_infos['bid_info_type'] = items_info["bid_info_type"]
        items_infos['bid_public_time'] = items_info["bid_public_time"]
        items_infos['bid_name'] = items_info["bid_name"]
        # items_infos['po_html_con'] = contentHtml
        items_infos['bid_content'] = content
        items_infos['bid_json_data'] = datajson
        items_infos['bid_url'] = items_info["bid_url"]
        items_infos["bid_id"] = items_info["bid_id"]
        items_infos['website_name'] = "辽宁省招标投标监管网"
        items_infos['website_url'] = "https://www.lntb.gov.cn/#/trade"
        items_infos['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        # print(
        #     items_infos["po_info_type"],
        #     items_infos["po_id"],
        #     items_infos["bid_url"],
        #     items_infos["po_public_time"]
        # )
        yield items_infos