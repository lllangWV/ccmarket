#!/bin/bash
# RS Loop - runs RS_LOOP_PROMPT.md through Claude in an infinite loop
# Source: plugins/ralph/scripts/run_rs_loop.sh
#
# Usage: ./run_rs_loop.sh <topic> [model]
#   topic: Research goal/topic (required)
#   model: opus (default), sonnet, or haiku

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BRANCH=$(git rev-parse --abbrev-ref HEAD)
TOPIC="${1:?Error: Please provide a research topic as the first argument}"
MODEL="${2:-opus}"

echo "Starting RS loop..."
echo "  Branch: $BRANCH"
echo "  Topic: $TOPIC"
echo "  Model: $MODEL"
echo "  Prompt: $SCRIPT_DIR/RS_LOOP_PROMPT.md"
echo "  Press Ctrl+C to stop"
echo ""

while true; do
    (cat "$SCRIPT_DIR/RS_LOOP_PROMPT.md"; echo -e "\n\nResearch goal: $TOPIC") | claude -p \
        --dangerously-skip-permissions \
        --output-format=stream-json \
        --model "$MODEL" \
        --verbose \
        | bunx repomirror visualize

    git push origin "$BRANCH"

    echo -e "\n\n======================== LOOP COMPLETE ========================\n\n"
done
