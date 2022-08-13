#!/usr/bin/python3
"""
@Author  :   uint8_t
@Time    :   2022/08/12
@Version :   0.1.0
"""
import json
import random
import os
import platform


# class Generator:

# def __init__(self):
#     self.__address_list = self.__jsonreader()
#
#     self.__level4_list = self.__txtreader()
#
#     self.__level4_temp = []

# read json file to get level3 address
def jsonreader():
    if platform.system() == 'Windows':
        path = os.path.dirname(os.__file__) + '\\site-packages\\chinese_address_generator\\src\\level3.json'
    else:
        path = os.path.dirname(os.__file__) + '/site-packages/chinese_address_generator/src/level3.json'
    return json.loads(open(path, 'r', encoding='utf-8').read())


# read txt file to get level4 address
def txtreader():
    if platform.system() == 'Windows':
        path = os.path.dirname(os.__file__) + '\\site-packages\\chinese_address_generator\\src\\level4.txt'
    else:
        path = os.path.dirname(os.__file__) + '/site-packages/chinese_address_generator/src/level4.txt'
    return open(path, 'r', encoding='utf-8').readlines()


__address_list = jsonreader()

__level4_list = txtreader()

__level4_temp = []


# generate level1 address, province
def generatelevel1():
    try:
        province = random.choice(__address_list[:-3])
        return province['region'] + " " + province['code']
    except:
        pass


# generate level2 address, province + city
def generatelevel2():
    try:
        province = random.choice(__address_list[:-3])
        city = random.choice(province['regionEntitys'])
        return province['region'] + city['region'] + " " + city['code']
    except:
        pass


# generate level3 address, province + city + county
def generatelevel3():
    try:
        province = random.choice(__address_list[:-3])
        city = random.choice(province['regionEntitys'])
        county = random.choice(city['regionEntitys'][1:])
        return province['region'] + city['region'] + county['region'] + " " + county['code']
    except:
        pass


# generate level4 address, province + city + county + town
def generatelevel4():
    try:
        province = random.choice(__address_list[:-3])
        city = random.choice(province['regionEntitys'])
        county = random.choice(city['regionEntitys'][1:])
        for item in __level4_list:
            if item[0:6] == county['code']:
                __level4_temp.append(item[13:])
        town = random.choice(__level4_temp)
        return province['region'] + city['region'] + county['region'] + town + " " + county['code']
    except:
        pass
