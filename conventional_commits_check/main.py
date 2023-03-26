import re
import sys
import os
from subprocess import check_output, CalledProcessError, STDOUT


CONVENTIONAL_EMOJIS = {
    "feat": "✨",
    "fix": "🐛",
    "docs": "📚",
    "style": "💄",
    "refactor": "🧹",
    "perf": "🚀",
    "test": "🧪",
    "build": "👷",
    "ci": "👷‍♂️",
    "chore": "🧹",
    "revert": "⏪",
}


def check_conventional_commits_emoji(commit_msg: str) -> None:
    pattern = r"^(?P<prefix>[\w]+)(\([a-z]+\))?:\s(?P<message>.+)"
    match = re.match(pattern, commit_msg)

    check_emoji = commit_msg.split(' ')[0] in CONVENTIONAL_EMOJIS.values()
    if check_emoji:
        sys.exit(0)

    if not match:
        sys.stderr.write(
            "Commit message does not follow Conventional Commits rules.\n")
        sys.exit(1)

    prefix = match.group("prefix").lower()
    message = match.group("message")
    if prefix not in CONVENTIONAL_EMOJIS:
        sys.stderr.write(f"Invalid prefix: {prefix}\n")
        sys.exit(1)

    return f"{CONVENTIONAL_EMOJIS[prefix]} {commit_msg}"


def main() -> None:
    try:
        commit_msg = check_output(
            ["git", "log", "-1", "--pretty=format:%B"], stderr=STDOUT).decode().strip()
    except CalledProcessError as e:
        sys.stderr.write(f"Failed to get commit message: {e}\n")
        sys.exit(1)
    new_commit_msg = check_conventional_commits_emoji(commit_msg)

    try:
        os.system(f'git commit --amend -m "{new_commit_msg}"')
    except CalledProcessError as e:
        sys.stderr.write(f"Failed to update commit message: {e}\n")
        sys.exit(1)

    print("Commit message successfully updated with emoji.")


if __name__ == "__main__":
    main()
