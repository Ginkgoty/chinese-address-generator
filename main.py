#!/usr/bin/python3
"""
@Author  :   uint8_t
@Time    :   2022/08/12
@Version :   0.1.0
"""
import json
import random


class Generator:
    __address_list = []

    __level4_list = []

    __level4_temp = []

    def __init__(self):
        self.__address_list = self.__jsonreader()

        self.__level4_list = self.__txtreader()

        self.__level4_temp = []

    # read json file to get level3 address
    def __jsonreader(self):
        return json.load(open('src/level3.json', 'r', encoding='utf-8'))

    # read txt file to get level4 address
    def __txtreader(self):
        return open('src/level4.txt', 'r', encoding='utf-8').readlines()

    # generate level1 address, province
    def generatelevel1(self):
        try:
            province = random.choice(self.__address_list[:-3])
            return province['region'] + " " + province['code']
        except:
            pass

    # generate level2 address, province + city
    def generatelevel2(self):
        try:
            province = random.choice(self.__address_list[:-3])
            city = random.choice(province['regionEntitys'])
            return province['region'] + city['region'] + " " + city['code']
        except:
            pass

    # generate level3 address, province + city + county
    def generatelevel3(self):
        try:
            province = random.choice(self.__address_list[:-3])
            city = random.choice(province['regionEntitys'])
            county = random.choice(city['regionEntitys'][1:])
            return province['region'] + city['region'] + county['region'] + " " + county['code']
        except:
            pass

    # generate level4 address, province + city + county + town
    def generatelevel4(self):
        try:
            province = random.choice(self.__address_list[:-3])
            city = random.choice(province['regionEntitys'])
            county = random.choice(city['regionEntitys'][1:])
            for item in self.__level4_list:
                if item[0:6] == county['code']:
                    self.__level4_temp.append(item[13:])
            town = random.choice(self.__level4_temp)
            return province['region'] + city['region'] + county['region'] + town + " " + county['code']
        except:
            pass


if __name__ == '__main__':
    generator = Generator()
    generator.generatelevel1()
    generator.generatelevel2()
    generator.generatelevel3()
    generator.generatelevel4()
