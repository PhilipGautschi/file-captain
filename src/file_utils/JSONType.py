# ──────────────────────────────────────────────────────────────────────────────────────
#  File        : src/file_utils/JSONType.py
#  Author      : Philip Gautschi
#  Created     : 20 Mai 2025
#  Updated     : 03 May 2025 - Version 1.0.0
#  Description : provides a recursive defined JSONType
#  Dependencies: only standard libraries
#  License     : Copyright (c) 2025 Philip Gautschi. All rights reserved.
# ──────────────────────────────────────────────────────────────────────────────────────

type JSONType = None | bool | int | float | str | list[JSONType] | dict[str, JSONType]
