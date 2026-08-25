# Chinese Address Generator

[简体中文](../README.md)

[![CI](https://github.com/Ginkgoty/chinese-address-generator/actions/workflows/ci.yml/badge.svg)](https://github.com/Ginkgoty/chinese-address-generator/actions/workflows/ci.yml)
[![Release](https://github.com/Ginkgoty/chinese-address-generator/actions/workflows/release.yml/badge.svg)](https://github.com/Ginkgoty/chinese-address-generator/actions/workflows/release.yml)
[![PyPI](https://img.shields.io/pypi/v/chinese-address-generator.svg)](https://pypi.org/project/chinese-address-generator/)
[![Python](https://img.shields.io/pypi/pyversions/chinese-address-generator.svg)](https://pypi.org/project/chinese-address-generator/)
[![License](https://img.shields.io/pypi/l/chinese-address-generator.svg)](../LICENSE)

Generate random Chinese administrative addresses from authoritative, bundled data. The package
works offline at runtime, has no runtime dependencies, and supports Python 3.8 through 3.14.

The bundled snapshot is sourced from the Ministry of Civil Affairs' National Database for
Geographical Names. It is current as of **2025-12-31**, the latest annual dataset published as of
2026-08-25.

## Installation

```bash
pip install chinese-address-generator
```

## Python API

Use `generate_address()` when you need structured output:

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
print(address.as_dict())  # JSON-serialisable dictionary
```

Levels correspond to actual administrative divisions published by the authority:

| Level | Division | Code returned | Bundled records |
| --- | --- | --- | ---: |
| 1 | Province-level | 6 digits | 33 |
| 2 | Prefecture-level | 6 digits | 333 |
| 3 | County-level | 6 digits | 2,845 |
| 4 | Township-level (towns, townships, subdistricts) | 9 digits | 38,723 |

Some hierarchies legitimately skip a level. Direct-administered municipalities, for example, link
their county-level divisions directly to the province-level municipality. An `Address` therefore
models the authoritative path instead of inventing a placeholder prefecture.

### Reproducible generation

```python
from chinese_address_generator import AddressGenerator

generator = AddressGenerator(seed=2026)
print(generator.generate(level=4))
```

### String compatibility API

The original 0.x function names remain available during the compatibility period and return
`"full address code"` strings, but each call emits `DeprecationWarning`. Migrate to the matching
snake-case API:

```python
from chinese_address_generator import generator

generator.generatelevel1()  # Use generate_level1() instead
generator.generatelevel2()  # Use generate_level2() instead
generator.generatelevel3()  # Use generate_level3() instead
generator.generatelevel4()  # Use generate_level4() instead
```

`generate_level1()` through `generate_level4()` are the recommended string APIs and do not emit
deprecation warnings.

### Inspecting the dataset

```python
from chinese_address_generator import get_data_metadata, load_divisions

townships = load_divisions(level=4)
metadata = get_data_metadata()
print(metadata["data_as_of"])  # 2025-12-31
```

## Command line

```console
$ cnaddrgen --level 4 --num 2
安徽省宣城市绩溪县上庄镇 341824103
河北省石家庄市长安区建北街道 130102001

$ cnaddrgen --level 4 --seed 2026 --json
{"address": "...", "code": "...", "level": 4, ...}
```

`python -m chinese_address_generator` provides the same interface.

## Data provenance and L4 accuracy

The source is the Ministry of Civil Affairs' official
[Administrative Division Codes](https://dmfw.mca.gov.cn/XzqhVersionPublish.html) publication. Its
notice states that the dataset covers province, prefecture, county, and township administrative
establishments and is current as of 2025-12-31. Province/prefecture/county codes are determined by
the Ministry; township codes are determined by provincial-level civil affairs departments.

L4 names are therefore sampled from official township-level records—they are not synthetic names.
The package does not contain village/community-level urban-rural classification codes, postal
addresses, house numbers, or geographic coordinates.

The official source lists Taiwan Province as “data unavailable” without a numeric code, so that one
record is preserved in dataset metadata but excluded from generation. Hong Kong and Macao are
available at level 1; the source does not publish lower-level records for them in this dataset.

## Development with uv

```bash
uv sync
uv run pytest
uv run ruff check .
uv build
uv run twine check dist/*
```

Ruff enforces both PEP 8 code rules and PEP 257 docstring rules. The statement and branch coverage
gate is 100%.

Refresh the bundled snapshot from the official API:

```bash
uv run python tools/update_data.py
```

The updater validates record counts, code lengths, uniqueness, and every parent relationship before
atomically replacing the bundled file. Update its table name and source date only after the official
publication page announces a new annual snapshot.

## Releasing

Production releases are published automatically through GitHub Actions and PyPI Trusted Publishing;
no long-lived PyPI token is stored in the repository. The release job requires a `v`-prefixed Git
tag that exactly matches the package version and deploys through the protected `pypi` environment.

See the [release guide](RELEASING.en.md) for initial setup and the complete maintainer procedure.

## License

Code is released under the [MIT License](../LICENSE).
