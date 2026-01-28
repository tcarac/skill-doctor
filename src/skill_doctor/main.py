#!/usr/bin/env python3
"""Main entry point for Skill Doctor GitHub Action."""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List

from . import __version__
from .github_integration import create_annotations, create_pr_comment
from .models import ValidationResult
from .skill_finder import find_skills
from .validator import validate_skill


def parse_bool(value: str) -> bool:
    """Parse a boolean value from string."""
    return value.lower() in ("true", "1", "yes", "y")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Skill Doctor - Validate Agent Skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--path", default=".", help="Path to skill or pattern")
    parser.add_argument(
        "--mode",
        default="single",
        choices=["single", "multiple", "changed"],
        help="Validation mode",
    )
    parser.add_argument("--fail-on-error", default="true", help="Fail on validation errors")
    parser.add_argument("--comment-on-pr", default="true", help="Post PR comment")
    parser.add_argument("--create-annotations", default="true", help="Create GitHub annotations")
    parser.add_argument(
        "--auto-fix-suggestions", default="true", help="Include auto-fix suggestions"
    )
    parser.add_argument("--output-json", default="false", help="Output JSON results")
    parser.add_argument("--github-token", default="", help="GitHub token")

    return parser.parse_args()


def print_results(results: List[ValidationResult], show_suggestions: bool = True) -> None:
    """Print validation results to console.

    Args:
        results: List of validation results
        show_suggestions: Whether to show fix suggestions
    """
    total_skills = len(results)
    passed_skills = sum(1 for r in results if r.is_valid)
    failed_skills = total_skills - passed_skills
    total_errors = sum(len(r.errors or []) for r in results)

    print()
    print("=" * 80)
    print("Skill Doctor - Validation Results")
    print("=" * 80)
    print()

    # Summary
    print(f"Total skills validated: {total_skills}")
    print(f"✅ Passed: {passed_skills}")
    if failed_skills > 0:
        print(f"❌ Failed: {failed_skills}")
        print(f"Total errors: {total_errors}")
    print()

    # Details
    for result in results:
        skill_name = result.skill_name or Path(result.skill_path).name

        if result.is_valid:
            print(f"✅ {skill_name}")
            print(f"   Location: {result.skill_path}")
            print()
        else:
            print(f"❌ {skill_name}")
            print(f"   Location: {result.skill_path}")
            print()
            if result.errors:
                for error in result.errors:
                    location = f"line {error.line}" if error.line else "general"
                    print(f"   • [{location}] {error.message}")
                    if show_suggestions and error.suggestion:
                        print(f"     💡 {error.suggestion}")
            print()

    print("=" * 80)
    print()


def set_output(name: str, value: str) -> None:
    """Set a GitHub Actions output variable.

    Args:
        name: Output variable name
        value: Output variable value
    """
    # GitHub Actions output format
    output_file = os.environ.get("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"{name}={value}\n")
    else:
        print(f"::set-output name={name}::{value}")


def save_json_results(results: List[ValidationResult], output_path: str = "results.json") -> str:
    """Save results as JSON.

    Args:
        results: List of validation results
        output_path: Path to save JSON file

    Returns:
        Path to the saved JSON file
    """
    data = {
        "version": __version__,
        "total_skills": len(results),
        "passed": sum(1 for r in results if r.is_valid),
        "failed": sum(1 for r in results if not r.is_valid),
        "total_errors": sum(len(r.errors or []) for r in results),
        "skills": [
            {
                "path": r.skill_path,
                "name": r.skill_name,
                "valid": r.is_valid,
                "errors": [
                    {
                        "message": e.message,
                        "line": e.line,
                        "file": e.file,
                        "suggestion": e.suggestion,
                    }
                    for e in (r.errors or [])
                ],
            }
            for r in results
        ],
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return output_path


def main() -> int:
    """Main entry point.

    Returns:
        Exit code (0 for success, 1 for validation failure, 2 for error)
    """
    args = parse_args()

    # Parse boolean flags
    fail_on_error = parse_bool(args.fail_on_error)
    comment_on_pr = parse_bool(args.comment_on_pr)
    create_annot = parse_bool(args.create_annotations)
    show_suggestions = parse_bool(args.auto_fix_suggestions)
    output_json = parse_bool(args.output_json)

    # Set GitHub token if provided
    if args.github_token:
        os.environ["INPUT_GITHUB-TOKEN"] = args.github_token

    print(f"Skill Doctor v{__version__}")
    print(f"Mode: {args.mode}")
    print(f"Path: {args.path}")
    print()

    # Find skills to validate
    skill_dirs = find_skills(args.path, args.mode)

    if not skill_dirs:
        print("No skills found to validate.")
        return 2

    print(f"Found {len(skill_dirs)} skill(s) to validate")
    print()

    # Validate each skill
    results: List[ValidationResult] = []
    for skill_dir in skill_dirs:
        print(f"Validating: {skill_dir}")
        result = validate_skill(skill_dir)
        results.append(result)

    # Print results
    print_results(results, show_suggestions)

    # Set GitHub Actions outputs
    total_errors = sum(len(r.errors or []) for r in results)
    validation_status = "passed" if all(r.is_valid for r in results) else "failed"

    set_output("validation-status", validation_status)
    set_output("skills-validated", str(len(results)))
    set_output("errors-found", str(total_errors))

    # Create PR comment
    if comment_on_pr and os.environ.get("GITHUB_EVENT_NAME") == "pull_request":
        print("Creating PR comment...")
        create_pr_comment(results)

    # Create annotations
    if create_annot and os.environ.get("GITHUB_ACTIONS"):
        print("Creating GitHub annotations...")
        create_annotations(results)

    # Save JSON results
    if output_json:
        json_path = save_json_results(results)
        set_output("json-results", json_path)
        print(f"JSON results saved to: {json_path}")

    # Determine exit code
    if validation_status == "failed":
        if fail_on_error:
            print("❌ Validation failed")
            return 1
        else:
            print("⚠️  Validation failed (but not failing workflow)")
            return 0
    else:
        print("✅ All skills passed validation")
        return 0


if __name__ == "__main__":
    sys.exit(main())
