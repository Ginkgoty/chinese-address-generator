# 中国地址随机生成器

[English](docs/README.en.md)

[![CI](https://github.com/Ginkgoty/chinese-address-generator/actions/workflows/ci.yml/badge.svg)](https://github.com/Ginkgoty/chinese-address-generator/actions/workflows/ci.yml)
[![Release](https://github.com/Ginkgoty/chinese-address-generator/actions/workflows/release.yml/badge.svg)](https://github.com/Ginkgoty/chinese-address-generator/actions/workflows/release.yml)
[![PyPI](https://img.shields.io/pypi/v/chinese-address-generator.svg)](https://pypi.org/project/chinese-address-generator/)
[![Python](https://img.shields.io/pypi/pyversions/chinese-address-generator.svg)](https://pypi.org/project/chinese-address-generator/)
[![License](https://img.shields.io/pypi/l/chinese-address-generator.svg)](LICENSE)

基于权威内置数据随机生成中国行政区划地址。运行时完全离线、没有第三方依赖，支持
Python 3.8–3.14。

当前数据来自民政部国家地名信息库，截止日期为 **2025-12-31**；截至 2026-08-25，
这是官方发布的最新年度行政区划代码数据。

## 安装

```bash
pip install chinese-address-generator
```

## Python API

需要结构化结果时，推荐使用 `generate_address()`：

```python
from chinese_address_generator import generate_address

address = generate_address(level=4)

print(address)  # 安徽省宣城市绩溪县上庄镇 341824103
print(address.full_name)  # 安徽省宣城市绩溪县上庄镇
print(address.code)  # 341824103
print(address.province)  # 安徽省
print(address.prefecture)  # 宣城市
print(address.county)  # 绩溪县
print(address.township)  # 上庄镇
print(address.as_dict())  # 可直接进行 JSON 序列化的字典
```

各级含义严格对应官方发布的行政区划建制：

| 级别 | 行政区划 | 返回代码 | 内置记录数 |
| --- | --- | --- | ---: |
| L1 | 省级 | 6 位 | 33 |
| L2 | 地级 | 6 位 | 333 |
| L3 | 县级 | 6 位 | 2,845 |
| L4 | 乡级（镇、乡、街道等） | 9 位 | 38,723 |

某些权威层级会跳级。例如，直辖市的县级单位直接隶属于省级直辖市。因此 `Address` 会
保留真实层级路径，不会人为构造一个地级占位节点。

### 可复现的随机结果

```python
from chinese_address_generator import AddressGenerator

generator = AddressGenerator(seed=2026)
print(generator.generate(level=4))
```

### 兼容旧版字符串 API

0.x 的函数名在兼容期内仍然可用，并返回 `"完整地址 代码"` 字符串，但调用时会发出
`DeprecationWarning`。请主动迁移到对应的下划线命名 API：

```python
from chinese_address_generator import generator

generator.generatelevel1()  # 请改用 generate_level1()
generator.generatelevel2()  # 请改用 generate_level2()
generator.generatelevel3()  # 请改用 generate_level3()
generator.generatelevel4()  # 请改用 generate_level4()
```

`generate_level1()` 至 `generate_level4()` 是推荐使用且不会发出弃用警告的字符串 API。

### 读取数据和元数据

```python
from chinese_address_generator import get_data_metadata, load_divisions

townships = load_divisions(level=4)
metadata = get_data_metadata()
print(metadata["data_as_of"])  # 2025-12-31
```

## 命令行

```console
$ cnaddrgen --level 4 --num 2
安徽省宣城市绩溪县上庄镇 341824103
河北省石家庄市长安区建北街道 130102001

$ cnaddrgen --level 4 --seed 2026 --json
{"address": "...", "code": "...", "level": 4, ...}
```

也可以使用 `python -m chinese_address_generator`。

## 数据权威性与 L4 说明

数据来源为民政部国家地名信息库发布的
[行政区划代码](https://dmfw.mca.gov.cn/XzqhVersionPublish.html)。官方说明明确指出，该数据
包括全国省、地、县、乡四级行政区划建制，截至 2025-12-31；其中省、地、县级代码由
国务院民政部门确定，乡级代码由省、自治区、直辖市人民政府民政部门确定。

因此，L4 是从权威乡级记录中随机抽取，并不是随机拼接或编造名称。项目不包含村/社区级
城乡划分代码、邮政地址、门牌号或经纬度。

官方数据将台湾省代码标记为“资料暂缺”，因此项目在元数据中记录这一排除项，但不会生成
没有数字代码的结果。香港、澳门可参与 L1 生成；该数据集未提供其更低层级记录。

## 使用 uv 开发

```bash
uv sync
uv run pytest
uv run ruff check .
uv build
uv run twine check dist/*
```

Ruff 会强制执行 PEP 8 代码规则和 PEP 257 docstring 规则；测试的语句及分支覆盖率门槛为
100%。

从官方接口刷新数据：

```bash
uv run python tools/update_data.py
```

更新工具会校验记录总数、代码长度、唯一性及所有父子关系，然后以原子方式替换内置数据。
只有在官方页面公布新的年度快照后，才应调整工具中的表名和数据截止日期。

## 发布维护

正式版本通过 GitHub Actions 和 PyPI Trusted Publishing 自动发布，不在仓库中保存长期
PyPI Token。发布任务要求 `v` 开头的 Git 标签与包版本完全一致，并通过受保护的 `pypi`
Environment 后才会上传。

完整的首次配置和发布步骤请参阅[发布指南](docs/RELEASING.md)。

## 许可证

项目代码使用 [MIT License](LICENSE)。
