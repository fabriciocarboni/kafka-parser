# -*- coding: utf-8 -*-

import yaml
import os


def parse_kafka_principal(useQuotaBaseDir):

    # check if directory is not empty
    if os.listdir(useQuotaBaseDir):
        yaml_file = [f for f in os.listdir(useQuotaBaseDir) if f.endswith(('yml', 'yaml'))]
        for f in yaml_file:
            with open(useQuotaBaseDir + f, 'r') as f:
                try:
                    yml = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    print(e)

    #looping through dict to find the list containing kafkaprincipal
    for key, value in yml.items():
        if isinstance(value, dict):
            for k, v in value.items():
                if isinstance(v, dict):
                    for x, y in v.items():
                        if isinstance(y, list):
                            kafka_princ = y
        
    for item in kafka_princ:
        for key, value in item.items():
            #print(key, "->", value)
            if(key == 'kafkaPrincipal'):
                #regexp to find spaces after comma
                exp = ''
                #value_cleaned = value.replace(", ",",")
                msg = '[WARNING] There are errors in kafkaPrincipal, please update it'
                print(msg)
                print(value_cleaned)

            




if __name__ == '__main__':

    
    #useQuotaBaseDir = '/home/fabricio/Documents/kafka-parser/'
    useQuotaBaseDir = 'C:/Users/patf001/Documents/my_stuff/kafka-parser/'

    parse_kafka_principal(useQuotaBaseDir)