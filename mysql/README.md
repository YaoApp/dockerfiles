# MySQL Dockerfile

## Usage

```bash
docker run -d -p 3306:3306 -e MYSQL_PASSWORD=123456 yaoapp/mysql:8.0-amd64
```

```bash
docker run -d -p 3306:3306 -e MYSQL_PASSWORD=123456 yaoapp/mysql:8.0-arm64
```

## Build

```bash
docker build --platform linux/amd64 --build-arg USER=yao --build-arg DATABASE=yao -t yaoapp/mysql:8.0-amd64 .
```

```bash
docker build --platform linux/arm64 --build-arg USER=yao --build-arg DATABASE=yao -t yaoapp/mysql:8.0-arm64 .
```
