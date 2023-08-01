# -*- coding: utf-8 -*-
"""
Created on 2023-06-09 09:16:37
---------
@summary:
---------
@author: zhongxing
"""

import feapder
import requests
from feapder.network.user_pool import GuestUserPool
from feapder.utils import metrics
from feapder.utils.log import log

from items.t_zx_tendering_shandong_jining_list_task_item import TZxTenderingShandongJiningListTaskItem


class TenderingJiningListTask(feapder.BatchSpider):

    def init_task(self):
        pass

    def start_requests(self, task):
        id, url, post_url, page, data_id, one_title, two_title = task
        r = requests.get(url, verify=False)
        Token = r.cookies.get("XSRF-TOKEN")
        r_token = r.cookies.get('__RequestVerificationToken')
        # user_pool = GuestUserPool("jining:user_pool", page_url=url)  # 暂时停用，框架有BUG
        # user = user_pool.get_user(block=True)
        data = '{"skipCount":%s,"maxResultCount":20,"categoryCode":"%s","includeAllSite":false,"FilterText":"","tenantId":"3","regionId":"0","tenderProjectType":""}'% (page, data_id)
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Content-Length": "148",
            "Content-Type": "application/json",
            "Cookie": f"__RequestVerificationToken={r_token}; XSRF-TOKEN={Token}",
            "Host": "jnggzy.jnzbtb.cn:4430",
            "Origin": "https://jnggzy.jnzbtb.cn:4430",
            "Referer": f"https://jnggzy.jnzbtb.cn:4430/JiNing/Bulletins?CategoryCode={data_id}",
            "Sec-Ch-Ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "X-Xsrf-Token": Token
        }
        yield feapder.Request(post_url, url1=url, data=data, headers=headers, task_id=id, one_title=one_title, two_title=two_title, page=page, data_id=data_id)

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
        for items in res_json.get('result').get('items'):
            item = TZxTenderingShandongJiningListTaskItem()
            item.url = request.url1
            item.one_title = request.one_title
            item.two_title = request.two_title
            item.page = request.page
            item.data_id = request.data_id
            item.category_code = items.get('categoryCode')
            item.release_date = items.get('releaseDate')
            item.title = items.get('title')
            item.creation_time = items.get('creationTime')
            item.last_modification_time = items.get('lastModificationTime')
            item.list_id = items.get('id')
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
    spider = TenderingJiningListTask.to_DebugBatchSpider(
        task_id=1,
        redis_key="tendering_crawler:shandong_jining_seed_task",  # 分布式爬虫调度信息存储位置
        task_table="t_zx_tendering_shandong_jining_seed_task",  # mysql中的任务表
        task_keys=["id", "url", "post_url", "page", "data_id", "one_title", "two_title"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="jining_list_batch_record",  # mysql中的批次记录表
        batch_name="获取列表任务",  # 批次名字
        batch_interval=1,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    # parser = ArgumentParser(description="TenderingJiningListTask爬虫")
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

    # parser.start()

    # 直接启动
    spider.start()  # 启动爬虫
    # spider.start_monitor_task() # 添加任务

    # 通过命令行启动
    # python tendering_jining_list_task.py --start_master  # 添加任务
    # python tendering_jining_list_task.py --start_worker  # 启动爬虫
