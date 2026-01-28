"""Tests for the validator module."""

from pathlib import Path

import pytest

from skill_doctor.validator import find_skill_md, parse_frontmatter, validate_skill


@pytest.fixture
def valid_skill_path():
    """Path to valid test skill."""
    return Path(__file__).parent / "fixtures" / "valid-skill"


@pytest.fixture
def invalid_skill_path():
    """Path to invalid test skill."""
    return Path(__file__).parent / "fixtures" / "invalid-skill"


def test_find_skill_md_uppercase(valid_skill_path):
    """Test finding SKILL.md (uppercase)."""
    skill_md = find_skill_md(valid_skill_path)
    assert skill_md is not None
    assert skill_md.name == "SKILL.md"
    assert skill_md.exists()


def test_find_skill_md_missing(tmp_path):
    """Test finding SKILL.md when it doesn't exist."""
    skill_md = find_skill_md(tmp_path)
    assert skill_md is None


def test_parse_frontmatter_valid():
    """Test parsing valid frontmatter."""
    content = """---
name: test-skill
description: A test skill
---

# Body content
"""
    metadata, body = parse_frontmatter(content)
    assert metadata["name"] == "test-skill"
    assert metadata["description"] == "A test skill"
    assert body.strip() == "# Body content"


def test_parse_frontmatter_missing():
    """Test parsing content without frontmatter."""
    content = "# No frontmatter here"
    with pytest.raises(ValueError, match="must start with YAML frontmatter"):
        parse_frontmatter(content)


def test_parse_frontmatter_not_closed():
    """Test parsing frontmatter that isn't closed."""
    content = """---
name: test-skill
"""
    with pytest.raises(ValueError, match="not properly closed"):
        parse_frontmatter(content)


def test_validate_valid_skill(valid_skill_path):
    """Test validating a valid skill."""
    result = validate_skill(valid_skill_path)
    assert result.is_valid
    assert result.skill_name == "valid-skill"
    assert len(result.errors or []) == 0


def test_validate_invalid_skill(invalid_skill_path):
    """Test validating an invalid skill."""
    result = validate_skill(invalid_skill_path)
    assert not result.is_valid
    assert len(result.errors or []) > 0

    # Check for specific errors
    error_messages = [e.message for e in (result.errors or [])]
    assert any("must be lowercase" in msg for msg in error_messages)


def test_validate_nonexistent_path(tmp_path):
    """Test validating a path that doesn't exist."""
    nonexistent = tmp_path / "nonexistent"
    result = validate_skill(nonexistent)
    assert not result.is_valid
    assert len(result.errors or []) > 0
    assert any("does not exist" in e.message for e in (result.errors or []))


def test_validate_not_directory(tmp_path):
    """Test validating a path that is not a directory."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("test")
    result = validate_skill(file_path)
    assert not result.is_valid
    assert any("Not a directory" in e.message for e in (result.errors or []))


def test_validate_missing_skill_md(tmp_path):
    """Test validating a directory without SKILL.md."""
    result = validate_skill(tmp_path)
    assert not result.is_valid
    assert any("Missing required file" in e.message for e in (result.errors or []))


def test_validate_missing_name(tmp_path):
    """Test skill missing required 'name' field."""
    skill_dir = tmp_path / "test-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("""---
description: A skill without a name
---
Body content
""")
    result = validate_skill(skill_dir)
    assert not result.is_valid
    assert any(
        "Missing required field" in e.message and "name" in e.message for e in (result.errors or [])
    )


def test_validate_missing_description(tmp_path):
    """Test skill missing required 'description' field."""
    skill_dir = tmp_path / "test-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("""---
name: test-skill
---
Body content
""")
    result = validate_skill(skill_dir)
    assert not result.is_valid
    assert any(
        "Missing required field" in e.message and "description" in e.message
        for e in (result.errors or [])
    )


def test_validate_name_too_long(tmp_path):
    """Test skill name exceeding maximum length."""
    long_name = "x" * 65
    skill_dir = tmp_path / long_name
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(f"""---
name: {long_name}
description: Test skill
---
Body content
""")
    result = validate_skill(skill_dir)
    assert not result.is_valid
    assert any(
        "exceeds" in e.message and "character limit" in e.message for e in (result.errors or [])
    )


def test_validate_name_with_uppercase(tmp_path):
    """Test skill name with uppercase letters."""
    skill_dir = tmp_path / "Test-Skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("""---
name: Test-Skill
description: Test skill
---
Body content
""")
    result = validate_skill(skill_dir)
    assert not result.is_valid
    assert any("must be lowercase" in e.message for e in (result.errors or []))


def test_validate_name_with_consecutive_hyphens(tmp_path):
    """Test skill name with consecutive hyphens."""
    skill_dir = tmp_path / "test--skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("""---
name: test--skill
description: Test skill
---
Body content
""")
    result = validate_skill(skill_dir)
    assert not result.is_valid
    assert any("consecutive hyphens" in e.message for e in (result.errors or []))


def test_validate_description_too_long(tmp_path):
    """Test description exceeding maximum length."""
    skill_dir = tmp_path / "test-skill"
    skill_dir.mkdir()
    long_desc = "x" * 1025
    (skill_dir / "SKILL.md").write_text(f"""---
name: test-skill
description: {long_desc}
---
Body content
""")
    result = validate_skill(skill_dir)
    assert not result.is_valid
    assert any("Description exceeds" in e.message for e in (result.errors or []))


def test_validate_name_directory_mismatch(tmp_path):
    """Test when directory name doesn't match skill name."""
    skill_dir = tmp_path / "wrong-name"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("""---
name: test-skill
description: Test skill
---
Body content
""")
    result = validate_skill(skill_dir)
    assert not result.is_valid
    assert any("must match skill name" in e.message for e in (result.errors or []))
