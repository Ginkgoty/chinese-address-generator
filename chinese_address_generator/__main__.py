# SPDX-FileCopyrightText: 2022-2026 Ginkgoty
# SPDX-License-Identifier: MIT

"""Support ``python -m chinese_address_generator``."""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
