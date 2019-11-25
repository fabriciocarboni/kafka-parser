# -*- coding: utf-8 -*-


import yaml


useQuotaBaseDir = '/home/fabricio/Documents/kafka-parser/file.yml'

with open(useQuotaBaseDir, 'r') as f:
    try:
        yml = yaml.safe_load(f)
        #print(type(yml))
        print(yml)
    except yaml.YAMLError as e:
        print(e)


#print("myTopic" in [x for v in yml.values() for x in v])


# for i in yml.values():
#     if isinstance(i,dict):
#         for k,v in i.items():
#             print(v)


# for key, value in yml.items():

#     ##print(type(value))
#     if isinstance(value, dict):
#         for k, v in value.items():
#             if isinstance(v, dict):
#                 print(v)
# 


# kafkaPrincipal = "'CN=Something', 'CN=Somethin g', 'CN=Something'"

# print(kafkaPrincipal)
# print("----")
# new_var = kafkaPrincipal.replace(", ", ",")
# print(new_var)


