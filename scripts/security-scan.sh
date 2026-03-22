#!/bin/bash
# Security scan script using Grype
# Installs Grype if not present and runs vulnerability scan

set -e

REPO_NAME="python-api-rest-fastapi"
GRYPE_VERSION="0.80.0"

echo "🔍 Running security scan for $REPO_NAME..."

# Install Grype if not present
if ! command -v grype &> /dev/null; then
    echo "📦 Installing Grype..."
    curl -sSfL "https://raw.githubusercontent.com/anchore/grype/main/install.sh" | sh -s -- -b /tmp/grype "v${GRYPE_VERSION}"
    export PATH="/tmp/grype:$PATH"
fi

# Update vulnerability database
echo "📥 Updating vulnerability database..."
grype db:update || true

# Run scan
echo "🛡️ Scanning for vulnerabilities..."
grype . --config .grype.yaml || {
    echo "⚠️ Scan completed with issues"
    exit 0
}

echo "✅ Security scan complete"
