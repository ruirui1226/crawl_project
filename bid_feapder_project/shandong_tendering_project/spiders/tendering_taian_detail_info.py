# -*- coding: utf-8 -*-
"""
Created on 2023-06-12 17:43:14
---------
@summary:
---------
@author: zhongxing
"""

import feapder
from feapder import ArgumentParser
from feapder.utils import metrics
from feapder.utils.log import log

from items.t_zx_tendering_shandong_taian_details_info_item import TZxTenderingShandongTaianDetailsInfoItem


class TeneringTaianDetailInfo(feapder.BatchSpider):
    def start_requests(self, task):
        id, linkurl = task
        url = 'http://www.taggzyjy.com.cn/' + linkurl
        yield feapder.Request(url, task_id=id, linkurl=linkurl)

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
        detail = response.text
        item = TZxTenderingShandongTaianDetailsInfoItem()
        item.url = request.url
        item.linkurl = request.linkurl
        item.details_content = detail
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
    spider = TeneringTaianDetailInfo(
        # task_id=1,
        redis_key="tendering_crawler:shandong_taian_list_task",  # 分布式爬虫调度信息存储位置
        task_table="t_zx_tendering_shandong_tanan_list_task",  # mysql中的任务表
        task_keys=["id", "linkurl"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="taian_details_batch_record",  # mysql中的批次记录表
        batch_name="泰安详情任务",  # 批次名字
        batch_interval=1,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    # parser = ArgumentParser(description="TeneringTaianDetailInfo爬虫")
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
    # python tendering_taian_detail_info.py --start_master  # 添加任务
    # python tendering_taian_detail_info.py --start_worker  # 启动爬虫
