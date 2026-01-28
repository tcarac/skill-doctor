# Pre-commit Hooks

This project uses [pre-commit](https://pre-commit.com/) to run automated checks before each commit, ensuring code quality and consistency.

## Installation

Pre-commit hooks are automatically installed when you set up the development environment:

```bash
uv sync --all-extras
uv run pre-commit install
```

## What Gets Checked

### File Quality Checks

- ✅ **Trailing whitespace** - Removed automatically
- ✅ **End of file** - Ensures newline at end
- ✅ **Large files** - Prevents accidental commits (>500KB)
- ✅ **Case conflicts** - Detects case-sensitive filename issues
- ✅ **Merge conflicts** - Catches unresolved conflicts
- ✅ **Private keys** - Detects accidentally committed keys
- ✅ **Line endings** - Normalizes to LF

### Python Code Quality

- ✅ **Black** - Code formatting (line length: 100)
- ✅ **isort** - Import sorting
- ✅ **Ruff** - Fast Python linter and formatter
- ✅ **mypy** - Type checking
- ✅ **Bandit** - Security vulnerability scanning
- ✅ **Docstring checks** - Ensures docstrings come first
- ✅ **Debug statements** - Catches leftover debug code
- ✅ **Test naming** - Validates pytest naming conventions

### Configuration Files

- ✅ **YAML validation** - Syntax checking for all YAML files
- ✅ **TOML validation** - Syntax checking for pyproject.toml
- ✅ **JSON validation** - Syntax checking for JSON files
- ✅ **Markdown linting** - Style and formatting checks
- ✅ **Dockerfile linting** - Best practices with hadolint

### Security

- ✅ **Secret detection** - Catches accidentally committed secrets
- ✅ **Bandit** - Python security issues

### GitHub-Specific

- ✅ **Workflow validation** - GitHub Actions YAML validation
- ✅ **Dependabot validation** - Dependabot config validation

### Spell Checking

- ✅ **Codespell** - Catches common typos in code and docs

## Running Manually

### Run on All Files

```bash
uv run pre-commit run --all-files
```

### Run on Staged Files Only

```bash
uv run pre-commit run
```

### Run Specific Hook

```bash
uv run pre-commit run black --all-files
uv run pre-commit run mypy --all-files
```

### Skip Pre-commit Hooks (NOT RECOMMENDED)

```bash
git commit --no-verify -m "message"
```

## Auto-fixing

Many hooks automatically fix issues:

- **Black** - Reformats code
- **isort** - Reorders imports
- **Ruff** - Fixes many linting issues
- **Trailing whitespace** - Removes extra spaces
- **End of file** - Adds missing newlines
- **Markdownlint** - Fixes markdown formatting

After auto-fixes, you need to:

1. Review the changes
2. Stage the fixes: `git add .`
3. Commit again

## Updating Hooks

Pre-commit hooks are automatically updated weekly by the pre-commit.ci bot. To update manually:

```bash
uv run pre-commit autoupdate
```

## Configuration

### Main Configuration

All hooks are configured in `.pre-commit-config.yaml`

### Tool-Specific Configs

- **Black**: `pyproject.toml` → `[tool.black]`
- **isort**: `pyproject.toml` → `[tool.isort]`
- **Ruff**: `pyproject.toml` → `[tool.ruff]`
- **mypy**: `pyproject.toml` → `[tool.mypy]`
- **Bandit**: `pyproject.toml` → `[tool.bandit]`
- **Pytest**: `pyproject.toml` → `[tool.pytest.ini_options]`
- **Markdownlint**: `.markdownlint.yaml`
- **Yamllint**: Inline in `.pre-commit-config.yaml`

## Troubleshooting

### Hook Fails on Import Errors

If mypy fails on imports:

```bash
uv sync --all-extras  # Reinstall dependencies
```

### Slow First Run

The first run installs all hook environments (takes 2-3 minutes). Subsequent runs are fast.

### Clear Hook Cache

```bash
uv run pre-commit clean
uv run pre-commit install --install-hooks
```

### Skip Specific Files

Add to `.pre-commit-config.yaml`:

```yaml
- id: mypy
  exclude: ^tests/
```

## CI Integration

Pre-commit hooks also run in CI:

- `.github/workflows/ci.yml` runs equivalent checks
- Ensures consistency between local and CI environments

## Best Practices

1. **Run before committing** - Let pre-commit catch issues early
2. **Review auto-fixes** - Don't blindly accept all changes
3. **Keep hooks updated** - Accept pre-commit.ci bot updates
4. **Don't skip hooks** - Use `--no-verify` sparingly
5. **Add exceptions carefully** - Document why certain files are excluded

## Adding New Hooks

1. Add hook to `.pre-commit-config.yaml`
2. Test with `uv run pre-commit run <hook-id> --all-files`
3. Document in this file
4. Commit changes

Example:

```yaml
- repo: https://github.com/owner/repo
  rev: v1.0.0
  hooks:
    - id: hook-id
      args: ['--flag']
```

## Disabling a Hook

Temporarily disable a hook in `.pre-commit-config.yaml`:

```yaml
- id: mypy
  stages: [manual]  # Only runs with --hook-stage manual
```

Or remove it entirely (requires team approval).

## Resources

- [Pre-commit Documentation](https://pre-commit.com/)
- [Supported Hooks](https://pre-commit.com/hooks.html)
- [Pre-commit CI](https://pre-commit.ci/)
