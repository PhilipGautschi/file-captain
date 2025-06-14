"""File utilities for loading and saving data with automatic format detection.

This module provides simple functions to load and save data to files and
automatically detects file format based on path extension. Supports both
string and Path objects for file paths, with built-in error handling and
optional overwrite protection.

Exports:
    load_file: Load data from a file with automatic format detection
    save_file: Save data to a file with optional overwrite protection

Copyright (c) 2025 Philip Gautschi, Nicolas Brehm
SPDX-License-Identifier: MIT
"""

__version__ = "1.0.0"
__author__ = "Philip Gautschi, Nicolas Brehm"

from .core import load_file, save_file

__all__ = ["load_file", "save_file"]
