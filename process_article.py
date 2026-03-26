#!/usr/bin/env python3
"""Fetch a URL, extract clean article text, generate audio, update manifest."""

import os, re, json, sys, time
from pathlib import Path
from urllib.request import Request, urlopen
from datetime import datetime

BASE_DIR = Path(__file__).parent
ARTICLES_DIR = BASE_DIR / "articles"
AUDIO_DIR = BASE_DIR / "docs" / "audio"
ARTICLES_DIR.mkdir(exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Load API key from environment or .env
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text().strip().split("\n"):
            if line.startswith("OPENAI_API_KEY="):
                api_key = line.split("=", 1)[1].strip()
                break

if not api_key:
    print("ERROR: No OPENAI_API_KEY found")
    sys.exit(1)


def extract_article(url):
    """Fetch URL and extract clean article text using trafilatura."""
    import trafilatura

    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        raise Exception(f"Failed to fetch: {url}")

    metadata = trafilatura.extract_metadata(downloaded)
    text = trafilatura.extract(
        downloaded,
        include_comments=False,
        include_tables=False,
        no_fallback=False,
        favor_recall=True,
    )

    if not text:
        raise Exception(f"No article text extracted from: {url}")

    title = metadata.title if metadata and metadata.title else "Untitled"
    author = metadata.author if metadata and metadata.author else ""

    # Strip common cruft trafilatura may leave behind
    cruft = [
        r"(?i)subscribe to .*?newsletter.*?\n",
        r"(?i)sign up for .*?\n",
        r"(?i)get .* delivered to your inbox.*?\n",
        r"(?i)share this post.*?\n",
        r"(?i)leave a comment.*?\n",
        r"(?i)like this post.*?\n",
        r"(?i)thanks for reading.*?[!\n]",
        r"(?i)if you enjoyed this.*?\n",
        r"(?i)click here to .*?\n",
        r"(?i)follow .* on (?:twitter|x).*?\n",
        r"(?i)(?:^|\n)share\n",
        r"(?i)(?:^|\n)advertisement\n",
        r"(?i)sponsored content.*?\n",
        r"(?i)related articles.*?\n",
        r"(?i)read more:.*?\n",
        r"(?i)already a .*?subscriber.*?\n",
        r"(?i)this post is for .*?subscribers.*?\n",
        r"(?i)\d+ likes?\n",
        r"(?i)\d+ comments?\n",
        r"(?i)\d+ shares?\n",
        r"©.*?\d{4}.*?\n",
    ]
    for pattern in cruft:
        text = re.sub(pattern, "\n", text)

    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip(), title, author


def make_slug(title):
    """Create a URL-safe slug from a title."""
    slug = re.sub(r"[^a-zA-Z0-9\s-]", "", title.lower())
    slug = re.sub(r"[\s-]+", "-", slug).strip("-")
    return slug[:80]


def split_text(text, max_chars=3500):
    """Split text into chunks at sentence boundaries."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks, current = [], ""
    for s in sentences:
        if len(current) + len(s) + 1 > max_chars and current:
            chunks.append(current.strip())
            current = s
        else:
            current = current + " " + s if current else s
    if current.strip():
        chunks.append(current.strip())
    return chunks


def tts_chunk(text, output_path):
    """Call OpenAI TTS API for a single chunk with retry."""
    payload = json.dumps({
        "model": "tts-1-hd",
        "input": text,
        "voice": "onyx",
        "speed": 0.95,
    }).encode("utf-8")

    for attempt in range(6):
        try:
            req = Request(
                "https://api.openai.com/v1/audio/speech",
                data=payload,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
            )
            resp = urlopen(req, timeout=180)
            data = resp.read()
            break
        except Exception as e:
            wait = 2 ** attempt * 2
            print(f"  Retry {attempt + 1}/6, waiting {wait}s... ({e})")
            time.sleep(wait)
            if attempt == 5:
                raise
    else:
        raise Exception("Failed after 6 retries")

    if data[:1] == b"{":
        raise Exception(f"API error: {json.loads(data)}")

    with open(output_path, "wb") as f:
        f.write(data)
    return len(data)


def generate_audio(text, slug):
    """Generate concatenated MP3 from text chunks."""
    output = AUDIO_DIR / f"{slug}.mp3"

    chunks = split_text(text)
    print(f"  {len(chunks)} chunks ({len(text)} chars)")

    chunk_files = []
    for i, chunk in enumerate(chunks):
        chunk_path = AUDIO_DIR / f"_{slug}_chunk_{i:03d}.mp3"
        if chunk_path.exists() and chunk_path.stat().st_size > 1000:
            print(f"    Chunk {i + 1}/{len(chunks)} (cached)")
            chunk_files.append(chunk_path)
            continue
        print(f"    Chunk {i + 1}/{len(chunks)} ({len(chunk)} chars)...", end=" ", flush=True)
        size = tts_chunk(chunk, chunk_path)
        print(f"{size // 1024}KB")
        chunk_files.append(chunk_path)
        time.sleep(2)  # rate limit courtesy

    with open(output, "wb") as out:
        for cf in chunk_files:
            out.write(cf.read_bytes())
            cf.unlink()

    size_mb = output.stat().st_size / (1024 * 1024)
    print(f"  Done: {output.name} ({size_mb:.1f} MB)")
    return output


def update_manifest(slug, title, author, source_url):
    """Add or update entry in articles-manifest.json."""
    manifest_path = BASE_DIR / "docs" / "articles-manifest.json"

    manifest = []
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())

    # Update existing or insert at top
    for entry in manifest:
        if entry.get("slug") == slug:
            entry.update(title=title, author=author, url=source_url,
                         date=datetime.now().strftime("%-d %B %Y"))
            break
    else:
        manifest.insert(0, {
            "slug": slug,
            "title": title,
            "author": author,
            "url": source_url,
            "file": f"{slug}.mp3",
            "date": datetime.now().strftime("%-d %B %Y"),
        })

    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"  Manifest updated: {len(manifest)} articles")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: process_article.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    print(f"\nFetching: {url}")

    text, title, author = extract_article(url)
    slug = make_slug(title)

    print(f"  Title: {title}")
    if author:
        print(f"  Author: {author}")
    print(f"  Length: {len(text)} chars")

    # Save extracted text for reference
    (ARTICLES_DIR / f"{slug}.txt").write_text(
        f"Title: {title}\nAuthor: {author}\nURL: {url}\n\n{text}"
    )

    print(f"\nGenerating audio...")
    generate_audio(text, slug)
    update_manifest(slug, title, author, url)
    print("\nDone!")
