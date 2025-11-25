# R2R MCP Server

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.13+-green.svg)](https://gofastmcp.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

FastMCP-based Model Context Protocol (MCP) сервер для R2R API, обеспечивающий интеграцию с системами управления документами, графами знаний и RAG.

## Возможности

- **Автоматическая генерация** MCP компонентов из OpenAPI спецификации
- **Семантическая маршрутизация**: GET операции как Resources, POST/PUT/DELETE как Tools
- **Аутентификация**: Поддержка Bearer token через переменные окружения
- **Двойной транспорт**: stdio (для Claude Desktop) и HTTP (для разработки/тестирования)
- **Полное покрытие R2R API**:
  - Управление chunks (поиск, создание, обновление, удаление)
  - Управление документами (загрузка, экспорт, метаданные)
  - Коллекции и права доступа
  - Граф знаний (извлечение сущностей, дедупликация, построение сообществ)
  - Конверсации и сообщения

## Установка

### 1. Клонирование и настройка окружения

```bash
# Установка зависимостей через uv (рекомендуется)
uv venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

uv pip install -e .
```

### 2. Конфигурация

Создайте `.env` файл на основе `.env.example`:

```bash
cp .env.example .env
```

Отредактируйте `.env`:

```env
R2R_BASE_URL=http://localhost:7272
R2R_API_KEY=your_actual_api_key_here
R2R_TIMEOUT=30.0
```

## Использование

### Запуск для Claude Desktop (stdio)

```bash
uv run python -m src.server
```

### Запуск HTTP сервера (для разработки)

```bash
uv run python -m src.server http 8000
```

Затем подключитесь через MCP клиент к `http://localhost:8000/mcp`

### Интеграция с Claude Desktop

Добавьте в `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "r2r": {
      "command": "uv",
      "args": [
        "--directory",
        "/полный/путь/к/fastapi-r2r-openapi-integration",
        "run",
        "python",
        "-m",
        "src.server"
      ],
      "env": {
        "R2R_BASE_URL": "http://localhost:7272",
        "R2R_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Архитектура Route Maps

Сервер использует семантическую маршрутизацию для оптимальной организации endpoints:

### Resources (только чтение)

- `GET /v3/chunks/{id}` → ResourceTemplate
- `GET /v3/documents/{id}` → ResourceTemplate
- `GET /v3/documents` → Resource (список)
- `GET /health` → Resource

### Tools (модификация данных)

- `POST /v3/chunks/search` → Tool (поиск)
- `POST /v3/documents` → Tool (создание)
- `DELETE /v3/documents/{id}` → Tool (удаление)
- `POST /v3/documents/{id}/extract` → Tool (извлечение сущностей)
- `POST /v3/graphs/{collection_id}/communities/build` → Tool (граф знаний)

## Примеры использования

### Поиск документов

```python
# Через MCP клиент
result = await client.call_tool("search_chunks", {
    "query": "machine learning",
    "limit": 5
})
```

### Получение документа

```python
# Как Resource
content = await client.read_resource("uri://r2r/documents/uuid-here")
```

### Извлечение сущностей из документа

```python
# Tool для граф знаний
result = await client.call_tool("extract_entities_from_document", {
    "id": "document-uuid"
})
```

## Разработка

### Линтинг и форматирование

```bash
# Проверка кода
uv run ruff check .

# Автоисправление
uv run ruff check --fix .

# Форматирование
uv run ruff format .
```

### Обновление OpenAPI спецификации

```bash
curl -o openapi.json http://localhost:7272/openapi.json
```

## Структура проекта

```text
fastapi-r2r-openapi-integration/
├── src/
│   ├── __init__.py
│   └── server.py          # Основной MCP сервер
├── openapi.json           # R2R OpenAPI спецификация
├── pyproject.toml         # Зависимости и конфигурация
├── .env.example           # Пример конфигурации
├── .gitignore
└── README.md
```

## Полезные ссылки

- [FastMCP Documentation](https://gofastmcp.com)
- [R2R API Documentation](http://localhost:7272/docs)
- [Model Context Protocol](https://modelcontextprotocol.io)

## Лицензия

MIT
