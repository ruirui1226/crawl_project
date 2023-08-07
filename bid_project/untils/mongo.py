# -*- coding: utf-8 -*-
"""
@desc: 
@version: python3
@author: shenr
@time: 2023/8/2 
"""
import pymongo
from bid_project.conf.env_demo import *


class MongoConnection:
    def __init__(
        self, ip=MONGO_HOST, port=MONGO_PORT, user=MONGO_USER, pwd=MONGO_PWD, db=MONGO_DB
    ):
        # 1.创建连接 mongodb://用户名:密码@ip:端口
        client = pymongo.MongoClient(f"mongodb://{user}:{pwd}@{ip}:{port}")

        # 2.指定数据库
        self.db = client[db]

    def insert(self, collection, query, many=False):
        """
        插入方法
        :param collection: 集合
        :param query: 数据
        :param many: 控制是否匹配多个
        :return:
        """
        # 指定集合

        data_collection = self.db[collection]
        if many:
            data_collection.insert_many(query)
        else:
            data_collection.insert_one(query)

    def find(self, collection, query, many=True):
        data_collection = self.db[collection]
        if many:
            result = []
            results = data_collection.find(query)
            for data in results:
                result.append(data)
            return result
        else:
            result = data_collection.find_one(query)
            return result

    def update(self, collection, query, new_value, many=False):
        data_collection = self.db[collection]
        if many:
            data_collection.update_many(query, {"$set": new_value})
        else:
            data_collection.update_one(query, {"$set": new_value})

    def delete(self, collection, query, many=False):
        data_collection = self.db[collection]
        if many:
            data_collection.delete_many(query)
        else:
            data_collection.delete_one(query)
