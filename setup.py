from setuptools import setup, find_packages

setup(
    name="conventional-commits-check",
    version="0.1.0",
    description="A pre-commit hook to check Conventional Commits and add emojis.",
    author="Ali Yaman",
    packages=find_packages(),
    install_requires=["pre-commit"],
    entry_points={"console_scripts": [
        "conventional-commits-check = conventional_commits_check.main:main"]},
)
