# Contributing to Skill Doctor

Thank you for your interest in contributing to Skill Doctor! This document provides guidelines for contributing to the project.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/tcarac/skill-doctor.git
   cd skill-doctor
   ```

2. **Install dependencies with uv**
   ```bash
   uv sync --all-extras
   ```

3. **Activate the virtual environment**
   ```bash
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate     # On Windows
   ```

## Development Workflow

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run specific test file
uv run pytest tests/test_validator.py

# Run with verbose output
uv run pytest -v
```

### Code Quality

```bash
# Format code with Black
uv run black src tests

# Sort imports with isort
uv run isort src tests

# Lint with Pylint
uv run pylint src

# Type check with mypy
uv run mypy src

# Run all quality checks
uv run black src tests && uv run isort src tests && uv run pylint src && uv run mypy src
```

### Testing the Action Locally

You can test the validator directly:

```bash
# Validate a single skill
uv run python -m skill_doctor.main --path=path/to/skill --mode=single

# Validate multiple skills
uv run python -m skill_doctor.main --path="skills/*" --mode=multiple
```

## Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, documented code
   - Add tests for new functionality
   - Update documentation as needed

3. **Ensure tests pass**
   ```bash
   uv run pytest
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**
   - Provide a clear description of the changes
   - Reference any related issues
   - Ensure CI checks pass

## Coding Standards

### Python Style

- Follow PEP 8 guidelines
- Use type hints for function signatures
- Maximum line length: 100 characters
- Use Black for formatting

### Documentation

- Add docstrings to all public functions and classes
- Use Google-style docstrings
- Include examples where helpful

### Testing

- Write tests for all new functionality
- Aim for >80% code coverage
- Use descriptive test names
- Include both positive and negative test cases

## Project Structure

```
skill-doctor/
├── src/skill_doctor/       # Main package
│   ├── __init__.py         # Package initialization
│   ├── main.py             # CLI entry point
│   ├── validator.py        # Core validation logic
│   ├── models.py           # Data models
│   ├── skill_finder.py     # Skill discovery
│   └── github_integration.py  # GitHub API integration
├── tests/                  # Test suite
│   ├── fixtures/           # Test data
│   └── test_*.py           # Test files
├── .github/workflows/      # CI/CD workflows
└── examples/               # Example workflows
```

## Reporting Issues

When reporting issues, please include:

1. **Description**: Clear description of the problem
2. **Steps to reproduce**: How to reproduce the issue
3. **Expected behavior**: What you expected to happen
4. **Actual behavior**: What actually happened
5. **Environment**: OS, Python version, etc.
6. **Example**: Sample SKILL.md file if applicable

## Feature Requests

We welcome feature requests! Please:

1. Check if the feature has already been requested
2. Provide a clear use case
3. Describe the expected behavior
4. Consider if it aligns with the Agent Skills specification

## Questions?

If you have questions:

- Open a GitHub issue with the "question" label
- Check existing documentation and issues first

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
