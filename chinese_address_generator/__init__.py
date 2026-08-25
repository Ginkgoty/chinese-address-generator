# SPDX-FileCopyrightText: 2022-2026 Ginkgoty
# SPDX-License-Identifier: MIT

"""Generate Chinese administrative addresses from authoritative data."""

from ._data import get_data_metadata, load_divisions
from ._version import __version__
from .generator import (
    AddressGenerator,
    generate_address,
    generate_level1,
    generate_level2,
    generate_level3,
    generate_level4,
    generatelevel1,
    generatelevel2,
    generatelevel3,
    generatelevel4,
)
from .models import Address, Division

__all__ = [
    "Address",
    "AddressGenerator",
    "Division",
    "__version__",
    "generate_address",
    "generate_level1",
    "generate_level2",
    "generate_level3",
    "generate_level4",
    "generatelevel1",
    "generatelevel2",
    "generatelevel3",
    "generatelevel4",
    "get_data_metadata",
    "load_divisions",
]
