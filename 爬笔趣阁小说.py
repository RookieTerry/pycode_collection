#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 HackerTerry, Inc. All Rights Reserved
#
# @Time    : 2022/1/24 22:12
# @Author  : Terry Zhang
# @Email   : goudan1974@163.com
# @Blog    : https://www.terry906.top
# @File    : 异步爬小说.py
# @Software: PyCharm

# 这里以刘慈欣的《流浪地球》为例
# 所有章节的内容和名称：https://www.bbiquge.net/book_126623/     
# 某一个章节内容：https://www.bbiquge.net/book_126623/45495704.html

import requests
import os
import json
from lxml import etree

os.environ['NO_PROXY'] = 'www.bbiquge.net'
dict = {}
title_list = []
link_list = []

def getCatalog(url,headers):
    resp = requests.get(url,headers).text
    tree = etree.HTML(resp)
    dl_list = tree.xpath("/html/body/div[4]/dl[@class='zjlist']/dd/a[@href]")
    for dl in dl_list:
        for i in range(0,len(dl_list)):
            title = dl.xpath("/html/body/div[4]/dl/dd/a/text()")
            title_list.append(str(title[i]))
            link = dl.xpath("/html/body/div[4]/dl/dd/a/@href")
            link_list.append(str(link[i]))
            dict[title[i]] = url + link[i]
    with open("爬到的小说/小说列表.txt", "w") as f:
        f.write(json.dumps(dict,ensure_ascii=False))  # json库中的dumps方法把字典写入文件
    print(dict)
    return dict


def getContent(url,headers):
    resps = requests.get(url,headers).text
    trees = etree.HTML(resps)
    article = trees.xpath("/html/body/div[3]/div[2]/div[1][@id='content']/text()")
    print(article)
    return article

if __name__ == '__main__':
    url = 'https://www.bbiquge.net/book_126623/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55",
        "Referer": "https://www.bbiquge.net/book_126623/",
        "Connection": "close"
    }
    if not os.path.exists("爬到的小说/笔趣阁"):
        print("没有'笔趣阁'这个目录，正在为你创建>>>>>")
        os.mkdir("爬到的小说/笔趣阁")
        print("创建成功>>>>>")
    dicts = getCatalog(url,headers)
    for key,value in dicts.items():
        articles = getContent(value, headers)
        with open("爬到的小说/笔趣阁/流浪地球" + key + ".txt", "w", encoding="utf-8") as f:
            f.writelines(str(articles).replace("&quot;","").replace("\xa0","") + '\n')   # writelines方法可将字符串或列表写入文件中
