# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import json
import logging

from pymysql import cursors
from kafka import KafkaProducer
from kafka.errors import kafka_errors
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings

from bid_scrapy_project.common.common import parse_escape_string, parse_string, parse_json_data, parse_date
from bid_scrapy_project.common.convert_item import convert_data
from bid_scrapy_project.common.my_filter import Redis_Fingerprint
from bid_scrapy_project.items import BidScrapyProjectItem, GovernmentProcurementItem

settings = get_project_settings()


class DupefilterPipeline(object):
    """格式化相关，列表详情去重"""

    def __init__(self):
        self.rf = Redis_Fingerprint()

    def process_item(self, item, spider):
        for field in item.fields:
            item.setdefault(field, "")

        if isinstance(item, BidScrapyProjectItem):
            item["bid_content"] = parse_string(item["bid_content"])
            item["bid_json_data"] = parse_json_data(item["bid_json_data"])
            item["bid_public_time"] = parse_date(item["bid_public_time"])
            if item["bid_html_con"]:
                item["bid_html_con"] = item["bid_html_con"].strip()

        elif isinstance(item, GovernmentProcurementItem):
            item["po_content"] = parse_string(item["po_content"])
            item["po_json_data"] = parse_json_data(item["po_json_data"])
            item["po_public_time"] = parse_date(item["po_public_time"])
            if item["po_html_con"]:
                item["po_html_con"] = item["po_html_con"].strip()
        if settings.get("SCHEDULER_PERSIST", False):
            if item.get("list_parse", ""):
                url = item["list_parse"]
                if self.rf.run(spider.name, url):
                    raise DropItem()

        return item


class BidScrapyProjectPipeline(object):
    """使用mysql存储数据"""

    def __init__(self, db_pool):
        self.db_pool = db_pool
        # self.bf = BloomFilter()

    @classmethod
    def from_settings(cls, settings):
        db_params = dict(
            host=settings["MYSQL_HOST"],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            port=settings["MYSQL_PORT"],
            database=settings["MYSQL_DBNAME"],
            charset="utf8",
            use_unicode=True,
            cursorclass=cursors.DictCursor,
        )
        # 创建连接池
        db_pool = adbapi.ConnectionPool("pymysql", **db_params)

        # 返回一个pipeline对象
        return cls(db_pool)

    def process_item(self, item, spider):
        # if isinstance(item, BidScrapyProjectItem):
        # 设置 item默认值,防止item不全报错
        for field in item.fields:
            item.setdefault(field, "")
        # 把要执行的sql放入连接池
        query = self.db_pool.runInteraction(self.insert, item)
        # 如果sql执行发送错误,自动回调addErrBack()函数
        query.addErrback(self.handle_error)

        # 返回Item
        return item

    def insert(self, cursor, item):
        table_name = settings["MYSQL_TABLE_NAME_NEW"]
        new_item = convert_data(item)
        str_fields = ", ".join([fields for fields, data in new_item.items()])
        str_data = "'" + "', '".join("%s" % parse_escape_string(data) for fields, data in new_item.items()) + "'"
        sql = f"""insert into {table_name} ({str_fields}) values ({str_data}) """
        try:
            cursor.execute(sql)
        except Exception as e:
            logging.error(f'数据插入异常-{e}:{item["bid_url"]}')
        else:
            logging.info(f"新数据入库-{item['bid_url']}")

    # 错误函数
    def handle_error(self, failure):
        # #输出错误信息
        if failure:
            logging.error(f"数据插入失败,原因是:{failure}")


class KafkaPipeline(object):
    """使用kafka处理数据"""

    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=settings["KAFKA_IP_PORT"])

    def process_item(self, item, spider):
        for field in item.fields:
            item.setdefault(field, "")

        bid_key = settings["MYSQL_TABLE_NAME"]
        new_item = convert_data(item)
        # 存入kafka的数据需要 encode
        data_str = json.dumps(
            new_item,
            sort_keys=True,
            # indent=4,
            # separators=(",", ":"),
            # ensure_ascii=False,
        )
        future = self.producer.send(
            settings["KAFKA_TOPIC_NAME"], key=bytes(bid_key, encoding="utf-8"), value=bytes(data_str, encoding="utf-8")
        )
        try:
            future.get(timeout=10)
            logging.info(f'{item["bid_url"]}:数据发送成功')
        except kafka_errors:
            logging.error(f'{item["bid_url"]}:数据发送失败：{kafka_errors}')

        return item

    def close_spider(self, spider):
        # 结束后关闭producer
        self.producer.close()
