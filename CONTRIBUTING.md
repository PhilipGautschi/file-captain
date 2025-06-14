# Contributing to file-captain

Thank you for considering contributing to file-captain! We welcome contributions from everyone.

## Development Setup

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/philipgautschi/file-captain.git
cd file-captain
```
3. Create a virtual environment:
```bash
python -m venv .venv 
source .venv/bin/activate # On Windows: .venv\Scripts\activate
```
4. Install in development mode:
```bash
pip install -e ".[dev]"
```
## Code Style

We use several tools to maintain code quality:

```bash
# Format code
black src/ tests/
isort src/ tests/

# Type checking
mypy src/

# Run tests
pytest --cov
```
## Pull Request Process
1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass and code is formatted
5. Update documentation if needed
6. Commit with clear, descriptive messages
7. Push to your fork and create a pull request

## Reporting Issues
Please use the [GitHub issue tracker](https://github.com/philipgautschi/file-captain/issues) to report bugs or request features.
Include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages (if any)

## Code of Conduct
Be respectful and constructive in all interactions. We aim to create a welcoming environment for all contributors.
