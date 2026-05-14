#!/bin/bash
set -e

# Start the recipe dashboard server in background
cd /app/recipes
node server.js &
DASHBOARD_PID=$!
echo "📺 Dashboard running on port 8080 (PID: $DASHBOARD_PID)"

# Start OpenClaw agent in foreground
echo "🎬 Starting OpenClaw Video Kitchen agent..."
cd /workspace
exec openclaw start
