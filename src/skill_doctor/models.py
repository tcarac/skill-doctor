"""Data models for Agent Skills."""

from dataclasses import dataclass


@dataclass
class SkillProperties:
    """Properties of an Agent Skill from SKILL.md frontmatter."""

    name: str
    description: str
    license: str | None = None
    compatibility: str | None = None
    allowed_tools: str | None = None
    metadata: dict[str, str] | None = None


@dataclass
class ValidationError:
    """A validation error found in a skill."""

    message: str
    line: int | None = None
    file: str = "SKILL.md"
    suggestion: str | None = None

    def __str__(self) -> str:
        """Format error message."""
        location = f"{self.file}"
        if self.line:
            location += f":{self.line}"
        result = f"{location}: {self.message}"
        if self.suggestion:
            result += f"\n  Suggestion: {self.suggestion}"
        return result


@dataclass
class ValidationResult:
    """Result of validating a skill."""

    skill_path: str
    skill_name: str | None = None
    is_valid: bool = True
    errors: list[ValidationError] | None = None

    def __post_init__(self) -> None:
        """Initialize errors list if None."""
        if self.errors is None:
            self.errors = []

    def add_error(
        self,
        message: str,
        line: int | None = None,
        file: str = "SKILL.md",
        suggestion: str | None = None,
    ) -> None:
        """Add a validation error."""
        if self.errors is None:
            self.errors = []
        self.errors.append(ValidationError(message, line, file, suggestion))
        self.is_valid = False
