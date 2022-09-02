# Redis Dockerfile

## Usage

```bash
docker run -d -p 6371:6379 -e REDIS_PASSWORD=123456 yaoapp/redis:6.2-amd64
```

```bash
docker run -d -p 6371:6379 -e REDIS_PASSWORD=123456 yaoapp/redis:6.2-arm64
```

## Build

```bash
docker build --platform linux/amd64 -t yaoapp/redis:6.2-amd64 .
```

```bash
docker build --platform linux/arm64 -t yaoapp/redis:6.2-arm64 .
```
