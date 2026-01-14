#!/bin/bash
# RSRPRI Loop - runs full RS → RP → RI pipeline in an infinite loop
# Source: plugins/ralph/scripts/run_rsrpri_loop.sh
#
# Usage: ./run_rsrpri_loop.sh <topic> [model]
#   topic: Research goal/topic for RS phase (required on first run)
#   model: opus (default), sonnet, or haiku
#
# The loop runs:
#   1. RS (Research-to-Specs) - research external docs, generate specs
#   2. RP (Research-Plan) - analyze code vs specs, update IMPLEMENTATION_PLAN.md
#   3. RI (Research-Implement) - implement highest priority task from plan

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BRANCH=$(git rev-parse --abbrev-ref HEAD)
TOPIC="${1:-}"
MODEL="${2:-opus}"

echo "Starting RSRPRI loop..."
echo "  Branch: $BRANCH"
echo "  Topic: ${TOPIC:-<will use existing specs>}"
echo "  Model: $MODEL"
echo "  Press Ctrl+C to stop"
echo ""

ITERATION=1

while true; do
    echo ""
    echo "================================================================================"
    echo "  ITERATION $ITERATION"
    echo "================================================================================"
    echo ""

    # Phase 1: RS (Research-to-Specs)
    echo ">>> Phase 1: RS (Research-to-Specs)"
    echo "--------------------------------------------------------------------------------"
    if [ -n "$TOPIC" ]; then
        (cat "$SCRIPT_DIR/RS_LOOP_PROMPT.md"; echo -e "\n\nResearch goal: $TOPIC") | claude -p \
            --dangerously-skip-permissions \
            --output-format=stream-json \
            --model "$MODEL" \
            --verbose \
            | bunx repomirror visualize
    else
        # If no topic, RS will check specs/README.md for pending research goals
        cat "$SCRIPT_DIR/RS_LOOP_PROMPT.md" | claude -p \
            --dangerously-skip-permissions \
            --output-format=stream-json \
            --model "$MODEL" \
            --verbose \
            | bunx repomirror visualize
    fi

    git push origin "$BRANCH" 2>/dev/null || true
    echo -e "\n>>> RS phase complete\n"

    # Phase 2: RP (Research-Plan)
    echo ">>> Phase 2: RP (Research-Plan)"
    echo "--------------------------------------------------------------------------------"
    cat "$SCRIPT_DIR/RP_LOOP_PROMPT.md" | claude -p \
        --dangerously-skip-permissions \
        --output-format=stream-json \
        --model "$MODEL" \
        --verbose \
        | bunx repomirror visualize

    git push origin "$BRANCH" 2>/dev/null || true
    echo -e "\n>>> RP phase complete\n"

    # Phase 3: RI (Research-Implement)
    echo ">>> Phase 3: RI (Research-Implement)"
    echo "--------------------------------------------------------------------------------"
    cat "$SCRIPT_DIR/RI_LOOP_PROMPT.md" | claude -p \
        --dangerously-skip-permissions \
        --output-format=stream-json \
        --model "$MODEL" \
        --verbose \
        | bunx repomirror visualize

    git push origin "$BRANCH" 2>/dev/null || true
    echo -e "\n>>> RI phase complete\n"

    echo ""
    echo "======================== ITERATION $ITERATION COMPLETE ========================"
    echo ""

    ITERATION=$((ITERATION + 1))
done
