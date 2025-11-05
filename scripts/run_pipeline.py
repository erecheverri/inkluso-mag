"""
Orchestrator script for the Inkluso Magazine pipeline.

This script reads a brief YAML file describing an issue and generates draft articles using Agent Mode.
"""
import argparse
import pathlib
import sys
import yaml
from agents.agent_mode import run_agent

def generate_article(issue, slug, title_hint, bullets):
    bullet_text = ""
    if bullets:
        bullet_text = "\n".join(f"- {b}" for b in bullets)
    prompt = (
        f"Write a magazine article with the working title '{title_hint}' for issue {issue}. "
        f"The article should cover the following points:\n{bullet_text}\n\n"
        "Respond in Markdown format with an engaging introduction, thoughtful body, and conclusion."
    )
    content = run_agent(prompt)
    return f"# {title_hint}\n\n{content.strip()}\n"


def main(brief_path):
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
