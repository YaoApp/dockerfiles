# ===========================================
#  MCP Everything Server - Multi-Service
#  Runs SSE and StreamableHttp services simultaneously
#
#  Build (Multi-platform):
#  docker buildx build --platform linux/amd64,linux/arm64 -t yaoapp/mcp-everything:latest --push .
#
#  Build (Single platform):
#  docker build -t yaoapp/mcp-everything:latest .
#
#  Usage:
#  docker run -d -p 3021:3021 -p 3022:3022 yaoapp/mcp-everything:latest
#  docker run -it --rm  -p 3021:3021 -p 3022:3022 yaoapp/mcp-everything:latest /bin/sh
#
#  Services:
#  - SSE Service: http://localhost:3021
#  - StreamableHttp Service: http://localhost:3022
#
# ===========================================

FROM node:22-alpine

# Build arguments for multi-platform support
ARG TARGETPLATFORM
ARG BUILDPLATFORM
ARG TARGETOS
ARG TARGETARCH

# Set working directory
WORKDIR /app

# Copy source files
ADD servers /app
ADD start-services.sh /app/start-services.sh

# Install pnpm v8 (compatible with lockfileVersion 6.0)
RUN npm install -g pnpm@8

# Install dependencies and build
RUN pnpm install 
RUN cd everything && pnpm install && pnpm build

# Make the start script executable
RUN chmod +x /app/start-services.sh

# Expose ports 3021 and 3022
EXPOSE 3021 3022

CMD ["sh", "/app/start-services.sh"]