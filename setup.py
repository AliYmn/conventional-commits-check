from setuptools import setup, find_packages
import sys

if sys.version_info[0] < 3:
    with open("README.md") as f:
        README = f.read()
else:
    with open("README.md", encoding="utf-8") as f:
        README = f.read()

setup(
    name="conventional-commits-check",
    version="2.8.0",
    description=("A pre-commit hook to check Conventional Commits and add emojis."),
    author="Ali Yaman",
    packages=find_packages(),
    license="MIT",
    long_description_content_type="text/markdown",
    long_description=README,
    url="https://github.com/AliYmn/conventional-commits-check",
    install_requires=["pyyaml==6.0.2"],
    entry_points={
        "console_scripts": [
            "conventional-commits-check = conventional_commits_check.main:main"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Version Control",
        "Topic :: Utilities",
    ],
    include_package_data=True,
)
