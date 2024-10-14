#!/usr/bin/env python3
import argparse
import re
import sys
import yaml
import os

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
    "merge": "🔀",
}


def load_custom_rules(config_file="commits_check_config.yaml"):
    config_path = os.path.join(os.getcwd(), config_file)

    if not os.path.exists(config_path):
        return {}, {}

    with open(config_path, "r") as file:
        config_data = yaml.safe_load(file)

    return config_data.get("additional_commands", {}), config_data.get(
        "additional_emojis", {}
    )


def main():
    additional_commands, additional_emojis = load_custom_rules()

    # Merge additional commands and emojis with the existing ones
    COMMIT_TYPES.update(additional_commands)
    EMOJIS.update(additional_emojis)

    parser = argparse.ArgumentParser()
    parser.add_argument("commit_message_file")
    parser.add_argument("--emoji-disabled", action="store_true", help="Disable emojis in commit messages")
    args = parser.parse_args()

    with open(args.commit_message_file, "r") as file:
        commit_message = file.read()

    commit_type = None
    for commit, pattern in COMMIT_TYPES.items():
        if re.match(pattern, commit_message.strip()):
            commit_type = commit
            break

    if not commit_type:
        print("💥 Commit message does not follow Conventional Commits rules.")
        sys.exit(1)

    emoji = EMOJIS.get(commit_type)

    if emoji and not args.emoji_disabled:
        new_commit_message = f"{emoji} {commit_message}"
        with open(args.commit_message_file, "w") as file:
            file.write(new_commit_message)

    print(
        "🎉 Commit message follows Conventional Commits rules and has been updated with an emoji."
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
