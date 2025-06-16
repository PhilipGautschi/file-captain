"""Unit tests for the file_captain.core module.

This test suite validates the functionality of load_file and save_file functions,
including format detection, error handling, overwrite protection, and edge cases
such as corrupted files and permission errors.

Tests cover:
    - JSON, pickle, TOML, text and YAML file operations
    - Path handling (string and Path objects)
    - Overwrite protection mechanism
    - Error handling for corrupted files and OS errors

Copyright (c) 2025 Philip Gautschi, Nicolas Brehm
SPDX-License-Identifier: MIT
"""

import logging
import tempfile
from dataclasses import dataclass
from unittest.mock import patch

import pytest

from file_captain import load_file, save_file

# ------------------------------------------------------------------------------
# Fixtures and Utilities
# ------------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def configure_logging(caplog):
    """Automatically configures logging to DEBUG level for all tests."""
    caplog.set_level(logging.DEBUG)


@pytest.fixture
def temp_json_path(tmp_path):
    """Returns a temporary path for a JSON test file."""
    return tmp_path / "test.json"


@pytest.fixture
def temp_text_path(tmp_path):
    """Returns a temporary path for a text test file."""
    return tmp_path / "test.txt"


def assert_log_contains(caplog, message, level):
    """Assert a log contains the message substring and level."""
    assert any(
        message in record.message and record.levelname == level
        for record in caplog.records
    )


@dataclass
class SampleData:
    """Example data class for use in pickle tests."""

    a = "Text in unicode 🧠."
    b = 2
    c = (1, 2.12, 3)


# ------------------------------------------------------------------------------
# Test Cases
# ------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "data, extension",
    [
        ("Hello, world and some unicode characters! 🧠 字 Ω", ".txt"),
        ({"foo": "bar"}, ".json"),
        ({"Capitalized": "extension"}, ".jSoN"),
        ("No extension", ""),
        ("Unknown extension", ".unknown"),
        ({"key": "value", "num": 42}, ".pickle"),
        ([1, 2, 3, {"nested": "dict"}], ".pkl"),
        (SampleData(), ".pkl"),
        ({"key": "value", "num": 42, "🧠": "🧠"}, ".toml"),
        ({"key": "value", "num": 42}, ".yaml"),
        ({"key": "value", "num": 42}, ".yml"),
    ],
)
def test_write_and_read_various_suffix(tmp_path, data, extension, caplog):
    """Test reading and writing files with various supported extensions."""
    testfile = tmp_path / f"file_captain{extension}"
    caplog.clear()
    assert save_file(testfile, data)
    assert_log_contains(caplog, "Data written to", "INFO")

    caplog.clear()
    assert load_file(testfile) == data
    assert_log_contains(caplog, "Data loaded from", "INFO")


def test_write_and_read_path(temp_text_path):
    """Test using both string and Path objects as file paths."""
    data = "Calling read and write with paths as strings and as path objects"
    assert save_file(temp_text_path, data)
    assert load_file(temp_text_path) == data

    assert save_file(str(temp_text_path), data, overwrite_protection=False)
    assert load_file(str(temp_text_path)) == data


def test_overwrite_protection(temp_text_path, caplog):
    """Test overwrite protection mechanism when writing files."""
    data = "Check overwrite protection"
    assert save_file(temp_text_path, data)

    data2 = "Another string"
    caplog.clear()
    assert save_file(temp_text_path, data2) is False
    assert_log_contains(caplog, "File already exists.", "WARNING")
    assert load_file(temp_text_path) == data

    caplog.clear()
    assert save_file(temp_text_path, data2, overwrite_protection=False)
    assert_log_contains(caplog, "Data written to", "INFO")
    assert load_file(temp_text_path) == data2


@pytest.mark.parametrize(
    "data, extension",
    [
        (b'{"This": "JSON"\n"is": "corrupted"}', ".json"),
        (b"\xff\xfe\xfa", ".json"),
        (b"\xff\xfe\xfa", ".pickle"),
        (b"\xff\xfe\xfa", ".toml"),
        (b"\xff\xfe\xfa", ".txt"),
        (b"\xff\xfe\xfa", ".yaml"),
    ],
)
def test_load_corrupted(tmp_path, data, extension, caplog):
    """Test loading of corrupted or incompatible files returns None and logs a warning."""
    testfile = tmp_path / f"file_captain{extension}"
    with testfile.open("wb") as outfile:
        outfile.write(data)

    caplog.clear()
    assert load_file(testfile) is None
    assert_log_contains(caplog, "Decoding error", "WARNING")


def test_save_load_directory(caplog):
    """Test handling of attempts to read or write directories (should fail gracefully)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        caplog.clear()
        assert load_file(tmpdir) is None
        assert_log_contains(caplog, "No data loaded from", "WARNING")

        caplog.clear()
        assert save_file(tmpdir, "Directory", overwrite_protection=False) is False
        assert_log_contains(caplog, "No data written to", "WARNING")


def test_load_does_not_exist(temp_text_path, caplog):
    """Test loading a non-existent file returns None and logs a warning."""
    caplog.clear()
    assert load_file(temp_text_path) is None
    assert_log_contains(caplog, "No data loaded from", "WARNING")


def test_permission_error(temp_text_path, caplog):
    """Test handling of file permission errors when reading or writing."""
    data = "Check permission error"
    with patch("pathlib.Path.open", side_effect=PermissionError("Permission denied")):

        caplog.clear()
        assert save_file(temp_text_path, data) is False
        assert_log_contains(caplog, "No data written to", "WARNING")

        caplog.clear()
        assert load_file(temp_text_path) is None
        assert_log_contains(caplog, "No data loaded from", "WARNING")
