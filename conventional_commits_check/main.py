#!/usr/bin/env python3
import argparse
import re
import sys
import yaml
import os
import pkg_resources
from conventional_commits_check.commit_types import commit_types


def get_regex_pattern(commit_type: str) -> str:
    """
    Constructs a regex pattern for a given commit type.

    Args:
        commit_type (str): The type of commit to match.

    Returns:
        str: A regex pattern string.
    """
    return f"^(. ?)?{commit_type}(\\(.+\\))?\\!?:"


def load_rules():
    """
    Loads commit type rules from the Python module.

    Returns:
        dict: A dictionary of commit types.
    """
    return commit_types


def get_commit_message(args):
    """
    Reads the commit message from a file.

    Args:
        args: Command line arguments containing the commit message file path.

    Returns:
        str: The commit message.
    """
    with open(args.commit_message_file, "r") as file:
        return file.read()


def update_commit_message(args, commit_message):
    """
    Writes the updated commit message back to the file.

    Args:
        args: Command line arguments containing the commit message file path.
        commit_message (str): The updated commit message.
    """
    with open(args.commit_message_file, "w") as file:
        file.write(commit_message)


def check_commit_message(commit_message, args):
    """
    Checks if the commit message follows Conventional Commits rules and updates it with an emoji if applicable.

    Args:
        commit_message (str): The commit message to check.
        args: Command line arguments.

    Returns:
        tuple: A tuple containing the updated commit message and a result message.
    """
    commit_types = load_rules()
    additional_commands = load_rules_from_yaml("./commits_check_config.yaml")
    commit_types.update(additional_commands)
    commit_type, props = (None, None)
    for commit_type_for_matching, props in commit_types.items():
        if re.match(
            get_regex_pattern(commit_type_for_matching), commit_message.strip()
        ):
            commit_type, _ = (commit_type_for_matching, props)
            break

    if not commit_type:
        return None, "💥 Commit message does not follow Conventional Commits rules."

    emoji = props["emoji"]

    if emoji and not args.emoji_disabled:
        if not commit_message.startswith(emoji):
            index = commit_message.find(commit_type)
            commit_message = f"{emoji} {commit_message[index:]}"

            return (
                commit_message,
                "🎉 Commit message follows Conventional Commits rules and has been updated with an emoji.",
            )

    return commit_message, "🎉 Commit message follows Conventional Commits rules."


def main():
    """
    Main function to parse arguments, check the commit message, and update it if necessary.
    """
    parser = argparse.ArgumentParser(
        description="Check and update commit messages to follow Conventional Commits rules."
    )
    parser.add_argument("commit_message_file", help="Path to the commit message file.")
    parser.add_argument(
        "--emoji-disabled",
        action="store_true",
        help="Disable emojis in commit messages",
    )
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
