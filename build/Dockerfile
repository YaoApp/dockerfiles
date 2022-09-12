# ===========================================
#  Yao Compilation Environment 
# 
#  Build:
#  docker build --platform linux/amd64 -t yaoapp/yao-build:0.10.1-amd64 .
#
#  Tests:
#  docker run -it --rm yaoapp/yao-build:0.10.1-amd64 /bin/bash
#
# ===========================================
FROM ubuntu:20.04

ENV NODE_VERSION=16.13.0
ENV NVM_DIR=/root/.nvm
ENV PATH="/root/go/bin/:/usr/local/go/bin:/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"

# Install deps
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y libc6-armel-cross libc6-dev-armel-cross binutils-arm-linux-gnueabi libncurses5-dev build-essential bison flex libssl-dev bc \
    gcc-arm-linux-gnueabi g++-arm-linux-gnueabi \
    gcc-arm-linux-gnueabihf g++-arm-linux-gnueabihf \
    g++-aarch64-linux-gnu crossbuild-essential-arm64 \
    git curl wget

# Install nodejs
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Install golang
RUN wget https://go.dev/dl/go1.18.6.linux-amd64.tar.gz -O /tmp/go1.18.6.linux-amd64.tar.gz && \
    rm -rf /usr/local/go && tar -C /usr/local -xzf /tmp/go1.18.6.linux-amd64.tar.gz && \
    rm /tmp/go1.18.6.linux-amd64.tar.gz  

# Install yarn
RUN npm install -g yarn 

# Download yao source
RUN mkdir /source && cd /source && \ 
    git clone https://github.com/yaoapp/yao && \
    git clone https://github.com/yaoapp/gou && \
    git clone https://github.com/yaoapp/xun && \
    git clone https://github.com/yaoapp/kun && \
    git clone https://github.com/rogchap/v8go && \
    cd v8go && git checkout 5e91d3d9dcabd2986f901b6b31590e49fc3c4dd8  && \
    cd /source/yao && make tools

VOLUME [ "/source" ]
WORKDIR /source

CMD ["tail -f"]

