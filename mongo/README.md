# MongoDB Dockerfile

## Usage

```bash
docker run -d -p 27017:27017 -e MONGO_INITDB_ROOT_PASSWORD=123456 yaoapp/mongo:6.0-amd64
```

```bash
docker run -d -p 27017:27017 -e MONGO_INITDB_ROOT_PASSWORD=123456 yaoapp/mongo:6.0-arm64
```

mongo-express

```bash
docker run -d -p 8081:8081 -e ME_CONFIG_MONGODB_ADMINUSERNAME=admin -e ME_CONFIG_MONGODB_ADMINPASSWORD=654321 -e ME_CONFIG_MONGODB_URL=mongodb://root:123456@172.17.0.1:27017 mongo-express
```

## Build

```bash
docker build --platform linux/amd64 --build-arg USER=root -t yaoapp/mongo:6.0-amd64 .
```

```bash
docker build --platform linux/arm64 --build-arg USER=root -t yaoapp/mongo:6.0-arm64 .
```
