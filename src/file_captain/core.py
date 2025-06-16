"""File utilities for loading and saving data with automatic format detection.

This module provides simple functions to load and save data to files and
automatically detects file format based on path extension. Supports both
string and Path objects for file paths, with built-in error handling and
optional overwrite protection.

Supported formats: JSON, pickle, TOML, plain text and YAML.

Functions:
    load_file: Load data from a file with automatic format detection
    save_file: Save data to a file with optional overwrite protection

Copyright (c) 2025 Philip Gautschi, Nicolas Brehm
SPDX-License-Identifier: MIT
"""

import json
import logging
import pickle
import tomllib
from collections.abc import Callable
from datetime import date, datetime, time
from pathlib import Path
from typing import Any

import tomli_w
import yaml

logger = logging.getLogger(__name__)

# fmt: off
JSONType = None | bool | int | float | str | list["JSONType"] | dict[str, "JSONType"]
TOMLValue = bool | int | float | str | date | time | datetime | list["TOMLValue"] | dict[str, "TOMLValue"]
TOMLType = dict[str, "TOMLValue"]
YAMLType = None | bool | int | float | str | date | time | datetime | list["YAMLType"] | dict[Any, "YAMLType"]
# fmt: on


def _read_json_from_file(path: Path) -> JSONType | None:
    """Read JSON data from a file and return it, or None on decode error."""
    with path.open("r", encoding="utf8") as infile:
        try:
            data: JSONType = json.load(infile)

        except (UnicodeDecodeError, json.JSONDecodeError) as err:
            logger.warning("Decoding error: %s", err)
            return None

        else:
            logger.debug("JSON Decoding successful")
            return data


def _write_json_to_file(path: Path, data: JSONType) -> None:
    """Write JSON data to a file."""
    with path.open("w", encoding="utf8") as outfile:
        json.dump(data, outfile, indent=4)

    return None


def _read_pickle_from_file(path: Path) -> Any | None:
    """Read and unpickle data from a file, or return None on decode error."""
    with path.open("rb") as infile:
        try:
            data = pickle.load(infile)

        except pickle.UnpicklingError as err:
            logger.warning("Decoding error: %s", err)
            return None

        else:
            logger.debug("Pickle decoding successful.")
            return data


def _write_pickle_to_file(path: Path, data: Any) -> None:
    """Write data to a file using pickle."""
    with path.open("wb") as outfile:
        pickle.dump(data, outfile)  # type: ignore[arg-type]

    return None


def _read_toml_from_file(path: Path) -> TOMLType | None:
    """Read TOML data from a file and return it, or None on decode error."""
    with path.open("rb") as infile:
        try:
            data = tomllib.load(infile)

        except (UnicodeDecodeError, tomllib.TOMLDecodeError) as err:
            logger.warning("Decoding error: %s", err)
            return None

        else:
            logger.debug("TOML decoding successful")
            return data


def _write_toml_to_file(path: Path, data: TOMLType) -> None:
    """Write TOML data to a file."""
    with path.open("wb") as outfile:
        tomli_w.dump(data, outfile)

    return None


def _read_text_from_file(path: Path) -> str | None:
    """Read text data from a file and return it, or None on decode error."""
    with path.open("r", encoding="utf8") as infile:
        try:
            data: str = infile.read()

        except UnicodeDecodeError as err:
            logger.warning("Decoding error: %s", err)
            return None

        else:
            logger.debug("Unicode decoding successful.")
            return data


def _write_text_to_file(path: Path, data: str) -> None:
    """Write text data to a file."""
    with path.open("w", encoding="utf8") as outfile:
        outfile.write(data)

    return None


def _read_yaml_from_file(path: Path) -> YAMLType | None:
    """Read YAML data from a file and return it, or None on decode error."""
    with path.open("r", encoding="utf8") as infile:
        try:
            data = yaml.safe_load(infile)

        except (UnicodeDecodeError, yaml.YAMLError) as err:
            logger.warning("Decoding error: %s", err)
            return None

        else:
            logger.debug("YAML decoding successful")
            return data


def _write_yaml_to_file(path: Path, data: YAMLType) -> None:
    """Write YAML data to a file."""
    with path.open("w", encoding="utf8") as outfile:
        yaml.dump(data, outfile, default_flow_style=False, indent=2)

    return None


_READERS: dict[str, Callable[[Path], Any]] = {
    ".json": _read_json_from_file,
    ".pickle": _read_pickle_from_file,
    ".pkl": _read_pickle_from_file,
    ".toml": _read_toml_from_file,
    ".txt": _read_text_from_file,
    ".yaml": _read_yaml_from_file,
    ".yml": _read_yaml_from_file,
}

_WRITERS: dict[str, Callable[[Path, Any], None]] = {
    ".json": _write_json_to_file,
    ".pickle": _write_pickle_to_file,
    ".pkl": _write_pickle_to_file,
    ".toml": _write_toml_to_file,
    ".txt": _write_text_to_file,
    ".yaml": _write_yaml_to_file,
    ".yml": _write_yaml_to_file,
}


def load_file(path_string: str | Path) -> Any:
    """Returns data from the file system. Autodetects format based on file extension.

    Args:
        path_string (str | Path): Path to the file (absolute or relative).

    Returns:
        JSONType: parsed JSON data for .json files.
        Any: Deserialized python object for .pickle/.pkl files.
        TOMLType: Parsed TOML data for .toml files.
        str: Raw string content for .txt files and unknown file extensions.
        YAMLType: Parsed YAML data for .yaml/.yml files.
        None: If an error occurs during reading, parsing.

    Examples:
        >>> config = load_file("path/to/config.json")
    """

    path = Path(path_string)
    suffix = path.suffix.lower()
    reader = _READERS.get(suffix, _read_text_from_file)

    try:
        data = reader(path)

    except OSError as err:
        logger.warning("No data loaded from %s: %s", path, err)
        return None

    else:
        if data is not None:
            logger.info("Data loaded from %s.", path)

        return data


def save_file(
    path_string: str | Path, data: Any, overwrite_protection: bool = True
) -> bool:
    """Writes data to the file system. Autodetects format based on file extension.

    Args:
        path_string (str | Path): Path to the file (absolute or relative).
        data (Any): Data to be written.
        overwrite_protection (bool, optional): If True, prevents overwriting existing
            files; defaults to True.

    Returns:
        bool: True if writing was successful, False, otherwise.

    Examples:
        >>> my_data = {"Host": "localhost", "Port": 3306, "Database": "mydb"}
        >>> save_file("path/to/config.json", my_data, overwrite_protection=False)
    """

    path = Path(path_string)
    suffix = path.suffix.lower()
    writer = _WRITERS.get(suffix, _write_text_to_file)

    try:
        if overwrite_protection and path.exists():
            logger.warning("File already exists. No data written to %s.", path)
            return False

        path.parent.mkdir(parents=True, exist_ok=True)
        writer(path, data)

    except OSError as err:
        logger.warning("No data written to %s: %s", path, err)
        return False

    else:
        logger.info("Data written to %s.", path)
        return True
