#!/usr/bin/env python3
"""
wiki_cron.py — OpenClaw automation for the investment research wiki.

Usage:
    python3 wiki_cron.py detect    # Detect new raw analyses without wiki pages
    python3 wiki_cron.py lint      # Run wiki health checks
    python3 wiki_cron.py notify    # Send Telegram notification with status

Environment variables:
    TELEGRAM_BOT_TOKEN  — Telegram bot token
    TELEGRAM_CHAT_ID    — Telegram chat ID for notifications
"""

import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

REPO = Path(__file__).parent
WIKI = REPO / "wiki"
COMPANIES_DIR = WIKI / "companies"
METADATA_FILE = WIKI / "company_metadata.json"
LINT_DIR = WIKI / "linting"


def slug(name):
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def get_raw_analyses():
    """Find all raw analysis .md files."""
    files = {}
    for f in sorted(REPO.glob("*.md")):
        name = f.name
        if name.endswith("-qanalysis.md"):
            company = name.replace("-qanalysis.md", "")
            key = company.lower()
            files[key] = {"company": company, "file": name, "type": "qanalysis"}
        elif name.endswith("-analysis.md"):
            company = name.replace("-analysis.md", "")
            key = company.lower()
            if key not in files:
                files[key] = {"company": company, "file": name, "type": "analysis"}
    return files


def get_wiki_pages():
    """List all existing wiki company pages."""
    if not COMPANIES_DIR.exists():
        return set()
    return {f.stem for f in COMPANIES_DIR.glob("*.md")}


def detect_new():
    """Detect raw analyses that don't have corresponding wiki pages."""
    raw = get_raw_analyses()
    wiki = get_wiki_pages()
    missing = []
    for key, info in sorted(raw.items()):
        s = slug(info["company"])
        if s not in wiki:
            missing.append(info)
    return missing


def lint_check():
    """Run comprehensive wiki health checks."""
    issues = []

    # 1. Orphan detection: wiki pages without raw files
    raw = get_raw_analyses()
    raw_slugs = {slug(info["company"]) for info in raw.values()}
    wiki = get_wiki_pages()
    orphans = wiki - raw_slugs
    if orphans:
        issues.append(f"Orphan wiki pages (no raw analysis): {', '.join(sorted(orphans))}")

    # 2. Missing wiki pages
    missing = detect_new()
    if missing:
        issues.append(f"Raw analyses without wiki pages: {', '.join(m['company'] for m in missing)}")

    # 3. Stale data check (>6 months)
    six_months_ago = datetime.now() - timedelta(days=180)
    stale = []
    for f in COMPANIES_DIR.glob("*.md"):
        try:
            content = f.read_text()
            date_match = re.search(r"last_updated:\s*(\d{4}-\d{2}-\d{2})", content)
            if date_match:
                last_updated = datetime.strptime(date_match.group(1), "%Y-%m-%d")
                if last_updated < six_months_ago:
                    stale.append(f.stem)
        except Exception:
            pass
    if stale:
        issues.append(f"Stale wiki pages (>6 months): {', '.join(sorted(stale))}")

    # 4. Broken wikilinks
    all_wiki_files = set()
    for d in [COMPANIES_DIR, WIKI / "sectors", WIKI / "regions", WIKI / "concepts", WIKI / "comparisons"]:
        if d.exists():
            all_wiki_files.update(f"{d.name}/{f.stem}" for f in d.glob("*.md"))

    broken_links = []
    for d in [COMPANIES_DIR, WIKI / "sectors", WIKI / "regions", WIKI / "concepts", WIKI / "comparisons"]:
        if not d.exists():
            continue
        for f in d.glob("*.md"):
            content = f.read_text()
            links = re.findall(r"\[\[wiki/(\w+/[\w-]+)", content)
            for link in links:
                if link not in all_wiki_files:
                    broken_links.append(f"{f.name}: [[wiki/{link}]]")
    if broken_links:
        issues.append(f"Broken wikilinks ({len(broken_links)}): {'; '.join(broken_links[:10])}")

    # 5. Missing frontmatter
    no_frontmatter = []
    for f in COMPANIES_DIR.glob("*.md"):
        content = f.read_text()
        if not content.startswith("---"):
            no_frontmatter.append(f.stem)
    if no_frontmatter:
        issues.append(f"Missing frontmatter: {', '.join(sorted(no_frontmatter))}")

    # 6. Concept coverage
    if METADATA_FILE.exists():
        with open(METADATA_FILE) as mf:
            metadata = json.load(mf)
        concept_files = list((WIKI / "concepts").glob("*.md"))
        concept_count = len([f for f in concept_files if f.stem != "_index"])
        if concept_count < 10:
            issues.append(f"Low concept coverage: only {concept_count} concept pages (target: 10+)")

    return issues


def generate_lint_report():
    """Generate and save a lint report."""
    LINT_DIR.mkdir(parents=True, exist_ok=True)
    issues = lint_check()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"# Wiki Lint Report",
        f"",
        f"**Generated:** {timestamp}",
        f"",
    ]

    if not issues:
        lines.append("All checks passed. No issues found.")
    else:
        lines.append(f"**{len(issues)} issue(s) found:**")
        lines.append("")
        for i, issue in enumerate(issues, 1):
            lines.append(f"{i}. {issue}")

    # Stats
    wiki_pages = len(get_wiki_pages())
    raw_files = len(get_raw_analyses())
    lines.extend([
        "",
        "---",
        "",
        "## Stats",
        f"- Raw analyses: {raw_files}",
        f"- Wiki company pages: {wiki_pages}",
        f"- Coverage: {wiki_pages}/{raw_files} ({100*wiki_pages//max(raw_files,1)}%)",
    ])

    report_path = LINT_DIR / f"lint-{datetime.now().strftime('%Y-%m-%d')}.md"
    report_path.write_text("\n".join(lines))
    return report_path, issues


def send_telegram(message):
    """Send a Telegram notification."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID not set. Skipping notification.")
        return False

    import urllib.request
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = json.dumps({"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

    try:
        urllib.request.urlopen(req)
        return True
    except Exception as e:
        print(f"Telegram send failed: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 wiki_cron.py [detect|lint|notify]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "detect":
        missing = detect_new()
        if missing:
            print(f"Found {len(missing)} raw analyses without wiki pages:")
            for m in missing:
                print(f"  - {m['company']} ({m['file']})")
            msg = f"*Wiki Update Needed*\n{len(missing)} new analysis(es) detected without wiki pages:\n"
            msg += "\n".join(f"- {m['company']}" for m in missing)
            send_telegram(msg)
        else:
            print("All raw analyses have corresponding wiki pages.")

    elif cmd == "lint":
        report_path, issues = generate_lint_report()
        print(f"Lint report saved to {report_path}")
        if issues:
            print(f"\n{len(issues)} issue(s) found:")
            for issue in issues:
                print(f"  - {issue}")
            msg = f"*Weekly Wiki Lint*\n{len(issues)} issue(s) found:\n"
            msg += "\n".join(f"- {issue[:100]}" for issue in issues)
            send_telegram(msg)
        else:
            print("All checks passed!")
            send_telegram("*Weekly Wiki Lint*\nAll checks passed. Wiki is healthy.")

    elif cmd == "notify":
        wiki_pages = len(get_wiki_pages())
        raw_files = len(get_raw_analyses())
        msg = f"*Wiki Status*\n{wiki_pages} wiki pages covering {raw_files} raw analyses ({100*wiki_pages//max(raw_files,1)}% coverage)"
        if send_telegram(msg):
            print("Notification sent.")
        else:
            print(msg)

    else:
        print(f"Unknown command: {cmd}")
        print("Usage: python3 wiki_cron.py [detect|lint|notify]")
        sys.exit(1)


if __name__ == "__main__":
    main()
