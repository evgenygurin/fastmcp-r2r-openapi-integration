# R2R MCP Server

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.13+-green.svg)](https://gofastmcp.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

FastMCP-based Model Context Protocol (MCP) сервер для R2R API, обеспечивающий интеграцию с системами управления документами, графами знаний и RAG.

> **⚡ Важно**: Для корректной работы с OpenAPI 3.1 спецификацией рекомендуется включить экспериментальный парсер FastMCP. Добавьте `FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPENAPI_PARSER=true` в `.env` файл.

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
# Обязательные параметры
R2R_BASE_URL=http://localhost:7272
R2R_API_KEY=your_actual_api_key_here

# Рекомендуется: включить экспериментальный парсер (лучшая совместимость с OpenAPI 3.1)
FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPENAPI_PARSER=true

# Опциональные параметры производительности
R2R_TIMEOUT=30.0              # Таймаут запросов (секунды)
DEBUG_LOGGING=false           # Детальное логирование для отладки
```

**ВАЖНО:** Формат API ключа в .env файле:
```env
# ✅ ПРАВИЛЬНО - без кавычек, без "Bearer"
R2R_API_KEY=your_actual_api_key_here

# ❌ НЕПРАВИЛЬНО - с кавычками
R2R_API_KEY="your_actual_api_key_here"

# ❌ НЕПРАВИЛЬНО - со словом Bearer
R2R_API_KEY=Bearer your_actual_api_key_here
```

Код автоматически добавляет "Bearer " при формировании HTTP заголовка.

**Performance Optimizations:**
- **DEBUG_LOGGING=true** - показывает детали работы OpenAPI парсера и построения запросов
- **Experimental parser** - автоматически используется для 100-200ms faster startup

## Использование

### Деплой на FastMCP Cloud (рекомендуется) 🚀

Самый простой способ - задеплоить на [FastMCP Cloud](https://fastmcp.cloud):

1. **Entrypoint:** `src/server.py:mcp`
2. **Environment Variables:** Добавьте ваши R2R креденшалы
3. **Authentication:** Включите для безопасности

📖 Подробная инструкция: [DEPLOYMENT.md](docs/DEPLOYMENT.md)

### Запуск для Claude Desktop (stdio)

**Рекомендуется через start.sh** (автоматически экспортирует переменные из .env):

```bash
./start.sh
# или
make run
```

**Альтернативно** (требует ручного экспорта переменных):

```bash
# Экспортируем переменные из .env
set -a && source .env && set +a

# Запускаем сервер
uv run python -m src.server
```

### Запуск HTTP сервера (для разработки)

**Рекомендуется через start.sh**:

```bash
./start.sh http 8000
# или
make run-http
```

**Альтернативно**:

```bash
# Экспортируем переменные из .env
set -a && source .env && set +a

# Запускаем HTTP сервер
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
        "/path/to/fastmcp-r2r-openapi-integration",
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
.
├── src/
│   ├── __init__.py
│   └── server.py          # Основной MCP сервер
├── docs/
│   ├── DEPLOYMENT.md      # Руководство по деплою
│   ├── QUICKSTART.md      # Быстрый старт
│   └── SUMMARY.md         # Обзор проекта
├── requirements.txt       # Python зависимости
├── pyproject.toml         # Конфигурация проекта (uv + ruff)
├── Makefile               # Удобные команды
├── CLAUDE.md              # Память для Claude Code
├── LICENSE                # MIT License
├── README.md              # Эта документация
├── .env.example           # Шаблон конфигурации
├── .gitignore             # Git игнорирование
└── openapi.json           # R2R OpenAPI спецификация
```

## Полезные ссылки

### Документация

- [FastMCP Documentation](https://gofastmcp.com)
- [R2R Documentation](https://r2r-docs.sciphi.ai/)
- [Model Context Protocol](https://modelcontextprotocol.io)

### Внутренняя документация

- **[R2R ↔ FastMCP Integration Analysis](./docs/R2R_FASTMCP_INTEGRATION.md)** - Комплексный анализ интеграции:
  - Архитектурная совместимость (4-layer model)
  - Функциональные пересечения
  - Возможности перехода (migration paths)
  - Симбиоз: лучшие практики
  - Production patterns
  - Практические примеры

- **[FastMCP Architecture](./docs/fastmcp/09-layered-architecture.md)** - Многослойная архитектура FastMCP приложений
- **[R2R Documentation Hub](./docs/r2r/README.md)** - 8 разделов R2R documentation
- **[FastMCP Documentation Hub](./docs/fastmcp/README.md)** - 8 разделов FastMCP documentation
- **[Claude Code Documentation Hub](./docs/claude_code/README.md)** - 13 разделов Claude Code documentation

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for version history and release notes.

## Лицензия

MIT
