from setuptools import setup, find_packages

setup(
    name="codepromptify",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "rich",
        "questionary",
        "streamlit",
        "argparse",
        "streamlit-mermaid",
        "pathlib"
    ],
    entry_points={
        "console_scripts": [
            "codepromptify=codepromptify.main:main",
        ],
    },
)
