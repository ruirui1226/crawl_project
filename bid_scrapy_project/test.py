# -*- coding: utf-8 -*-
# @Time : 2023/6/14 9:55
# @Author: mayj
import json

data = '{"token":"","pn":0,"rn":10,"sdt":"","edt":"","wd":"","inc_wd":"","exc_wd":"","fields":"","cnum":"","sort":"{\\"webdate\\":\\"0\\",\\"id\\":\\"0\\"}","ssort":"","cl":10000,"terminal":"","condition":[{"fieldName":"categorynum","equal":"002","notEqual":null,"equalList":null,"notEqualList":null,"isLike":true,"likeType":2}],"time":[{"fieldName":"webdate","startTime":"2023-06-15 00:00:00","endTime":"2023-06-15 23:59:59"}],"highlights":"","statistics":null,"unionCondition":[],"accuracy":"","noParticiple":"1","searchRange":null,"noWd":true}'

a = json.loads(data)
a["pn"] = 10
print(type(a))