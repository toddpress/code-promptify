# codepromptify.py
import argparse
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from .utils import (
    collect_files_promptaware,
    detect_stack,
    summarize_architecture,
    generate_prompt,
    list_ollama_models,
    ollama_enrich,
    generate_basic_readme
)

console = Console()

def interactive_terminal_mode(codebase_path: Path, output_path: Path):
    import questionary
    files = collect_files_promptaware(codebase_path)
    stack_info = detect_stack(files)
    arch = summarize_architecture(files)

    use_llm = questionary.confirm("Use Ollama to improve the summary?").ask()
    if use_llm:
        models = list_ollama_models()
        if not models:
            console.print("[red]No Ollama models found. Skipping LLM enrichment.[/red]")
        else:
            questionary.print(f"\nAvailable models: {', '.join(models)}", style="bold italic")
            model = questionary.text("Which Ollama model to use?").ask()
            while True:
                prompt = generate_prompt(files, stack_info, arch)
                enriched = ollama_enrich(prompt, model)

                console.rule("Generated README (Preview)")
                console.print(Markdown(enriched))
                action = questionary.select("Next action", choices=["Accept", "Try another model", "Abort"]).ask()

                if action == "Accept":
                    output_path.write_text(enriched)
                    console.print(f"[green]Saved to {output_path}[/green]")
                    return
                elif action == "Try another model":
                    model = questionary.select("Choose a model", choices=models).ask()
                else:
                    console.print("[yellow]Aborted. No file written.[/yellow]")
                    return

    # fallback
    readme = generate_basic_readme(output_path.stem, stack_info, arch)
    output_path.write_text(readme)
    console.print(f"[green]Saved to {output_path}[/green]")

def main():
    parser = argparse.ArgumentParser(
        description="🦄 CodePromptify — generate README.md files from your codebase using local LLMs (Ollama optional)",
        epilog="Example: python codepromptify.py --path ./myproject --output README.md"
    )
    parser.add_argument("--gui", action="store_true", help="Launch Streamlit GUI instead of CLI")
    parser.add_argument("--path", type=Path, default=Path("."), help="Path to codebase (default: current dir)")
    parser.add_argument("--output", type=Path, default=None, help="Output README file (default: README.md in codebase dir)")

    args = parser.parse_args()

    if args.gui:
        from .gui import run
        run()
    else:
        codebase = args.path.resolve()
        output_file = args.output or codebase / "README.md"
        interactive_terminal_mode(codebase, output_file)

if __name__ == "__main__":
    main()


# def interactive_terminal_mode(codebase_path: Path, output_path: Path):
#     files = collect_files_promptaware(codebase_path)
#     stack_info = detect_stack(files)
#     arch = summarize_architecture(files)

#     use_llm = questionary.confirm("Use Ollama to improve the summary?").ask()
#     if use_llm:
#         models = list_ollama_models()
#         if not models:
#             console.print("[red]No Ollama models found. Skipping LLM enrichment.[/red]")
#         else:
#             model = questionary.select("Choose an Ollama model", choices=models).ask()
#             while True:
#                 prompt = generate_prompt(files, stack_info, arch)
#                 enriched = ollama_enrich(prompt, model)

#                 console.rule("Generated README (Preview)")
#                 console.print(Markdown(enriched))
#                 action = questionary.select("Next action", choices=["Accept", "Try another model", "Abort"]).ask()

#                 if action == "Accept":
#                     output_path.write_text(enriched)
#                     console.print(f"[green]Saved to {output_path}[/green]")
#                     return
#                 elif action == "Try another model":
#                     model = questionary.select("Choose a model", choices=models).ask()
#                 else:
#                     console.print("[yellow]Aborted. No file written.[/yellow]")
#                     return

#     # fallback
#     readme = generate_basic_readme(output_path.stem, stack_info, arch)
#     output_path.write_text(readme)
#     console.print(f"[green]Saved to {output_path}[/green]")

# def print_help():
#     console.print("""
# [bold cyan]CodePromptify[/bold cyan] — generate architecture-aware READMEs from your codebase.

# [bold]Usage:[/bold]
#   python codepromptify.py                Interactive CLI (terminal prompts)
#   python codepromptify.py --gui         Launch Streamlit GUI
#   python codepromptify.py --help        Show this help message

# [bold]What it does:[/bold]
#   - Scans your codebase recursively
#   - Skips noise via `.promptignore`
#   - Detects tech stack and architecture
#   - Optionally uses Ollama to improve summaries
#   - Outputs a beautiful README with Mermaid diagrams

# [bold]Pro tip:[/bold] Add a .promptignore file to your repo to fine-tune exclusions.
#     """)

# def main():
#     if "--help" in sys.argv:
#         print_help()
#         return
#     elif "--gui" in sys.argv:
#         import gui
#         gui.run()
#         return

#     codebase = Path(questionary.path("Codebase directory?").ask() or ".").resolve()
#     output = questionary.text("Output filename?", default="README.md").ask()
#     interactive_terminal_mode(codebase, codebase / output)

if __name__ == "__main__":
    main()
