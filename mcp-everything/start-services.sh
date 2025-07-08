#!/bin/sh

# Exit on any error
set -e

echo "Starting MCP Everything Services..."

# Check if the everything directory exists
if [ ! -d "/app/everything" ]; then
    echo "Error: /app/everything directory not found"
    exit 1
fi

# Check if package.json exists
if [ ! -f "/app/everything/package.json" ]; then
    echo "Error: /app/everything/package.json not found"
    exit 1
fi

# Check if pnpm is available
if ! command -v pnpm >/dev/null 2>&1; then
    echo "Error: pnpm is not installed"
    exit 1
fi

# Check if built files exist
if [ ! -d "/app/everything/dist" ]; then
    echo "Error: /app/everything/dist directory not found. Did the build complete?"
    exit 1
fi

echo "Starting SSE service on port 3021..."
cd /app/everything && PORT=3021 pnpm start:sse &
SSE_PID=$!

echo "Starting StreamableHttp service on port 3022..."
cd /app/everything && PORT=3022 pnpm start:streamableHttp &
STREAMABLE_PID=$!

echo "Services started with PIDs: SSE=$SSE_PID, StreamableHttp=$STREAMABLE_PID"

# Function to handle cleanup
cleanup() {
    echo "Cleaning up processes..."
    kill $SSE_PID $STREAMABLE_PID 2>/dev/null || true
    exit 0
}

# Set up signal handlers
trap cleanup SIGTERM SIGINT

# Wait for either service to exit
wait $SSE_PID $STREAMABLE_PID

# If we reach here, one of the services exited
echo "One of the services exited, cleaning up..."
cleanup 