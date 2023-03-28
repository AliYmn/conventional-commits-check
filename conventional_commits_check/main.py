#!/usr/bin/env python3
import argparse
import re
import sys
from typing import Dict
import yaml

COMMIT_TYPES = {
    "feat": "^feat(\(.+\))?:",
    "fix": "^fix(\(.+\))?:",
    "docs": "^docs(\(.+\))?:",
    "style": "^style(\(.+\))?:",
    "refactor": "^refactor(\(.+\))?:",
    "perf": "^perf(\(.+\))?:",
    "test": "^test(\(.+\))?:",
    "build": "^build(\(.+\))?:",
    "ci": "^ci(\(.+\))?:",
    "chore": "^chore(\(.+\))?:",
    "revert": "^revert: ",
}

EMOJIS = {
    "feat": "✨",
    "fix": "🐛",
    "docs": "📚",
    "style": "💎",
    "refactor": "🧹",
    "perf": "🚀",
    "test": "🧪",
    "build": "🏗️",
    "ci": "👷",
    "chore": "♻️",
    "revert": "⏪",
}


def load_custom_rules(config_file=".pre-commit-config.yaml"):
    try:
        with open(config_file, "r") as file:
            config_data = yaml.safe_load(file)

        for repo in config_data["repos"]:
            if repo.get("repo") == "local":
                for hook in repo["hooks"]:
                    if hook["id"] == "conventional-commits-check":
                        return hook.get("additional_commands", {}), hook.get("additional_emojis", {})

    except FileNotFoundError:
        pass

    return {}, {}


def main():
    additional_commands, additional_emojis = load_custom_rules()

    # Merge additional commands and emojis with the existing ones
    COMMIT_TYPES.update(additional_commands)
    EMOJIS.update(additional_emojis)

    parser = argparse.ArgumentParser()
    parser.add_argument("commit_message_file")
    args = parser.parse_args()

    with open(args.commit_message_file, "r") as file:
        commit_message = file.read()

    commit_type = None
    for commit, pattern in COMMIT_TYPES.items():
        if re.match(pattern, commit_message.strip()):
            commit_type = commit
            break

    if not commit_type:
        print("Commit message does not follow Conventional Commits rules.")
        sys.exit(1)

    emoji = EMOJIS.get(commit_type)

    if emoji:
        new_commit_message = f"{emoji} {commit_message}"
        with open(args.commit_message_file, "w") as file:
            file.write(new_commit_message)

    print("Commit message follows Conventional Commits rules and has been updated with an emoji.")
    sys.exit(0)


if __name__ == "__main__":
    main()
