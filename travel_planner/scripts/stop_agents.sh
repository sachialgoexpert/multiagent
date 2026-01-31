#!/usr/bin/env bash

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PID_FILE="$PROJECT_ROOT/agent_pids.txt"

echo "🛑 Stopping all agents..."
echo "------------------------"

if [ ! -f "$PID_FILE" ]; then
  echo "⚠ No PID file found"
  exit 0
fi

while IFS=: read -r PID NAME; do
  if kill -0 "$PID" 2>/dev/null; then
    echo "⏹ Stopping $NAME (PID $PID)"
    kill "$PID"
  fi
done < "$PID_FILE"

rm -f "$PID_FILE"
echo "✅ All agents stopped"
