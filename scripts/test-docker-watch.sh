#!/usr/bin/env bash
#
# Watch mode for Docker testing
# Requires: fswatch (macOS) or inotifywait (Linux)
#
set -e

echo "🔍 Watching for changes in Dockerfile, src/, and tests/"
echo "Press Ctrl+C to stop"
echo ""

run_tests() {
  echo "🔄 Running tests..."
  ./scripts/test-docker-local.sh
  echo ""
  echo "✅ Tests complete. Waiting for changes..."
}

# Check if we're in the right directory
if [ ! -f "Dockerfile" ]; then
  echo "❌ Error: Must run from project root (where Dockerfile is located)"
  exit 1
fi

# Initial run
run_tests

# Watch for changes
if command -v fswatch &> /dev/null; then
  # macOS with fswatch
  fswatch -o Dockerfile src/ tests/ .dockerignore | while read; do
    run_tests
  done
elif command -v inotifywait &> /dev/null; then
  # Linux with inotifywait
  while inotifywait -r -e modify Dockerfile src/ tests/ .dockerignore 2>/dev/null; do
    run_tests
  done
else
  echo "❌ Please install fswatch (macOS) or inotifywait (Linux) for watch mode"
  echo ""
  echo "Install on macOS: brew install fswatch"
  echo "Install on Linux: apt-get install inotify-tools"
  exit 1
fi
