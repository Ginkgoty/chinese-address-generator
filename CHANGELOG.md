# Changelog

All notable changes to this project are documented in this file.

## 1.0.0 - 2026-08-25

### Added

- Added the complete Ministry of Civil Affairs administrative division snapshot dated 2025-12-31.
- Added authoritative township-level (L4) names and 9-digit codes.
- Added immutable `Address` and `Division` models plus seeded generation.
- Added JSON Lines CLI output and a working `python -m chinese_address_generator` entry point.
- Added uv-based development, linting, tests, packaging checks, and Python 3.8–3.14 CI.
- Added English and Simplified Chinese documentation.
- Added SPDX file metadata and strict PEP 257 docstring checks.

### Changed

- Rebuilt the package around lazy, indexed data loading with no runtime dependencies.
- Samples uniformly from all divisions at the requested level.
- Uses 6-digit codes for L1–L3 and official 9-digit township codes for L4.
- Modernised packaging from `setup.py` to `pyproject.toml`.
- Made `_version.py` the single source of the package version.

### Compatibility

- The original `generatelevel1()` through `generatelevel4()` names remain available but now emit
  `DeprecationWarning`; use `generate_level1()` through `generate_level4()` instead.
- L4 output now ends in a 9-digit township code instead of a 6-digit county code.
- The mutable `level3_list` and `level4_list` module globals were replaced by
  `load_divisions()` and `get_data_metadata()`.

## 0.2.0 - 2024-05-03

- Updated the bundled source data to the 2023 National Bureau of Statistics pages.
- Added the original HTML crawler and command-line interface.

## 0.1.8 - 2022-08-13

- Published the initial PyPI release.
