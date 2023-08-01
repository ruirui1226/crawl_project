# -*- coding: utf-8 -*-
# @Time : 2023/7/4 11:25
# @Author: mayj
""" 批量运行爬虫 """
import sys
import logging
from scrapy import spiderloader
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from bid_scrapy_project.common.common import divide_into_n_strand

spider_list = [
    "shandong_ggzy",
    "shandong_cgw",
    "yantai_ggjy",
    "sd_jinan_ggjy",
    "sd_qingdao_ggjy",
    "sd_zibo_ggjy",
    "zaozhuang_ggjy",
    "dongying_ggjy",
    # "weifang",
    "ggzyjy_jining",
    "ggzyjy_taian",
    "ggzyjy_weihai",
    "rizhao_ggzy",
    "linyi",
    "dezhou_ggzy",
    "sd_liaocheng_ggjy",
    "binzhou_ggzy",
]

error_spider_list = ["weifang", "gansu_ggjy", "guangdong_ggjy", "jiangsu_ggjy", "Xinjiang", "fujian_cgw"]

question_list = ["heilongj_cgw"]

# 批次id
batch_id = "n"
# 分几批执行
nums = "4"
try:
    batch_id = sys.argv[1]
except:
    pass

try:
    nums = sys.argv[2]
except:
    pass


def run_spider():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    # 查看现有爬虫
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)
    crawlers = []
    # 将 spider 逐个添加到 CrawlerProcess 实例及 crawlers 列表中

    # for spider in spider_loader.list():
    # 根据传入参数判断运行哪个批次的爬虫
    if batch_id == "n":
        new_spider_list = spider_list
    else:
        new_spider_list = list(set(spider_loader.list()) - set(spider_list) - set(error_spider_list))
        new_spider_list.sort()
        new_spider_list = divide_into_n_strand(new_spider_list, int(nums))[int(batch_id)]
        new_spider_list = list(set(new_spider_list) - set(question_list))

    for spider in new_spider_list:
        logging.info(f"Running spider {spider}")
        crawler = process.create_crawler(spider)
        crawlers.append(crawler)
        process.crawl(crawler)

    # 开始爬虫
    process.start()
    # 获取爬虫的统计信息
    stats_dict = {}
    for crawler in crawlers:
        stats_dict[crawler.spider.name] = crawler.stats.get_stats()

    return stats_dict


def main():
    spider_stats = run_spider()
    logging.info(spider_stats)


if __name__ == "__main__":
    main()
