# Chinese Address Generator
## Dataset
Data source: `National Bureau of Statistics` — "***2023 National Statistical Regional Division Code and Urban-Rural Division Code***" authoritative data.  
Link: ***https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/index.html***

## How to Use
### Installation via pip
```bash
pip install chinese-address-generator
```

### Usage in Command Line
```bash
$ cnaddrgen -h
usage: cnaddrgen [-h] --level {1,2,3,4} --num NUM [--version]

Chinese address generator

options:
  -h, --help            show this help message and exit
  --level {1,2,3,4}, -l {1,2,3,4}
                        Level of address
  --num NUM, -n NUM     Number of addresses to generate.
  --version, -v         Version of chinese-address-generator
```
#### Example
```bash
$ cnaddrgen -l 4 -n 4            
西藏自治区拉萨市西藏文化旅游创意园区西藏文化旅游创意园区 540173
安徽省合肥市合肥新站高新技术产业开发区三十头街道 340178
重庆市璧山区河边镇 500120
广西壮族自治区南宁市江南区那洪街道 450105
```

### Usage in Project
#### Import generator
```python
from chinese_address_generator import generator
```
#### Generate Level-1 address[省、自治区、直辖市]
```python
generator.generatelevel1()

$ 天津市 120000
```
#### Generate Level-2 address[省、自治区、直辖市]-[市、地区]
```python
generator.generatelevel2()

$ 江苏省南京市 320100
```
#### Generate Level-3 address[省、自治区、直辖市]-[市、地区]-[区、县]
```python
generator.generatelevel3()

$ 陕西省西安市阎良区 610114
```
#### Generate Level-4 address[省、自治区、直辖市]-[市、地区]-[区、县]-[乡、镇、街道]
```python
generator.generatelevel4()

$ 江西省南昌市红谷滩区龙兴街道 360113
```
## Additional Information
### Viewing Raw Data
```bash
import chinese_address_generator
chinese_address_generator.level3_list
chinese_address_generator.level4_list
```