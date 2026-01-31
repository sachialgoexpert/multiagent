#!/usr/bin/env bash

set -e

# repo root (two levels up from scripts/)
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
LOG_DIR="$PROJECT_ROOT/logs"
PID_FILE="$PROJECT_ROOT/agent_pids.txt"

mkdir -p "$LOG_DIR"

AGENTS=(
  "main_planner:8000:travel_planner.agents.main_planner.app:app"
  "flight_agent:8001:travel_planner.agents.flight_agent.app:app"
  "hotel_agent:8002:travel_planner.agents.hotel_agent.app:app"
  "food_agent:8003:travel_planner.agents.food_agent.app:app"
  "local_transport_agent:8004:travel_planner.agents.local_transport_agent.app:app"
)

start_agents() {
  echo "🚀 Starting all agents..."
  echo "" > "$PID_FILE"

  for AGENT in "${AGENTS[@]}"; do
    NAME=$(echo "$AGENT" | cut -d: -f1)
    PORT=$(echo "$AGENT" | cut -d: -f2)
    APP=$(echo "$AGENT" | cut -d: -f3)

    echo "▶ Starting $NAME on port $PORT"

    uvicorn "$APP" \
      --port "$PORT" \
      --reload \
      > "$LOG_DIR/$NAME.log" 2>&1 &

    echo "$!:${NAME}" >> "$PID_FILE"
    sleep 1
  done

  echo "✅ All agents started"
  echo "📄 Logs in $LOG_DIR"
}

stop_agents() {
  echo "🛑 Stopping all agents..."

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
}

case "$1" in
  start) start_agents ;;
  stop) stop_agents ;;
  restart)
    stop_agents
    start_agents
    ;;
  *)
    echo "Usage: $0 {start|stop|restart}"
    exit 1
    ;;
esac
