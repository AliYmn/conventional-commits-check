# Conventional Commits Check

<img src="https://raw.githubusercontent.com/AliYmn/conventional-commits-check/master/images/result.png">

`conventional-commits-check` is a Python pre-commit hook that enforces Conventional Commits rules on your commit messages and automatically adds relevant emojis based on the commit type.

Conventional Commits is a lightweight convention that provides a set of rules for creating an explicit commit history. This pre-commit hook helps ensure your commit messages adhere to the convention and provides additional context with emojis.

# Automatic Emoji Insertionadsasd

Automatic emoji insertion at the beginning of the Commit 🎉

```json
{
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
```

# Customization

```bash
touch conventional_commits_check_config.yaml
````

`NOTE` : Please do not leave it blank if you create it.

To add custom commit types and emojis, update your `conventional_commits_check_config.yaml` file with the additional_commands and additional_emojis fields. Here's an example:

```yaml
additional_commands:
  database: "^database(\\(.+\\))?:"
  design: "^design(\\(.+\\))?:"

additional_emojis:
  database: "🗃️"
  design: "🎨"
````

# Customization Current Emoji

This is how you can change the emojis of existing commands.

```yaml
additional_commands:
  fix: "^fix(\\(.+\\))?:"
  feat: "^feat(\\(.+\\))?:"

additional_emojis:
  fix: "🗃️"
  feat: "🎨"
````

## Features

- Checks if commit messages follow the Conventional Commits rules.
- Adds an emoji to the commit message based on the commit type.
- Blocks commits with non-conforming messages.

## Installation

Follow these steps to add the `conventional-commits-check` pre-commit hook to your project:

1. In your project's root directory, open the existing `.pre-commit-config.yaml` file (or create one if it doesn't exist) and add the following content:

```yaml
repos:
  - repo: https://github.com/AliYmn/conventional-commits-check
    rev: v0.3.0  # Use the latest release version
    hooks:
      - id: conventional-commits-check
        stages: [commit-msg]
```

2. Update the pre-commit hooks in your project:


```bash
pre-commit install --hook-type commit-msg -f
```

3. Install the conventional-commits-check package:


```bash
pip install -U conventional-commits-check
```

4. You may need to update the pre-commit package;

```bash
pre-commit autoupdate
```

# Usage

Once the hook is added to your project, it will automatically run every time you create a commit. The hook will check the commit messages according to the Conventional Commits rules and add the corresponding emojis. If a commit message does not follow the rules, the commit will be blocked.