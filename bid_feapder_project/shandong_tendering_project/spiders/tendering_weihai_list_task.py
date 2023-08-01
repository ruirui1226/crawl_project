# -*- coding: utf-8 -*-
"""
Created on 2023-06-12 16:31:13
---------
@summary:
---------
@author: zhongxing
"""

import feapder
from feapder import ArgumentParser
from feapder.utils import metrics
from feapder.utils.log import log

from items.t_zx_tendering_shandong_weihai_list_task_item import TZxTenderingShandongWeihaiListTaskItem


class TenderingWeihaiListTask(feapder.BatchSpider):

    def start_requests(self, task):
        id, url, post_url, page, data_id, one_title, two_title = task
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Authorization': 'Bearer 764e677d5eb4e9937a0846a9c386f707',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=2F3189429E6831D248BC5D025D81E57E; oauthClientId=demoClient; oauthPath=http://127.0.0.1:8080/EpointWebBuilder; oauthLoginUrl=http://127.0.0.1:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://127.0.0.1:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=f199ec915d7e95f18232898286f0da0a; noOauthAccessToken=764e677d5eb4e9937a0846a9c386f707',
            'Origin': 'http://ggzyjy.weihai.cn',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://ggzyjy.weihai.cn/jyxx/003001/transInfo.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        data = f'params=%7B%22siteGuid%22%3A%227eb5f7f1-9041-43ad-8e13-8fcb82ea831a%22%2C%22categoryNum%22%3A%22{data_id}%22%2C%22kw%22%3A%22%22%2C%22startDate%22%3A%22%22%2C%22endDate%22%3A%22%22%2C%22pageIndex%22%3A{page}%2C%22pageSize%22%3A12%2C%22area%22%3A%22%22%7D'
        yield feapder.Request(post_url, headers=headers, url1=url, data=data, task_id=id, data_id=data_id, page=page, one_title=one_title, two_title=two_title)

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
        for items in res_json.get('custom').get('infodata'):
            item = TZxTenderingShandongWeihaiListTaskItem(**items)
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
    spider = TenderingWeihaiListTask(
        # task_id=1,
        redis_key="tendering_crawler:shandong_weihai_list_task",  # 分布式爬虫调度信息存储位置
        task_table="t_zx_tendering_shandong_weihai_seed_task",  # mysql中的任务表
        task_keys=["id", "url", "post_url", "page", "data_id", "one_title", "two_title"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="weihai_list_batch_record",  # mysql中的批次记录表
        batch_name="获取列表任务",  # 批次名字
        batch_interval=1,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    # parser = ArgumentParser(description="TenderingWeihaiListTask爬虫")
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
    # python tendering_weihai_list_task.py --start_master  # 添加任务
    # python tendering_weihai_list_task.py --start_worker  # 启动爬虫
