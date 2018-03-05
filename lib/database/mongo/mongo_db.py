# coding=utf-8
# Author=JKZ
"""
操作MongoDB数据库的底层库

"""

import pymongo
import time

def get_info_by_para(mongodb_host, mongodb_port, table_name, collection_name, **args):
    """
    根据指定条件查询对应信息
    :param mongodb_host:
    :param mongodb_port:
    :param table_name:
    :param collection_name:
    :param args: 查询条件
    :return:
    """
    client = pymongo.MongoClient(mongodb_host, mongodb_port)
    db = client[table_name]
    print table_name, "collections:", db.collection_names()
    db_collection = db[collection_name]
    info_list = []  # for return
    i = 0
    print "search condition:", args
    if len(args) == 0:  # 未设定查询条件时获取所有记录
        info_items = db_collection.find()
        for piece_info in info_items:
            print i, piece_info
            info_list.append(piece_info)
            i += 1
    else:
        info_items = db_collection.find(args)
        for piece_info in info_items:
            print i, piece_info
            info_list.append(piece_info)
            i += 1
    return info_list


def del_info_by_para(mongodb_host, mongodb_port, table_name, collection_name, **args):
    """
    根据指定条件删除对应信息
    :param mongodb_host:
    :param mongodb_port:
    :param table_name:
    :param collection_name:
    :param args:
    :return:
    """
    client = pymongo.MongoClient(mongodb_host, mongodb_port)
    db = client[table_name]
    db_collection = db[collection_name]
    info_list = []  # for return
    if len(args) == 0:
        print "！！！ Please input the args will be removed"
    else:
        info_items = db_collection.remove(args)
        # for piece_info in info_items:
        #     print piece_info
        #     info_list.append(piece_info)
    return info_list


if __name__ == "__main__":
    get_info_by_para("192.168.1.194", 27017, "test", "server_node", name="dir", version="safdasfsadfsafassd")
    # get_info_by_para("192.168.1.194", 27017, "test", "server_node")
