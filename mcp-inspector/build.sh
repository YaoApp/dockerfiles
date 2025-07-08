#!/bin/bash

# ===========================================
# MCP Inspector Docker Build Script
# ===========================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="yaoapp/mcp-inspector"
IMAGE_TAG="latest"
FULL_IMAGE_NAME="${IMAGE_NAME}:${IMAGE_TAG}"

# Functions
print_header() {
    echo -e "${BLUE}============================================${NC}"
    echo -e "${BLUE}  MCP Inspector Docker Build Script${NC}"
    echo -e "${BLUE}============================================${NC}"
    echo
}

print_step() {
    echo -e "${GREEN}[STEP]${NC} $1"
}

print_info() {
    echo -e "${YELLOW}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed or not in PATH"
        exit 1
    fi
    print_info "Docker version: $(docker --version)"
}

# Build the Docker image
build_image() {
    print_step "Building Docker image: ${FULL_IMAGE_NAME}"
    
    if docker build -t "${FULL_IMAGE_NAME}" .; then
        print_success "Docker image built successfully"
    else
        print_error "Failed to build Docker image"
        exit 1
    fi
}

# Test the Docker image
test_image() {
    print_step "Testing Docker image"
    
    # Test 1: Check if the image can start
    print_info "Test 1: Starting container..."
    CONTAINER_ID=$(docker run -d -p 6274:6274 -p 6277:6277 "${FULL_IMAGE_NAME}")
    
    if [ -z "$CONTAINER_ID" ]; then
        print_error "Failed to start container"
        exit 1
    fi
    
    print_info "Container started with ID: ${CONTAINER_ID}"
    
    # Wait for services to start
    print_info "Waiting for services to start..."
    sleep 5
    
    # Test 2: Check if the container is running
    if docker ps | grep -q "${CONTAINER_ID}"; then
        print_success "Container is running"
    else
        print_error "Container is not running"
        docker logs "${CONTAINER_ID}"
        docker rm -f "${CONTAINER_ID}" 2>/dev/null
        exit 1
    fi
    
    # Test 3: Check if ports are accessible
    print_info "Test 3: Checking port accessibility..."
    if command -v nc &> /dev/null; then
        if nc -z localhost 6274; then
            print_success "Port 6274 is accessible"
        else
            print_error "Port 6274 is not accessible"
        fi
        
        if nc -z localhost 6277; then
            print_success "Port 6277 is accessible"
        else
            print_error "Port 6277 is not accessible"
        fi
    else
        print_info "netcat not available, skipping port check"
    fi
    
    # Test 4: Check logs
    print_info "Test 4: Checking container logs..."
    LOGS=$(docker logs "${CONTAINER_ID}" 2>&1)
    if echo "$LOGS" | grep -q "Starting MCP Inspector"; then
        print_success "Container logs look good"
    else
        print_error "Container logs show issues:"
        echo "$LOGS"
    fi
    
    # Cleanup
    print_info "Stopping and removing test container..."
    docker stop "${CONTAINER_ID}" >/dev/null 2>&1
    docker rm "${CONTAINER_ID}" >/dev/null 2>&1
    
    print_success "All tests passed!"
}

# Show image info
show_image_info() {
    print_step "Image Information"
    echo
    docker images "${IMAGE_NAME}" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
    echo
}

# Show usage instructions
show_usage() {
    print_step "Usage Instructions"
    echo
    echo -e "${YELLOW}Build the image:${NC}"
    echo "  docker build -t ${FULL_IMAGE_NAME} ."
    echo
    echo -e "${YELLOW}Run in UI mode:${NC}"
    echo "  docker run -d -p 6274:6274 -p 6277:6277 ${FULL_IMAGE_NAME}"
    echo "  # Then open http://localhost:6274"
    echo
    echo -e "${YELLOW}Run in CLI mode:${NC}"
    echo "  docker run -it --rm ${FULL_IMAGE_NAME} --cli"
    echo
    echo -e "${YELLOW}Run interactively:${NC}"
    echo "  docker run -it --rm -p 6274:6274 -p 6277:6277 ${FULL_IMAGE_NAME}"
    echo
    echo -e "${YELLOW}Get shell access:${NC}"
    echo "  docker run -it --rm ${FULL_IMAGE_NAME} /bin/sh"
    echo
}

# Main execution
main() {
    print_header
    
    # Parse arguments
    BUILD_ONLY=false
    TEST_ONLY=false
    HELP=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --build-only)
                BUILD_ONLY=true
                shift
                ;;
            --test-only)
                TEST_ONLY=true
                shift
                ;;
            --help|-h)
                HELP=true
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                HELP=true
                shift
                ;;
        esac
    done
    
    if [ "$HELP" = true ]; then
        echo "Usage: $0 [OPTIONS]"
        echo
        echo "Options:"
        echo "  --build-only    Only build the image, skip testing"
        echo "  --test-only     Only test the image, skip building"
        echo "  --help, -h      Show this help message"
        echo
        echo "Default: Build and test the image"
        exit 0
    fi
    
    # Check prerequisites
    check_docker
    
    # Execute based on options
    if [ "$TEST_ONLY" = true ]; then
        test_image
    elif [ "$BUILD_ONLY" = true ]; then
        build_image
    else
        build_image
        test_image
    fi
    
    # Show results
    show_image_info
    show_usage
    
    print_success "Build script completed successfully!"
}

# Run main function
main "$@" 