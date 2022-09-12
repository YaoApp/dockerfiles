# Yao Compilation Environment Dockerfile

Yao Compilation Environment

## Usage

```bash
docker run -it --rm yaoapp/yao-build:0.10.1-amd64 /bin/bash
```

```bash
docker run -it --rm -v /path/source:/source yaoapp/yao-build:0.10.1-amd64 /bin/bash
```

## Build

```bash
docker build --platform linux/amd64 -t yaoapp/yao-build:0.10.1-amd64 .
```
