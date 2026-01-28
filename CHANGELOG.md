# Changelog

All notable changes to Skill Doctor will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-28

### Added

- Initial release of Skill Doctor
- Core validation logic following Agent Skills specification v1.0
- Support for validating single skills, multiple skills, and changed skills in PRs
- GitHub integration with PR comments and annotations
- Auto-fix suggestions for common validation errors
- Comprehensive validation checks:
  - Name format validation (lowercase, no consecutive hyphens, 1-64 chars)
  - Description validation (non-empty, max 1024 chars)
  - Directory name matching
  - Optional field validation (compatibility, license, metadata, allowed-tools)
  - Frontmatter structure validation
- Multiple validation modes:
  - `single` - Validate a single skill directory
  - `multiple` - Validate multiple skills using glob patterns
  - `changed` - Validate only changed skills in PR context
- GitHub Actions integration:
  - Configurable failure behavior
  - PR comment generation with detailed results
  - GitHub annotations for inline error display
  - JSON output for downstream processing
- Comprehensive test suite with >80% coverage
- Docker-based action for consistent execution
- Modern Python tooling with `uv` for dependency management

### Documentation

- Complete README with usage examples
- Contributing guidelines
- Security policy
- Apache 2.0 license
- API documentation via docstrings

[1.0.0]: https://github.com/tcarac/skill-doctor/releases/tag/v1.0.0
