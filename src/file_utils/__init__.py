"""File utilities package for loading and saving data with automatic format detection.

This package provides a simple interface for file I/O operations with automatic
format detection based on file extensions. Supports built-in error handling and
optional overwrite protection.

Exports:
    load_file: Load data from JSON, pickle or text files
    save_file: Save data to files with format auto-detection

Copyright (c) 2025 Philip Gautschi, Nicolas Brehm
SPDX-License-Identifier: MIT
"""

__version__ = "1.0.0"
__author__ = "Philip Gautschi, Nicolas Brehm"

from .core import load_file, save_file

__all__ = ["save_file", "load_file"]
