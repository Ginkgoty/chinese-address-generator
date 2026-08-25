# SPDX-FileCopyrightText: 2022-2026 Ginkgoty
# SPDX-License-Identifier: MIT

from pathlib import Path

import pytest

from chinese_address_generator import _data, get_data_metadata, load_divisions
from chinese_address_generator._data import Dataset, get_dataset
from chinese_address_generator.models import Division


def test_dataset_metadata_and_counts():
    metadata = get_data_metadata()

    assert metadata["data_as_of"] == "2025-12-31"
    assert metadata["source_table"] == "Xzqh20251231"
    assert metadata["counts"] == {"1": 33, "2": 333, "3": 2845, "4": 38723}
    assert metadata["included_item_count"] == 41934
    assert metadata["excluded"][0]["name"] == "台湾省"


def test_all_codes_and_parent_relationships_are_valid():
    divisions = load_divisions()
    by_code = {division.code: division for division in divisions}

    assert len(divisions) == len(by_code) == 41934
    for division in divisions:
        expected_length = 9 if division.level == 4 else 6
        assert division.code.isdigit()
        assert len(division.code) == expected_length
        if division.level == 1:
            assert division.parent_code == ""
        else:
            parent = by_code[division.parent_code]
            assert parent.level < division.level


def test_load_divisions_can_filter_levels():
    assert len(load_divisions(1)) == 33
    assert len(load_divisions(2)) == 333
    assert len(load_divisions(3)) == 2845
    assert len(load_divisions(4)) == 38723

    with pytest.raises(ValueError, match="level must"):
        load_divisions(0)


def test_direct_municipality_path_skips_prefecture_placeholder():
    dataset = get_dataset()
    path = dataset.path_for(dataset.by_code["110101"])

    assert [(item.level, item.name) for item in path] == [(1, "北京市"), (3, "东城区")]


def test_path_resolution_detects_cycles():
    division = Division(level=1, code="990000", parent_code="990000", name="循环")
    dataset = Dataset(
        divisions=(division,),
        by_code={division.code: division},
        by_level={1: (division,)},
        metadata={},
    )

    with pytest.raises(RuntimeError, match="cycle detected"):
        dataset.path_for(division)


def test_modern_resource_reader_can_be_used_on_python_38(monkeypatch):
    package_root = Path(__file__).parents[1] / "chinese_address_generator"
    monkeypatch.setattr(_data.resources, "files", lambda _package: package_root, raising=False)
    get_dataset.cache_clear()

    assert get_dataset().metadata["data_as_of"] == "2025-12-31"

    get_dataset.cache_clear()
