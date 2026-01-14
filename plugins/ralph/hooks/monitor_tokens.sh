#!/bin/bash
# PostToolUse hook to display context usage every N tool calls
# Configuration is loaded from monitor_tokens.conf.json

CONFIG_FILE="${CLAUDE_PLUGIN_ROOT}/hooks/monitor_tokens.conf.json"
STATE_DIR="${HOME}/.claude/context-usage-monitor-state"
DEBUG_LOG="${STATE_DIR}/debug.log"

mkdir -p "$STATE_DIR"

# Debug function
debug() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') | $1" >> "$DEBUG_LOG"
}

# Load configuration
load_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        PRINT_EVERY_N=5
        MAX_CONTEXT_PERCENT=75
        CONTEXT_WINDOW=200000
        BLOCK_AT_THRESHOLD=false
        return
    fi

    PRINT_EVERY_N=$(jq -r '.print_every_n // 5' "$CONFIG_FILE")
    MAX_CONTEXT_PERCENT=$(jq -r '.max_context_percent // 75' "$CONFIG_FILE")
    CONTEXT_WINDOW=$(jq -r '.context_window // 200000' "$CONFIG_FILE")
    BLOCK_AT_THRESHOLD=$(jq -r '.block_at_threshold // false' "$CONFIG_FILE")
}

load_config

# Read input
INPUT=$(cat)
debug "INPUT: $INPUT"
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty')
debug "SESSION_ID: $SESSION_ID"

if [ -z "$SESSION_ID" ]; then
    debug "EXIT: No session_id"
    exit 0
fi

# Track tool call count
COUNT_FILE="${STATE_DIR}/${SESSION_ID}.count"
COUNT=$(cat "$COUNT_FILE" 2>/dev/null || echo 0)
COUNT=$((COUNT + 1))
echo "$COUNT" > "$COUNT_FILE"

# Only print every N calls
debug "COUNT: $COUNT, PRINT_EVERY_N: $PRINT_EVERY_N"
if [ $((COUNT % PRINT_EVERY_N)) -ne 0 ]; then
    debug "EXIT: Not printing (count % N != 0)"
    exit 0
fi

# Get transcript path
TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path // empty')
debug "TRANSCRIPT_PATH from input: $TRANSCRIPT_PATH"
if [ -z "$TRANSCRIPT_PATH" ] || [ "$TRANSCRIPT_PATH" = "null" ]; then
    CWD=$(echo "$INPUT" | jq -r '.cwd // empty')
    debug "CWD: $CWD"
    if [ -n "$CWD" ]; then
        SAFE_CWD=$(echo "$CWD" | sed 's|[/_]|-|g')
        TRANSCRIPT_PATH="${HOME}/.claude/projects/${SAFE_CWD}/${SESSION_ID}.jsonl"
        debug "Computed TRANSCRIPT_PATH: $TRANSCRIPT_PATH"
    fi
fi

if [ ! -f "$TRANSCRIPT_PATH" ]; then
    debug "EXIT: Transcript file not found at $TRANSCRIPT_PATH"
    exit 0
fi
debug "Transcript file exists"

# Get usage data
LATEST_USAGE=$(tac "$TRANSCRIPT_PATH" | grep -m1 '"usage"' | jq -r '.message.usage // empty' 2>/dev/null)
debug "LATEST_USAGE: $LATEST_USAGE"

if [ -z "$LATEST_USAGE" ] || [ "$LATEST_USAGE" = "null" ]; then
    debug "EXIT: No usage data found"
    exit 0
fi

# Calculate context
CACHE_READ=$(echo "$LATEST_USAGE" | jq '.cache_read_input_tokens // 0')
CACHE_CREATE=$(echo "$LATEST_USAGE" | jq '.cache_creation_input_tokens // 0')
INPUT_TOKENS=$(echo "$LATEST_USAGE" | jq '.input_tokens // 0')

CONTEXT_TOKENS=$((CACHE_READ + CACHE_CREATE + INPUT_TOKENS))
CONTEXT_PERCENT=$((CONTEXT_TOKENS * 100 / CONTEXT_WINDOW))

# Build the context message
CONTEXT_MSG="[Context: ${CONTEXT_PERCENT}% | ${CONTEXT_TOKENS}/${CONTEXT_WINDOW} tokens | Tool call #${COUNT}]"

# Block if over threshold (for PostToolUse, we can warn but not block)
if [ "$BLOCK_AT_THRESHOLD" = "true" ] && [ "$CONTEXT_PERCENT" -gt "$MAX_CONTEXT_PERCENT" ]; then
    CONTEXT_MSG="WARNING: CONTEXT LIMIT EXCEEDED (${CONTEXT_PERCENT}% > ${MAX_CONTEXT_PERCENT}%) - ${CONTEXT_MSG}"
fi

# Output message to stderr for user visibility (shown in verbose mode)
echo "$CONTEXT_MSG" >&2

# Output JSON with additionalContext to inject into model context
debug "Outputting JSON with additionalContext: $CONTEXT_MSG"
jq -n --arg ctx "$CONTEXT_MSG" '{
    "hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": $ctx
    }
}'
debug "JSON output complete"
exit 0
