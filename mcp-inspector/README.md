# MCP Inspector Docker Image

This Docker image provides a containerized version of the [MCP Inspector](https://github.com/modelcontextprotocol/inspector) - a visual testing tool for Model Context Protocol (MCP) servers.

## Features

- **UI Mode**: Visual interface for testing MCP servers
- **CLI Mode**: Command-line interface for automated testing
- **Proxy Server**: Built-in proxy for MCP server communication
- **Authentication**: Support for secure connections
- **Configuration**: Environment variable based configuration

## Quick Start

### Build the Image

```bash
docker build -t yaoapp/mcp-inspector:latest .
```

### Run in UI Mode (Default)

```bash
# Run in background
docker run -d -p 6274:6274 -p 6277:6277 yaoapp/mcp-inspector:latest

# Run interactively
docker run -it --rm -p 6274:6274 -p 6277:6277 yaoapp/mcp-inspector:latest
```

Then open your browser and navigate to `http://localhost:6274`

### Run in CLI Mode

```bash
# Run CLI mode
docker run -it --rm yaoapp/mcp-inspector:latest --cli

# Run CLI mode with specific server
docker run -it --rm yaoapp/mcp-inspector:latest --cli --server-command "node server.js"
```

## Ports

- **6274**: Inspector UI (Web interface)
- **6277**: Proxy Server (MCP server proxy)

## Environment Variables

You can customize the behavior using environment variables:

```bash
docker run -d \
  -p 6274:6274 \
  -p 6277:6277 \
  -e HOST=0.0.0.0 \
  -e CLIENT_PORT=6274 \
  -e PROXY_PORT=6277 \
  -e MCP_AUTO_OPEN_ENABLED=false \
  -e DANGEROUSLY_OMIT_AUTH=true \
  -e MCP_SERVER_REQUEST_TIMEOUT=10000 \
  -e ALLOWED_ORIGINS="http://localhost:6274,http://127.0.0.1:6274,http://0.0.0.0:6274" \
  yaoapp/mcp-inspector:latest
```

### Available Environment Variables

| Variable                     | Description          | Default                                                           |
| ---------------------------- | -------------------- | ----------------------------------------------------------------- |
| `HOST`                       | Bind address         | `0.0.0.0`                                                         |
| `CLIENT_PORT`                | Client UI port       | `6274`                                                            |
| `PROXY_PORT`                 | Proxy server port    | `6277`                                                            |
| `MCP_AUTO_OPEN_ENABLED`      | Auto open browser    | `false`                                                           |
| `DANGEROUSLY_OMIT_AUTH`      | Skip authentication  | `true`                                                            |
| `MCP_SERVER_REQUEST_TIMEOUT` | Request timeout (ms) | `10000`                                                           |
| `ALLOWED_ORIGINS`            | Allowed CORS origins | `http://localhost:6274,http://127.0.0.1:6274,http://0.0.0.0:6274` |

## Usage Examples

### Testing a Local MCP Server

If you have an MCP server running on your host machine:

```bash
# Run the inspector
docker run -d -p 6274:6274 -p 6277:6277 yaoapp/mcp-inspector:latest

# Access the UI at http://localhost:6274
# Configure it to connect to your server at host.docker.internal:YOUR_SERVER_PORT
```

### Testing with Docker Compose

Create a `docker-compose.yml`:

```yaml
version: "3.8"
services:
  mcp-inspector:
    image: yaoapp/mcp-inspector:latest
    ports:
      - "6274:6274"
      - "6277:6277"
    environment:
      - HOST=0.0.0.0
      - MCP_AUTO_OPEN_ENABLED=false
    depends_on:
      - your-mcp-server

  your-mcp-server:
    # Your MCP server configuration
    image: your-mcp-server:latest
    ports:
      - "3000:3000"
```

### Development Mode

For development, you can mount your local MCP server:

```bash
docker run -it --rm \
  -p 6274:6274 \
  -p 6277:6277 \
  -v $(pwd)/your-mcp-server:/app/server \
  yaoapp/mcp-inspector:latest
```

## CLI Mode Options

The CLI mode supports various options:

```bash
# Test a specific server
docker run -it --rm yaoapp/mcp-inspector:latest --cli --server-command "node server.js"

# Test with custom configuration
docker run -it --rm yaoapp/mcp-inspector:latest --cli --config /app/config/test-config.json

# Run tests and exit
docker run -it --rm yaoapp/mcp-inspector:latest --cli --run-tests
```

## Security Considerations

- The default configuration binds to all interfaces (`0.0.0.0`) for Docker compatibility
- For production use, consider setting `DANGEROUSLY_OMIT_AUTH=false` (default)
- Use proper network isolation and firewall rules
- Consider using HTTPS in production environments

## Troubleshooting

### Common Issues

1. **Port conflicts**: Make sure ports 6274 and 6277 are not in use
2. **Connection refused**: Check that your MCP server is accessible from the container
3. **Authentication errors**: Verify your server supports the required authentication methods
4. **CORS (Cross-Origin) errors**: See CORS configuration section below

### CORS Configuration

If you encounter CORS errors when the Inspector tries to connect to your MCP server, you have several options:

#### Option 1: Use Wildcard CORS (Development Only)

```bash
docker run -d -p 6274:6274 -p 6277:6277 \
  -e ALLOWED_ORIGINS="http://localhost:6274,http://127.0.0.1:6274,http://0.0.0.0:6274" \
  -e DANGEROUSLY_OMIT_AUTH=true \
  yaoapp/mcp-inspector:latest
```

#### Option 2: Specify Allowed Origins

```bash
docker run -d -p 6274:6274 -p 6277:6277 \
  -e ALLOWED_ORIGINS="http://localhost:6274,http://localhost:6277" \
  yaoapp/mcp-inspector:latest
```

#### Option 3: Use Host Network Mode (Linux Only)

```bash
docker run -d --network host \
  yaoapp/mcp-inspector:latest
```

#### Option 4: Connect MCP Server to Same Docker Network

```yaml
version: "3.8"
services:
  mcp-inspector:
    image: yaoapp/mcp-inspector:latest
    ports:
      - "6274:6274"
      - "6277:6277"
    environment:
      - ALLOWED_ORIGINS=http://localhost:6274,http://127.0.0.1:6274,http://0.0.0.0:6274
      - DANGEROUSLY_OMIT_AUTH=true
    networks:
      - mcp-network

  your-mcp-server:
    image: your-mcp-server:latest
    ports:
      - "6277:6277"
    networks:
      - mcp-network

networks:
  mcp-network:
    driver: bridge
```

### Debug Mode

Run with debug logging:

```bash
docker run -it --rm \
  -p 6274:6274 \
  -p 6277:6277 \
  -e DEBUG=mcp:* \
  yaoapp/mcp-inspector:latest
```

### Shell Access

Get shell access to the container:

```bash
docker run -it --rm \
  -p 6274:6274 \
  -p 6277:6277 \
  yaoapp/mcp-inspector:latest /bin/sh
```

## Building from Source

```bash
# Clone the repository
git clone https://github.com/your-org/your-repo.git
cd your-repo/dockerfiles/mcp-inspector

# Build the image
docker build -t yaoapp/mcp-inspector:latest .

# Run it
docker run -d -p 6274:6274 -p 6277:6277 yaoapp/mcp-inspector:latest
```

## License

This Docker image is provided under the same license as the MCP Inspector project.
