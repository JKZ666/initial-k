# coding=utf-8
# Author=JKZ

"""
接收udp数据包，处理丢包、乱序等情况，缓存数据，供http调用
"""

from socket import *
import time
import threading

HOST = '127.0.0.1'
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST, PORT)

# data_pool = []

# Timer（定时器）是Thread的派生类，
# 用于在指定时间后调用一个方法。
# def func():
#   print 'hello timer!'
# timer = threading.Timer(5, func)
# timer.start()


def calculate_ack_seq(data_pool):
    """
    将所有数据包按seq去重排序，计算返回的ack_seq（第一个不连续的seq）
    seq为数据包前4位（4bit？？？body格式需定义）
    :param data_pool:
    :return:
    """
    # 取出所有包的seq num，并去重，按从小到大排序
    seq_list = sorted(list(set([int(str(x)[:4]) for x in data_pool])))
    # ack_seq num先默认为第一个seq
    ack_seq = seq_list[0]

    for i in range(len(seq_list)-1):
        # 判断下一个seq是否等于此seq的num加1，如果不是，则跳出for循环，ack_seq等于此seq的num加1
        if seq_list[i+1] != seq_list[i] + 1:
            print seq_list[i+1], seq_list[i]
            ack_seq = seq_list[i]+1
            break
        else:
            ack_seq = seq_list[i+1]+1

    return ack_seq


def udp_srv_main():
    """
    main
    :return:
    """

    udpSerSock = socket(AF_INET, SOCK_DGRAM,)
    udpSerSock.bind(ADDR)
    data_pool = []
    init_time = time.time()
    while True:
        # print 'wating for message...'
        data, addr = udpSerSock.recvfrom(BUFSIZE,)
        data_seq = data[0]
        data_pool.append(data)
        # udpSerSock.sendto('[%s] %s' % (time.ctime(), data), addr)
        print time.ctime(), ":", data
        # print '...received from and retuned to:', addr
        time.sleep(2)
        curent_time = time.time()
        print curent_time
        print init_time
        while len(data_pool) == 9 or (time.time()-init_time) > 3:  # 数据包达到一定数量或时间？
            # 去重
            data_pool_set = list(set(data_pool))
            # 排序
            data_pool_sorted = sorted(data_pool_set, key=lambda d: int(d[:4]))
            print "list set:", data_pool_set
            print "list sort:", data_pool_sorted
            udpSerSock.sendto('[%s] %s' % (time.ctime(), data), addr)
            data_pool = []
            init_time = curent_time
    udpSerSock.close()

if __name__ == "__main__":
    test = [0002, 0003, 0004, 0005]
    # calculate_ack_seq(data_pool=test)
    print time.time()
    udp_srv_main()

