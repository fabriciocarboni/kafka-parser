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
            file
            for file in os.listdir(useQuotaBaseDir)
            if file.endswith(("yml", "yaml"))
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

    # find defined above key in ymal file
    kafka_principal_items = list(findkeys(yml, key))

    # Checking kafkaPrincipal values
    for item in kafka_principal_items:

        # looking for spaces after any comma
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
    for (producer_byte_rate, consumer_byte_rate) in zip(
        producer_byte_rate_items, consumer_byte_rate_items
    ):

        if int(producer_byte_rate) >= int(max_producer_byte_rate):
            set_producer_byte_rate = max_producer_byte_rate
            print("producer:" + str(set_producer_byte_rate))
        else:
            set_producer_byte_rate = producer_byte_rate
            print("producer:" + str(set_producer_byte_rate))
        
        if int(consumer_byte_rate) >= int(max_consumer_byte_rate):
            set_consumer_byte_rate = max_consumer_byte_rate
            print("consumer:" + str(set_consumer_byte_rate))
        else:
            set_consumer_byte_rate = consumer_byte_rate
            print("consumer:" + str(set_consumer_byte_rate))

        cmd = (
            "kafka-configs.sh  --zookeeper localhost:2181 --alter --add-config 'producer_byte_rate="
            + str(set_producer_byte_rate)
            + ",consumer_byte_rate="
            + str(set_consumer_byte_rate)
            + "' --entity-type users --entity-name '$userPrinciple'"
        )
        print(cmd)

        # execute command
        # os.system(cmd)


if __name__ == "__main__":

    useQuotaBaseDir = "/home/fabricio/Documents/kafka-parser/"
    # useQuotaBaseDir = 'C:/Users/patf001/Documents/my_stuff/kafka-parser/'

    parse_kafka_principal(useQuotaBaseDir)

