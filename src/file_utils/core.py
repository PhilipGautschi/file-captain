"""File utilities for loading and saving data with automatic format detection.

This module provides simple functions to load and save data to files,
automatically detecting JSON vs text format based on file extension.
Supports both string and Path objects for file paths, with built-in
error handling and optional overwrite protection.

Functions:
    load_file: Load data from a file (JSON or text) with automatic format detection
    save_file: Save data to a file with optional overwrite protection

Copyright (c) 2025 Philip Gautschi, Nicolas Brehm
SPDX-License-Identifier: MIT
"""

import json
import logging
import pickle
from collections.abc import Callable
from pathlib import Path
from typing import Any

type JSONType = None | bool | int | float | str | list[JSONType] | dict[str, JSONType]

logger = logging.getLogger(__name__)


def _read_json_from_file(path: Path) -> JSONType | None:
    with path.open("r") as infile:
        try:
            data: JSONType = json.load(infile)

        except (UnicodeDecodeError, json.JSONDecodeError) as err:
            logger.warning("Decoding error: %s", err)
            return None

        else:
            logger.debug("JSON decoding successful")
            return data


def _write_json_to_file(path: Path, data: JSONType) -> None:
    with path.open("w") as outfile:
        json.dump(data, outfile, indent=4)

    return None


def _read_text_from_file(path: Path) -> str | None:
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
    with path.open("w", encoding="utf8") as outfile:
        outfile.write(data)

    return None


def _read_pickle_from_file(path: Path) -> Any | None:
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
    with path.open("wb") as outfile:
        pickle.dump(data, outfile)  # type: ignore[arg-type]

    return None


READERS: dict[str, Callable[[Path], JSONType | str | Any | None]] = {
    ".json": _read_json_from_file,
    ".txt": _read_text_from_file,
    ".pickle": _read_pickle_from_file,
    ".pkl": _read_pickle_from_file,
}

WRITERS: dict[str, Callable[[Path, Any], None]] = {
    ".json": _write_json_to_file,
    ".txt": _write_text_to_file,
    ".pickle": _write_pickle_to_file,
    ".pkl": _write_pickle_to_file,
}


def load_file(
    path_string: str | Path,
) -> JSONType | str | Any | None:
    """Returns data from a JSON, plain text, or pickle file.

    Args:
        path_string (str | Path): Path to the file (absolute or relative).

    Returns:
        JSONType: JSON data (dict, list, str, int, float, bool, or None) for .json files.
        str: Raw string content for .txt files and unknown file extensions.
        Any: Deserialized Python object for .pickle/.pkl files (could be any type).
        None: If an error occurs during reading, parsing, or if the file doesn't exist.

    Examples:
        >>> config = load_file("path/to/config.json")
    """

    path = Path(path_string)
    suffix = path.suffix.lower()
    reader = READERS.get(suffix, _read_text_from_file)

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
    path_string: str | Path,
    data: JSONType | str | Any,
    overwrite_protection: bool = True,
) -> bool:
    """Writes data to a JSON, plain text, or a pickle file.

    Args:
        path_string (str | Path): Path to the file (absolute or relative).
        data (JSONType | str | Any): Data to be written.
        overwrite_protection (bool, optional): If True, prevents overwriting existing
            files; defaults to True.

    Returns:
        bool: True if writing was successful, False if the file could not be written.

    Examples:
        >>> my_data = {"Host": "localhost", "Port": 3306, "Database": "mydb"}
        >>> save_file("path/to/file_utils.json", my_data, overwrite_protection=False)
    """

    path = Path(path_string)
    suffix = path.suffix.lower()
    writer = WRITERS.get(suffix, _write_text_to_file)

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
