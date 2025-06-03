# ──────────────────────────────────────────────────────────────────────────────────────
#  Author      : Philip Gautschi
#  Created     : 04 May 2025
#  Updated     : 03 June 2025 - Version 1.0.0
#  Description : read and write dictionaries and strings to and from a file_utils system.
#  Dependencies: only standard libraries
#  License     : Copyright (c) 2025 Philip Gautschi. All rights reserved.
# ──────────────────────────────────────────────────────────────────────────────────────

import json
import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any

from .JSONType import JSONType

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


READERS: dict[str, Callable[[Path], JSONType | str | None]] = {
    ".json": _read_json_from_file,
    ".txt": _read_text_from_file,
}

WRITERS: dict[str, Callable[[Path, Any], None]] = {
    ".json": _write_json_to_file,
    ".txt": _write_text_to_file,
}


def load_file(
    path_string: str | Path,
) -> JSONType | str | None:
    """Returns data from a JSON or plain text file_utils.

    Args:
        path_string (str | Path): Path to the file_utils (absolute or relative).

    Returns:
        dict[str, Any]: Parsed data if the file_utils type is JSON
        str:  Raw string content if the file_utils is a plain text.
        None: If an error occurs during reading or parsing.

    Examples:
        >>> my_data = load_file("path/to/file_utils.json")
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
    data: JSONType | str,
    overwrite_protection: bool = True,
) -> bool:
    """Writes data to a JSON or plain text file_utils.

    Args:
        data (JSONType | str): Data to be written (supports dict or str).
        path_string (str | Path): Path to the file_utils (absolute or relative).
        overwrite_protection (bool, optional): If True, prevents overwriting existing
            files; defaults to True.

    Returns:
        bool: True if writing was successful, False if the file_utils could not be written.

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
