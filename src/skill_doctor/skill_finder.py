"""Find skills in a repository."""

import os
import subprocess
from pathlib import Path
from typing import List


def find_skills_by_pattern(pattern: str, base_path: Path = Path(".")) -> List[Path]:
    """Find skill directories matching a glob pattern.

    Args:
        pattern: Glob pattern to match (e.g., 'skills/*')
        base_path: Base path to search from

    Returns:
        List of paths to skill directories
    """
    base_path = Path(base_path).resolve()
    results = []

    # Handle single directory
    target_path = base_path / pattern
    if target_path.is_dir():
        # Check if it contains SKILL.md
        if (target_path / "SKILL.md").exists() or (target_path / "skill.md").exists():
            results.append(target_path)
        return results

    # Handle glob pattern
    for skill_dir in base_path.glob(pattern):
        if skill_dir.is_dir():
            # Check if it contains SKILL.md
            if (skill_dir / "SKILL.md").exists() or (skill_dir / "skill.md").exists():
                results.append(skill_dir)

    return sorted(results)


def find_changed_skills(base_ref: str = "origin/main") -> List[Path]:
    """Find skills that have changed in the current PR.

    Args:
        base_ref: Base branch reference (default: origin/main)

    Returns:
        List of paths to changed skill directories
    """
    try:
        # Get changed files
        result = subprocess.run(
            ["git", "diff", "--name-only", base_ref, "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        changed_files = result.stdout.strip().split("\n")

        # Find unique skill directories
        skill_dirs = set()
        for file_path in changed_files:
            if not file_path:
                continue

            path = Path(file_path)

            # Check if SKILL.md was changed
            if path.name.lower() == "skill.md":
                skill_dir = path.parent
                if skill_dir.is_dir():
                    skill_dirs.add(skill_dir.resolve())
            # Check if file is within a skill directory
            else:
                for parent in path.parents:
                    if (parent / "SKILL.md").exists() or (parent / "skill.md").exists():
                        skill_dirs.add(parent.resolve())
                        break

        return sorted(skill_dirs)

    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to detect changed files: {e}")
        return []
    except Exception as e:
        print(f"Warning: Error finding changed skills: {e}")
        return []


def find_skills(
    path: str = ".", mode: str = "single", base_ref: str = "origin/main"
) -> List[Path]:
    """Find skills based on the specified mode.

    Args:
        path: Path or pattern to search
        mode: Validation mode (single, multiple, or changed)
        base_ref: Base branch for changed mode

    Returns:
        List of skill directories to validate
    """
    if mode == "changed":
        # In PR context, find changed skills
        if "GITHUB_EVENT_NAME" in os.environ and os.environ["GITHUB_EVENT_NAME"] == "pull_request":
            return find_changed_skills(base_ref)
        else:
            print("Warning: 'changed' mode requires PR context, falling back to 'single' mode")
            mode = "single"

    if mode == "single":
        # Validate a single skill directory
        skill_path = Path(path).resolve()
        if skill_path.is_dir():
            return [skill_path]
        else:
            print(f"Error: Path is not a directory: {skill_path}")
            return []

    elif mode == "multiple":
        # Find multiple skills using glob pattern
        return find_skills_by_pattern(path, Path("."))

    else:
        print(f"Error: Invalid mode '{mode}'. Must be 'single', 'multiple', or 'changed'")
        return []
