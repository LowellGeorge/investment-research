#!/bin/bash
# Generate MP3 audio from investment research markdown files using OpenAI TTS
# Usage: ./generate-audio.sh [filename.md]  (or no args to generate all)

set -e

cd "$(dirname "$0")"
source .env
mkdir -p audio

# OpenAI TTS has a 4096 character limit per request, so we chunk the text
generate_audio() {
    local md_file="$1"
    local base_name=$(basename "$md_file" .md)
    local output_file="audio/${base_name}.mp3"

    # Skip if audio already exists and is newer than the markdown
    if [ -f "$output_file" ] && [ "$output_file" -nt "$md_file" ]; then
        echo "  Skipping $base_name (audio is up to date)"
        return 0
    fi

    echo "  Generating audio for: $base_name"

    # Strip markdown formatting for cleaner speech
    local clean_text=$(sed \
        -e 's/^#\+\s*//' \
        -e 's/\*\*//g' \
        -e 's/\*//g' \
        -e 's/\[([^]]*)\]([^)]*)/\1/g' \
        -e 's/^- //' \
        -e 's/^[0-9]\+\. //' \
        -e '/^---$/d' \
        -e '/^```/,/^```/d' \
        -e '/^\s*$/d' \
        "$md_file")

    # Split into chunks of ~4000 chars (leaving room for JSON escaping)
    local chunk_dir=$(mktemp -d)
    echo "$clean_text" | fold -s -w 3800 | awk -v dir="$chunk_dir" '
    BEGIN { n=0; file=dir"/chunk_000.txt" }
    {
        if (length(content) + length($0) > 3800) {
            print content > file
            close(file)
            n++
            file = sprintf("%s/chunk_%03d.txt", dir, n)
            content = $0
        } else {
            content = content "\n" $0
        }
    }
    END { if (content) print content > file }
    '

    # Generate audio for each chunk
    local chunk_files=()
    for chunk in "$chunk_dir"/chunk_*.txt; do
        local chunk_num=$(basename "$chunk" .txt)
        local chunk_mp3="$chunk_dir/${chunk_num}.mp3"

        # JSON-escape the text
        local text_content=$(cat "$chunk" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")

        curl -s https://api.openai.com/v1/audio/speech \
            -H "Authorization: Bearer $OPENAI_API_KEY" \
            -H "Content-Type: application/json" \
            -d "{\"model\": \"tts-1-hd\", \"input\": $text_content, \"voice\": \"onyx\", \"speed\": 0.95}" \
            --output "$chunk_mp3"

        # Check for errors
        if file "$chunk_mp3" | grep -q "JSON"; then
            echo "    ERROR on chunk $chunk_num:"
            cat "$chunk_mp3"
            rm -rf "$chunk_dir"
            return 1
        fi

        chunk_files+=("$chunk_mp3")
        echo "    Generated chunk $chunk_num"
    done

    # Concatenate chunks using ffmpeg if available, otherwise cat (works for MP3)
    if command -v ffmpeg &>/dev/null; then
        local concat_list="$chunk_dir/concat.txt"
        for f in "${chunk_files[@]}"; do
            echo "file '$f'" >> "$concat_list"
        done
        ffmpeg -y -f concat -safe 0 -i "$concat_list" -c copy "$output_file" 2>/dev/null
    else
        cat "${chunk_files[@]}" > "$output_file"
    fi

    rm -rf "$chunk_dir"

    local size=$(ls -lh "$output_file" | awk '{print $5}')
    echo "  Done: $output_file ($size)"
}

# Process files
if [ -n "$1" ]; then
    generate_audio "$1"
else
    echo "Generating audio for all analysis reports..."
    for md_file in *-analysis.md; do
        [ -f "$md_file" ] && generate_audio "$md_file"
    done
fi

echo ""
echo "All audio files are in the audio/ directory."
