"""
Orchestrator script for the Inkluso Magazine pipeline.

This script reads a brief YAML file describing an issue (date, article slugs, titles, and bullet points)
and generates draft articles using the Agent Mode delegate in `agents/agent_mode.py`.  It then writes
the drafts to the `content/drafts/<issue>/<slug>/draft.md` directories.

To run:

    python scripts/run_pipeline.py --brief content/briefs/2025-11-issue.yml

The script expects the following environment variables:
    OPENAI_API_KEY  – your OpenAI API key
    OPENAI_MODEL    – the model name (defaults to gpt-5-reasoning)

Additional agent endpoints can be integrated by modifying this file to call your XTKA, LOTI,
SIG1, Goblino, and GMTK services.  For now, all content generation is delegated to the
`run_agent` function provided in `agents/agent_mode.py`.
"""
import argparse
import pathlib
import os
import sys

import yaml

from agents.agent_mode import run_agent


def generate_article(issue: str, slug: str, title_hint: str, bullets: list[str] | None) -> str:
    """Generate a draft article using Agent Mode.

    Parameters
    ----------
    issue : str
        The issue date (e.g., "2025-11").
    slug : str
        A short slug identifying the article (e.g., "editorial").
    title_hint : str
        A hint for the article’s title.
    bullets : list[str] | None
        Bullet points describing what to cover in the article.

    Returns
    -------
    str
        Markdown content of the draft article.
    """
    bullet_text = ""
    if bullets:
        bullet_text = "\n".join(f"- {b}" for b in bullets)
    prompt = (
        f"Write a magazine article with the working title '{title_hint}' for issue {issue}. "
        f"The article should cover the following points:\n{bullet_text}\n\n"
        "Respond in Markdown format with an engaging introduction, thoughtful body, and conclusion."
    )
    print(f"[INFO] Generating article for slug='{slug}' with title hint='{title_hint}'...")
    content = run_agent(prompt)
    return f"# {title_hint}\n\n{content.strip()}\n"


def main(brief_path: str) -> None:
    # Load brief YAML
    with open(brief_path, 'r') as f:
        brief = yaml.safe_load(f)

    issue = brief.get('issue')
    articles = brief.get('articles', [])
    if not issue or not articles:
        print(f"Error: Brief '{brief_path}' is missing 'issue' or 'articles'.", file=sys.stderr)
        sys.exit(1)

    for article in articles:
        slug = article['slug']
        title_hint = article.get('title_hint', slug.replace('-', ' ').title())
        bullets = article.get('bullets', [])
        draft = generate_article(issue, slug, title_hint, bullets)
        out_dir = pathlib.Path('content/drafts') / issue / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        draft_path = out_dir / 'draft.md'
        with open(draft_path, 'w') as out_file:
            out_file.write(draft)
        print(f"[INFO] Wrote draft to {draft_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate drafts for Inkluso Magazine.')
    parser.add_argument('--brief', required=True, help='Path to the brief YAML file.')
    args = parser.parse_args()
    main(args.brief)