# -*- coding: utf-8 -*-

import yaml
import re
import os


def parse_kafka_principal(useQuotaBaseDir):

    key = 'kafkaPrincipal'

    # check if directory is not empty
    if os.listdir(useQuotaBaseDir):
        yaml_file = [f for f in os.listdir(
            useQuotaBaseDir) if f.endswith(('yml', 'yaml'))]

        for f in yaml_file:
            with open(useQuotaBaseDir + f, 'r') as f:
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

    for item in kafka_principal_items:

        match = re.search(r', ', item)

        if match:
            print(
                '[WARNING] There are spaces after comma in kafkaPrincipal parameter, please update it')
            clean_spaces = item.replace(", ", ",")
            print('[INFO] it should be like this => ' + clean_spaces)
            print('')

    # execute command
    #cmd = 'kafka-configs.sh --zookeeper localhost:2181 --alter --add-config producer_byte_rate = $VALUE1, consumer_byte_rate = $vALUE2  --entity-type users --entity-name \'userPrincipal\''


if __name__ == '__main__':

    #print(list(findkeys(d, 'id')))

    #useQuotaBaseDir = '/home/fabricio/Documents/kafka-parser/'
    useQuotaBaseDir = 'C:/Users/patf001/Documents/my_stuff/kafka-parser/'

    parse_kafka_principal(useQuotaBaseDir)
