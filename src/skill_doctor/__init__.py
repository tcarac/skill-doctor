"""Skill Doctor - A GitHub Action to validate Agent Skills."""

__version__ = "1.0.0"
__author__ = "Tomas Caraccia"
__license__ = "Apache-2.0"

from .models import SkillProperties
from .validator import ValidationResult, validate_skill

__all__ = [
    "validate_skill",
    "ValidationResult",
    "SkillProperties",
]
