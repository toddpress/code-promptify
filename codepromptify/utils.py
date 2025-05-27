import subprocess
from pathlib import Path
from typing import List, Tuple
from fnmatch import fnmatch

PROMPTIGNORE_DEFAULT = ['.git', 'node_modules', '__pycache__', '*.lock', '*.log', 'dist', 'build', '.venv', '.env']
ALLOWED_EXTENSIONS = {'.py', '.js', '.ts', '.jsx', '.tsx', '.json', '.html', '.css', '.md'}

def load_promptignore(path: Path) -> List[str]:
    ignore_file = path / ".promptignore"
    patterns = PROMPTIGNORE_DEFAULT[:]
    if ignore_file.exists():
        patterns += ignore_file.read_text().splitlines()
    return patterns

def is_ignored(path: Path, patterns: List[str]) -> bool:
    rel = str(path)
    return any(fnmatch(rel, pat) for pat in patterns)

def collect_files_promptaware(root: Path) -> List[Tuple[Path, str]]:
    patterns = load_promptignore(root)
    collected = []
    for path in root.rglob("*"):
        if is_ignored(path.relative_to(root), patterns):
            continue
        if path.is_file() and path.suffix in ALLOWED_EXTENSIONS:
            try:
                collected.append((path.relative_to(root), path.read_text(encoding="utf-8")))
            except Exception:
                continue
    return collected

def detect_stack(files: List[Tuple[Path, str]]) -> str:
    langs = set()
    deps = []
    for path, _ in files:
        if path.suffix == ".py":
            langs.add("Python")
        if path.suffix in {".js", ".jsx", ".ts", ".tsx"}:
            langs.add("JavaScript/TypeScript")
        if path.name == "package.json":
            deps.append("Node.js")
        if path.name == "requirements.txt":
            deps.append("Python deps (Flask/FastAPI/etc)")
        if path.name == "Dockerfile":
            deps.append("Docker")
        if "tailwind" in path.name.lower():
            deps.append("Tailwind CSS")
    return "\n".join(f"- {x}" for x in sorted(langs | set(deps)))

def summarize_architecture(files: List[Tuple[Path, str]]) -> dict:
    modules = set()
    for path, _ in files:
        parts = list(path.parts)
        if "services" in parts or "routes" in parts:
            modules.add("Routing / Services")
        if "models" in parts or "schemas" in parts:
            modules.add("Data Models")
        if "components" in parts or path.suffix in {".tsx", ".jsx"}:
            modules.add("Frontend UI")

    desc = "This app uses a modular design with APIs, logic, and components."
    diagram = """flowchart TD
    UI[Frontend] --> API[API Layer]
    API --> Logic[Business Logic]
    Logic --> DB[(Database)]
    Logic --> Ext[External Services]
    """

    return {
        "description": desc,
        "diagram": diagram,
        "components": "\n".join(f"- {m}" for m in sorted(modules)),
    }

def generate_prompt(files: List[Tuple[Path, str]], stack: str, arch: dict) -> str:
    filenames = "\n".join(str(f[0]) for f in files[:50])
    return f"""
You are a software architect. Given this stack:
{stack}

Initial summary:
{arch['description']}

Files:
{filenames}

Rewrite a more complete architecture summary. Include mermaid diagram and improved stack if appropriate. Format as markdown.
"""

def list_ollama_models() -> List[str]:
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        return [line.split()[0] for line in result.stdout.strip().splitlines()[1:]]
    except Exception:
        return []

def ollama_enrich(prompt: str, model: str) -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            text=True,
            capture_output=True,
        )
        return result.stdout.strip()
    except Exception as e:
        return f"[ERROR running Ollama: {e}]"

def generate_basic_readme(name: str, stack: str, arch: dict) -> str:
    return f"""# {name}

## Tech Stack
{stack}

## Application Architecture
{arch['description']}

```mermaid
{arch['diagram']}
Key Components
{arch['components']}
"""
