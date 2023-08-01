# coding:utf-8
"""
    布隆过滤器
"""
import redis
from hashlib import md5

from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class BloomFilter(object):
    def __init__(
        self,
        host=settings["REDIS_HOST"],
        pwd=settings["REDIS_PWD"],
        port=6379,
        db=0,
        blockNum=1,
        key="bid_scrapy_project:bloomfilter",
    ):
        self.server = redis.Redis(host=host, password=pwd, port=port, db=db)
        self.bit_size = 1 << 31  # Redis的String类型最大容量为512M，现使用256M
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.key = key
        self.blockNum = blockNum
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

    def isContains(self, str_input):
        """判断数据是否存在"""
        if not str_input:
            return False
        m5 = md5()
        m5.update(str_input.encode("utf-8"))
        str_input = m5.hexdigest()
        ret = True
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            ret = ret & self.server.getbit(name, loc)
        return ret

    def insert(self, str_input):
        """插入数据"""
        m5 = md5()
        m5.update(str_input.encode("utf-8"))
        str_input = m5.hexdigest()
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            self.server.setbit(name, loc, 1)


# if __name__ == '__main__':
#     """ 第一次运行时会显示 not exists!，之后再运行会显示 exists! """
#     bf = BloomFilter()
#     if bf.isContains('http://www.tencent.com'):  # 判断字符串是否存在
#         print('exists!')
#     else:
#         print('not exists!')
#         bf.insert('http://www.tencent.com')
