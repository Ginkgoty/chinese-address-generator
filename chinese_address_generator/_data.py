# SPDX-FileCopyrightText: 2022-2026 Ginkgoty
# SPDX-License-Identifier: MIT

"""Lazy loading and indexing of the bundled administrative dataset."""

from __future__ import annotations

import json
from collections.abc import Mapping
from copy import deepcopy
from dataclasses import dataclass
from functools import lru_cache
from importlib import resources
from types import MappingProxyType
from typing import Any

from .models import Division


@dataclass(frozen=True)
class Dataset:
    """Provide immutable indexes over the bundled divisions.

    Attributes:
        divisions: Every bundled division in stable source order.
        by_code: Division lookup keyed by official code.
        by_level: Division collections keyed by administrative level.
        metadata: Provenance and integrity metadata for the data snapshot.
    """

    divisions: tuple[Division, ...]
    by_code: Mapping[str, Division]
    by_level: Mapping[int, tuple[Division, ...]]
    metadata: Mapping[str, Any]

    def path_for(self, division: Division) -> tuple[Division, ...]:
        """Resolve a division to its complete parent path.

        Args:
            division: Endpoint whose hierarchy should be resolved.

        Returns:
            Ordered divisions from the province to ``division``.

        Raises:
            RuntimeError: If a cycle is present in the bundled hierarchy.
        """
        path = []
        current: Division | None = division
        seen = set()
        while current is not None:
            if current.code in seen:
                raise RuntimeError(f"cycle detected in division data at {current.code}")
            seen.add(current.code)
            path.append(current)
            current = self.by_code.get(current.parent_code)
        path.reverse()
        return tuple(path)


@lru_cache(maxsize=1)
def get_dataset() -> Dataset:
    """Load and cache the packaged dataset on first use.

    Returns:
        Immutable division indexes and data provenance metadata.
    """
    if hasattr(resources, "files"):
        data_file = resources.files("chinese_address_generator").joinpath("data/divisions.json")
        with data_file.open("r", encoding="utf-8") as stream:
            payload = json.load(stream)
    else:  # pragma: no cover - covered by the Python 3.8 CI job
        with resources.open_text(
            "chinese_address_generator.data", "divisions.json", encoding="utf-8"
        ) as stream:
            payload = json.load(stream)

    divisions = tuple(Division(*record) for record in payload["divisions"])
    by_code: dict[str, Division] = {division.code: division for division in divisions}
    levels: dict[int, list[Division]] = {1: [], 2: [], 3: [], 4: []}
    for division in divisions:
        levels[division.level].append(division)

    return Dataset(
        divisions=divisions,
        by_code=MappingProxyType(by_code),
        by_level=MappingProxyType(
            {level: tuple(level_divisions) for level, level_divisions in levels.items()}
        ),
        metadata=MappingProxyType(payload["metadata"]),
    )


def load_divisions(level: int | None = None) -> tuple[Division, ...]:
    """Return bundled divisions, optionally filtered by level.

    Args:
        level: Administrative level from 1 through 4, or ``None`` for all records.

    Returns:
        An immutable tuple of matching divisions.

    Raises:
        ValueError: If ``level`` is outside the supported range.
    """
    dataset = get_dataset()
    if level is None:
        return dataset.divisions
    if isinstance(level, bool) or level not in dataset.by_level:
        raise ValueError("level must be one of 1, 2, 3, or 4")
    return dataset.by_level[level]


def get_data_metadata() -> dict[str, Any]:
    """Return a deep copy of the bundled dataset metadata."""
    return deepcopy(dict(get_dataset().metadata))


__all__ = ["get_data_metadata", "load_divisions"]
