# coding=utf-8
# Author=JKZ
# 从kafka实时消费指定topic的数据
import inspect
import io
import json
import logging
import os
import avro
import requests
import avro.io
import avro.schema
import sys
from pykafka import KafkaClient
from pykafka.simpleconsumer import OffsetType
import time

SCHEMA_HOST = "kafka-bridge-1"
SCHEMA_PORT = 8081
# KAFKA_HOSTS = 'node1.kafka-ext.ys-internal.com:2181,' \
#               'node2.kafka-ext.ys-internal.com:2181,node3.kafka-ext.ys-internal.com:2181'
KAFKA_HOSTS = "kafka-node-1:9092,kafka-node-2:9092,kafka-node-3:9092"

# get current dir path
file_path = os.path.abspath(inspect.getfile(sys.modules[__name__]))
parent_path = os.path.dirname(file_path)

# 配置log文件
log_file = "{0}/stdout.log".format(parent_path)
logging.basicConfig(filename=log_file, level=logging.ERROR, format="[%(asctime)s]: %(message)s")
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logger = logging.getLogger('kafka_consumer')
logger.setLevel(level=logging.INFO)
logger.addHandler(console)


def get_latest_schema_info(topics, schema_host=SCHEMA_HOST, schema_port=SCHEMA_PORT):
    """
    获取topic最新schema
    :param topics: 一个或多个topic的name列表
    :param schema_host:
    :param schema_port:
    :return: {topic_name: (schema, id),...}
    """
    # get latest schema format and schema_id of topic
    schemas = {}
    if type(topics) != list:
        topics = [topics]
    for topic in topics:
        r = requests.get(
            "http://{0}:{1}/subjects/{2}-value/versions/latest".format(
                schema_host, schema_port, topic))
        if r.status_code == 200:
            rsp = r.json()
            schemas[topic] = rsp["schema"], rsp["id"]
            # return rsp["schema"], rsp["id"]
        else:
            raise ValueError(r.text)

    return schemas


def new_consumer(topics, consumer_group, kafka_hosts):
    """
    从kafka消费数据
    :param topics:
    :param consumer_group:
    :param kafka_hosts:
    :return:
    """
    # get data from kafka
    consumers = {}
    client = KafkaClient(hosts=kafka_hosts)
    if type(topics) != list:
        topics = [topics]
    for topic in topics:
        kafka_topic = client.topics[topic]
        consumer = kafka_topic.get_simple_consumer(
            consumer_group=consumer_group,
            consumer_timeout_ms=500,
            auto_commit_enable=True,
            auto_commit_interval_ms=1,
            auto_offset_reset=OffsetType.LATEST,
            reset_offset_on_start=True,
            consumer_id=consumer_group)
        consumers[topic] = consumer
        consumer.commit_offsets()
    return consumers


def search_schema(topics):
    schemas = {}
    for topic in topics:
        topic_schema, topic_schema_id = get_latest_schema_info(topic)
        schemas[topic] = [topic_schema, topic_schema_id]
    return schemas


def read_logs_from_kafka(consumers, schemas):
    """
    解析log
    :param consumers:
    :param schemas:
    :return:
    """
    topics_logs = {}
    for topic, consumer in consumers.items():
        collect_logs = []
        for message in consumer:
            if message is not None:
                msg_partition = message.partition.id
                msg_offset = message.offset
                bytes_msg = io.BytesIO(message.value[5:])
                decode_msg = avro.io.BinaryDecoder(bytes_msg)
                recode_msg = avro.io.DatumReader(
                    avro.schema.parse(schemas[topic][0])).read(decode_msg)
                # get partition，offset，value
                msg_collect = [msg_partition, msg_offset, recode_msg]
                collect_logs.append(msg_collect)
        # 将logs按timestamp排序
        collect_logs.sort(key=lambda x: x[2]["timestamp"])
        if len(collect_logs) > 0:
            logger.info("Topic: {0}, consumed kafka logs count: {1}".format(topic, len(collect_logs)))
        for index, log in enumerate(collect_logs):
            # print index, log
            log[2]["topic"] = topic
            logger.info(json.dumps(log[2]))
        topics_logs[topic] = collect_logs
    return topics_logs


# ---------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    topic_list = ["topic_name_1", "topic_name2"]
    topics_schemas = get_latest_schema_info(topic_list)
    while True:
        consumers = new_consumer(topic_list, consumer_group="online_teste", kafka_hosts=KAFKA_HOSTS)
        read_logs_from_kafka(consumers, topics_schemas)

