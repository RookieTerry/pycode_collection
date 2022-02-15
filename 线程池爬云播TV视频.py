#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 HackerTerry, Inc. All Rights Reserved 
#
# @Time    : 2022/2/3 14:07
# @Author  : Terry Zhang
# @Email   : goudan1974@163.com
# @Blog    : https://www.terry906.top
# @File    : 线程池爬云播TV视频.py
# @Software: PyCharm

import requests
import re
from concurrent.futures import ThreadPoolExecutor
from ffmpy3 import FFmpeg

def get_first_m3u8(url,headers):  # 获取第一个m3u8链接
    resp = requests.get(url,headers)
    obj = re.compile(r'"link_pre":"","url":"(?P<first_m3u8>.*?)","url_next"',re.S)  # 正则表达式可按需要修改
    m3u8_url = obj.finditer(resp.text)
    for it in m3u8_url:
        first_m3u8 = it.group("first_m3u8").replace("\\","")
        print(first_m3u8)
        return first_m3u8

def download_first_m3u8(url,name,headers):  # 读取第一个m3u8文件的内容
    resp = requests.get(url,headers)
    with open(name, "w", encoding="utf-8") as f1:
        f1.write(resp.text)
    with open(name,"r") as f2:
        for line in f2:
            if line.startswith("#"):
                continue
            else:
                line.strip()
                print(line)
                return line

def get_second_m3u8(url,headers):  # 获取第二个m3u8链接
    first_m3u8 = get_first_m3u8(url,headers)
    line = download_first_m3u8(first_m3u8,"爬到的视频/first_m3u8.txt",headers)
    second_m3u8 = first_m3u8.split("/20220112")[0] + line
    print(second_m3u8)
    return second_m3u8

def ffmpeg_path(inputs_path, outputs_path):  # ffmpeg下载函数
    '''
    :param inputs_path: 输入的文件传入字典格式{文件：操作}
    :param outputs_path: 输出的文件传入字典格式{文件：操作}
    :return:
    '''
    a = FFmpeg(
                inputs={inputs_path: None},
                outputs={outputs_path: '-c copy',
                         }
    )
    print(a.cmd)
    a.run()

if __name__ == '__main__':
    url = "https://www.yunbtv.net/vodplay/ITgou-1-1.html"  # 使用时只需更改这里的URL即可
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "Referer": "https://www.yunbtv.net/"
    }
    second_m3u8 = get_second_m3u8(url,headers)
    with ThreadPoolExecutor(50) as t:
        t.submit(ffmpeg_path,second_m3u8,"爬到的视频/IT狗第一集.mp4")
