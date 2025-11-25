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
TRANSPORT=${1:-stdio}
PORT=${2:-8000}

if [ "$TRANSPORT" = "http" ]; then
    echo "🚀 Starting R2R MCP Server in HTTP mode on port ${PORT}..."
    uv run python -m src.server http "$PORT"
else
    echo "🚀 Starting R2R MCP Server in stdio mode..."
    uv run python -m src.server
fi
