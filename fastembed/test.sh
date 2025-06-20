#!/bin/bash
set -e

# FastEmbed API Test Script
# Usage: ./test.sh <password> [port]

PASSWORD=${1:-"test123"}
PORT=${2:-8000}
BASE_URL="http://localhost:${PORT}"

if [ -z "$1" ]; then
    echo "Usage: $0 <password> [port]"
    echo "Example: $0 mypassword 8000"
    exit 1
fi

echo "Testing FastEmbed API at ${BASE_URL}"
echo "Using password: ${PASSWORD}"
echo "================================="

# Test health endpoint (no auth required)
echo "1. Testing health endpoint..."
curl -s -X GET "${BASE_URL}/health" | jq '.' || echo "Health check failed"

echo -e "\n2. Testing models endpoint (with auth)..."
curl -s -X GET "${BASE_URL}/models" \
    -H "Authorization: Bearer ${PASSWORD}" | jq '.' || echo "Models endpoint failed"

echo -e "\n3. Testing embed endpoint (with auth)..."
curl -s -X POST "${BASE_URL}/embed" \
    -H "Authorization: Bearer ${PASSWORD}" \
    -H "Content-Type: application/json" \
    -d '{
        "texts": ["Hello world", "FastEmbed is awesome"],
        "model": "BAAI/bge-small-en-v1.5"
    }' | jq '.usage' || echo "Embed endpoint failed"

echo -e "\n4. Testing invalid auth..."
curl -s -X GET "${BASE_URL}/models" \
    -H "Authorization: Bearer wrongpassword" | jq '.' || echo "Expected auth failure"

echo -e "\n✅ Tests completed!" 