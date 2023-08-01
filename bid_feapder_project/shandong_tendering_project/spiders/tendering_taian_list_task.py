# -*- coding: utf-8 -*-
"""
Created on 2023-06-12 13:58:44
---------
@summary:
---------
@author: zhongxing
"""

import feapder
from feapder import ArgumentParser
from feapder.utils import metrics
from feapder.utils.log import log

from items.t_zx_tendering_shandong_tanan_list_task_item import TZxTenderingShandongTananListTaskItem


class TenderingTaianListTask(feapder.BatchSpider):

    def start_requests(self, task):
        id, url, page, data_id, post_url, one_title, two_title = task
        headers = {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Content-Length": "502",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Host": "www.taggzyjy.com.cn",
                "Origin": "http://www.taggzyjy.com.cn",
                "Proxy-Connection": "keep-alive",
                "Referer": f"http://www.taggzyjy.com.cn/jydt/{data_id}/notice_construction.html",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"
        }
        data = '{"token":"","pn":%s,"rn":15,"sdt":"","edt":"","wd":" ","inc_wd":"","exc_wd":"","fields":"title","cnum":"001","sort":"{\\"webdate\\":0}","ssort":"title","cl":200,"terminal":"","condition":[{"fieldName":"categorynum","equal":"%s","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2}],"time":[{"fieldName":"webdate","startTime":"","endTime":""}],"highlights":"title","statistics":null,"unionCondition":null,"accuracy":"","noParticiple":"0","searchRange":null,"isBusiness":"1"}' % (page, data_id)

        yield feapder.Request(post_url, headers=headers, data=data, url1=url, data_id=data_id, one_title=one_title, two_title=two_title, page=page, task_id=id)

    def parse(self, request, response):
        if response.status_code != 200:
            log.warning(request.target + 'not 200! status:' + str(response.status_code))
            metrics.emit_counter("response_status_not_200", count=1, classify="channel_task")
            return False
        if response is None:
            log.error("response is None! " + request.url)
            metrics.emit_counter("response_is_none", count=1, classify="channel_task")
            yield self.update_task_batch(request.task_id, 1)
            return False
        res_json = response.json
        for items in res_json.get('result').get('records'):
            item = TZxTenderingShandongTananListTaskItem(**items)
            item.url = request.url1
            item.one_title = request.one_title
            item.two_title = request.two_title
            item.page = request.page
            item.data_id = request.data_id
            yield item
        yield self.update_task_batch(request.task_id, 1)

    def exception_request(self, request, response, e):
        log.error("exception_request:" + request.url)
        metrics.emit_counter("exception_request", count=1, classify="channel_task")
        # yield request

    def failed_request(self, request, response, e):
        log.error("failed_request:" + request.url)
        metrics.emit_counter("failed_request", count=1, classify="channel_task")
        yield self.update_task_batch(request.task_id, -1)


if __name__ == "__main__":
    spider = TenderingTaianListTask(
        # task_id=1,
        redis_key="tendering_crawler:shandong_taian_list_task",  # 分布式爬虫调度信息存储位置
        task_table="t_zx_tendering_shandong_taian_seed_task",  # mysql中的任务表
        task_keys=["id", "url", "page", "data_id", "post_url", "one_title", "two_title"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="tanan_list_batch_record",  # mysql中的批次记录表
        batch_name="获取列表任务",  # 批次名字
        batch_interval=1,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    # parser = ArgumentParser(description="TenderingTaianListTask爬虫")
    #
    # parser.add_argument(
    #     "--start_master",
    #     action="store_true",
    #     help="添加任务",
    #     function=spider.start_monitor_task,
    # )
    # parser.add_argument(
    #     "--start_worker", action="store_true", help="启动爬虫", function=spider.start
    # )
    #
    # parser.start()

    # 直接启动
    spider.start()  # 启动爬虫
    # spider.start_monitor_task() # 添加任务

    # 通过命令行启动
    # python tendering_taian_list_task.py --start_master  # 添加任务
    # python tendering_taian_list_task.py --start_worker  # 启动爬虫
