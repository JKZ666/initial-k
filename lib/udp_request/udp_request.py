# coding=utf-8
# Author=JKZ
"""
UDP request functions
最底层的UDP包发送库

"""
import socket
import binascii


def send_udp_request(req_from, api_host, api_port, req_data, listening_port, socket_timeout=5):
    try:
        print "-------------------------%sRequest-----------------------------" % req_from
        print "listening port: " + str(listening_port)
        print "sent data: " + str(req_data)
        print "------------------------------------------------------------------------"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", listening_port))
        s.settimeout(socket_timeout)
        s.sendto(binascii.a2b_hex(req_data), (api_host, int(api_port)))
        data, addr = s.recvfrom(1024)
        # print binascii.b2a_hex(data)
        s.close()
        print "+++++++++++++++++++++++++++%sResponse++++++++++++++++++++++++++" % req_from
        print "received data: " + str(binascii.b2a_hex(data))
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        return binascii.b2a_hex(data)

    except Exception, e:
        print "error:", e
        if isinstance(e, socket.timeout):
            return None
        else:
            return False


def send_udp_request_keep_listening(req_from, api_host, api_port, req_data, listening_port, socket_timeout=5):
    """
    发送response后接受其后收到的二十个包并返回list    by gzh
    :param req_from:
    :param api_host:
    :param api_port:
    :param req_data:
    :param listening_port:
    :param socket_timeout:
    :return:
    """
    try:
        print "-------------------------%sRequest-----------------------------" % req_from
        print "listening port: " + str(listening_port)
        print "sent data: " + str(req_data)
        print "------------------------------------------------------------------------"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", int(listening_port)))
        s.settimeout(socket_timeout)
        s.sendto(binascii.a2b_hex(req_data), (api_host, int(api_port)))
        response_list = list()
        for i in range(20):
            data, addr = s.recvfrom(1024)
            response_list.append(binascii.b2a_hex(data))
            print "+++++++++++++++++++++++++++%sResponse++++++++++++++++++++++++++" % req_from
            print "response list " + str(i + 1) + ' : ' + response_list[i]
            print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        # print binascii.b2a_hex(data)
        s.close()
        return response_list

    except Exception, e:
        print "error:", e
        if isinstance(e, socket.timeout):
            return response_list
        else:
            return False


def send_udp_request_special(req_from, api_host, api_port, req_data, listening_port, socket_timeout=5):
    """
    特殊的发包方法，用于快速发包，并方便存入列表
    :param req_from:
    :param api_host:
    :param api_port:
    :param req_data:
    :param listening_port:
    :param socket_timeout:
    :return:
    """
    try:
        print "-------------------------%sRequest-----------------------------" % req_from
        print "listening port: " + str(listening_port)
        print "sent data: " + str(req_data)
        print "------------------------------------------------------------------------"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", listening_port))
        s.settimeout(socket_timeout)
        s.sendto(binascii.a2b_hex(req_data), (api_host, int(api_port)))
        data, addr = s.recvfrom(1024)
        # print binascii.b2a_hex(data)
        s.close()
        print "+++++++++++++++++++++++++++%sResponse++++++++++++++++++++++++++" % req_from
        print "received data: " + str(binascii.b2a_hex(data))
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        return binascii.b2a_hex(data)

    except Exception, e:
        print "error:", e
        if isinstance(e, socket.timeout):
            return ''
        else:
            return False


def verify_push_data(listening_port=60680, socket_timeout=5):
    """
    校验指定端口在timeout内是否收到数据
    :param listening_port:
    :param socket_timeout:
    :return:
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", listening_port))
        s.settimeout(socket_timeout)
        s.recvfrom(1024)
        s.close()
        return True
    except Exception, e:
        print "error:", e
        if isinstance(e, socket.timeout):
            return False
        else:
            return False

