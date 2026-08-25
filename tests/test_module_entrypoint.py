# SPDX-FileCopyrightText: 2022-2026 Ginkgoty
# SPDX-License-Identifier: MIT

import runpy

import pytest

from chinese_address_generator import cli


def test_module_does_not_run_cli_when_imported(monkeypatch):
    monkeypatch.setattr(cli, "main", lambda: pytest.fail("CLI unexpectedly ran"))

    runpy.run_module("chinese_address_generator.__main__", run_name="imported_entrypoint")


def test_module_runs_cli_and_propagates_exit_code(monkeypatch):
    monkeypatch.setattr(cli, "main", lambda: 17)

    with pytest.raises(SystemExit) as exc_info:
        runpy.run_module("chinese_address_generator.__main__", run_name="__main__")

    assert exc_info.value.code == 17
