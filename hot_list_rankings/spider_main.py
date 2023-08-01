# -*- coding: utf-8 -*-
"""
@desc: 
@version: python3
@author: shenr
@time: 2023/7/7 
"""
import os
cmd_list = ["baidu.py", "bilibili.py", "douyin.py", "toutiao.py", "weibo.py", "weixin.py", "xiaohongshu.py"]
for each in cmd_list:
    print(f"=============当前爬取{each}===============")
    cmd = f"python {each}"
    os.system(cmd)
