#!/bin/bash
# RP Loop - runs RP_LOOP_PROMPT.md through Claude in an infinite loop
# Source: plugins/ralph/scripts/run_rp_loop.sh
#
# Usage: ./run_rp_loop.sh [model]
#   model: opus (default), sonnet, or haiku

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BRANCH=$(git rev-parse --abbrev-ref HEAD)
MODEL="${1:-opus}"

echo "Starting RP loop..."
echo "  Branch: $BRANCH"
echo "  Model: $MODEL"
echo "  Prompt: $SCRIPT_DIR/RP_LOOP_PROMPT.md"
echo "  Press Ctrl+C to stop"
echo ""

while true; do
    cat "$SCRIPT_DIR/RP_LOOP_PROMPT.md" | claude -p \
        --dangerously-skip-permissions \
        --output-format=stream-json \
        --model "$MODEL" \
        --verbose \
        | bunx repomirror visualize

    git push origin "$BRANCH"

    echo -e "\n\n======================== LOOP COMPLETE ========================\n\n"
done
