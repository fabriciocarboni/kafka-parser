# -*- coding: utf-8 -*-

import yaml
import re
import os


def parse_kafka_principal(useQuotaBaseDir):

    key = "kafkaPrincipal"
    key_producer_byte_rate = "producer_byte_rate"
    key_consumer_byte_rate = "consumer_byte_rate"
    max_producer_byte_rate = 262144
    max_consumer_byte_rate = 262144

    if os.listdir(useQuotaBaseDir):
        yaml_file = [
            f for f in os.listdir(useQuotaBaseDir) if f.endswith(("yml", "yaml"))
        ]

        for f in yaml_file:
            with open(useQuotaBaseDir + f, "r") as f:
                try:
                    yml = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    print(e)

        def findkeys(node, kv):
            if isinstance(node, list):
                for i in node:
                    for x in findkeys(i, kv):
                        yield x
            elif isinstance(node, dict):
                if kv in node:
                    yield node[kv]
                for j in node.values():
                    for x in findkeys(j, kv):
                        yield x

    kafka_principal_items = list(findkeys(yml, key))

    # Checking kafkaPrincipal values
    for item in kafka_principal_items:

        match = re.search(r", ", item)

        if match:
            print(
                "[WARNING] There are spaces after comma in "
                + key
                + " parameter, please update it"
            )
            clean_spaces = item.replace(", ", ",")
            print("[WARNING] it should be like this => " + clean_spaces)
            print("")

    # Checking producer_byte_rate and consumer_byte_rate
    producer_byte_rate_items = list(findkeys(yml, key_producer_byte_rate))
    consumer_byte_rate_items = list(findkeys(yml, key_consumer_byte_rate))

    # Looping through 2 lists at the same time and compare byte rate
    for (x, y) in zip(producer_byte_rate_items, consumer_byte_rate_items):
        # print("producer: ", x ,"; consumer: ", y)
        if (int(x) >= max_producer_byte_rate) or (int(y) >= max_consumer_byte_rate):
            cmd = (
                "kafka-configs.sh  --zookeeper localhost:2181 --alter --add-config 'producer_byte_rate="
                + str(max_producer_byte_rate)
                + ",consumer_byte_rate="
                + str(max_consumer_byte_rate)
                + "' --entity-type users --entity-name '$userPrinciple'"
            )
            print(cmd)
            # print("producer: ", str(max_producer_byte_rate), "; consumer: ", str(max_consumer_byte_rate))

            # execute command
            # os.system(cmd)


if __name__ == "__main__":

    # print(list(findkeys(d, 'id')))

    useQuotaBaseDir = "/home/fabricio/Documents/kafka-parser/"
    # useQuotaBaseDir = 'C:/Users/patf001/Documents/my_stuff/kafka-parser/'

    parse_kafka_principal(useQuotaBaseDir)

