#!/bin/bash
# Monitor script for python-api-rest-fastapi
# Usage: ./monitor.sh

set -euo pipefail

echo "🔍 Monitoring python-api-rest-fastapi..."

PORT="${PORT:-8000}"

# Check if the process is running
if pgrep -f "uvicorn" > /dev/null; then
    echo "✅ Uvicorn process is running"
else
    echo "❌ Uvicorn process is NOT running"
fi

# Check API health endpoint
if curl -s -f "http://localhost:${PORT}/health" > /dev/null 2>&1; then
    echo "✅ API health check OK"
else
    echo "❌ API health check FAILED"
fi

# Check Docker container
if command -v docker &> /dev/null; then
    if docker ps --format '{{.Names}}' | grep -q "python-api-rest"; then
        echo "✅ Docker container is running"
    fi
fi

# System resources
echo "📊 System Resources:"
MEMORY_USAGE=$(free | awk '/Mem:/ {printf "%.0f", $3/$2 * 100}')
echo "  🧠 Memory: ${MEMORY_USAGE}%"

DISK_USAGE=$(df -h . | awk 'NR==2 {print $5}' | sed 's/%//')
echo "  💾 Disk: ${DISK_USAGE}%"

echo "✅ Monitoring complete"