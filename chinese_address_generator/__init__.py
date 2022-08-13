"""
@Author  :   uint8_t
@Time    :   2022/08/12
@Version :   0.1.0
"""
import json

class Reader:
    level3_list = json.load(open('src/level3.json', 'r', encoding='utf-8'))

    level4_list = open('src/level4.txt', 'r', encoding='utf-8').readlines()
