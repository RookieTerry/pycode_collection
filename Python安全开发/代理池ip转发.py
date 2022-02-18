#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 HackerTerry, Inc. All Rights Reserved 
#
# @Time    : 2022/2/19 11:30
# @Author  : Terry Zhang
# @Email   : goudan1974@163.com
# @Blog    : https://www.terry906.top
# @File    : 代理池ip转发.py
# @Software: PyCharm

import socket, time, random, threading, requests, re
from socket import error

localtime = time.asctime(time.localtime(time.time()))


class ProxyServerTest():
    def __init__(self, proxyip):
        # 本地socket服务
        self.ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.proxyip = proxyip

    def run(self):
        global mbsocket
        try:
            # 本地服务IP和端口
            self.ser.bind(('127.0.0.1', 5320))
            # 最大连接数
            self.ser.listen(10)
        except error as e:
            print("[-]The local service : " + str(e))
            return "[-]The local service : " + str(e)

        while True:
            try:
                # 接收客户端数据
                client, addr = self.ser.accept()
                print('[*]accept %s connect' % (addr,))
                data = client.recv(1024)
                if not data:
                    break
                print('[*' + localtime + ']: Accept data...')
            except error as e:
                print("[-]Local receiving client : " + str(e))
                return "[-]Local receiving client : " + str(e)

            while True:
                # 目标代理服务器，将客户端接收数据转发给代理服务器
                mbsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                print("[!]Now proxy ip:" + str(self.proxyip))
                prip = self.proxyip[0]
                prpo = self.proxyip[1]

                try:
                    mbsocket.settimeout(3)
                    mbsocket.connect((prip, prpo))
                except:
                    print("[-]RE_Connect...")
                    continue
                break

            try:
                mbsocket.send(data)
            except error as e:
                print("[-]Sent to the proxy server : " + str(e))
                return "[-]Sent to the proxy server : " + str(e)

            while True:
                try:
                    # 从代理服务器接收数据，然后转发回客户端
                    data_1 = mbsocket.recv(1024)
                    if not data_1:
                        break
                    print('[*' + localtime + ']: Send data...')
                    client.send(data_1)
                except socket.timeout as e:
                    print(self.proxyip)
                    print("[-]Back to the client : " + str(e))
                    continue
            # 关闭连接
        client.close()
        mbsocket.close()


def main():
    global try_ip
    file = open("proxies.txt", "r") # 筛选过后的代理ip文件名为proxies.txt
    for i in file:
        ip = i.split(':')
        ip_list = (ip[0], int(ip[1]))
        # print(ip_list)

        try:
            try_ip = ProxyServerTest(ip_list)
        except Exception as e:
            print("[-]main : " + str(e))
            return "[-]main : " + str(e)

    t = threading.Thread(target=try_ip.run, name='LoveJaky')
    print('[*]Waiting for connection...')
    # 关闭多线程
    t.start()
    t.join()


if __name__ == '__main__':
    main()
