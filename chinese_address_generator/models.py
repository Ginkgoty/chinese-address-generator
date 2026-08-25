# SPDX-FileCopyrightText: 2022-2026 Ginkgoty
# SPDX-License-Identifier: MIT

"""Public immutable models returned by the generator."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Union

JsonValue = Union[str, int, None]


@dataclass(frozen=True)
class Division:
    """Represent one official administrative division.

    Attributes:
        level: Administrative level from 1 through 4.
        code: Official six- or nine-digit division code.
        parent_code: Code of the parent division, or an empty string at level 1.
        name: Official division name.
    """

    level: int
    code: str
    parent_code: str
    name: str


@dataclass(frozen=True)
class Address:
    """Represent a generated address and its authoritative hierarchy.

    Attributes:
        divisions: Ordered divisions from the province to the selected endpoint.
    """

    divisions: tuple[Division, ...]

    @property
    def level(self) -> int:
        """Return the administrative level of the address endpoint."""
        return self.divisions[-1].level

    @property
    def code(self) -> str:
        """Return the official code of the address endpoint."""
        return self.divisions[-1].code

    @property
    def full_name(self) -> str:
        """Return all available component names joined without separators."""
        return "".join(division.name for division in self.divisions)

    def name_at(self, level: int) -> str | None:
        """Return the component name at an administrative level.

        Args:
            level: Administrative level to find.

        Returns:
            The matching name, or ``None`` when the hierarchy skips the level.
        """
        for division in self.divisions:
            if division.level == level:
                return division.name
        return None

    @property
    def province(self) -> str | None:
        """Return the province-level name when available."""
        return self.name_at(1)

    @property
    def prefecture(self) -> str | None:
        """Return the prefecture-level name when available."""
        return self.name_at(2)

    @property
    def county(self) -> str | None:
        """Return the county-level name when available."""
        return self.name_at(3)

    @property
    def township(self) -> str | None:
        """Return the township-level name when available."""
        return self.name_at(4)

    def format(self, *, include_code: bool = True, separator: str = " ") -> str:
        """Format the address as text.

        Args:
            include_code: Append the endpoint code when true.
            separator: Text inserted between the name and code.

        Returns:
            The compact full name, optionally followed by its code.
        """
        if include_code:
            return f"{self.full_name}{separator}{self.code}"
        return self.full_name

    def as_dict(self) -> dict[str, JsonValue]:
        """Return a JSON-serialisable representation of the address."""
        return {
            "address": self.full_name,
            "code": self.code,
            "level": self.level,
            "province": self.province,
            "prefecture": self.prefecture,
            "county": self.county,
            "township": self.township,
        }

    def __str__(self) -> str:
        """Return the default human-readable representation."""
        return self.format()


__all__ = ["Address", "Division"]
