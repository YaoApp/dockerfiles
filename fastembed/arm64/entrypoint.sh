#!/bin/bash
set -e

echo "FastEmbed API Server Starting..."
echo "GPU Support: ${ENABLE_GPU}"
echo "Port: ${PORT}"
echo "Workers: ${WORKERS}"

# Check if password is set
if [ -z "$FASTEMBED_PASSWORD" ]; then
    echo "Error: FASTEMBED_PASSWORD environment variable is required"
    exit 1
fi

# Start the application
exec python app.py 