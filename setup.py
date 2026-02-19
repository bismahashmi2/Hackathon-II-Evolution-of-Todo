import setuptools
from pathlib import Path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="todo-app",
    version="0.1.0",
    author="Todo App Team",
    author_email="team@todoapp.com",
    description="A console-based todo application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/todoapp/todo-app",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    entry_points={
        "console_scripts": [
            "todo=src.cli.main:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/todoapp/todo-app/issues",
        "Source": "https://github.com/todoapp/todo-app",
    },
)