# 🦄 CodePromptify

[![PyPI](https://img.shields.io/pypi/v/codepromptify.svg)](https://pypi.org/project/codepromptify/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/toddpress/codepromptify)](https://github.com/toddpress/codepromptify/releases)
[![CI](https://github.com/toddpress/codepromptify/actions/workflows/release.yml/badge.svg)](https://github.com/toddpress/codepromptify/actions/workflows/release.yml)

> Generate architecture-aware README.md files from your codebase using local LLMs via e.g. Ollama.

---

## Features

- [WIP] - Detects tech stack and architecture
- Recursively scans your codebase (with `.promptignore` support)
- Generates Markdown README with Mermaid diagrams
- Uses **Ollama** to refine summaries and stack descriptions
- Run via
  - _sweet_ CLI or
  - beautiful Streamlit GUI
- (coming soon) Generates promptable summaries of your codebase

---

## Installation

```bash
pip install -e .
```

---

## Usage

### CLI Mode (interactive)

```bash
codepromptify
```

### GUI Mode (Streamlit)

Launch a web interface to guide you through `code-promptify`-ing your code.

```bash
codepromptify --gui
```

### Advanced

```bash
codepromptify --path ./myproject --output docs/README.md
```

---

## .promptignore

Supports `.promptignore` like `.gitignore`.

Example:

```txt
node_modules/
*.test.js
build/
.env
```

---

## Requirements

* Python 3.9+
* (Optional) [Ollama](https://ollama.com/) with local models like `llama3`, `gemma`, etc.

---

## License

MIT

---
