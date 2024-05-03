#!/usr/bin/python3
"""
@Author  :   Ginkgoty
@Time    :   2024/05/03
@Version :   0.2.0
"""
import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import pathlib2

"""
行政区划代码来自于“国家统计局——2023年度全国统计用区划代码和城乡划分代码”
"""
BASE_URL = 'https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/'
level3_json = []
level4_csv = []

# HTTP Get
response = requests.get(BASE_URL+'index.html')
response.encoding = 'utf-8'

if response.status_code == 200:
    # Parse HTML by bs4
    soup = BeautifulSoup(response.text, 'html.parser')
    # Get `province` table
    table = soup.find('table', class_='provincetable')

    # Find all provinces
    provinces = table.find_all('a', href=True)
    province_dict = []
    city_dict = []
    county_dict = []
    town_dict = []
    level1_tmp = []
    level2_tmp = []
    level3_tmp = []
    for p in provinces:
        province_dict.append(
            [p['href'], p['href'].rstrip('.html'), p.contents[0]])

    # Process each province
    for pvc in province_dict:
        print(f"province {pvc[2]}")
        response = requests.get(BASE_URL+pvc[0])
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get `city` table
        if response.status_code == 200:
            table = soup.find('table', class_='citytable')

            # Find all cities
            cities = table.find_all('a', href=True)
            for i in range(0, len(cities), 2):
                if pvc[2] in ['北京市', '天津市', '上海市', '重庆市']:
                    city_dict.append(
                        [cities[i]['href'], cities[i].contents[0], ''])
                    break
                city_dict.append(
                    [cities[i]['href'], cities[i].contents[0], cities[i+1].contents[0]])

            # Process each cities
            for cty in city_dict:
                print(f"city {cty[2]}")
                response = requests.get(BASE_URL+cty[0])
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'html.parser')

                # Get county table
                if response.status_code == 200:
                    if cty[2] in ['东莞市', '中山市', '儋州市']:
                        table = soup.find('table', class_='countytable')
                        # Find all towns
                        towns = table.find_all('a', href=True)
                        for i in range(0, len(towns), 2):
                            level4_csv.append(
                                [towns[i].contents[0], towns[i+1].contents[0]])
                        continue

                    table = soup.find('table', class_='countytable')

                    # Find all counties
                    counties = table.find_all('a', href=True)
                    for i in range(0, len(counties), 2):
                        county_dict.append(
                            [counties[i]['href'], counties[i].contents[0], counties[i+1].contents[0]])

                    # Process each county
                    for cuy in county_dict:
                        print(f"county {cuy[2]}")
                        level3_tmp.append(
                            dict(code=cuy[1][:6], region=cuy[2]))
                        response = requests.get(
                            BASE_URL+f'{cty[0][:2]}/'+cuy[0])
                        response.encoding = 'utf-8'
                        soup = BeautifulSoup(response.text, 'html.parser')

                        # Get towntable
                        if response.status_code == 200:
                            table = soup.find('table', class_='towntable')

                            # Find all counties
                            towns = table.find_all('a', href=True)
                            for i in range(0, len(towns), 2):
                                # town_dict.append(
                                #     [towns[i]['href'], towns[i].contents[0], towns[i+1].contents[0]])
                                level4_csv.append(
                                    [towns[i].contents[0], towns[i+1].contents[0]])
                        else:
                            print(f"Failed to retrieve the province {pvc[2]} city {
                                cty[2]} county {cuy[2]} webpage. Status code: {response.status_code}")

                    level2_tmp.append(
                        dict(code=cty[1][:6], region=cty[2], regionEntitys=level3_tmp[:]))
                    county_dict.clear()
                    level3_tmp.clear()

                else:
                    print(f"Failed to retrieve the province {pvc[2]} city {
                        cty[2]} webpage. Status code: {response.status_code}")
                # time.sleep(2)

                level3_json.append(dict(code=pvc[1].ljust(
                    6, '0'), region=pvc[2], regionEntitys=level2_tmp[:]))
                city_dict.clear()
                level2_tmp.clear()

        else:
            print(f"Failed to retrieve the provice {
                  pvc[2]} webpage. Status code: {response.status_code}")

    data_path = pathlib2.Path(__file__).parent.joinpath("src")

    with open(data_path.joinpath('new_level3.json'), 'w', encoding='utf-8') as f:
        json.dump(level3_json, f, ensure_ascii=False, indent=4)

    with open(data_path.joinpath('new_level4.txt'), 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(level4_csv)

else:
    print(f"Failed to retrieve the index webpage. Status code: {
          response.status_code}")
