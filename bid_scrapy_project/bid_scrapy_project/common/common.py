# -*- coding: utf-8 -*-
# @Time : 2023/6/14 10:43
# @Author: mayj
import re
import time
import hashlib
import datetime
from datetime import datetime as datetime1

import logging
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from lxml import html
from pymysql.converters import escape_string


def get_md5(key: str):
    """生成MD5,统一id长度"""
    key += "&1234"
    md5_obj = hashlib.md5(key.encode("utf-8"))
    return md5_obj.hexdigest()


def urljoin_url(base_url, url):
    """拼接完整url"""
    if "http" not in url:
        url = urljoin(base_url, url)
    return url


def parse_escape_string(need_str):
    """处理字符串转义字符"""
    if isinstance(need_str, tuple):
        try:
            need_str = need_str[0]
        except:
            pass
    if isinstance(need_str, str):
        need_str = escape_string(need_str)
    return need_str


def timestamp_to_str(timeStamp):
    """时间戳转换为标准日期"""
    if len(str(timeStamp)) == 13:
        timeStamp = float(timeStamp / 1000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def gettime_day(days=3, tomorrow=0, cut=False):
    """
    获取当前时间, 几天前时间（默认）或几天后时间
    :param days: 多少天前时间
    :param tomorrow: 多少天后时间
    :param cut: 返回时间格式 2022-11-11 11:11:11（False） 2022-11-11（True）
    :return: 获取当前时间(end_of_day), 几天前时间或几天后时间(start_of_day)
    """
    current_date = datetime.date.today()
    end_of_day = datetime.datetime.combine(current_date, datetime.time(23, 59, 59))
    if tomorrow:
        three_days_ago = end_of_day + datetime.timedelta(tomorrow)
    else:
        three_days_ago = end_of_day - datetime.timedelta(days)
    start_of_day = three_days_ago.replace(hour=0, minute=0, second=0)
    if cut:
        end_of_day = str(end_of_day).split(" ")[0]
        start_of_day = str(start_of_day).split(" ")[0]
    return end_of_day, start_of_day


def divide_into_n_strand(listTemp, n):
    """将一个list尽量均分成n份，限制len(list)==n，份数大于原list内元素个数则分配空list[]"""
    twoList = [[] for i in range(n)]
    for i, e in enumerate(listTemp):
        twoList[i % n].append(e)
    return twoList


def time_standard(old_time):
    """时间格式转换"""
    timeArray = time.strptime(old_time, "%y.%m.%d")
    ts = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return ts


def parse_string(content):
    """处理字符串空格，换行符等"""
    if content:
        try:
            content = content.replace("\n", "").replace("\r", "")
            content = re.sub(r"\s+", "", content)
        except:
            pass
    if content:
        try:
            content.strip()
        except:
            pass

    return content


def parse_json_data(data):
    """处理json_data"""
    if data:
        data = str(data)
    return data


def parse_date(date_str):
    """处理时间字符串"""
    if not date_str:
        logging.error("时间字符串不存在")
        return date_str
    date_str = str(date_str)
    if "/" in date_str:
        date_str = date_str.replace("/", "-")
    return date_str


def remove_node(HTML, tags):
    """
    删除tag （style） 标签名
    tags 列表  ["style", "script"]
    """
    tree = html.fromstring(HTML)
    for tag in tags:
        ele = tree.xpath("//{}".format(tag))
        for e in ele:
            e.getparent().remove(e)
    Html = html.tostring(tree).decode()
    return BeautifulSoup(Html, "lxml")


def format_time(time_str):
    time_str = str(time_str)
    # 定义各种可能的时间格式
    if "日" in time_str or "秒" in time_str:
        time_str = (
            time_str.replace("年", "-")
            .replace("月", "-")
            .replace("日", "")
            .replace("T", " ")
            .replace("时", "")
            .replace("分", ":")
            .replace("秒", "")
            .replace("：", ":")
        )
    else:
        time_str = (
            time_str.replace("年", "-")
            .replace("月", "")
            .replace("T", " ")
            .replace("时", "")
            .replace("分", "")
            .replace("：", ":")
        )
    if "上午" in time_str:
        time_str = time_str.replace("上午", "AM")
    elif "下午" in time_str:
        time_str = time_str.replace("下午", "PM")
    formats = [
        "%Y-%m-%d%p%I:%M",
        "%Y-%m-%d%p%I:%M:%S",
        "%Y-%m-%d %p%I:%M",
        "%Y-%m-%d %p%I:%M:%S",
        "%Y-%m-%d%I:%M%p",
        "%Y-%m-%d%I:%M:%S%p",
        "%Y-%m-%d %I:%M%p",
        "%Y-%m-%d %I:%M:%S%p",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M",
        "%Y-%m-%d%H:%M:%S",
        "%Y/%m/%d%H:%M:%S",
        "%Y-%m-%d%H:%M",
        "%Y/%m/%d%H:%M",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%H:%M:%S",
        "%H:%M",
    ]

    for fmt in formats:
        try:
            dt = datetime1.strptime(time_str, fmt)
            formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            return formatted_time

        except ValueError:
            pass

    return time_str