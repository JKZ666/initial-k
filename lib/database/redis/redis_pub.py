# coding=utf-8
# Author=JKZ

import logging
import redis

log_file = "pub.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format="[%(asctime)s]: %(message)s")
logger = logging.getLogger('pub')
logger.setLevel(level=logging.INFO)

rc = redis.StrictRedis(host="192.168.2.23", port="6379", db=0)
i = 0
while True:
    # input = raw_input("publish:")
    # if input == 'over':
    #     print '停止发布'
    #     rc.publish('spub', 'over')
    #     break
    # rc.publish('spub', input)
    rc.publish('spub', str(i).zfill(32))
    logging.info(str(i))
    i += 1

