# Inkluso Magazine

This repository contains the scaffolding for **Inkluso Magazine**, an automated magazine built on GitHub.  When a new brief (a short YAML file describing an issue’s articles) is added to the `content/briefs` directory and the **Inkluso Agents Pipeline** workflow is run, the pipeline will use your configured agents (or fall back to OpenAI’s Agent Mode) to generate drafts, enrich them with fresh research, and package them for publication.

## Repository Layout

- `.github/workflows/generate_content.yml` – GitHub Actions workflow that reads a brief, triggers your agents (or my Agent Mode) to draft and enrich articles, and opens a pull request with the generated drafts.
- `.github/workflows/build_and_deploy.yml` – workflow that builds the static site and PDF after a pull request is merged to `main`.  It publishes the site via GitHub Pages and attaches a PDF release.
- `agents/agent_mode.py` – a helper module that calls OpenAI’s chat completions API.  It acts as a generic Agent Mode delegate for any online research tasks.
- `scripts/run_pipeline.py` – orchestrates the pipeline: it reads a brief YAML file, loops through its articles, calls Agent Mode to generate content, and writes drafts to `content/drafts/<issue>/<slug>/draft.md`.
- `requirements.txt` – Python dependencies for the pipeline.
- `content/` – contains input briefs and generated drafts.
- `runbook.md` – step‑by‑step instructions for using this repository.

## Getting Started

1. [Create a new GitHub repository](https://github.com/new) and import these files (you can upload them directly using the GitHub UI).
2. In your repository settings, add the following **Secrets** under **Settings → Secrets → Actions**:
   - `OPENAI_API_KEY`: your OpenAI API key (used for Agent Mode).
   - `OPENAI_MODEL`: the model name, e.g. `gpt-5-reasoning`.
   - You can add additional secrets for XTKA, LOTI, SIG1, Goblino, and GMTK when they are ready.
3. Place a brief YAML file in `content/briefs/` (see the example in this repo).
4. From the **Actions** tab, run the **Inkluso Agents Pipeline** workflow and merge the resulting pull request to the `dev` branch.
5. Merge `dev` into `main` to trigger the **Build and Deploy** workflow.

For detailed, step‑by‑step instructions, see [runbook.md](runbook.md).
