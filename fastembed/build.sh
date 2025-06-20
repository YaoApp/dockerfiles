#!/bin/bash
set -e

# FastEmbed Docker Build Script
# Usage: ./build.sh [amd64|arm64|all]

ARCH=${1:-all}
IMAGE_NAME="yaoapp/fastembed"
VERSION="latest"

build_arch() {
    local arch=$1
    local platform="linux/${arch}"
    local tag="${IMAGE_NAME}:${VERSION}-${arch}"
    
    echo "Building ${tag} for platform ${platform}..."
    
    cd ${arch}
    docker build --platform ${platform} -t ${tag} .
    cd ..
    
    echo "✅ Successfully built ${tag}"
}

case $ARCH in
    "amd64")
        build_arch amd64
        ;;
    "arm64")
        build_arch arm64
        ;;
    "all")
        build_arch amd64
        build_arch arm64
        echo "🎉 All architectures built successfully!"
        ;;
    *)
        echo "Usage: $0 [amd64|arm64|all]"
        exit 1
        ;;
esac

echo ""
echo "Available images:"
docker images | grep ${IMAGE_NAME} | head -10 