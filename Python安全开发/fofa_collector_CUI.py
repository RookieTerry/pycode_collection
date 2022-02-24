#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 HackerTerry, Inc. All Rights Reserved 
#
# @Time    : 2022/2/19 22:30
# @Author  : Terry Zhang
# @Email   : goudan1974@163.com
# @Blog    : https://www.terry906.top
# @File    : fofa_collector_CUI.py
# @Software: PyCharm
# 2022年新版fofa批量脚本

import asyncio
import aiohttp
import aiofiles
import argparse
import base64
import re
import csv

async def fofa_search(email,word,key,proxies,size):
    global results
    word = (base64.b64encode(bytes(word.strip('\''),encoding='utf-8'))).decode('utf-8')
    url = f"https://fofa.info/api/v1/search/all?email={email}&key={key}&qbase64={word}&size={size}"
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55"
    }
    proxies = {
        "https":"https://" + proxies
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url,headers=headers,proxies=proxies,verify=False,timeout=15) as resp:
                resp = await resp.text()
                obj = re.compile(r'"results":(.*?),"size":',re.S)
                results = eval(obj.findall(resp)[0])  # eval函数把字符串形式的列表转换成二维列表
                print("[+]已找到结果，准备保存为表格...")
    except Exception as e:
        print("[!]"+str(e))
        exit()
    except KeyboardInterrupt:
        print("[-]用户操作退出...")
        exit()

    try:
        async with aiofiles.open("脚本生成/fofa_result.csv","w") as f:
            csvwriter = csv.writer(f)
            for result in results:
                await csvwriter.writerow(result)
        print("[+]已保存为表格！")
    except Exception as e:
        print("[!]"+str(e))
        exit()
    except KeyboardInterrupt:
        print("[-]用户操作退出...")
        exit()

if __name__ == '__main__':
    print('''
     _____      __        ____      _ _           _
    |  ___|__  / _| __ _ / ___|___ | | | ___  ___| |_ ___  _ __
    | |_ / _ \| |_ / _` | |   / _ \| | |/ _ \/ __| __/ _ \| '__|
    |  _| (_) |  _| (_| | |__| (_) | | |  __/ (__| || (_) | |
    |_|  \___/|_|  \__,_|\____\___/|_|_|\___|\___|\__\___/|_|   2022 v1.0

    版权所有 (C) 2022 HackerTerry,保留所有权利
    
    ''')

    parser = argparse.ArgumentParser(usage="python3 fofa_collector_CUI.py [-h] [-e] [-w] [-t] [-p] [-s]")
    parser.add_argument('-e', '--email', type=str,required=True,help='fofa注册邮箱')
    parser.add_argument('-w','--word',type=str,required=True,help='fofa查询语法')
    parser.add_argument('-k','--key',type=str,required=True,help='fofa会员api key')
    parser.add_argument('-p','--proxies',type=str,required=False,help='代理服务器ip和端口，可不指定')
    parser.add_argument('-s','--size',type=int,required=False,default=100,help='单次查询返回记录数，最大为10000')
    args = parser.parse_args()
    if not args.proxies:
        args.proxies = ''

    asyncio.run(fofa_search(args.email,args.word,args.key,args.proxies,args.size))
