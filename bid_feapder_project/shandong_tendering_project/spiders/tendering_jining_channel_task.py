# -*- coding: utf-8 -*-
"""
Created on 2023-06-07 17:35:54
---------
@summary:
---------
@author: zhongxing
"""

import feapder
from feapder import ArgumentParser
from feapder.utils import metrics
from feapder.utils.log import log

from items.t_zx_tendering_shandong_jining_seed_task_item import TZxTenderingShandongJiningSeedTaskItem


class TenderingJining(feapder.BatchSpider):

    def start_requests(self, task):
        id, url = task
        yield feapder.Request(url, task_id=id, callback=self.channel_parse)

    def channel_parse(self, request, response):
        if response.status_code != 200:
            log.warning(request.target + 'not 200! status:' + str(response.status_code))
            metrics.emit_counter("response_status_not_200", count=1, classify="channel_task")
            return False
        if response is None:
            log.error("response is None! " + request.url)
            metrics.emit_counter("response_is_none", count=1, classify="channel_task")
            yield self.update_task_batch(request.task_id, 1)
            return False
        # panel_list = response.xpath('//div[@id="myAccordion"]//a[@class="nav-link"]')
        panel_list = response.xpath('//div[@id="myAccordion"]//div[@class="panel"]')
        for panel in panel_list:
            one_title = panel.xpath('./div[@class="column-header"]/a[@data-toggle="collapse"]/text()').extract_first()
            nav_links = panel.xpath('.//a[@class="nav-link"]')
            for nav_link in nav_links:
                for page_i in range(0, 60, 20):
                    two_title = nav_link.xpath(".//span[@class='title']/text()").extract_first().replace(' ', '').replace('\r\n', '')
                    url = nav_link.xpath("./@href").extract_first()
                    post_url = 'https://jnggzy.jnzbtb.cn:4430/api/services/app/stPrtBulletin/GetBulletinList'
                    data_id = nav_link.xpath("./@data-id").extract_first()
                    item = TZxTenderingShandongJiningSeedTaskItem()
                    item.url = url
                    item.post_url = post_url
                    item.data_id = data_id
                    item.page = page_i
                    item.one_title = one_title
                    item.two_title = two_title
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
    spider = TenderingJining(
        # task_id=1,
        redis_key="tendering_crawler:shandong_jining_channel_task",  # 分布式爬虫调度信息存储位置
        task_table="t_zx_tendering_shandong_jining_channel_task",  # mysql中的任务表
        task_keys=["id", "url"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="t_zx_jining_batch_record",  # mysql中的批次记录表
        batch_name="获取种子任务",  # 批次名字
        batch_interval=1,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    # parser = ArgumentParser(description="TenderingJining爬虫")
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
    # python tendering_jining_channel_task.py --start_master  # 添加任务
    # python tendering_jining_channel_task.py --start_worker  # 启动爬虫
