# chinese-address-generator(中国地址随机生成器)
## 使用方法
### 通过pip安装
    pip install chinese-address-generator
### 导入生成器
    from chinese_address_generator import generator
### 生成一级地址——省
    generator.generatelevel1() #返回字符串
### 生成二级地址——省、市
    generator.generatelevel2() #返回字符串
### 生成三级地址——省、市、县
    generator.generatelevel3() #返回字符串
### 生成四级地址——省、市、县、街道
    generator.generatelevel4() #返回字符串
## 补充说明
### 查看原始数据
    import chinese_address_generator
    chinese_address_generator.level3_list #三级地址列表
    chinese_address_generator.level4_list #四级地址列表
## 故障分析
### Error 1
源代码采取
    os.path.dirname(os.__file__)
对数据文件，即src/*，进行定位，所以需要检查您存放pip包的实际site-packages目录是否与os.__file__中的那个site-packages目录相对应。
### Error 2
    generator.generatelevel4() #返回字符串
有时会返回None，该问题出自源数据，来自https://github.com/moonrailgun/chinese-address-generator


具体原因是部分地址在level4.txt中的数值代码与level3中的不对应，后续版本会加大测试力度尽可能减轻该问题.
