#!/usr/bin/env python3
"""Generate MP3 audio from investment research markdown files using OpenAI TTS."""

import os, re, json, sys, time
from pathlib import Path
from urllib.request import Request, urlopen

BASE_DIR = Path(__file__).parent
AUDIO_DIR = BASE_DIR / "audio"
AUDIO_DIR.mkdir(exist_ok=True)

# Load API key
env_file = BASE_DIR / ".env"
api_key = None
for line in env_file.read_text().strip().split("\n"):
    if line.startswith("OPENAI_API_KEY="):
        api_key = line.split("=", 1)[1].strip()
        break

if not api_key:
    print("ERROR: No OPENAI_API_KEY found in .env")
    sys.exit(1)

def clean_markdown(text):
    """Strip markdown formatting for cleaner speech."""
    text = re.sub(r'^---+\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'```[^`]*```', '', text, flags=re.DOTALL)
    text = re.sub(r'^\s*[-*]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def split_text(text, max_chars=3500):
    """Split text into chunks at sentence boundaries."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current = ""
    for s in sentences:
        if len(current) + len(s) + 1 > max_chars and current:
            chunks.append(current.strip())
            current = s
        else:
            current = current + " " + s if current else s
    if current.strip():
        chunks.append(current.strip())
    return chunks

def tts_chunk(text, output_path, api_key):
    """Call OpenAI TTS API for a single chunk."""
    payload = json.dumps({
        "model": "tts-1-hd",
        "input": text,
        "voice": "onyx",
        "speed": 0.95
    }).encode("utf-8")

    req = Request(
        "https://api.openai.com/v1/audio/speech",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )

    for attempt in range(6):
        try:
            fresh_req = Request(
                "https://api.openai.com/v1/audio/speech",
                data=payload,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
            )
            resp = urlopen(fresh_req, timeout=180)
            data = resp.read()
            break
        except Exception as e:
            wait = 2 ** attempt * 2
            err_str = str(e)
            if '429' in err_str or 'Too Many' in err_str:
                print(f"rate limited, waiting {wait}s...", end=" ", flush=True)
            elif 'IncompleteRead' in err_str or 'timeout' in err_str.lower():
                print(f"connection error, retrying in {wait}s...", end=" ", flush=True)
            else:
                print(f"error: {err_str}, retrying in {wait}s...", end=" ", flush=True)
            time.sleep(wait)
            if attempt == 5:
                raise
    else:
        raise Exception("Failed after 6 retries")

    # Check if it's an error (JSON response instead of audio)
    if data[:1] == b'{':
        error = json.loads(data)
        raise Exception(f"API error: {error}")

    with open(output_path, 'wb') as f:
        f.write(data)
    return len(data)

def generate_report_audio(md_file):
    """Generate audio for a single report."""
    name = md_file.stem
    output = AUDIO_DIR / f"{name}.mp3"

    # Skip if up to date
    if output.exists() and output.stat().st_mtime > md_file.stat().st_mtime:
        print(f"  Skipping {name} (up to date)")
        return output

    print(f"  Processing: {name}")
    text = clean_markdown(md_file.read_text())
    chunks = split_text(text)
    print(f"  Split into {len(chunks)} chunks ({len(text)} chars total)")

    chunk_files = []
    tag = re.sub(r'[^a-zA-Z0-9]', '_', name)
    for i, chunk in enumerate(chunks):
        chunk_path = AUDIO_DIR / f"_{tag}_chunk_{i:03d}.mp3"
        if chunk_path.exists() and chunk_path.stat().st_size > 1000:
            print(f"    Chunk {i+1}/{len(chunks)} (cached)")
            chunk_files.append(chunk_path)
            continue
        print(f"    Chunk {i+1}/{len(chunks)} ({len(chunk)} chars)...", end=" ", flush=True)
        size = tts_chunk(chunk, chunk_path, api_key)
        print(f"{size // 1024}KB")
        chunk_files.append(chunk_path)
        time.sleep(2)  # Rate limit courtesy

    # Concatenate chunks
    with open(output, 'wb') as out:
        for cf in chunk_files:
            out.write(cf.read_bytes())
            cf.unlink()  # Clean up chunk

    size_mb = output.stat().st_size / (1024 * 1024)
    print(f"  Done: {output.name} ({size_mb:.1f} MB)")
    return output

def generate_manifest(audio_files):
    """Create manifest.json for the web player — includes ALL audio files in docs/audio/."""
    manifest = []
    emojis = {"SK Hynix": "🇰🇷", "TSMC": "🇹🇼", "Tencent": "🇨🇳", "HDFC Bank": "🇮🇳"}

    docs_audio = BASE_DIR / "docs" / "audio"
    docs_audio.mkdir(parents=True, exist_ok=True)

    # Include all MP3s in docs/audio, not just the ones generated this run
    all_audio = set(docs_audio.glob("*-analysis.mp3"))
    for f in audio_files:
        all_audio.add(f)

    for f in sorted(all_audio, key=lambda x: x.name):
        name = f.stem.replace("-analysis", "")
        manifest.append({
            "name": name,
            "file": f.name,
            "emoji": emojis.get(name, "📊"),
            "date": "15 March 2026"
        })

    docs_dir = BASE_DIR / "docs"
    # Also put audio in docs for GitHub Pages
    docs_audio = docs_dir / "audio"
    docs_audio.mkdir(parents=True, exist_ok=True)

    for f in audio_files:
        target = docs_audio / f.name
        import shutil
        shutil.copy2(f, target)

    manifest_path = docs_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"\n  Manifest written: {manifest_path}")
    print(f"  Audio copied to docs/audio/ for GitHub Pages")

if __name__ == "__main__":
    files = sys.argv[1:] if len(sys.argv) > 1 else None

    if files:
        md_files = [Path(f) for f in files]
    else:
        md_files = sorted(BASE_DIR.glob("*-analysis.md"))

    print(f"Generating audio for {len(md_files)} reports...\n")

    audio_files = []
    for md in md_files:
        result = generate_report_audio(md)
        if result:
            audio_files.append(result)

    generate_manifest(audio_files)
    print("\nAll done!")
