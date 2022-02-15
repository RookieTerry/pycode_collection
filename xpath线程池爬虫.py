#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
# Copyright (C) 2021 HackerTerry, Inc. All Rights Reserved
#
# @Time    : 2022/1/20 21:39
# @Author  : Terry Zhang
# @Email   : zhangtianyu906@gmail.com
# @Blog: https://www.terry906.top
# @File    : xpath爬虫.py
# @Software: PyCharm

# 爬取武汉白沙洲农副产品大市场当天菜价

import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import csv

file = open("price.csv","w",encoding='utf-8')
csvwriter = csv.writer(file)

def get_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55"
    }
    resp = requests.get(url=url,headers=headers).text
    requests.get(url,headers).encoding = 'utf-8'
    # parser = etree.HTMLParser(encoding='utf-8')
    tree = etree.HTML(resp)
    result = tree.xpath("/html/body/form/table[4]/tr/td[3]/table[5]")[0]  # 注意删掉tbody
    trs = result.xpath("./tr")
    for tr in trs:
        txt = tr.xpath("./td/text()")
        csvwriter.writerow(txt)
    print(url+"爬取完毕！")

if __name__ == '__main__':
    with ThreadPoolExecutor(20) as t:  # 一个线程池中有20个线程
        for i in range(1,67):
            t.submit(get_price,f"http://www.whbsz.com.cn/Price.aspx?PageNo={i}")

