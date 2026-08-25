#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2022-2026 Ginkgoty
# SPDX-License-Identifier: MIT

"""Build the bundled dataset from the Ministry of Civil Affairs API."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from collections.abc import Sequence
from datetime import date
from pathlib import Path
from typing import Any, Tuple

SOURCE_PAGE = "https://dmfw.mca.gov.cn/XzqhVersionPublish.html"
SOURCE_ENDPOINT = "https://dmfw.mca.gov.cn/xzqh/getCodeList"
DEFAULT_TABLE = "Xzqh20251231"
DEFAULT_SOURCE_DATE = "2025-12-31"
DEFAULT_OUTPUT = Path(__file__).parents[1] / "chinese_address_generator/data/divisions.json"

Record = Tuple[int, str, str, str]


def fetch_payload(table: str, page_size: int = 50_000, retries: int = 4) -> bytes:
    """Download all published divisions in one paginated API request.

    Args:
        table: Official source table identifier.
        page_size: Maximum records requested from the endpoint.
        retries: Total download attempts before failing.

    Returns:
        Raw response bytes from the official endpoint.

    Raises:
        RuntimeError: If all download attempts fail.
    """
    body = urllib.parse.urlencode(
        {
            "parentCode": "",
            "placeCode": "",
            "title": "",
            "tableName": table,
            "pageNum": 1,
            "pageSize": page_size,
        }
    ).encode("ascii")
    request = urllib.request.Request(
        SOURCE_ENDPOINT,
        data=body,
        headers={
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": SOURCE_PAGE,
            "User-Agent": "Mozilla/5.0 chinese-address-generator-data-builder/1.0",
            "X-Requested-With": "XMLHttpRequest",
        },
        method="POST",
    )

    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read()
        except (TimeoutError, urllib.error.URLError) as exc:
            if attempt == retries - 1:
                raise RuntimeError("failed to download the official dataset") from exc
            time.sleep(2**attempt)
    raise AssertionError("unreachable")


def parse_payload(raw: bytes) -> tuple[list[Record], dict[str, Any]]:
    """Normalise and validate an official API response.

    Args:
        raw: UTF-8 JSON response bytes from the official endpoint.

    Returns:
        Normalised division records and snapshot details.

    Raises:
        ValueError: If the response is unsuccessful, incomplete, or malformed.
    """
    payload = json.loads(raw.decode("utf-8"))
    if payload.get("status") != 200:
        raise ValueError(f"official API returned status {payload.get('status')!r}")
    source_records = payload.get("data")
    if not isinstance(source_records, list) or payload.get("total") != len(source_records):
        raise ValueError("official API returned an incomplete page")

    records: list[Record] = []
    excluded = []
    for item in source_records:
        level = item.get("level")
        code = item.get("code")
        name = item.get("name")
        parent_code = item.get("parentCode", "")
        if level not in (1, 2, 3, 4) or not isinstance(name, str) or not name:
            raise ValueError(f"invalid source record: {item!r}")
        if not isinstance(code, str) or not code.isdigit():
            excluded.append(
                {
                    "name": name,
                    "source_code": code,
                    "reason": "the official source does not publish a numeric code",
                }
            )
            continue
        if len(code) != 9:
            raise ValueError(f"unexpected source code length: {item!r}")

        normalised_code = code if level == 4 else code[:6]
        normalised_parent = "" if level == 1 else str(parent_code)[:6]
        records.append((level, normalised_code, normalised_parent, name))

    records.sort(key=lambda record: (record[0], record[1]))
    validate_records(records)
    counts = Counter(record[0] for record in records)
    details = {
        "source_item_count": len(source_records),
        "included_item_count": len(records),
        "counts": {str(level): counts[level] for level in (1, 2, 3, 4)},
        "excluded": excluded,
    }
    return records, details


def validate_records(records: Sequence[Record]) -> None:
    """Validate codes, uniqueness, and every parent relationship.

    Args:
        records: Normalised division records to validate.

    Raises:
        ValueError: If any record or parent relationship is invalid.
    """
    by_code = {record[1]: record for record in records}
    if len(by_code) != len(records):
        raise ValueError("normalised division codes are not unique")

    for level, code, parent_code, _name in records:
        expected_length = 9 if level == 4 else 6
        if len(code) != expected_length or not code.isdigit():
            raise ValueError(f"invalid level-{level} code: {code!r}")
        if level == 1:
            if parent_code:
                raise ValueError(f"province {code} unexpectedly has a parent")
            continue
        parent = by_code.get(parent_code)
        if parent is None:
            raise ValueError(f"division {code} references missing parent {parent_code}")
        if parent[0] >= level:
            raise ValueError(f"division {code} has invalid level-{parent[0]} parent")


def build_dataset(raw: bytes, table: str, source_date: str) -> dict[str, Any]:
    """Build the distributable dataset and its provenance metadata.

    Args:
        raw: UTF-8 JSON response bytes from the official endpoint.
        table: Official source table identifier.
        source_date: ISO date through which the source data is current.

    Returns:
        A mapping ready to serialise as the bundled dataset.
    """
    records, details = parse_payload(raw)
    return {
        "metadata": {
            "authority": "Ministry of Civil Affairs of the People's Republic of China",
            "source_page": SOURCE_PAGE,
            "source_endpoint": SOURCE_ENDPOINT,
            "source_table": table,
            "data_as_of": source_date,
            "retrieved_at": date.today().isoformat(),
            "source_sha256": hashlib.sha256(raw).hexdigest(),
            **details,
        },
        "divisions": records,
    }


def write_dataset(dataset: dict[str, Any], output: Path) -> None:
    """Write compact UTF-8 JSON atomically.

    Args:
        dataset: Validated dataset to serialise.
        output: Destination path for the bundled JSON file.
    """
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=output.parent, delete=False
    ) as stream:
        json.dump(dataset, stream, ensure_ascii=False, separators=(",", ":"))
        stream.write("\n")
        temporary_name = stream.name
    os.replace(temporary_name, output)


def build_parser() -> argparse.ArgumentParser:
    """Build and return the data updater's argument parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="use a previously downloaded API response")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--table", default=DEFAULT_TABLE)
    parser.add_argument("--source-date", default=DEFAULT_SOURCE_DATE)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the data update command.

    Args:
        argv: Arguments to parse. Uses :data:`sys.argv` when omitted.

    Returns:
        A process exit status. Successful execution returns zero.
    """
    args = build_parser().parse_args(argv)
    raw = args.input.read_bytes() if args.input else fetch_payload(args.table)
    dataset = build_dataset(raw, args.table, args.source_date)
    write_dataset(dataset, args.output)
    metadata = dataset["metadata"]
    print(
        f"wrote {metadata['included_item_count']} divisions "
        f"(as of {metadata['data_as_of']}) to {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
