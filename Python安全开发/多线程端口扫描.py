#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 HackerTerry, Inc. All Rights Reserved 
#
# @Time    : 2022/2/16 11:23
# @Author  : Terry Zhang
# @Email   : goudan1974@163.com
# @Blog    : https://www.terry906.top
# @File    : 多线程端口扫描.py
# @Software: PyCharm

import socket
import optparse
import threading
import time
import queue

portList = queue.Queue()

def test_connection(ip,ports):
    global s
    ip = socket.gethostbyname(ip)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 建立ipv4的TCP连接
        # s.settimeout(2)
        if (s.connect_ex((ip,ports))) == 0:
            print("[+]端口" + str(ports) + "开放")
            return True
        else:
            print("[-]端口" + str(ports) + "关闭")
            return False
    except Exception as e:
        print("[-]连接出错...")
        return False
    except KeyboardInterrupt:
        print("[-]用户操作退出...")
        exit()
        return False
    finally:
        s.close()

def port_scan(ip,ports):
    try:
        if "-" in ports:
            ports = ports.split("-")
            start_port = ports[0]
            end_port = ports[1]
            for port in range(int(start_port),int(end_port)+1):
                portList.put(port)
                t = threading.Thread(target=test_connection, args=(ip, portList.get()))
                t.start()
                t.join()
        elif "," in ports:
            ports = ports.split(",")
            for port in ports:
                portList.put(port)
                t = threading.Thread(target=test_connection, args=(ip, portList.get(port)))
                t.start()
                t.join()
        else:
            test_connection(ip,int(ports))
        return ports
    except KeyboardInterrupt:
        print("[-]用户操作退出...")
        exit()

if __name__ == '__main__':
    usage = "python3 %prog -i 域名或ip -p 端口"
    parse = optparse.OptionParser(usage=usage)
    parse.add_option("-i", "--ip", type="string", dest="ip", help="域名或ip")
    parse.add_option("-p", "--ports", type="string", dest="ports", help="端口（可指定多个和范围）")
    # parse.add_option("-t", "--threads", type="int", dest="threads", default="10", help="线程数")
    option, args = parse.parse_args()

    print('''
     ____            _   ____
    |  _ \ ___  _ __| |_/ ___|  ___ __ _ _ __  _ __   ___ _ __
    | |_) / _ \| '__| __\___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
    |  __/ (_) | |  | |_ ___) | (_| (_| | | | | | | |  __/ |
    |_|   \___/|_|   \__|____/ \___\__,_|_| |_|_| |_|\___|_|   v1.0
    
    版权所有 (C) 2022 HackerTerry,保留所有权利
    ''')
    print("[*]开始端口扫描...")
    start_time = time.time()

    port_scan(option.ip,option.ports)
    end_time = time.time()
    print("[*]总共用时："+str(end_time-start_time)+"秒")
