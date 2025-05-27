import streamlit as st
from streamlit_mermaid import st_mermaid

from pathlib import Path
from .utils import (
    collect_files_promptaware,
    detect_stack,
    summarize_architecture,
    generate_prompt,
    list_ollama_models,
    ollama_enrich,
    generate_basic_readme
)

def run():
    st.title("🦄 CodePromptify GUI")
    st.markdown("Summon a README from your codebase with architecture summaries and Mermaid diagrams.")

    codebase_path = st.text_input("Path to your codebase", value=str(Path.cwd()))
    run_button = st.button("Analyze and Generate")

    if run_button:
        root = Path(codebase_path).expanduser().resolve()
        files = collect_files_promptaware(root)

        if not files:
            st.error("No valid files found. Check path or .promptignore.")
            return

        stack_info = detect_stack(files)
        arch = summarize_architecture(files)
        prompt = generate_prompt(files, stack_info, arch)

        st.subheader("Initial Stack")
        st.code(stack_info)
        st.subheader("Architecture Summary")
        st.markdown(arch["description"])
        st.markdown("---")
        st.subheader("Architecture Diagram")
        st.code(arch["diagram"], language="mermaid")

        with st.expander("Preview Mermaid Diagram"):
            mermaid_code = arch["diagram"] if arch["diagram"] else "graph TD;\n    A[Start] --> B[End];"
            mermaid_code = st.text_area("Mermaid Diagram", mermaid_code)
            try:
                st_mermaid(mermaid_code, height="500px") if arch["diagram"] else st.empty()
            except Exception as e:
                st.error(f"Error rendering Mermaid diagram: {e}")

        if st.checkbox("Use Ollama to improve summary"):
            models = list_ollama_models()
            if not models:
                st.warning("No models found in Ollama.")
                return
            model = st.selectbox("Choose Ollama Model", models)
            if st.button("Run with Ollama"):
                response = ollama_enrich(prompt, model)
                st.subheader("Improved README")
                st.markdown(response)
                if st.button("Save README.md"):
                    (root / "README.md").write_text(response)
                    st.success("README.md written!")

        else:
            readme = generate_basic_readme("README", stack_info, arch)
            st.subheader("Generated README (Basic)")
            st.markdown(readme)
            if st.button("Save README.md"):
                (root / "README.md").write_text(readme)
                st.success("README.md written!")
