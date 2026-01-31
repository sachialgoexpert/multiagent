#!/usr/bin/env bash

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PID_FILE="$PROJECT_ROOT/agent_pids.txt"

AGENTS=(
  "main_planner:8000"
  "flight_agent:8001"
  "hotel_agent:8002"
  "food_agent:8003"
  "local_transport_agent:8004"
)

echo "📊 Agent Status Check"
echo "----------------------"

if [ ! -f "$PID_FILE" ]; then
  echo "❌ No PID file found. Agents not running."
  exit 0
fi

while IFS=: read -r PID NAME; do
  PORT=$(printf "%s\n" "${AGENTS[@]}" | grep "^$NAME:" | cut -d: -f2)

  if kill -0 "$PID" 2>/dev/null; then
    if lsof -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
      echo "✅ $NAME running (PID $PID, port $PORT)"
    else
      echo "⚠ $NAME alive but port $PORT not listening"
    fi
  else
    echo "❌ $NAME not running"
  fi
done < "$PID_FILE"
