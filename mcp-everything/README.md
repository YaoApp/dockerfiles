# MCP Everything Server - Docker Container

A comprehensive Model Context Protocol (MCP) server that runs multiple services simultaneously, providing both Server-Sent Events (SSE) and Streamable HTTP interfaces.

## 🚀 Features

- **Multi-Service Architecture**: Runs SSE and StreamableHttp services concurrently
- **Model Context Protocol**: Full implementation of MCP protocol features
- **Dual Interface Support**:
  - SSE Service on port 3021
  - StreamableHttp Service on port 3022
- **Containerized Deployment**: Easy Docker-based deployment
- **Development Ready**: Includes development tools and hot-reload support

## 📋 Prerequisites

- Docker installed on your system
- Docker Compose (optional, for advanced setups)

## 🏗️ Quick Start

### Using Pre-built Image

```bash
# Pull and run the container
docker run -d -p 3021:3021 -p 3022:3022 yaoapp/mcp-everything:latest

# Or run interactively for debugging
docker run -it --rm -p 3021:3021 -p 3022:3022 yaoapp/mcp-everything:latest /bin/sh
```

### Building from Source

```bash
# Clone the repository (or navigate to the directory)
cd dockerfiles/mcp-everything

# Build the Docker image
docker build -t yaoapp/mcp-everything:latest .

# Run the container
docker run -d -p 3021:3021 -p 3022:3022 yaoapp/mcp-everything:latest
```

## 🔧 Configuration

### Environment Variables

| Variable    | Description                     | Default    |
| ----------- | ------------------------------- | ---------- |
| `SSE_PORT`  | Port for SSE service            | 3021       |
| `HTTP_PORT` | Port for StreamableHttp service | 3022       |
| `NODE_ENV`  | Node.js environment             | production |

### Docker Compose Example

```yaml
version: "3.8"
services:
  mcp-everything:
    image: yaoapp/mcp-everything:latest
    ports:
      - "3021:3021"
      - "3022:3022"
    environment:
      - NODE_ENV=production
    restart: unless-stopped
```

## 🌐 API Endpoints

### SSE Service (Port 3021)

The Server-Sent Events service provides real-time streaming capabilities:

```
GET http://localhost:3021/sse
POST http://localhost:3021/message?sessionId=<session_id>
```

### StreamableHttp Service (Port 3022)

The StreamableHttp service provides HTTP-based MCP protocol streaming:

```
POST http://localhost:3022/mcp
GET http://localhost:3022/mcp
DELETE http://localhost:3022/mcp
```

**Headers for StreamableHttp:**

- `mcp-session-id`: Session identifier for request routing
- `last-event-id`: For resumable connections (optional)

## 🛠️ Development

### Local Development Setup

1. **Install dependencies**:

   ```bash
   cd servers/everything
   pnpm install
   ```

2. **Run in development mode**:

   ```bash
   # Start SSE service on port 3021
   PORT=3021 pnpm run start:sse

   # Start StreamableHttp service on port 3022 (in another terminal)
   PORT=3022 pnpm run start:streamableHttp
   ```

3. **Build for production**:
   ```bash
   pnpm run build
   ```

### Docker Development

```bash
# Build development image
docker build -t mcp-everything:dev .

# Run with volume mounting for live development
docker run -it --rm \
  -p 3021:3021 \
  -p 3022:3022 \
  -v $(pwd)/servers:/app/servers \
  mcp-everything:dev
```

## 🔍 Health Checks

### Service Status

Check if services are running:

```bash
# SSE Service - Check if endpoint responds
curl -I http://localhost:3021/sse

# StreamableHttp Service - Check if endpoint responds
curl -I http://localhost:3022/mcp
```

### Container Logs

```bash
# View container logs
docker logs <container-id>

# Follow logs in real-time
docker logs -f <container-id>
```

## 📝 Usage Examples

### SSE Client Connection

```javascript
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";

// Connect to SSE service
const transport = new SSEClientTransport(new URL("http://localhost:3021/sse"));

const client = new Client(
  {
    name: "mcp-client",
    version: "1.0.0",
  },
  {
    capabilities: {},
  }
);

await client.connect(transport);
```

### StreamableHttp Client Connection

```javascript
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";

// Connect to StreamableHttp service
const transport = new StreamableHTTPClientTransport(
  new URL("http://localhost:3022/mcp")
);

const client = new Client(
  {
    name: "mcp-client",
    version: "1.0.0",
  },
  {
    capabilities: {},
  }
);

await client.connect(transport);
```

### Basic MCP Request Example

```bash
# Initialize MCP session with StreamableHttp service
curl -X POST http://localhost:3022/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {
        "name": "test-client",
        "version": "1.0.0"
      }
    }
  }'
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**

   ```bash
   # Check what's using the ports
   lsof -i :3021
   lsof -i :3022

   # Use different ports
   docker run -p 3023:3021 -p 3024:3022 yaoapp/mcp-everything:latest
   ```

2. **Build Failures**

   ```bash
   # Clean Docker cache
   docker system prune -a

   # Rebuild without cache
   docker build --no-cache -t yaoapp/mcp-everything:latest .
   ```

3. **Service Not Starting**

   ```bash
   # Check container logs
   docker logs <container-id>

   # Run interactively to debug
   docker run -it --rm yaoapp/mcp-everything:latest /bin/sh
   ```

### Debug Mode

Run the container in debug mode:

```bash
docker run -it --rm \
  -p 3021:3021 \
  -p 3022:3022 \
  -e NODE_ENV=development \
  yaoapp/mcp-everything:latest
```

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│         Docker Container            │
│  ┌─────────────┐  ┌─────────────┐   │
│  │ SSE Service │  │ StreamableHttp│   │
│  │   :3021     │  │   Service     │   │
│  │             │  │     :3022     │   │
│  └─────────────┘  └─────────────┘   │
│                                     │
│  ┌─────────────────────────────────┐ │
│  │      MCP Protocol Core          │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

## 📊 Performance

### Resource Requirements

- **CPU**: 1-2 cores recommended
- **Memory**: 512MB-1GB RAM
- **Disk**: 100MB for image + logs
- **Network**: Ports 3021, 3022

### Scaling

For high-traffic scenarios:

```bash
# Run multiple instances with load balancer
docker run -d -p 3021:3021 -p 3022:3022 --name mcp-1 yaoapp/mcp-everything:latest
docker run -d -p 3023:3021 -p 3024:3022 --name mcp-2 yaoapp/mcp-everything:latest
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [Docker Hub](https://hub.docker.com/r/yaoapp/mcp-everything)
- [GitHub Issues](https://github.com/your-org/mcp-everything/issues)

## 🆘 Support

- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Join our community discussions
- **Documentation**: Check the official MCP documentation

---

**Built with ❤️ using TypeScript, Node.js, and Docker**
