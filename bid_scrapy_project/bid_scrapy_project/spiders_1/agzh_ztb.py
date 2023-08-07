# -*- coding: utf-8 -*-
"""
@desc: 鞍钢智慧招投标平台
@version: python3
@author: liuwx
@time: 2023/07/31
"""
import scrapy
import re
import json
import time

from lxml import etree
from bid_scrapy_project.common.common import get_md5, remove_node
from bid_scrapy_project.items import BidScrapyProjectItem

class AgzhZtbSpider(scrapy.Spider):
    name = 'agzh_ztb'

    """
    一级、二级类别直接列出
    """
    def __init__(self):
        self.category_list = {
            "货物": {
                "招采公告/预审公告": '{"token":"","pn":0,"rn":10,"sdt":"","edt":"","wd":"%20","inc_wd":"","exc_wd":"","fields":"title","cnum":"001","sort":"{\\"webdate\\":\\"0\\"}","ssort":"title","cl":2000,"terminal":"","condition":[{"fieldName":"categorynum","equal":"001001","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2},{"fieldName":"projectnumber","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zblx","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zbfw","equal":"0","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"cglb","equal":"M","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0}],"time":[{"fieldName":"webdate","startTime":"1998-01-01 00:00:00","endTime":"2099-12-31 23:59:59"}],"highlights":"","statistics":null,"unionCondition":null,"accuracy":"","noParticiple":"1","searchRange":null,"isBusiness":"1"}',
                "变更公告": '{"token":"","pn":0,"rn":10,"sdt":"","edt":"","wd":"%20","inc_wd":"","exc_wd":"","fields":"title","cnum":"001","sort":"{\\"webdate\\":\\"0\\"}","ssort":"title","cl":2000,"terminal":"","condition":[{"fieldName":"categorynum","equal":"001002","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2},{"fieldName":"projectnumber","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zblx","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zbfw","equal":"0","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"cglb","equal":"M","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0}],"time":[{"fieldName":"webdate","startTime":"1998-01-01 00:00:00","endTime":"2099-12-31 23:59:59"}],"highlights":"","statistics":null,"unionCondition":null,"accuracy":"","noParticiple":"1","searchRange":null,"isBusiness":"1"}',
                "中标候选人公示": '{"token":"","pn":0,"rn":10,"sdt":"","edt":"","wd":"%20","inc_wd":"","exc_wd":"","fields":"title","cnum":"001","sort":"{\\"webdate\\":\\"0\\"}","ssort":"title","cl":2000,"terminal":"","condition":[{"fieldName":"categorynum","equal":"001003","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2},{"fieldName":"projectnumber","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zblx","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zbfw","equal":"0","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"cglb","equal":"M","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0}],"time":[{"fieldName":"webdate","startTime":"1998-01-01 00:00:00","endTime":"2099-12-31 23:59:59"}],"highlights":"","statistics":null,"unionCondition":null,"accuracy":"","noParticiple":"1","searchRange":null,"isBusiness":"1"}',
                "中标结果公告": '{"token":"","pn":0,"rn":10,"sdt":"","edt":"","wd":"%20","inc_wd":"","exc_wd":"","fields":"title","cnum":"001","sort":"{\\"webdate\\":\\"0\\"}","ssort":"title","cl":2000,"terminal":"","condition":[{"fieldName":"categorynum","equal":"001004","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2},{"fieldName":"projectnumber","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zblx","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zbfw","equal":"0","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"cglb","equal":"M","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0}],"time":[{"fieldName":"webdate","startTime":"1998-01-01 00:00:00","endTime":"2099-12-31 23:59:59"}],"highlights":"","statistics":null,"unionCondition":null,"accuracy":"","noParticiple":"1","searchRange":null,"isBusiness":"1"}',
                "异常公告": '{"token":"","pn":0,"rn":10,"sdt":"","edt":"","wd":"%20","inc_wd":"","exc_wd":"","fields":"title","cnum":"001","sort":"{\\"webdate\\":\\"0\\"}","ssort":"title","cl":2000,"terminal":"","condition":[{"fieldName":"categorynum","equal":"001005","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2},{"fieldName":"projectnumber","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zblx","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zbfw","equal":"0","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"cglb","equal":"M","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0}],"time":[{"fieldName":"webdate","startTime":"1998-01-01 00:00:00","endTime":"2099-12-31 23:59:59"}],"highlights":"","statistics":null,"unionCondition":null,"accuracy":"","noParticiple":"1","searchRange":null,"isBusiness":"1"}'
            },
            "工程": {
                "招采公告/预审公告": '{"token":"","pn":0,"rn":10,"sdt":"","edt":"","wd":"%20","inc_wd":"","exc_wd":"","fields":"title","cnum":"001","sort":"{\\"webdate\\":\\"0\\"}","ssort":"title","cl":2000,"terminal":"","condition":[{"fieldName":"categorynum","equal":"001001","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2},{"fieldName":"projectnumber","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zblx","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zbfw","equal":"0","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"cglb","equal":"A","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0}],"time":[{"fieldName":"webdate","startTime":"1998-01-01 00:00:00","endTime":"2099-12-31 23:59:59"}],"highlights":"","statistics":null,"unionCondition":null,"accuracy":"","noParticiple":"1","searchRange":null,"isBusiness":"1"}',
                "变更公告": '{"token":"","pn":0,"rn":10,"sdt":"","edt":"","wd":"%20","inc_wd":"","exc_wd":"","fields":"title","cnum":"001","sort":"{\\"webdate\\":\\"0\\"}","ssort":"title","cl":2000,"terminal":"","condition":[{"fieldName":"categorynum","equal":"001002","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2},{"fieldName":"projectnumber","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zblx","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zbfw","equal":"0","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"cglb","equal":"A","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0}],"time":[{"fieldName":"webdate","startTime":"1998-01-01 00:00:00","endTime":"2099-12-31 23:59:59"}],"highlights":"","statistics":null,"unionCondition":null,"accuracy":"","noParticiple":"1","searchRange":null,"isBusiness":"1"}',
                "中标候选人公示": '{"token":"","pn":0,"rn":10,"sdt":"","edt":"","wd":"%20","inc_wd":"","exc_wd":"","fields":"title","cnum":"001","sort":"{\\"webdate\\":\\"0\\"}","ssort":"title","cl":2000,"terminal":"","condition":[{"fieldName":"categorynum","equal":"001003","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2},{"fieldName":"projectnumber","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zblx","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zbfw","equal":"0","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"cglb","equal":"A","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0}],"time":[{"fieldName":"webdate","startTime":"1998-01-01 00:00:00","endTime":"2099-12-31 23:59:59"}],"highlights":"","statistics":null,"unionCondition":null,"accuracy":"","noParticiple":"1","searchRange":null,"isBusiness":"1"}',
                "中标结果公告": '{"token":"","pn":0,"rn":10,"sdt":"","edt":"","wd":"%20","inc_wd":"","exc_wd":"","fields":"title","cnum":"001","sort":"{\\"webdate\\":\\"0\\"}","ssort":"title","cl":2000,"terminal":"","condition":[{"fieldName":"categorynum","equal":"001004","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2},{"fieldName":"projectnumber","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zblx","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zbfw","equal":"0","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"cglb","equal":"A","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0}],"time":[{"fieldName":"webdate","startTime":"1998-01-01 00:00:00","endTime":"2099-12-31 23:59:59"}],"highlights":"","statistics":null,"unionCondition":null,"accuracy":"","noParticiple":"1","searchRange":null,"isBusiness":"1"}',
                "异常公告": '{"token":"","pn":0,"rn":10,"sdt":"","edt":"","wd":"%20","inc_wd":"","exc_wd":"","fields":"title","cnum":"001","sort":"{\\"webdate\\":\\"0\\"}","ssort":"title","cl":2000,"terminal":"","condition":[{"fieldName":"categorynum","equal":"001005","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2},{"fieldName":"projectnumber","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zblx","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zbfw","equal":"0","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"cglb","equal":"A","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0}],"time":[{"fieldName":"webdate","startTime":"1998-01-01 00:00:00","endTime":"2099-12-31 23:59:59"}],"highlights":"","statistics":null,"unionCondition":null,"accuracy":"","noParticiple":"1","searchRange":null,"isBusiness":"1"}'
            },
            "服务": {
                "招采公告/预审公告": '{"token":"","pn":0,"rn":10,"sdt":"","edt":"","wd":"%20","inc_wd":"","exc_wd":"","fields":"title","cnum":"001","sort":"{\\"webdate\\":\\"0\\"}","ssort":"title","cl":2000,"terminal":"","condition":[{"fieldName":"categorynum","equal":"001001","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2},{"fieldName":"projectnumber","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zblx","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zbfw","equal":"0","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"cglb","equal":"S","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0}],"time":[{"fieldName":"webdate","startTime":"1998-01-01 00:00:00","endTime":"2099-12-31 23:59:59"}],"highlights":"","statistics":null,"unionCondition":null,"accuracy":"","noParticiple":"1","searchRange":null,"isBusiness":"1"}',
                "变更公告": '{"token":"","pn":0,"rn":10,"sdt":"","edt":"","wd":"%20","inc_wd":"","exc_wd":"","fields":"title","cnum":"001","sort":"{\\"webdate\\":\\"0\\"}","ssort":"title","cl":2000,"terminal":"","condition":[{"fieldName":"categorynum","equal":"001002","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2},{"fieldName":"projectnumber","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zblx","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zbfw","equal":"0","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"cglb","equal":"S","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0}],"time":[{"fieldName":"webdate","startTime":"1998-01-01 00:00:00","endTime":"2099-12-31 23:59:59"}],"highlights":"","statistics":null,"unionCondition":null,"accuracy":"","noParticiple":"1","searchRange":null,"isBusiness":"1"}',
                "中标候选人公示": '{"token":"","pn":0,"rn":10,"sdt":"","edt":"","wd":"%20","inc_wd":"","exc_wd":"","fields":"title","cnum":"001","sort":"{\\"webdate\\":\\"0\\"}","ssort":"title","cl":2000,"terminal":"","condition":[{"fieldName":"categorynum","equal":"001003","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2},{"fieldName":"projectnumber","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zblx","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zbfw","equal":"0","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"cglb","equal":"S","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0}],"time":[{"fieldName":"webdate","startTime":"1998-01-01 00:00:00","endTime":"2099-12-31 23:59:59"}],"highlights":"","statistics":null,"unionCondition":null,"accuracy":"","noParticiple":"1","searchRange":null,"isBusiness":"1"}',
                "中标结果公告": '{"token":"","pn":0,"rn":10,"sdt":"","edt":"","wd":"%20","inc_wd":"","exc_wd":"","fields":"title","cnum":"001","sort":"{\\"webdate\\":\\"0\\"}","ssort":"title","cl":2000,"terminal":"","condition":[{"fieldName":"categorynum","equal":"001004","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2},{"fieldName":"projectnumber","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zblx","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zbfw","equal":"0","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"cglb","equal":"S","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0}],"time":[{"fieldName":"webdate","startTime":"1998-01-01 00:00:00","endTime":"2099-12-31 23:59:59"}],"highlights":"","statistics":null,"unionCondition":null,"accuracy":"","noParticiple":"1","searchRange":null,"isBusiness":"1"}',
                "异常公告": '{"token":"","pn":0,"rn":10,"sdt":"","edt":"","wd":"%20","inc_wd":"","exc_wd":"","fields":"title","cnum":"001","sort":"{\\"webdate\\":\\"0\\"}","ssort":"title","cl":2000,"terminal":"","condition":[{"fieldName":"categorynum","equal":"001005","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2},{"fieldName":"projectnumber","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zblx","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"zbfw","equal":"0","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0},{"fieldName":"cglb","equal":"S","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":0}],"time":[{"fieldName":"webdate","startTime":"1998-01-01 00:00:00","endTime":"2099-12-31 23:59:59"}],"highlights":"","statistics":null,"unionCondition":null,"accuracy":"","noParticiple":"1","searchRange":null,"isBusiness":"1"}',
            }
        }

        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://bid.ansteel.cn/zbjjxx/bidding_purchase.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        }

    """
    列表页请求
    """
    def start_requests(self):
        for category, info_types in self.category_list.items():
            for info_type, info_param in info_types.items():
                items = {
                    # 一级分类
                    "bid_category": category,
                    # 二级分类
                    "bid_info_type": info_type
                }
                # 列表页请求链接
                link = "https://bid.ansteel.cn/inteligentsearch/rest/esinteligentsearch/getFullTextDataNew"
                yield scrapy.Request(
                    url=link,
                    callback=self.parse,
                    method="POST",
                    body=info_param,
                    headers=self.headers,
                    meta={"items": items,"param": info_param},
                    dont_filter=True
                )

    """
    列表页详情获取（标题、发布时间、详情页链接）
    """
    def parse(self, response):
        # print(f"当前{json.loads(response.meta['param'])['pn']}页")
        # 翻页判断参数
        FLAG = True
        item_info = response.meta["items"]
        listjson = json.loads(response.text)
        data_list = listjson['result']['records']
        for data in data_list:
            # 获取发布时间
            pubtime = data["infodate"]
            if not pubtime:
                print("未获取到时间")
                FLAG = False
                continue
            # 截取发布时间年月日
            pubday = pubtime.split(' ')[0]
            # 获取当前年月日
            nowday = time.strftime("%Y-%m-%d")
            # 当发布时间不是当天时间时，跳出不采
            if pubday != nowday:
                FLAG = False
                print(pubtime + "不是当天最新文章，跳过")
                break
            # 获取文章标题
            title = data['title']
            # 获取文章链接
            url = data['linkurl']
            contentUrl = response.urljoin(url)
            items = {
                "bid_public_time": pubtime,
                "bid_url": contentUrl,
                "bid_name": title,
                "bid_id": get_md5(contentUrl)
            }
            items.update(item_info)
            yield scrapy.Request(
                contentUrl,
                callback=self.getContentInfo,
                meta={"items": items}
            )
        if FLAG == True:
            param = response.meta['param']
            # 当前page
            page = str(re.search('"pn":(\d+),"rn"', param).group(1))
            next_page = str(int(page) + 10)
            param = param.replace(f'"pn":{page},"rn"',f'"pn":{next_page},"rn"')
            yield scrapy.Request(
                url=response.url,
                callback=self.parse,
                method="POST",
                body=param,
                headers=self.headers,
                meta={"items": item_info, "param": param},
                dont_filter=True
            )

    """
    文章详情获取（发布内容）
    """
    def getContentInfo(self, response):
        items_info = response.meta["items"]
        type = items_info["bid_info_type"]
        # 带有html的文本
        if type == "异常公告":
            str_html_content = etree.HTML(response.text).xpath('//div[@class="article-info"]')
        else:
            str_html_content = etree.HTML(response.text).xpath('//div[@class="paragraph-box"]')
        if str_html_content:
            contentHtml = etree.tostring(str_html_content[0], encoding="utf-8").decode()
        else:
            print("未获取到html文本")
        # 纯净文本
        content = remove_node(contentHtml, ["style"]).text
        # 去掉换行、空格、制表符
        content = re.sub('\s|\t|\n', '', content)
        items_infos = BidScrapyProjectItem()
        items_infos['bid_category'] = items_info["bid_category"]
        items_infos['bid_info_type'] = items_info["bid_info_type"]
        items_infos['bid_public_time'] = items_info["bid_public_time"]
        items_infos['bid_name'] = items_info["bid_name"]
        items_infos['bid_html_con'] = contentHtml
        items_infos['bid_content'] = content
        items_infos['bid_url'] = items_info["bid_url"]
        items_infos['website_name'] = "鞍钢智慧招投标平台"
        items_infos['website_url'] = "https://bid.ansteel.cn/zbjjxx/bidding_purchase.html"
        items_infos["bid_id"] = items_info["bid_id"]
        items_infos['create_datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        # print(
        #     items_infos["bid_info_type"],
        #     items_infos["bid_id"],
        #     items_infos["bid_url"],
        #     items_infos["bid_public_time"]
        # )
        yield items_infos