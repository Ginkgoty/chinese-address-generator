# chinese-address-generator(中国地址随机生成器)
## 使用方法
### 通过pip安装
    pip install chinese-address-generator
### daoru生成器
    from chinese_address_generator import generator
### 生成一级地址——省
    generator.generatelevel1()
### 生成二级地址——省、市
    generator.generatelevel2()
### 生成三级地址——省、市、县
    generator.generatelevel3()
### 生成四级地址——省、市、县、街道
    generator.generatelevel4()
## 补充说明
### 查看原始数据
    import chinese_address_generator
    chinese_address_generator.level3_list #三级地址列表
    chinese_address_generator.level4_list #四级地址列表
