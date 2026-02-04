#!/bin/bash
cat << 'PROMPT'
To find available plugins:
1. Read ~/.claude/plugins/known_marketplaces.json
2. Read {installLocation}/.claude-plugin/marketplace.json
3. Plugin content at {installLocation}/plugins/<name>/
PROMPT