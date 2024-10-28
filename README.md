
# 🎉 Conventional Commits Check

![PyPI Version](https://img.shields.io/pypi/v/conventional-commits-check)
![License](https://img.shields.io/github/license/AliYmn/conventional-commits-check)
![Last Commit](https://img.shields.io/github/last-commit/AliYmn/conventional-commits-check)
![Issues](https://img.shields.io/github/issues/AliYmn/conventional-commits-check)

![Result Image](https://raw.githubusercontent.com/AliYmn/conventional-commits-check/master/images/result.png)

`conventional-commits-check` is a powerful and easy-to-use Python pre-commit hook that helps enforce [Conventional Commits](https://www.conventionalcommits.org/) rules on your commit messages. As a bonus, it adds relevant emojis based on your commit types to enhance readability and bring some fun to your commit history! 🚀

## 📜 What are Conventional Commits?

Conventional Commits provide a lightweight convention for creating a clear and explicit commit history. By using this hook, you'll ensure that your commit messages follow this convention, making your versioning easier to manage and your collaboration more seamless

## 💡 Features

- ✅ Enforces Conventional Commits rules on your commit messages.
- 🎨 Automatically adds context-specific emojis to the start of commit messages.
- 🛑 Blocks commits that do not conform to the Conventional Commits standard.
- 🔧 Allows for **custom commit types** and **custom emojis** via configuration.

## 🎉 Automatic Emoji Insertion

No more boring commit messages! Emojis will be automatically inserted at the start of your commit messages based on the type:

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
    "revert": "⏪"
}
```

## 🔧 Customization

Need to add your own commit types and emojis? No problem! Simply create a `commits_check_config.yaml` file and define your own rules:

```bash
touch commits_check_config.yaml
```

**Important:** Please ensure the file is not left blank.

Example `commits_check_config.yaml` with custom types and emojis:

```yaml
additional_commands:
  database: "^database(\(.+\))?:"
  design: "^design(\(.+\))?:"

additional_emojis:
  database: "🗃️"
  design: "🎨"
```

### 🖌️ Customizing Existing Emojis

You can also modify the emojis for existing commit types:

```yaml
additional_commands:
  fix: "^fix(\(.+\))?:"
  feat: "^feat(\(.+\))?:"

additional_emojis:
  fix: "🛠️"
  feat: "🎉"
```

## ⚙️ Installation

To add `conventional-commits-check` to your project, follow these steps:

1. **Update your `.pre-commit-config.yaml`:**

   In your project’s root directory, add the following:

   ```yaml
   repos:
     - repo: https://github.com/AliYmn/conventional-commits-check
       rev: v0.3.0  # Use the latest release version
       hooks:
         - id: conventional-commits-check
           stages: [commit-msg]
           args: ["--emoji-disabled"]  # Use this argument to disable emojis
   ```

2. **Install the pre-commit hook:**

   ```bash
   pre-commit install --hook-type commit-msg -f
   ```

3. **Install the `conventional-commits-check` package:**

   ```bash
   pip install -U conventional-commits-check
   ```

4. **Optional:** Update the pre-commit package:

   ```bash
   pre-commit autoupdate
   ```

## 🚀 Usage

Once the hook is added, it will automatically run each time you make a commit. The hook checks your commit message against Conventional Commits rules, adds the appropriate emoji, and prevents non-conforming commits.

## 👨‍💻 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to enhance `conventional-commits-check`. Let’s make commits fun and consistent! 😄

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

Enhance your workflow and bring some life to your commits with `conventional-commits-check`! 🎉✨🐛
