# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in Skill Doctor, please report it responsibly:

### How to Report

1. **Do not** open a public GitHub issue for security vulnerabilities
2. Email security concerns to: tomascaraccia@gmail.com
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Acknowledgment**: Within 48 hours of your report
- **Updates**: Regular updates on the progress of fixing the issue
- **Timeline**: We aim to address critical vulnerabilities within 7 days
- **Credit**: Security researchers will be credited (unless you prefer to remain anonymous)

## Security Best Practices

When using Skill Doctor in your workflows:

### GitHub Token Permissions

The action requires minimal permissions:
- `contents: read` - To read repository files
- `pull-requests: write` - To post comments on PRs (optional)
- `checks: write` - To create annotations (optional)

Example workflow with minimal permissions:

```yaml
name: Validate Skills

on: [pull_request]

permissions:
  contents: read
  pull-requests: write
  checks: write

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: tcarac/skill-doctor@v1
        with:
          path: 'skills/*'
          mode: 'multiple'
```

### Dependency Security

- All dependencies are regularly updated via Dependabot
- Security vulnerabilities are addressed promptly
- We use `uv` for reproducible dependency management

### Container Security

- Docker images are built from official Python slim images
- Only necessary packages are installed
- Images are scanned for vulnerabilities

## Known Security Considerations

### Git Operations

The action uses git commands when in "changed" mode:
- Only reads git diff output
- Does not modify repository history
- Runs in isolated GitHub Actions environment

### File Access

The action:
- Only reads SKILL.md files in specified directories
- Does not execute user code from skills
- Does not write files (except optional JSON output)

### GitHub API

When posting PR comments:
- Uses provided `GITHUB_TOKEN`
- Only creates/updates comments
- Does not access sensitive repository data

## Security Updates

Security updates are released as soon as possible after a vulnerability is confirmed. Check the [CHANGELOG](CHANGELOG.md) for security-related updates.

## Disclosure Policy

- Security issues are disclosed after a fix is available
- Critical vulnerabilities are disclosed within 90 days maximum
- Details are published in GitHub Security Advisories
