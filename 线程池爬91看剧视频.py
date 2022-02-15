#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 HackerTerry, Inc. All Rights Reserved 
#
# @Time    : 2022/1/29 16:15
# @Author  : Terry Zhang
# @Email   : goudan1974@163.com
# @Blog    : https://www.terry906.top
# @File    : 爬91看剧视频.py
# @Software: PyCharm

# 这里以爬取电影《黑客帝国：矩阵重启》为例

import requests
import re
import os
from concurrent.futures import ThreadPoolExecutor

def download_m3u8(url,headers):  # 下载m3u8文件
    resp = requests.get(url,headers)
    obj = re.compile(r"url: '(?P<url>.*?)',",re.S)  # 正则表达式也可替换为：r'var m3u8 = "(?P<url>.*?)";'
    m3u8_url = obj.search(resp.text).group("url")
    print(m3u8_url)
    resp.close()
    download = requests.get(m3u8_url)
    with open("爬到的视频/黑客帝国：矩阵重启.m3u8","wb") as f:
        f.write(download.content)
    download.close()

def download_ts(file,resps):
    # resps = requests.get(row, headers)
    ff = open(file,"wb")
    print(resps.content)
    ff.write(resps.content)
    ff.close()

# def merge_files():  # 合并文件
#     mergefiledir = os.getcwd() + '\\MergeFiles'
#     # 获取当前文件夹中的文件名称列表
#     filenames = os.listdir(mergefiledir)
#     # 打开当前目录下的result.txt文件，如果没有则创建
#     file = open('result.txt', 'w')
#     # 向文件中写入字符
#
#     # 先遍历文件名
#     for filename in filenames:
#         filepath = mergefiledir + '\\'
#         filepath = filepath + filename
#         # 遍历单个文件，读取行数
#         for line in open(filepath):
#             file.writelines(line)
#         file.write('\n')
#         # 关闭文件
#     file.close()

if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "Referer": "https://www.91kanju2.com/vod-detail/61343.html"
    }
    url = "https://www.91kanju2.com/vod-play/61343-1-1.html"
    download_m3u8(url,headers)
    # 解析m3u8并下载视频切片
    with open("爬到的视频/黑客帝国：矩阵重启.m3u8", "r", encoding="utf-8") as f:
        n = 1
        for row in f:
            row = row.strip()
            if row.startswith("#"):
                continue
            print(row)
            resps = requests.get(row,headers)
            while True:
                with ThreadPoolExecutor(50) as t:
                    t.submit(download_ts, f"爬到的视频/{n}.ts", resps)
                    if (resps.status_code) != 200:
                        break
                    else:
                        n += 1
                        print("One done!")
    print("All done!")
    os.system('copy ./爬到的视频/*.ts ./爬到的视频/黑客帝国：矩阵重启.mp4')