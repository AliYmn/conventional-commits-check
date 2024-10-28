import io
from unittest import TestCase
from unittest.mock import patch

from conventional_commits_check.main import main


class Test(TestCase):
    @patch('conventional_commits_check.main.get_commit_message', return_value='✨ feat: this is a sample message')
    @patch('conventional_commits_check.main.update_commit_message')
    @patch('sys.exit')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_conventional_commit_with_right_emoji(self,  mock_stdout, mock_exit, mock_get_commit_message, mock_update_commit_message):
        main()

        self.assertEqual(mock_exit.call_args[0][0], 0)
        self.assertIn("🎉 Commit message follows Conventional Commits rules.",
                      mock_stdout.getvalue())

    @patch('conventional_commits_check.main.get_commit_message', return_value='✅ feat: this is a sample message')
    @patch('conventional_commits_check.main.update_commit_message')
    @patch('sys.exit')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_conventional_commit_with_wrong_emoji(self,  mock_stdout, mock_exit, mock_get_commit_message, mock_update_commit_message):
        main()

        self.assertEqual(mock_exit.call_args[0][0], 0)
        self.assertIn("🎉 Commit message follows Conventional Commits rules and has been updated with an emoji.",
                      mock_stdout.getvalue())

    @patch('conventional_commits_check.main.get_commit_message', return_value='feat: this is a sample message')
    @patch('conventional_commits_check.main.update_commit_message')
    @patch('sys.exit')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_conventional_commit_without_emoji(self, mock_stdout, mock_exit, mock_get_commit_message,
                                                  mock_update_commit_message):
        main()

        self.assertEqual(mock_exit.call_args[0][0], 0)
        self.assertIn("🎉 Commit message follows Conventional Commits rules and has been updated with an emoji.",
                      mock_stdout.getvalue())

    @patch('conventional_commits_check.main.get_commit_message', return_value='this is a sample message')
    @patch('conventional_commits_check.main.update_commit_message')
    @patch('sys.exit')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_non_conventional_commit(self, mock_stdout, mock_exit, mock_get_commit_message,
                                               mock_update_commit_message):
        main()

        self.assertEqual(mock_exit.call_args[0][0], 1)
        self.assertIn("💥 Commit message does not follow Conventional Commits rules.",
                      mock_stdout.getvalue())

    @patch('conventional_commits_check.main.get_commit_message', return_value='feat(scope): this is a sample message')
    @patch('conventional_commits_check.main.update_commit_message')
    @patch('sys.exit')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_scoped_conventional_commit(self, mock_stdout, mock_exit, mock_get_commit_message,
                                               mock_update_commit_message):
        main()

        self.assertEqual(mock_exit.call_args[0][0], 0)
        self.assertIn("🎉 Commit message follows Conventional Commits rules and has been updated with an emoji.",
                      mock_stdout.getvalue())