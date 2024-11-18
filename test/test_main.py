import unittest
from unittest.mock import patch, mock_open
from conventional_commits_check.main import (
    check_commit_message,
    load_rules,
    get_regex_pattern,
)


class TestCommitCheck(unittest.TestCase):

    def setUp(self):
        # Set up mock data for commit types
        self.default_commit_types = {
            "feat": {"emoji": "✨"},
            "fix": {"emoji": "🐛"},
            "docs": {"emoji": "📚"},
        }

    @patch("builtins.open", new_callable=mock_open, read_data="feat: add new feature")
    def test_check_commit_message_with_valid_commit(self, mock_file):
        # Test with a valid commit message
        args = type("", (), {})()  # create an empty args object
        args.commit_message_file = "test_message.txt"
        args.emoji_disabled = False
        commit_message = "feat: add new feature"

        with patch(
            "yaml.safe_load",
            return_value={"additional_commit_types": self.default_commit_types},
        ):
            updated_message, result = check_commit_message(commit_message, args)
            self.assertEqual(updated_message, "✨ feat: add new feature")
            self.assertEqual(
                result,
                (
                    "🎉 Commit message follows Conventional Commits rules "
                    "and has been updated with an emoji."
                ),
            )

    @patch("builtins.open", new_callable=mock_open, read_data="custom: custom type")
    def test_check_commit_message_with_custom_commit_type(self, mock_file):
        # Test with a custom commit type loaded from YAML
        args = type("", (), {})()
        args.commit_message_file = "test_message.txt"
        args.emoji_disabled = False
        commit_message = "custom: custom type"

        custom_commit_types = {"custom": {"emoji": "🔧"}}

        with patch(
            "yaml.safe_load",
            return_value={"additional_commit_types": custom_commit_types},
        ):
            updated_message, result = check_commit_message(commit_message, args)
            self.assertEqual(updated_message, "🔧 custom: custom type")
            self.assertEqual(
                result,
                (
                    "🎉 Commit message follows Conventional Commits rules "
                    "and has been updated with an emoji."
                ),
            )

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="invalid: no valid commit type",
    )
    def test_check_commit_message_with_invalid_commit(self, mock_file):
        # Test with an invalid commit message
        args = type("", (), {})()
        args.commit_message_file = "test_message.txt"
        args.emoji_disabled = False
        commit_message = "invalid: no valid commit type"

        with patch(
            "yaml.safe_load",
            return_value={"additional_commit_types": self.default_commit_types},
        ):
            updated_message, result = check_commit_message(commit_message, args)
            self.assertIsNone(updated_message)
            self.assertEqual(
                result,
                ("💥 Commit message does not follow Conventional Commits " "rules."),
            )

    @patch("builtins.open", new_callable=mock_open, read_data="fix: bug fix")
    def test_check_commit_message_with_emoji_disabled(self, mock_file):
        # Test with emoji disabled
        args = type("", (), {})()
        args.commit_message_file = "test_message.txt"
        args.emoji_disabled = True
        commit_message = "fix: bug fix"

        with patch(
            "yaml.safe_load",
            return_value={"additional_commit_types": self.default_commit_types},
        ):
            updated_message, result = check_commit_message(commit_message, args)
            self.assertEqual(updated_message, "fix: bug fix")
            self.assertEqual(
                result, "🎉 Commit message follows Conventional Commits rules."
            )

    def test_get_regex_pattern(self):
        # Test regex pattern generation
        commit_type = "feat"
        expected_pattern = "^(. ?)?feat(\\(.+\\))?\\!?:"
        self.assertEqual(get_regex_pattern(commit_type), expected_pattern)

    @patch("builtins.open", new_callable=mock_open, read_data="feat: add new feature")
    @patch("os.path.exists", return_value=True)
    @patch(
        "conventional_commits_check.main.load_rules_from_yaml",
        return_value={"additional_commit_types": {}},
    )
    def test_load_rules(self, mock_load_yaml, mock_exists, mock_file):
        # Test loading rules from YAML
        loaded_rules = load_rules()
        self.assertIn("feat", loaded_rules)
        self.assertIn("fix", loaded_rules)
        self.assertIn("docs", loaded_rules)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="Merge remote-tracking branch 'origin' into staging",
    )
    def test_handle_auto_merge_commit(self, mock_file):
        # Test with an auto-merge commit message
        args = type("", (), {})()
        args.commit_message_file = "test_message.txt"
        args.emoji_disabled = False
        commit_message = "Merge remote-tracking branch 'origin' into staging"

        updated_message, result = check_commit_message(commit_message, args)
        self.assertEqual(
            updated_message, "🎉 merge: remote-tracking branch 'origin' into staging"
        )
        self.assertEqual(result, "✅ Auto-merge commit message successfully formatted.")

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="Merge branch 'feature-branch' into 'main'",
    )
    def test_handle_auto_merge_commit_with_emoji_disabled(self, mock_file):
        # Test with an auto-merge commit message and emoji disabled
        args = type("", (), {})()
        args.commit_message_file = "test_message.txt"
        args.emoji_disabled = True
        commit_message = "Merge branch 'feature-branch' into 'main'"

        updated_message, result = check_commit_message(commit_message, args)
        self.assertEqual(updated_message, "merge: branch 'feature-branch' into 'main'")
        self.assertEqual(result, "✅ Auto-merge commit message successfully formatted.")


if __name__ == "__main__":
    unittest.main()
