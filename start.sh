#!/bin/bash
# R2R MCP Server Entrypoint
# Автоматически загружает .env переменные перед запуском

set -euo pipefail

# Определяем директорию скрипта
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Загружаем .env если существует
if [ -f .env ]; then
    echo "Loading environment variables from .env..."
    set -a
    source .env
    set +a
else
    echo "Warning: .env file not found. Using environment variables."
fi

# Проверяем наличие venv
if [ ! -d .venv ]; then
    echo "Error: Virtual environment not found. Run 'uv venv' first."
    exit 1
fi

# Запускаем сервер через uv
echo "Starting R2R MCP Server..."
uv run python -m src.server "$@"
