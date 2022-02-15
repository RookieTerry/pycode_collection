#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 HackerTerry, Inc. All Rights Reserved 
#
# @Time    : 2022/1/29 17:49
# @Author  : Terry Zhang
# @Email   : zhangtianyu906@gmail.com
# @Blog    : https://www.terry906.top
# @File    : 爬豆瓣top250.py
# @Software: PyCharm

import requests
import re
import csv

url = "https://movie.douban.com/top250"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    "Referer": "https://movie.douban.com/top250",
    "Connection": "close"
}
resp = requests.get(url,headers)
page_content = resp.text
print(page_content)
obj = re.compile(r'<li>.*?<div class="item">.*?<span class="title">(?P<name>.*?)</span>.*?<p class="">.*?<br>(?P<year>.*?)&nbsp.*?<span '
                 r'class="rating_num" property="v:average">(?P<rate>.*?)'
                 r'</span><span property="v:best" content="10.0"></span><span>(?P<num>.*?人评价)</span>',re.S)
result = obj.finditer(page_content)
f = open("douban.csv","w",encoding="utf-8",newline="")
csvwriter = csv.writer(f)
for it in result:
    # print(it.group("name"))
    # print(it.group("year"))
    # print(it.group("rate"))
    # print(it.group("num"))
    dict = it.groupdict()
    dict["year"] = dict["year"].strip()
    csvwriter.writerow(dict.values())
f.close()
