"""Type definitions for JSON-compatible data structures.

This module defines type aliases for JSON data types to improve type safety
and code readability when working with JSON serializable data.

The JSONType union covers all valid JSON data types including primitives,
arrays, and objects as defined by the JSON specification.

Copyright (c) 2025 Philip Gautschi
SPDX-License-Identifier: MIT
"""

type JSONType = None | bool | int | float | str | list[JSONType] | dict[str, JSONType]
