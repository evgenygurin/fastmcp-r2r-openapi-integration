#!/usr/bin/env bash
set -e

# R2R MCP Server Startup Script
# Exports all environment variables from .env and starts the server

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "Please create .env from .env.example:"
    echo "  cp .env.example .env"
    exit 1
fi

# Export all variables from .env (ignoring comments and empty lines)
echo "📦 Loading environment variables from .env..."
set -a
source .env
set +a

# Display loaded configuration (without exposing full API key)
echo "✅ Environment variables loaded:"
echo "   R2R_BASE_URL: ${R2R_BASE_URL}"
echo "   R2R_API_KEY: ${R2R_API_KEY:0:10}...${R2R_API_KEY: -10}"
echo "   R2R_TIMEOUT: ${R2R_TIMEOUT:-30.0}"
echo "   DEBUG_LOGGING: ${DEBUG_LOGGING:-false}"
echo ""

# Determine transport mode (default: stdio)
# Usage:
#   ./start.sh                           # stdio mode (Claude Desktop)
#   ./start.sh http                      # legacy HTTP on 0.0.0.0:8000
#   ./start.sh streamable-http           # streamable HTTP on 0.0.0.0:8000 (recommended)
#   ./start.sh streamable-http 127.0.0.1 9000  # custom host and port

TRANSPORT=${1:-stdio}
HOST=${2:-0.0.0.0}
PORT=${3:-8000}

if [ "$TRANSPORT" = "http" ] || [ "$TRANSPORT" = "streamable-http" ]; then
    uv run python -m src.server "$TRANSPORT" "$HOST" "$PORT"
else
    uv run python -m src.server
fi
