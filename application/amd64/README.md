# Yao App Dockerfile

## Usage

### YAO + SQLite

```bash
docker run -d -p 5099:5099 \
    -e YAO_INIT=demo \
    -e YAO_PROCESS_RESET=flows.init.menu \
    -e YAO_PROCESS_DEMO=flows.demo.data  \
    yaoapp/yao-wms:1.0.3-amd64
```

### YAO + MySQL

```bash
docker run -d -p 3307:3306 -e MYSQL_PASSWORD=123456 yaoapp/mysql:8.0-amd64
```

```bash
docker run -d -p 5099:5099 \
    -e YAO_INIT=demo \
    -e YAO_PROCESS_RESET=flows.init.menu \
    -e YAO_PROCESS_DEMO=flows.demo.data  \
    -e YAO_DB_DRIVER=mysql \
    -e YAO_DB_PRIMARY="yao:123456@tcp(172.17.0.1:3307)/yao?charset=utf8mb4&parseTime=True&loc=Local" \
    yaoapp/yao-wms:1.0.3-amd64
```

### YAO + MySQL + REDIS

```bash
docker run -d -p 3307:3306 -e MYSQL_PASSWORD=123456 yaoapp/mysql:8.0-amd64
```

```bash
docker run -d -p 6371:6379 -e REDIS_PASSWORD=123456 yaoapp/redis:6.2-amd64
```

```bash
docker run -d -p 5099:5099 \
    -e YAO_INIT=demo \
    -e YAO_PROCESS_RESET=flows.init.menu \
    -e YAO_PROCESS_DEMO=flows.demo.data  \
    -e YAO_DB_DRIVER=mysql \
    -e YAO_DB_PRIMARY="yao:123456@tcp(172.17.0.1:3307)/yao?charset=utf8mb4&parseTime=True&loc=Local" \
    -e YAO_SESSION_STORE=redis \
    -e YAO_SESSION_HOST=172.17.0.1 \
    -e YAO_SESSION_PORT=6371 \
    -e YAO_SESSION_PASSWORD=123456 \
    yaoapp/yao-wms:1.0.3-amd64
```

## Build

```bash
 docker build \
   --platform linux/amd64 \
   --build-arg REPO=${REPO} \
   --build-arg TOKEN=${TOKEN} \
   --build-arg VERSION=${VERSION} \
   -t yaoapp/yao-wms:${VERSION}-amd64 .
```

```bash
 docker build --platform linux/amd64 \
      --build-arg REPO=github.com/YaoApp/yao-wms  \
      --build-arg TOKEN=xxxxxxxxx  \
      --build-arg VERSION=1.0.3  \
      -t yaoapp/yao-wms:1.0.3-amd64 .
```
