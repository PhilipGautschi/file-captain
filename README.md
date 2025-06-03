# file-utils

A lightweight Python utility library for reading and writing files with support for JSON and text formats.

## Features

- Simple API for file operations
- Automatic format detection based on file extensions
- Built-in error handling and logging
- Support for JSON and plain text files
- Overwrite protection for safe file operations
- Type hints for better development experience

## Installation

### For End Users

Install directly from the repository:

```bash
pip install git+https://github.com/philipgautschi/file-utils.git
```

### For Development

1. Clone the repository:
```bash
git clone https://github.com/philipgautschi/file-utils.git
cd file
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install in development mode with optional dependencies:
```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from file_utils import load_file, save_file

# Load data from a file
data = load_file("config.json")
text = load_file("document.txt")

# Save data to a file
my_config = {"host": "localhost", "port": 8080}
save_file("config.json", my_config)

# Save with overwrite protection disabled
save_file("backup.json", my_config, overwrite_protection=False)
```

## API Reference

### `load_file(path_string)`

Loads data from a JSON or text file.

**Parameters:**
- `path_string` (str | Path): Path to the file (absolute or relative)

**Returns:**
- `dict`: Parsed JSON data for .json files
- `str`: Raw text content for other file types
- `None`: If an error occurs during reading

### `save_file(path_string, data, overwrite_protection=True)`

Saves data to a JSON or text file.

**Parameters:**
- `path_string` (str | Path): Path to the file (absolute or relative)
- `data` (dict | str): Data to be written
- `overwrite_protection` (bool): Prevents overwriting existing files (default: True)

**Returns:**
- `bool`: True if successful, False otherwise

## Supported File Types

- **JSON files** (.json): Automatically parsed and formatted with 4-space indentation
- **Text files** (.txt and others): Handled as plain text with UTF-8 encoding

## Requirements

- Python 3.12 or higher
- No external dependencies for core functionality

## Development Dependencies

The following packages are available for development:

- pytest (testing)
- pytest-cov (coverage)
- black (code formatting)
- ruff (linting)
- mypy (type checking)
- isort (import sorting)
- bandit (security)
- flake8 (style guide)

Run tests:
```bash
pytest
```

## License

Proprietary - Copyright (c) 2025 Philip Gautschi. All rights reserved.

## Contributing

This is a private library for collaboration among friends and team members. Please coordinate with the maintainer before making changes.

## Support

For issues or questions, please contact the maintainer or create an issue in the repository.