# ──────────────────────────────────────────────────────────────────────────────────────
#  File        : tests/file_utils/test_core.py
#  Author      : Philip Gautschi
#  Created     : 04 May 2025
#  Updated     : 25 May 2025 - Version 1.0.0
#  Description : unit test for file_utils.py
#  Dependencies: pytest
#  License     : Copyright (c) 2025 Philip Gautschi. All rights reserved.
# ──────────────────────────────────────────────────────────────────────────────────────

import tempfile
import logging
from unittest.mock import patch
import pytest

from file_utils import load_file, save_file


@pytest.fixture(autouse=True)
def configure_logging(caplog):
    caplog.set_level(logging.DEBUG)
    
# Utility function. ────────────────────────────────────────────────────────────────────
@pytest.fixture
def temp_json_path(tmp_path):
    return tmp_path / "test.json"


@pytest.fixture
def temp_text_path(tmp_path):
    return tmp_path / "test.txt"


def assert_log_contains(caplog, message, level):
    assert any(
        message in record.message and record.levelname == level
        for record in caplog.records
    )

class TestClass:
    def __init__(self):
        self.a = [1, 'a', '🧠']
        self.b = 2
        self.c = (1, 2, 3)

@pytest.mark.parametrize("extension", [".pickle", ".pkl"])
def test_pickle_custom_class(tmp_path, extension, caplog):
    obj = TestClass()
    testfile = tmp_path / f"test_custom_class{extension}"

    caplog.clear()
    assert save_file(testfile, obj)
    assert_log_contains(caplog, "Data written to", "INFO")

    caplog.clear()
    loaded_obj = load_file(testfile)
    assert_log_contains(caplog, "Data loaded from", "INFO")

    # Compare attributes individually
    assert isinstance(loaded_obj, TestClass)
    assert loaded_obj.a == obj.a
    assert loaded_obj.b == obj.b
    assert loaded_obj.c == obj.c


# Test various suffixes and defaults to plain text. ────────────────────────────────────
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
    ],
)
def test_write_and_read_various_suffix(tmp_path, data, extension, caplog):
    testfile = tmp_path / f"file_utils{extension}"

    caplog.clear()
    assert save_file(testfile, data)
    assert_log_contains(caplog, "Data written to", "INFO")

    caplog.clear()
    assert load_file(testfile) == data
    assert_log_contains(caplog, "Data loaded from", "INFO")


# Test if path_string can be both strings or path objects. ─────────────────────────────
def test_write_and_read_path(temp_text_path):
    data = "Calling read and write with paths as strings and as path objects"
    assert save_file(temp_text_path, data)
    assert load_file(temp_text_path) == data

    assert save_file(str(temp_text_path), data, overwrite_protection=False)
    assert load_file(str(temp_text_path)) == data


# Test overwrite protection. ───────────────────────────────────────────────────────────
def test_overwrite_protection(temp_text_path, caplog):
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


# Test corrupted or wrong file_utils types. ──────────────────────────────────────────────────
@pytest.mark.parametrize(
    "data, extension",
    [
        (b'{"This": "JSON"\n"is": "corrupted"}', ".json"),
        (b"\xff\xfe\xfa", ".json"),
        (b"\xff\xfe\xfa", ".txt"),
    ],
)
def test_load_corrupted(tmp_path, data, extension, caplog):
    testfile = tmp_path / f"file_utils{extension}"
    with testfile.open("wb") as outfile:
        outfile.write(data)

    caplog.clear()
    assert load_file(testfile) is None
    assert_log_contains(caplog, "Decoding error", "WARNING")


# Test for different OS errors (FileNotFoundError, IsADirectoryError, PermissionError).
def test_save_load_directory(caplog):
    with tempfile.TemporaryDirectory() as tmpdir:
        caplog.clear()
        assert load_file(tmpdir) is None
        assert_log_contains(caplog, "No data loaded from", "WARNING")

        caplog.clear()
        assert save_file(tmpdir, "Directory", overwrite_protection=False) is False
        assert_log_contains(caplog, "No data written to", "WARNING")


def test_load_does_not_exist(temp_text_path, caplog):
    caplog.clear()
    assert load_file(temp_text_path) is None
    assert_log_contains(caplog, "No data loaded from", "WARNING")


def test_permission_error(temp_text_path, caplog):
    data = "Check permission error"
    with patch("pathlib.Path.open", side_effect=PermissionError("Permission denied")):

        caplog.clear()
        assert save_file(temp_text_path, data) is False
        assert_log_contains(caplog, "No data written to", "WARNING")

        caplog.clear()
        assert load_file(temp_text_path) is None
        assert_log_contains(caplog, "No data loaded from", "WARNING")