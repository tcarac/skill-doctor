"""GitHub integration for PR comments and annotations."""

import json
import os

from github import Github
from github.PullRequest import PullRequest

from .models import ValidationResult


def get_pr() -> PullRequest | None:
    """Get the current pull request from GitHub context.

    Returns:
        PullRequest object or None if not in PR context
    """
    if os.environ.get("GITHUB_EVENT_NAME") != "pull_request":
        return None

    token = os.environ.get("INPUT_GITHUB-TOKEN")
    if not token:
        print("Warning: No GitHub token provided")
        return None

    repo_name = os.environ.get("GITHUB_REPOSITORY")
    if not repo_name:
        return None

    try:
        # Load event data
        event_path = os.environ.get("GITHUB_EVENT_PATH")
        if not event_path:
            return None

        with open(event_path, encoding="utf-8") as f:
            event_data = json.load(f)

        pr_number = event_data.get("pull_request", {}).get("number")
        if not pr_number:
            return None

        g = Github(token)
        repo = g.get_repo(repo_name)
        return repo.get_pull(pr_number)

    except Exception as e:
        print(f"Warning: Failed to get PR context: {e}")
        return None


def create_pr_comment(results: list[ValidationResult]) -> None:
    """Post validation results as a PR comment.

    Args:
        results: List of validation results
    """
    pr = get_pr()
    if not pr:
        print("Skipping PR comment: not in PR context")
        return

    # Generate comment body
    comment = generate_comment_body(results)

    try:
        # Check if we already have a comment from this action
        comments = pr.get_issue_comments()
        bot_comment = None
        marker = "<!-- skill-doctor-results -->"

        for comment_obj in comments:
            if marker in comment_obj.body:
                bot_comment = comment_obj
                break

        full_comment = f"{marker}\n{comment}"

        if bot_comment:
            # Update existing comment
            bot_comment.edit(full_comment)
            print("Updated existing PR comment")
        else:
            # Create new comment
            pr.create_issue_comment(full_comment)
            print("Created new PR comment")

    except Exception as e:
        print(f"Warning: Failed to post PR comment: {e}")


def generate_comment_body(results: list[ValidationResult]) -> str:
    """Generate markdown comment body from validation results.

    Args:
        results: List of validation results

    Returns:
        Formatted markdown string
    """
    total_skills = len(results)
    passed_skills = sum(1 for r in results if r.is_valid)
    failed_skills = total_skills - passed_skills
    total_errors = sum(len(r.errors or []) for r in results)

    # Header
    if failed_skills == 0:
        header = "## ✅ Agent Skills Validation Passed"
        emoji = "✅"
    else:
        header = "## ❌ Agent Skills Validation Failed"
        emoji = "❌"

    lines = [header, ""]

    # Summary
    lines.append("### Summary")
    lines.append(f"- Total skills validated: **{total_skills}**")
    lines.append(f"- {emoji} Passed: **{passed_skills}**")
    if failed_skills > 0:
        lines.append(f"- ❌ Failed: **{failed_skills}**")
        lines.append(f"- Total errors: **{total_errors}**")
    lines.append("")

    # Details for each skill
    if failed_skills > 0:
        lines.append("---")
        lines.append("")

    for result in results:
        if not result.is_valid:
            skill_name = result.skill_name or Path(result.skill_path).name
            lines.append(f"### ❌ `{skill_name}`")
            lines.append(f"**Location:** `{result.skill_path}/SKILL.md`")
            lines.append("")

            if result.errors:
                lines.append("**Errors:**")
                for i, error in enumerate(result.errors, 1):
                    location = f"Line {error.line}" if error.line else "General"
                    lines.append(f"{i}. **{location}:** {error.message}")
                    if error.suggestion:
                        lines.append(f"   - 💡 **Suggestion:** {error.suggestion}")
                lines.append("")

    # Add passed skills summary
    if passed_skills > 0:
        lines.append("---")
        lines.append("")
        lines.append("### ✅ Passed Skills")
        for result in results:
            if result.is_valid:
                skill_name = result.skill_name or Path(result.skill_path).name
                lines.append(f"- `{skill_name}`")
        lines.append("")

    # Footer
    lines.append("---")
    lines.append(
        "*For more information, see the "
        "[Agent Skills Specification](https://agentskills.io/specification)*"
    )

    return "\n".join(lines)


def create_annotations(results: list[ValidationResult]) -> None:
    """Create GitHub annotations for validation errors.

    Args:
        results: List of validation results
    """
    if not os.environ.get("GITHUB_ACTIONS"):
        return

    for result in results:
        if not result.is_valid and result.errors:
            for error in result.errors:
                # Format: ::error file={name},line={line}::{message}
                skill_path = Path(result.skill_path)
                file_path = skill_path / "SKILL.md"

                annotation = "::error"
                annotation += f" file={file_path}"
                if error.line:
                    annotation += f",line={error.line}"
                annotation += f"::{error.message}"

                if error.suggestion:
                    annotation += f" (Suggestion: {error.suggestion})"

                print(annotation)


from pathlib import Path  # noqa: E402
