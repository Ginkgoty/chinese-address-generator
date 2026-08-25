# SPDX-FileCopyrightText: 2022-2026 Ginkgoty
# SPDX-License-Identifier: MIT

import random
import re
import warnings

import pytest

from chinese_address_generator import AddressGenerator, generate_address
from chinese_address_generator import generator as legacy


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_generate_address_returns_valid_path(level):
    address = generate_address(level, rng=random.Random(level))

    assert address.level == level
    assert address.divisions[-1].code == address.code
    assert [item.level for item in address.divisions] == sorted(
        item.level for item in address.divisions
    )
    assert address.full_name == "".join(item.name for item in address.divisions)
    assert str(address) == f"{address.full_name} {address.code}"


def test_seeded_generators_are_reproducible():
    first = AddressGenerator(seed=2026)
    second = AddressGenerator(seed=2026)

    assert [first.generate(4) for _ in range(5)] == [second.generate(4) for _ in range(5)]


def test_address_helpers_and_serialisation():
    address = AddressGenerator(seed=7).generate(4)
    result = address.as_dict()

    assert address.name_at(99) is None
    assert address.format(include_code=False) == address.full_name
    assert address.format(separator=" | ") == f"{address.full_name} | {address.code}"
    assert result["address"] == address.full_name
    assert result["code"] == address.code
    assert result["level"] == 4
    assert result["township"] == address.township


@pytest.mark.parametrize("level", [0, 5, True, -1])
def test_invalid_levels_raise(level):
    with pytest.raises(ValueError, match="level must"):
        generate_address(level)


@pytest.mark.parametrize(
    ("function", "replacement", "code_length"),
    [
        (legacy.generatelevel1, "generate_level1", 6),
        (legacy.generatelevel2, "generate_level2", 6),
        (legacy.generatelevel3, "generate_level3", 6),
        (legacy.generatelevel4, "generate_level4", 9),
    ],
)
def test_legacy_string_functions_warn(function, replacement, code_length):
    with pytest.warns(DeprecationWarning, match=rf"use {replacement}\(\)"):
        result = function()

    assert re.search(rf" \d{{{code_length}}}$", result)
    assert replacement in function.__deprecated__


def test_snake_case_string_functions_do_not_warn():
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        results = (
            legacy.generate_level1(),
            legacy.generate_level2(),
            legacy.generate_level3(),
            legacy.generate_level4(),
        )

    for result, code_length in zip(results, (6, 6, 6, 9)):
        assert re.search(rf" \d{{{code_length}}}$", result)
