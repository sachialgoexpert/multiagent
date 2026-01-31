for port in 8000 8001 8002 8003 8004; do
  pid=$(lsof -ti tcp:$port)
  if [ -n "$pid" ]; then
    echo "Stopping process on port $port (PID $pid)"
    kill $pid
  else
    echo "Port $port already free"
  fi
done