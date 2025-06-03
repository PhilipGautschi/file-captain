# ──────────────────────────────────────────────────────────────────────────────────────
#  File        : src/file_utils/__init__.py
#  Author      : Philip Gautschi
#  Created     : 03 June 2025
#  Updated     : 03 June 2025 - Version 1.0.0
#  Description : init file_utils for file_utils module
#  Dependencies: only standard libraries
#  License     : Copyright (c) 2025 Philip Gautschi. All rights reserved.
# ──────────────────────────────────────────────────────────────────────────────────────

__version__ = "1.0.0"
__author__ = "Philip Gautschi"

from src.file_utils.core import save_file
from src.file_utils.core import load_file

__all__ = ["save_file", "load_file"]