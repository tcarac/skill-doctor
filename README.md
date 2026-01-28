# 🩺 Skill Doctor

> A GitHub Action to validate Agent Skills against the official specification with helpful diagnostics

[![CI](https://github.com/tcarac/skill-doctor/workflows/CI/badge.svg)](https://github.com/tcarac/skill-doctor/actions)
[![CodeQL](https://github.com/tcarac/skill-doctor/workflows/CodeQL/badge.svg)](https://github.com/tcarac/skill-doctor/actions)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

Skill Doctor validates [Agent Skills](https://agentskills.io) to ensure they follow the official specification. It provides clear error messages, auto-fix suggestions, and seamless GitHub integration with PR comments and annotations.

## ✨ Features

- 🔍 **Comprehensive Validation** - Validates all aspects of the Agent Skills specification
- 💡 **Auto-Fix Suggestions** - Provides actionable suggestions for fixing common errors
- 💬 **PR Comments** - Posts detailed validation results as PR comments
- 📝 **Inline Annotations** - Shows errors directly in the Files Changed tab
- 🎯 **Multiple Modes** - Validate single skills, multiple skills, or only changed files
- ⚡ **Fast** - Built with modern Python tooling (uv) for quick execution
- 🔒 **Secure** - Minimal permissions required, runs in isolated containers

## 🚀 Quick Start

Add this to your `.github/workflows/validate-skills.yml`:

```yaml
name: Validate Skills

on:
  pull_request:
    branches:
      - main

permissions:
  contents: read
  pull-requests: write
  checks: write

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate Skills
        uses: tcarac/skill-doctor@v1
        with:
          path: 'skills/*'
          mode: 'multiple'
```

## 📋 Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `path` | Path to skill directory or glob pattern (e.g., `skills/*`) | No | `.` |
| `mode` | Validation mode: `single`, `multiple`, or `changed` | No | `single` |
| `fail-on-error` | Whether to fail the workflow on validation errors | No | `true` |
| `comment-on-pr` | Post validation results as PR comment | No | `true` |
| `create-annotations` | Create GitHub annotations for errors | No | `true` |
| `auto-fix-suggestions` | Include auto-fix suggestions in output | No | `true` |
| `output-json` | Output results as JSON artifact | No | `false` |
| `github-token` | GitHub token for API access | No | `${{ github.token }}` |

## 📤 Outputs

| Output | Description |
|--------|-------------|
| `validation-status` | Overall validation status: `passed` or `failed` |
| `skills-validated` | Number of skills validated |
| `errors-found` | Total number of errors found |
| `json-results` | Path to JSON results file (if `output-json` is enabled) |

## 📖 Usage Examples

### Validate Multiple Skills

```yaml
- uses: tcarac/skill-doctor@v1
  with:
    path: 'skills/*'
    mode: 'multiple'
    fail-on-error: true
```

### Validate Only Changed Skills (Optimized for Large Repos)

```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0  # Required for git diff

- uses: tcarac/skill-doctor@v1
  with:
    mode: 'changed'
```

### Warning Mode (Don't Fail Workflow)

```yaml
- uses: tcarac/skill-doctor@v1
  with:
    path: 'skills/*'
    mode: 'multiple'
    fail-on-error: false
```

### Single Skill Validation

```yaml
- uses: tcarac/skill-doctor@v1
  with:
    path: 'skills/my-skill'
    mode: 'single'
```

### Export Results as JSON

```yaml
- uses: tcarac/skill-doctor@v1
  id: validate
  with:
    path: 'skills/*'
    mode: 'multiple'
    output-json: true

- name: Upload Results
  uses: actions/upload-artifact@v4
  with:
    name: validation-results
    path: ${{ steps.validate.outputs.json-results }}
```

## 🧪 Testing

### Prerequisites

- Docker installed and running
- Python 3.11+ with uv
- (Optional) [Act](https://github.com/nektos/act) for local workflow testing

### Quick Test

Test the action quickly with the test scripts:

```bash
# Test with Python directly (fastest)
./scripts/test-action-local.sh

# Test Docker build and run
./scripts/test-docker-local.sh

# Or use make
make test
```

### Running All Tests

```bash
# Run all test suites
make test-all

# Or individually:
make test         # Python unit tests
make test-docker  # Docker integration tests
make test-act     # GitHub Actions locally (requires Act)
```

### Testing Your Changes

Before submitting a PR, ensure all tests pass:

1. **Run unit tests**: `make test`
2. **Test Docker build**: `make test-docker`
3. **Test the action locally** (optional): `make test-act`
4. **Run linters**: `make lint`

### Local Workflow Testing with Act

[Act](https://github.com/nektos/act) lets you run GitHub Actions workflows locally without pushing:

```bash
# Install Act
brew install act  # macOS
# or follow: https://github.com/nektos/act#installation

# Run the action test workflow
./scripts/test-with-act.sh test-action

# Run all CI jobs
act -j test
act -j lint
act -j test-action
```

### Troubleshooting Tests

#### Docker build fails

```bash
# Clean Docker build cache
docker builder prune -f

# Rebuild without cache
docker build --no-cache -t skill-doctor:test .
```

#### Act fails with permission errors

```bash
# Run with sudo (Linux)
sudo act -j test-action

# Or add your user to docker group
sudo usermod -aG docker $USER
```

#### Tests pass locally but fail in CI

```bash
# Run with same environment as CI using Act
act -j test-action --container-architecture linux/amd64
```

## 🎯 Validation Checks

Skill Doctor validates all aspects of the [Agent Skills specification](https://agentskills.io/specification):

### Required Fields

- ✅ `name` - Must be lowercase, 1-64 chars, no consecutive hyphens
- ✅ `description` - Must be non-empty, max 1024 chars

### Optional Fields

- ✅ `license` - License information
- ✅ `compatibility` - Environment requirements (max 500 chars)
- ✅ `metadata` - Custom key-value pairs
- ✅ `allowed-tools` - Pre-approved tool list (experimental)

### File Structure

- ✅ SKILL.md must exist (uppercase or lowercase)
- ✅ Valid YAML frontmatter format
- ✅ Directory name must match skill name
- ✅ No unexpected fields in frontmatter

## 💬 PR Comment Example

When validation fails, Skill Doctor posts a detailed comment:

```markdown
## ❌ Agent Skills Validation Failed

### Summary
- Total skills validated: **3**
- ❌ Failed: **1**
- Total errors: **2**

---

### ❌ `my-skill`
**Location:** `skills/my-skill/SKILL.md`

**Errors:**
1. **Line 2:** Skill name 'My-Skill' must be lowercase
   - 💡 **Suggestion:** Change to 'my-skill'
2. **Line 3:** Description exceeds 1024 character limit (1250 chars)
   - 💡 **Suggestion:** Trim description to 1024 characters or less
```

## 🔧 Local Development

### Setup

```bash
# Clone the repository
git clone https://github.com/tcarac/skill-doctor.git
cd skill-doctor

# Install dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Run locally
uv run python -m skill_doctor.main --path=path/to/skill --mode=single
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run specific test
uv run pytest tests/test_validator.py -v
```

### Code Quality

```bash
# Format code
uv run black src tests

# Sort imports
uv run isort src tests

# Lint
uv run pylint src

# Type check
uv run mypy src
```

## 📚 More Examples

Check out the [`examples/workflows/`](examples/workflows/) directory for more usage examples:

- [Basic Validation](examples/workflows/basic-validation.yml)
- [Changed Files Only](examples/workflows/pr-changed-only.yml)
- [Warning Mode](examples/workflows/warning-only.yml)

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 🔒 Security

For security concerns, please see [SECURITY.md](SECURITY.md).

## 📄 License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Built for the [Agent Skills](https://agentskills.io) specification
- Inspired by the skills-ref reference implementation
- Powered by [uv](https://docs.astral.sh/uv/) for fast Python tooling

## 📞 Support

- 📖 [Agent Skills Specification](https://agentskills.io/specification)
- 🐛 [Report Issues](https://github.com/tcarac/skill-doctor/issues)
- 💡 [Request Features](https://github.com/tcarac/skill-doctor/issues/new)

---

Made with ❤️ by [Tomas Caraccia](https://github.com/tcarac)
