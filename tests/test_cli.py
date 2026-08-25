# SPDX-FileCopyrightText: 2022-2026 Ginkgoty
# SPDX-License-Identifier: MIT

import json

import pytest

from chinese_address_generator.cli import main


def test_plain_cli_output_is_reproducible(capsys):
    assert main(["--level", "4", "--num", "2", "--seed", "2026"]) == 0
    first = capsys.readouterr().out

    assert main(["-l", "4", "-n", "2", "--seed", "2026"]) == 0
    second = capsys.readouterr().out
    assert first == second
    assert len(first.splitlines()) == 2


def test_json_cli_output(capsys):
    assert main(["--level", "3", "--json", "--seed", "1"]) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["level"] == 3
    assert len(payload["code"]) == 6
    assert payload["county"]


def test_cli_rejects_non_positive_count(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--level", "1", "--num", "0"])

    assert exc_info.value.code == 2
    assert "greater than zero" in capsys.readouterr().err


def test_cli_version(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])

    assert exc_info.value.code == 0
    assert "1.0.0" in capsys.readouterr().out
