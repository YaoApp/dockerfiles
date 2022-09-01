# YAO Dockerfile

## Usage

**Production**

```bash
docker run -d -p 5099:5099 -v /host/app:/data/app --restart unless-stopped yaoapp/yao:0.10.1-amd64
```

Arm64 Device

```bash
docker run -d -p 5099:5099 -v /host/app:/data/app --restart unless-stopped yaoapp/yao:0.10.1-arm64
```

**Development**

```bash
docker run -d -p 5099:5099 -v /host/app:/data/app yaoapp/yao:0.10.1-amd64-dev
```

Arm64 Device

```bash
docker run -d -p 5099:5099 -v /host/app:/data/app yaoapp/yao:0.10.1-arm64-dev
```

## Build

**Production**

```bash
docker build --platform linux/amd64 --build-arg VERSION=0.10.1 --build-arg ARCH=amd64 -t yaoapp/yao:0.10.1-amd64 .
```

Arm64 Device

```bash
docker build --platform linux/arm64 --build-arg VERSION=0.10.1 --build-arg ARCH=arm64 -t yaoapp/yao:0.10.1-arm64 .
```

**Development**

```bash
docker build --platform linux/amd64 --build-arg VERSION=0.10.1 --build-arg ARCH=amd64 -t yaoapp/yao:0.10.1-amd64-dev .
```

Arm64 Device

```bash
docker build --platform linux/arm64 --build-arg VERSION=0.10.1 --build-arg ARCH=arm64 -t yaoapp/yao:0.10.1-arm64-dev .
```
