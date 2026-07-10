#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$PROJECT_DIR/../../secfid"

npm_config_cache="$PROJECT_DIR/.npm-cache" npm ci --prefix "$PROJECT_DIR"
npm run build --prefix "$PROJECT_DIR"

rsync -a --delete "$PROJECT_DIR/dist/" "$OUTPUT_DIR/"

echo "SecFid site built at $OUTPUT_DIR"
