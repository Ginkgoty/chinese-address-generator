"""
@Author  :   uint8_t
@Time    :   2022/08/12
@Version :   0.1.0
"""

import json
import platform
import os
from pathlib2 import Path
path1 = Path(__file__).parent.joinpath("src").joinpath("level3.json")
path2 = Path(__file__).parent.joinpath("src").joinpath("level4.txt")
# if platform.system() == 'Windows':
#     path1 = str(os.path.dirname(os.__file__) + '\\site-packages\\chinese_address_generator\\src\\level3.json')
#     path2 = os.path.dirname(os.__file__) + '\\site-packages\\chinese_address_generator\\src\\level4.txt'
# else:
#     path1 = os.path.dirname(os.__file__) + '/site-packages/chinese_address_generator/src/level3.json'
#     path2 = os.path.dirname(os.__file__) + '/site-packages/chinese_address_generator/src/level4.txt'

level3_list = json.loads(open(path1, 'r', encoding='utf-8').read())
level4_list = open(path2, 'r', encoding='utf-8').readlines()
