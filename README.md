# file-utils

A lightweight Python utility library for reading and writing files with support for JSON, pickle and text formats.

## Features

- Simple API for file operations
- Automatic format detection based on file extensions
- Built-in error handling and logging
- Support for JSON, pickle and plain text files
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
cd file-utils
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

## ⚠️ Security Considerations

### Pickle Files - Security Warning

**CRITICAL**: Loading pickle files from untrusted sources is a **serious security risk**.

```python
# 🚨 DANGEROUS - Never do this with untrusted files
data = load_file("untrusted_file.pickle") # Could execute malicious code!
# ✅ SAFE - Only load pickle files you created or from trusted sources
data = load_file("my_own_data.pickle") # Safe if you created this file
```
**Why pickle is dangerous:**
- Pickle can execute arbitrary Python code during deserialization
- Malicious pickle files can compromise your system
- There's no way to safely validate pickle content without loading it

**Recommendations:**
- **Never load pickle files from untrusted sources** (internet, email, external systems)
- **Use JSON format** for data exchange when possible
- **Validate file sources** - only load pickles you created or from verified trusted sources
- **Consider alternatives** like JSON, YAML, or protocol buffers for data sharing

## Quick Start

```python
from file_utils import load_file, save_file

# Save data to a file
text_data = "Hello, world and some unicode characters! 🧠 字 Ω"
save_file("text.txt", text_data)

serializable_object = {"key1": "text-key", 2: "number-key"}
save_file("object.pickle", serializable_object)

dict_data = {"host": "localhost", "port": 8080}
save_file("dict.json", dict_data)

# Save with overwrite protection disabled
dict_data_new = {"host": "localhost", "port": 8080, "user": "admin"}
save_file("dict.json", dict_data_new, overwrite_protection=False)


# Load data from a file
loaded_text = load_file("text.txt")
print(loaded_text)
loaded_dict = load_file("dict.json")
print(loaded_dict)
object = load_file("object.pickle")
print(object)
```

## API Reference

### `load_file(path_string)`

Returns data from a JSON, plain text, or pickle file.

**Parameters:**
- `path_string` (str | Path): Path to the file (absolute or relative)

**Returns:**
- `JSONType`: Parsed JSON data for .json files
- `Any`: Deserialized object for .pickle or .pkl files 
- `str`: Raw text content for other file types
- `None`: If an error occurs during reading

### `save_file(path_string, data, overwrite_protection=True)`

Writes data to a JSON, plain text, or a pickle file.

**Parameters:**
- `path_string` (str | Path): Path to the file (absolute or relative)
- `data` (JSONType | str | Any): Data to be written
- `overwrite_protection` (bool): Prevents overwriting existing files (default: True)

**Returns:**
- `bool`: True if successful, False otherwise

## Supported File Types

- **JSON files** (.json): Automatically parsed and formatted with 4-space indentation
- **Pickle files** (.pickle or .pkl): Can handle all serializable objects.
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

Before a pull request make sure the following tests are succesfull.

Run tests:
```bash
pytest --cov
```

Run isort:
```bash
isort .
```

Run black:
```bash
black .
```

Run mypy:
```bash
mypy .
```

## License

MIT License - Copyright (c) 2025 Philip Gautschi, Nicolas Brehm

See [LICENSE](LICENSE) file for full license text.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Support

For issues or questions, please contact the maintainer or create an issue in the repository.