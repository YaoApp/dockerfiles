# ===========================================
#  MCP Inspector - Visual Testing Tool
#  Provides both UI and CLI modes for MCP server testing
#
#  Build:
#  docker build -t yaoapp/mcp-inspector:latest .
#
#  Usage:
#  docker run -d -p 6274:6274 -p 6277:6277 yaoapp/mcp-inspector:latest
#  docker run -it --rm -p 6274:6274 -p 6277:6277 yaoapp/mcp-inspector:latest /bin/sh
#
#  Services:
#  - Inspector UI: http://localhost:6274
#  - Proxy Server: http://localhost:6277
#
#  Environment Variables:
#  - HOST: Bind address (default: localhost, use 0.0.0.0 for all interfaces)
#  - CLIENT_PORT: Client port (default: 6274)
#  - PROXY_PORT: Proxy server port (default: 6277)
#  - DANGEROUSLY_OMIT_AUTH: Skip authentication (default: false)
#  - MCP_SERVER_REQUEST_TIMEOUT: Request timeout in ms (default: 10000)
#  - MCP_AUTO_OPEN_ENABLED: Auto open browser (default: true)
#
# ===========================================

FROM node:22-alpine

# Set working directory
WORKDIR /app

# Install pnpm globally
RUN npm install -g pnpm@8

# Install MCP Inspector globally
RUN npm install -g @modelcontextprotocol/inspector

# Create app directory and copy any configuration files
RUN mkdir -p /app/config

# Set environment variables for Docker container
ENV HOST=0.0.0.0
ENV CLIENT_PORT=6274
ENV PROXY_PORT=6277
ENV MCP_AUTO_OPEN_ENABLED=false
ENV ALLOWED_ORIGINS="http://localhost:6274,http://127.0.0.1:6274,http://0.0.0.0:6274"
ENV DANGEROUSLY_OMIT_AUTH=true

# Expose the inspector UI port and proxy server port
EXPOSE 6274 6277

# Create startup script
RUN cat > /app/start-inspector.sh << 'EOF'
#!/bin/sh
echo "Starting MCP Inspector..."
echo "Inspector UI will be available at: http://localhost:${CLIENT_PORT}"
echo "Proxy Server will be available at: http://localhost:6277"
echo ""
echo "Environment:"
echo "  HOST: ${HOST}"
echo "  CLIENT_PORT: ${CLIENT_PORT}"
echo "  PROXY_PORT: ${PROXY_PORT}"
echo "  MCP_AUTO_OPEN_ENABLED: ${MCP_AUTO_OPEN_ENABLED}"
echo "  ALLOWED_ORIGINS: ${ALLOWED_ORIGINS}"
echo "  DANGEROUSLY_OMIT_AUTH: ${DANGEROUSLY_OMIT_AUTH}"
echo ""

# Set additional environment variables for CORS and binding
export HOST="${HOST:-0.0.0.0}"
export CLIENT_PORT="${CLIENT_PORT:-6274}"
export PROXY_PORT="${PROXY_PORT:-6277}"
export ALLOWED_ORIGINS="${ALLOWED_ORIGINS:-http://localhost:6274,http://127.0.0.1:6274,http://0.0.0.0:6274}"
export DANGEROUSLY_OMIT_AUTH="${DANGEROUSLY_OMIT_AUTH:-true}"
export MCP_AUTO_OPEN_ENABLED="${MCP_AUTO_OPEN_ENABLED:-false}"

# Debug: show what environment variables are being used (comment out for production)
# echo "Debug: HOST=${HOST}"
# echo "Debug: CLIENT_PORT=${CLIENT_PORT}"
# echo "Debug: PROXY_PORT=${PROXY_PORT}"
# echo "Debug: ALLOWED_ORIGINS=${ALLOWED_ORIGINS}"
# echo "Debug: DANGEROUSLY_OMIT_AUTH=${DANGEROUSLY_OMIT_AUTH}"

# Check if running in CLI mode
if [ "$1" = "--cli" ]; then
    echo "Running in CLI mode..."
    shift
    exec npx @modelcontextprotocol/inspector --cli "$@"
else
    echo "Running in UI mode with CORS support..."
    exec npx @modelcontextprotocol/inspector "$@"
fi
EOF

# Make the start script executable
RUN chmod +x /app/start-inspector.sh

# Set the entrypoint
ENTRYPOINT ["/app/start-inspector.sh"]

# Default command (UI mode)
CMD []
