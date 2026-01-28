"""Core validation logic for Agent Skills."""

import re
import unicodedata
from pathlib import Path

import strictyaml

from .models import ValidationResult

# Constants from Agent Skills specification
MAX_SKILL_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_COMPATIBILITY_LENGTH = 500

ALLOWED_FIELDS = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
}


def find_skill_md(skill_dir: Path) -> Path | None:
    """Find the SKILL.md file in a skill directory.

    Prefers SKILL.md (uppercase) but accepts skill.md (lowercase).

    Args:
        skill_dir: Path to the skill directory

    Returns:
        Path to the SKILL.md file, or None if not found
    """
    for name in ("SKILL.md", "skill.md"):
        path = skill_dir / name
        if path.exists():
            return path
    return None


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from SKILL.md content.

    Args:
        content: Raw content of SKILL.md file

    Returns:
        Tuple of (metadata dict, markdown body)

    Raises:
        ValueError: If frontmatter is missing or invalid
    """
    if not content.startswith("---"):
        raise ValueError("SKILL.md must start with YAML frontmatter (---)")

    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError("SKILL.md frontmatter not properly closed with ---")

    frontmatter_str = parts[1]
    body = parts[2].strip()

    try:
        parsed = strictyaml.load(frontmatter_str)
        metadata = parsed.data
    except strictyaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in frontmatter: {e}") from e

    if not isinstance(metadata, dict):
        raise ValueError("SKILL.md frontmatter must be a YAML mapping")

    # Convert metadata field values to strings
    if "metadata" in metadata and isinstance(metadata["metadata"], dict):
        metadata["metadata"] = {str(k): str(v) for k, v in metadata["metadata"].items()}

    return metadata, body


def validate_name(name: str, skill_dir: Path | None, result: ValidationResult) -> None:
    """Validate skill name format and directory match."""
    if not name or not isinstance(name, str) or not name.strip():
        result.add_error(
            "Field 'name' must be a non-empty string",
            line=2,
            suggestion="Add a name field with a valid skill name",
        )
        return

    name = unicodedata.normalize("NFKC", name.strip())

    if len(name) > MAX_SKILL_NAME_LENGTH:
        result.add_error(
            f"Skill name '{name}' exceeds {MAX_SKILL_NAME_LENGTH} character limit "
            f"({len(name)} chars)",
            line=2,
            suggestion=f"Shorten the name to {MAX_SKILL_NAME_LENGTH} characters or less",
        )

    if name != name.lower():
        result.add_error(
            f"Skill name '{name}' must be lowercase",
            line=2,
            suggestion=f"Change to '{name.lower()}'",
        )

    if name.startswith("-") or name.endswith("-"):
        result.add_error(
            "Skill name cannot start or end with a hyphen",
            line=2,
            suggestion=f"Remove leading/trailing hyphens: '{name.strip('-')}'",
        )

    if "--" in name:
        result.add_error(
            "Skill name cannot contain consecutive hyphens",
            line=2,
            suggestion=f"Replace consecutive hyphens: '{re.sub(r'-+', '-', name)}'",
        )

    # Check for invalid characters
    if not all(c.isalnum() or c == "-" for c in name):
        invalid_chars = {c for c in name if not (c.isalnum() or c == "-")}
        result.add_error(
            f"Skill name '{name}' contains invalid characters: {', '.join(sorted(invalid_chars))}",
            line=2,
            suggestion="Only letters, digits, and hyphens are allowed",
        )

    # Check directory name matches
    if skill_dir:
        dir_name = unicodedata.normalize("NFKC", skill_dir.name)
        if dir_name != name:
            result.add_error(
                f"Directory name '{skill_dir.name}' must match skill name '{name}'",
                line=2,
                suggestion=f"Rename directory to '{name}'",
            )


def validate_description(description: str, result: ValidationResult) -> None:
    """Validate description format."""
    if not description or not isinstance(description, str) or not description.strip():
        result.add_error(
            "Field 'description' must be a non-empty string",
            line=3,
            suggestion="Add a clear description of what the skill does and when to use it",
        )
        return

    if len(description) > MAX_DESCRIPTION_LENGTH:
        result.add_error(
            f"Description exceeds {MAX_DESCRIPTION_LENGTH} character limit "
            f"({len(description)} chars)",
            line=3,
            suggestion=f"Trim description to {MAX_DESCRIPTION_LENGTH} characters or less",
        )


def validate_compatibility(compatibility: str, result: ValidationResult) -> None:
    """Validate compatibility format."""
    if not isinstance(compatibility, str):
        result.add_error(
            "Field 'compatibility' must be a string",
            suggestion="Ensure compatibility field is a string value",
        )
        return

    if len(compatibility) > MAX_COMPATIBILITY_LENGTH:
        result.add_error(
            f"Compatibility exceeds {MAX_COMPATIBILITY_LENGTH} character limit "
            f"({len(compatibility)} chars)",
            suggestion=f"Trim compatibility to {MAX_COMPATIBILITY_LENGTH} characters or less",
        )


def validate_metadata_fields(metadata: dict, result: ValidationResult) -> None:
    """Validate that only allowed fields are present."""
    extra_fields = set(metadata.keys()) - ALLOWED_FIELDS
    if extra_fields:
        result.add_error(
            f"Unexpected fields in frontmatter: {', '.join(sorted(extra_fields))}",
            line=1,
            suggestion=f"Remove unexpected fields or check spelling. "
            f"Allowed fields: {', '.join(sorted(ALLOWED_FIELDS))}",
        )


def validate_skill(skill_dir: Path) -> ValidationResult:
    """Validate a skill directory.

    Args:
        skill_dir: Path to the skill directory

    Returns:
        ValidationResult with any errors found
    """
    skill_dir = Path(skill_dir).resolve()
    result = ValidationResult(skill_path=str(skill_dir))

    # Check directory exists
    if not skill_dir.exists():
        result.add_error(f"Path does not exist: {skill_dir}")
        return result

    if not skill_dir.is_dir():
        result.add_error(f"Not a directory: {skill_dir}")
        return result

    # Find SKILL.md
    skill_md = find_skill_md(skill_dir)
    if skill_md is None:
        result.add_error(
            "Missing required file: SKILL.md",
            suggestion="Create a SKILL.md file with YAML frontmatter and instructions",
        )
        return result

    # Parse frontmatter
    try:
        content = skill_md.read_text(encoding="utf-8")
        metadata, _ = parse_frontmatter(content)
    except (OSError, UnicodeDecodeError) as e:
        result.add_error(f"Error reading SKILL.md: {e}")
        return result
    except ValueError as e:
        result.add_error(str(e))
        return result

    # Validate metadata fields
    validate_metadata_fields(metadata, result)

    # Validate required fields
    if "name" not in metadata:
        result.add_error(
            "Missing required field in frontmatter: name",
            line=1,
            suggestion="Add 'name: your-skill-name' to the frontmatter",
        )
    else:
        result.skill_name = metadata["name"]
        validate_name(metadata["name"], skill_dir, result)

    if "description" not in metadata:
        result.add_error(
            "Missing required field in frontmatter: description",
            line=1,
            suggestion="Add 'description: what this skill does' to the frontmatter",
        )
    else:
        validate_description(metadata["description"], result)

    # Validate optional fields
    if "compatibility" in metadata:
        validate_compatibility(metadata["compatibility"], result)

    return result
