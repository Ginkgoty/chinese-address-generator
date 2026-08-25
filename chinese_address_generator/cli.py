# SPDX-FileCopyrightText: 2022-2026 Ginkgoty
# SPDX-License-Identifier: MIT

"""Command-line interface for chinese-address-generator."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence

from ._version import __version__
from .generator import AddressGenerator


def build_parser() -> argparse.ArgumentParser:
    """Build and return the command-line argument parser."""
    parser = argparse.ArgumentParser(description="Generate Chinese administrative addresses")
    parser.add_argument(
        "--level",
        "-l",
        type=int,
        choices=(1, 2, 3, 4),
        required=True,
        help="administrative level: 1=province, 2=prefecture, 3=county, 4=township",
    )
    parser.add_argument(
        "--num",
        "-n",
        type=int,
        default=1,
        help="number of addresses to generate (default: 1)",
    )
    parser.add_argument("--seed", type=int, help="seed for reproducible output")
    parser.add_argument("--json", action="store_true", help="output one JSON object per line")
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line interface.

    Args:
        argv: Arguments to parse. Uses :data:`sys.argv` when omitted.

    Returns:
        A process exit status. Successful execution returns zero.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.num < 1:
        parser.error("--num must be greater than zero")

    generator = AddressGenerator(seed=args.seed)
    for _ in range(args.num):
        address = generator.generate(args.level)
        if args.json:
            print(json.dumps(address.as_dict(), ensure_ascii=False))
        else:
            print(address)
    return 0


__all__ = ["build_parser", "main"]
