# coding=utf-8
# Author=JKZ

import logging
import redis

log_file = "sub.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format="[%(asctime)s]: %(message)s")
logger = logging.getLogger('sub')
logger.setLevel(level=logging.INFO)

rc = redis.StrictRedis(host="192.168.2.23", port="6379", db=0)
p = rc.pubsub()
p.subscribe('spub')
for item in p.listen():
    # print item
    if item['type'] == 'message':
        data = item['data']
        # rc.set('s', 32)
        logging.info(str(data))
        # print data
        if item['data'] == 'over':
            break
p.unsubscribe('spub')
print '取消订阅'

