import os
import re
import sys
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


def check_conventional_commits(commit_msg: str) -> str:
    pattern = r"^(?P<prefix>[\w]+)(\([a-z]+\))?:\s(?P<message>.+)"
    match = re.match(pattern, commit_msg)

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


def main(argv=None) -> None:
    if argv is None:
        argv = sys.argv

    try:
        commit_msg_file = argv[1]
    except IndexError:
        sys.stderr.write("Error: No commit message file provided.\n")
        sys.exit(1)

    try:
        with open(commit_msg_file, "r") as file:
            commit_msg = file.read().strip()
    except FileNotFoundError as e:
        sys.stderr.write(f"Error: Failed to read commit message file: {e}\n")
        sys.exit(1)

    new_commit_msg = check_conventional_commits(commit_msg)

    with open(commit_msg_file, "w") as file:
        file.write(new_commit_msg)


if __name__ == "__main__":
    main()
