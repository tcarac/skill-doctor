# Repository Protection & Configuration

This document details all the security protections, policies, and configurations applied to the Skill Doctor repository.

## 🔐 Security Features

### Secret Scanning

- **Status**: ✅ Enabled
- **Push Protection**: ✅ Enabled
- Automatically scans for accidentally committed secrets
- Blocks pushes containing detected secrets
- Covers 200+ secret patterns from major providers

### Dependabot

- **Security Updates**: ✅ Enabled
- **Version Updates**: ✅ Enabled (via dependabot.yml)
- Automated pull requests for:
  - GitHub Actions updates (weekly)
  - Docker base image updates (weekly)
  - Python dependency updates (weekly)
- Auto-merge enabled for patch updates

### Vulnerability Alerts

- **Status**: ✅ Enabled
- Real-time notifications for known vulnerabilities in dependencies
- Integration with GitHub Advisory Database

### CodeQL Analysis

- **Status**: ✅ Enabled
- **Schedule**: Weekly + on PRs
- **Language**: Python
- **Queries**: Security + Quality
- Automated security scanning for:
  - SQL injection
  - Cross-site scripting
  - Code injection
  - Path traversal
  - And 100+ other vulnerability patterns

## 🛡️ Branch Protection Rules

### Main Branch (`main`)

#### Required Status Checks

- **Strict Status Checks**: ✅ Enabled (branch must be up to date before merging)
- **Required Checks**:
  - ✅ `test` - Python test suite across multiple versions
  - ✅ `lint` - Code quality checks (Black, isort, Pylint, mypy)
  - ✅ `test-action` - Self-test of the GitHub Action

#### Pull Request Reviews

- **Dismiss Stale Reviews**: ✅ Enabled
- **Require Code Owner Reviews**: ✅ Enabled (via CODEOWNERS)
- **Required Approving Reviews**: 0 (for single maintainer)
- **Last Push Approval**: ❌ Disabled

#### Restrictions

- **Force Pushes**: ❌ Blocked
- **Deletions**: ❌ Blocked
- **Required Linear History**: ✅ Enabled (no merge commits)
- **Required Conversation Resolution**: ✅ Enabled (all threads must be resolved)
- **Admin Enforcement**: ❌ Disabled (allows bypassing for initial setup)

## 📋 Repository Settings

### General

- **Visibility**: Public
- **Features**:
  - ✅ Issues enabled
  - ✅ Discussions enabled
  - ❌ Wiki disabled
  - ❌ Projects disabled (using Issues instead)
- **Default Branch**: `main`

### Merge Strategies

- ✅ **Squash Merging**: Enabled (preferred)
- ❌ **Merge Commits**: Disabled
- ✅ **Rebase Merging**: Enabled
- ✅ **Auto-Merge**: Enabled
- ✅ **Delete Branch on Merge**: Enabled

### Topics

Repository is tagged with:

- `github-actions`
- `agent-skills`
- `validation`
- `python`
- `cli`
- `docker`
- `ai-agents`
- `developer-tools`
- `code-quality`

## 🌍 Deployment Environments

### Production

- **Branch Policy**: Protected branches only
- **Reviewers**: None (automated deployments)
- **Wait Timer**: 0 minutes
- **Used For**: Production releases (v1.0.0, v2.0.0, etc.)

### Staging

- **Branch Policy**: Any branch
- **Reviewers**: None
- **Wait Timer**: 0 minutes
- **Used For**: Pre-release testing

## 🏷️ Issue Labels

### Type Labels

- `bug` - Something isn't working (red)
- `enhancement` - New feature or request (light blue)
- `documentation` - Improvements to documentation (blue)
- `question` - Further information requested (purple)

### Status Labels

- `needs-triage` - Needs initial review (yellow)
- `in-progress` - Work in progress (green)
- `blocked` - Blocked by dependencies (red)
- `wontfix` - Will not be worked on (white)
- `duplicate` - Already exists (gray)

### Priority Labels

- `priority:high` - High priority (red)
- `priority:medium` - Medium priority (yellow)
- `priority:low` - Low priority (green)

### Area Labels

- `area:validation` - Validation logic
- `area:github-integration` - GitHub API integration
- `area:ci-cd` - CI/CD workflows
- `area:docs` - Documentation
- `area:tests` - Tests

### Special Labels

- `good-first-issue` - Good for newcomers (purple)
- `help-wanted` - Extra attention needed (green)
- `security` - Security related (red)
- `dependencies` - Dependency updates (blue)

## 📝 Templates

### Issue Templates

1. **Bug Report** (`bug_report.yml`)
   - Description, reproduction steps, expected/actual behavior
   - Environment details (version, runner)
   - Workflow configuration
   - Logs and context

2. **Feature Request** (`feature_request.yml`)
   - Problem statement
   - Proposed solution
   - Alternatives considered
   - Specification alignment
   - Contribution willingness

3. **Issue Config** (`config.yml`)
   - Links to Agent Skills specification
   - Discussion forum
   - Security advisory reporting

### Pull Request Template

- Change type selection
- Related issues linking
- Changes description
- Testing checklist
- Code quality checklist
- Screenshots section

## 🔄 CI/CD Workflows

### CI (`ci.yml`)

- **Triggers**: PR to main, push to main
- **Jobs**:
  - Test on Python 3.11 & 3.12
  - Lint and format checks
  - Type checking
  - Self-test the action
  - Coverage reporting (Codecov)

### CodeQL (`codeql.yml`)

- **Triggers**: PR, push to main, weekly schedule
- **Jobs**:
  - Security scanning
  - Quality analysis
  - Automated security advisories

### Release (`release.yml`)

- **Triggers**: Tag push (v*)
- **Jobs**:
  - Generate release notes from commits
  - Create GitHub release
  - Update major version tag (v1, v2)

## 👥 Code Ownership

Defined in `.github/CODEOWNERS`:

- All files: @tcarac
- Source code: @tcarac
- Tests: @tcarac
- CI/CD: @tcarac
- Documentation: @tcarac

Code owner reviews are required for all changes.

## 📊 Monitoring & Maintenance

### Automated Updates

- **Dependabot**: Weekly checks for all ecosystems
- **CodeQL**: Weekly security scans
- **Label Automation**: Via GitHub Actions

### Manual Reviews

- Security advisories reviewed within 48 hours
- Critical vulnerabilities patched within 7 days
- Feature requests triaged weekly

## 🔧 Maintenance Commands

### Update Branch Protection

```bash
gh api --method PUT "/repos/tcarac/skill-doctor/branches/main/protection" \
  --input protection.json
```

### Create New Label

```bash
gh api --method POST "/repos/tcarac/skill-doctor/labels" \
  -f name="label-name" \
  -f color="ffffff" \
  -f description="Label description"
```

### Create New Environment

```bash
gh api --method PUT "/repos/tcarac/skill-doctor/environments/env-name" \
  --input environment.json
```

## 📚 Additional Resources

- [Branch Protection API](https://docs.github.com/en/rest/branches/branch-protection)
- [GitHub Security Features](https://docs.github.com/en/code-security)
- [Dependabot Configuration](https://docs.github.com/en/code-security/dependabot)
- [CodeQL Documentation](https://codeql.github.com/)

---

Last Updated: 2026-01-28
