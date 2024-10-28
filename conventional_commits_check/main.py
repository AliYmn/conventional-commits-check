#!/usr/bin/env python3
import argparse
import re
import sys
import yaml
import os


def get_regex_pattern(commit_type: str) -> str:
    return f"^(. ?)?{commit_type}(\\(.+\\))?\\!?:"



def load_rules(config_file):
    config_path = os.path.join(os.getcwd(), config_file)

    if not os.path.exists(config_path):
        return {}

    with open(config_path, "r") as file:
        config_data = yaml.safe_load(file)

    return config_data.get("additional_commit_types", {})

def get_commit_message(args):
    with open(args.commit_message_file, "r") as file:
        return file.read()

def update_commit_message(args, commit_message):
    with open(args.commit_message_file, "w") as file:
        file.write(commit_message)


def check_commit_message(commit_message, args):
    commit_types = load_rules("./conventional_commits_check/commit_types.yaml")
    additional_commands = load_rules("./commits_check_config.yaml")
    # Merge additional commands and emojis with the existing ones
    commit_types.update(additional_commands)


    commit_type, props = (None, None)
    for commit_type_for_matching, props in commit_types.items():
        if re.match(get_regex_pattern(commit_type_for_matching), commit_message.strip()):
            commit_type, found_props = (commit_type_for_matching, props)
            break

    if not commit_type:
        return None, "💥 Commit message does not follow Conventional Commits rules."

    emoji = props["emoji"]

    if emoji and not args.emoji_disabled:
        if not commit_message.startswith(emoji):
            index = commit_message.find(commit_type)
            commit_message = f"{emoji} {commit_message[index:]}"

            return commit_message, "🎉 Commit message follows Conventional Commits rules and has been updated with an emoji."


    return commit_message, "🎉 Commit message follows Conventional Commits rules."

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("commit_message_file")
    parser.add_argument("--emoji-disabled", action="store_true", help="Disable emojis in commit messages")
    args = parser.parse_args()

    commit_message = get_commit_message(args)

    (commit_message, result) = check_commit_message(commit_message, args)

    if commit_message:
        update_commit_message(args, commit_message)
        print(result)
        sys.exit(0)
    else:
        print(result)
        sys.exit(1)


if __name__ == "__main__":
    main()
