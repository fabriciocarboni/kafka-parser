
# This script aims to read an yaml file wit some configs inside.
# 1- Should find for the word 'kafkaPrincipal' as key and find ", "
#     spaces right after any comma.
# 2- If match, print warning message and the fixed value
# 3- The script should find for 'quota' definition and do validations over
#     the consumer_byte_rate and producer_byte_rate. We need to check if
#     the value provided is correct. (waiting definition from Rajeev)
# 4- After all validation, the script must run a command


# -*- coding: utf-8 -*-

import yaml
import os
import re


def parse_kafka_principal(useQuotaBaseDir):

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

    # looping through dict to find the list containing kafkaprincipal
    for key, value in yml.items():
        if isinstance(value, dict):
            for k, v in value.items():
                if isinstance(v, dict):
                    for x, y in v.items():
                        if isinstance(y, list):
                            kafka_princ = y

    for item in kafka_princ:
        for key, value in item.items():

            if(key == 'kafkaPrincipal'):

                match = re.search(r', ', value)

                if match:
                    print(
                        '[WARNING] There are spaces after comma in kafkaPrincipal parameter, please update it')
                    clean = value.replace(", ", ",")
                    print('[INFO] it should be like this => ' + clean)

    # execute command
    #cmd = 'kafka-configs.sh --zookeeper localhost:2181 --alter --add-config producer_byte_rate = $VALUE1, consumer_byte_rate = $vALUE2  --entity-type users --entity-name \'userPrincipal\''


if __name__ == '__main__':

    #useQuotaBaseDir = '/home/fabricio/Documents/kafka-parser/'
    useQuotaBaseDir = 'C:/Users/patf001/Documents/my_stuff/kafka-parser/'

    parse_kafka_principal(useQuotaBaseDir)
