# SPDX-FileCopyrightText: 2022-2026 Ginkgoty
# SPDX-License-Identifier: MIT

import hashlib
import json

import pytest

from tools.update_data import build_dataset, parse_payload, validate_records, write_dataset


def make_payload(records):
    return json.dumps(
        {"data": records, "message": "ok", "status": 200, "total": len(records)},
        ensure_ascii=False,
    ).encode()


def test_build_dataset_normalises_codes_and_records_exclusion(tmp_path):
    raw = make_payload(
        [
            {
                "name": "河北省",
                "code": "130000000",
                "level": 1,
                "parentCode": "000000000000",
            },
            {
                "name": "石家庄市",
                "code": "130100000",
                "level": 2,
                "parentCode": "130000000000",
            },
            {
                "name": "长安区",
                "code": "130102000",
                "level": 3,
                "parentCode": "130100000000",
            },
            {
                "name": "建北街道",
                "code": "130102001",
                "level": 4,
                "parentCode": "130102000000",
            },
            {
                "name": "台湾省",
                "code": "资料暂缺",
                "level": 1,
                "parentCode": "000000000000",
            },
        ]
    )

    dataset = build_dataset(raw, "XzqhTest", "2025-12-31")
    assert dataset["divisions"] == [
        (1, "130000", "", "河北省"),
        (2, "130100", "130000", "石家庄市"),
        (3, "130102", "130100", "长安区"),
        (4, "130102001", "130102", "建北街道"),
    ]
    assert dataset["metadata"]["source_sha256"] == hashlib.sha256(raw).hexdigest()
    assert dataset["metadata"]["excluded"][0]["name"] == "台湾省"

    output = tmp_path / "nested/divisions.json"
    write_dataset(dataset, output)
    assert json.loads(output.read_text(encoding="utf-8"))["metadata"]["source_table"] == (
        "XzqhTest"
    )


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        ({"status": 500, "data": [], "total": 0}, "status"),
        ({"status": 200, "data": [], "total": 1}, "incomplete"),
        (
            {
                "status": 200,
                "data": [{"name": "", "code": "130000000", "level": 1}],
                "total": 1,
            },
            "invalid source record",
        ),
        (
            {
                "status": 200,
                "data": [{"name": "河北省", "code": "13000000", "level": 1}],
                "total": 1,
            },
            "code length",
        ),
    ],
)
def test_parse_payload_rejects_invalid_responses(payload, message):
    with pytest.raises(ValueError, match=message):
        parse_payload(json.dumps(payload).encode())


def test_validate_records_rejects_duplicates_and_bad_parents():
    with pytest.raises(ValueError, match="not unique"):
        validate_records([(1, "130000", "", "河北省"), (1, "130000", "", "重复")])

    with pytest.raises(ValueError, match="missing parent"):
        validate_records([(2, "130100", "130000", "石家庄市")])

    with pytest.raises(ValueError, match="invalid level"):
        validate_records(
            [
                (1, "130000", "", "河北省"),
                (2, "130100", "130000", "石家庄市"),
                (2, "130200", "130100", "唐山市"),
            ]
        )


def test_metadata_is_returned_as_a_deep_copy():
    from chinese_address_generator import get_data_metadata

    first = get_data_metadata()
    first["counts"]["1"] = -1

    assert get_data_metadata()["counts"]["1"] == 33
