#!/bin/bash

# Start SSE service on port 3021
cd /app/everything && pnpm start:sse &
SSE_PID=$!

# Start streamableHttp service on port 3022
cd /app/everything && pnpm start:streamableHttp &
STREAMABLE_PID=$!

# Wait for either service to exit
wait $SSE_PID $STREAMABLE_PID

# Clean up processes
kill $SSE_PID $STREAMABLE_PID 2>/dev/null 