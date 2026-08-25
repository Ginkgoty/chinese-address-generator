# SPDX-FileCopyrightText: 2022-2026 Ginkgoty
# SPDX-License-Identifier: MIT

"""Random address generation backed by the bundled official dataset."""

import functools
import random
import warnings
from typing import Callable, Optional, TypeVar, cast

from ._data import get_dataset
from .models import Address

Function = TypeVar("Function", bound=Callable[..., object])


def _deprecated(message: str) -> Callable[[Function], Function]:
    """Decorate a compatibility API with a runtime deprecation warning."""

    def decorator(function: Function) -> Function:
        @functools.wraps(function)
        def wrapper(*args: object, **kwargs: object) -> object:
            warnings.warn(message, DeprecationWarning, stacklevel=2)
            return function(*args, **kwargs)

        wrapper.__deprecated__ = message
        return cast(Function, wrapper)

    return decorator


def _validate_level(level: int) -> None:
    """Validate a requested administrative level."""
    if isinstance(level, bool) or level not in (1, 2, 3, 4):
        raise ValueError("level must be one of 1, 2, 3, or 4")


def generate_address(level: int = 4, *, rng: Optional[random.Random] = None) -> Address:
    """Return a random address ending at the requested administrative level.

    Selection is uniform across all official divisions at the requested level.
    Pass a :class:`random.Random` instance for reproducible output.

    Args:
        level: Target administrative level from 1 through 4.
        rng: Optional random number generator used for selection.

    Returns:
        A structured address ending at the requested level.

    Raises:
        ValueError: If ``level`` is outside the supported range.
    """
    _validate_level(level)
    dataset = get_dataset()
    chooser = rng if rng is not None else random
    division = chooser.choice(dataset.by_level[level])
    return Address(dataset.path_for(division))


class AddressGenerator:
    """An isolated, optionally seeded random address generator."""

    def __init__(self, seed: Optional[int] = None) -> None:
        """Initialise an isolated generator.

        Args:
            seed: Optional seed used to make generated sequences reproducible.
        """
        self._random = random.Random(seed)

    def generate(self, level: int = 4) -> Address:
        """Return a random address using this instance's random state.

        Args:
            level: Target administrative level from 1 through 4.

        Returns:
            A structured address ending at the requested level.

        Raises:
            ValueError: If ``level`` is outside the supported range.
        """
        return generate_address(level, rng=self._random)


def generate_level1() -> str:
    """Return a province-level address using the legacy string format."""
    return str(generate_address(1))


def generate_level2() -> str:
    """Return a prefecture-level address using the legacy string format."""
    return str(generate_address(2))


def generate_level3() -> str:
    """Return a county-level address using the legacy string format."""
    return str(generate_address(3))


def generate_level4() -> str:
    """Return a township-level address using the legacy string format."""
    return str(generate_address(4))


# Backward-compatible names from versions 0.x.
@_deprecated("generatelevel1() is deprecated; use generate_level1() instead.")
def generatelevel1() -> str:
    """Return level 1 using the deprecated 0.x function name."""
    return generate_level1()


@_deprecated("generatelevel2() is deprecated; use generate_level2() instead.")
def generatelevel2() -> str:
    """Return level 2 using the deprecated 0.x function name."""
    return generate_level2()


@_deprecated("generatelevel3() is deprecated; use generate_level3() instead.")
def generatelevel3() -> str:
    """Return level 3 using the deprecated 0.x function name."""
    return generate_level3()


@_deprecated("generatelevel4() is deprecated; use generate_level4() instead.")
def generatelevel4() -> str:
    """Return level 4 using the deprecated 0.x function name."""
    return generate_level4()


__all__ = [
    "AddressGenerator",
    "generate_address",
    "generate_level1",
    "generate_level2",
    "generate_level3",
    "generate_level4",
    "generatelevel1",
    "generatelevel2",
    "generatelevel3",
    "generatelevel4",
]
