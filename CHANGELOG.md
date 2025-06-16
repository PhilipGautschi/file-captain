# Changelog
All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [1.0.2] - 2025-06-16

### Added
- Docstrings for all functions

### Changed
- Author field in pyproject.toml

### Fixed
- All textbased file operations are now forced to encoded in UTF-8

## [1.0.1] - 2025-06-14

### Fixed
- Corrected authorship for PyPi

## [1.0.0] - 2025-06-14
### Added
- `load_file()` function for reading files
- `save_file()` function for writing files
- Support for JSON files (.json)
- Support for pickle files (.pickle, .pkl)
- Support for TOML files (.json) 
- Support for text files (.txt and others)
- Support for YAML files (.yaml, .yml)
- Automatic format detection based on file path extension 
- Overwrite protection feature to prevent accidental file overwrites
- Error handling and logging for file operations
- Type hints support with `py.typed` marker
- Automatic directory creation for nested file paths
- Cross-platform path handling using `pathlib.Path`
- Test suite with pytest
- Documentation with usage examples

### Security
- Added explicit security warnings about pickle file usage in documentation
