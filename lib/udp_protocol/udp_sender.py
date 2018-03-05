# coding=utf-8
# Author=JKZ

"""
    发送udp数据包，重发机制?
"""

from socket import *

import time

HOST = 'localhost'
PORT = 21567
BUFSIZE = 1024

ADDR = (HOST, PORT)

udpCliSock = socket(AF_INET, SOCK_DGRAM)
num = 1
while True:
    # data = raw_input('>')

    data = str(num).zfill(4)
    if not data:
        break
    udpCliSock.sendto(data, ADDR)
    # data, ADDR = udpCliSock.recvfrom(BUFSIZE)
    if not data:
        break
    print data
    num += 1
    time.sleep(3)

udpCliSock.close()
