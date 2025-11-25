.PHONY: help install dev run run-http lint fix test update-spec clean

help:
	@echo "R2R MCP Server - Доступные команды:"
	@echo ""
	@echo "  make install      - Установка зависимостей"
	@echo "  make dev          - Установка dev зависимостей"
	@echo "  make run          - Запуск сервера (stdio)"
	@echo "  make run-http     - Запуск HTTP сервера на :8000"
	@echo "  make lint         - Проверка кода"
	@echo "  make fix          - Автоисправление кода"
	@echo "  make update-spec  - Обновить OpenAPI спецификацию"
	@echo "  make clean        - Очистка временных файлов"

install:
	uv pip install -e .

dev:
	uv pip install -e ".[dev]"

run:
	uv run python -m src.server

run-http:
	uv run python -m src.server http 8000

lint:
	uv run ruff check .
	uv run mypy src/

fix:
	uv run ruff check --fix .
	uv run ruff format .

update-spec:
	@if [ -z "$$R2R_BASE_URL" ]; then \
		curl -o openapi.json http://localhost:7272/openapi.json; \
	else \
		curl -o openapi.json $$R2R_BASE_URL/openapi.json; \
	fi

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf dist/ build/ .mypy_cache/ .ruff_cache/
