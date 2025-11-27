# R2R ↔ FastMCP: Быстрый старт интеграции

**5-минутное введение в симбиоз R2R и FastMCP**

---

## 🎯 Концепция в одном предложении

**FastMCP** предоставляет MCP интерфейс для LLM, **R2R** работает как RAG backend — вместе они образуют полноценную платформу для AI-powered applications.

---

## 🏗️ Архитектура

```text
┌──────────────────┐
│   LLM (Claude)   │  ← AI assistant
└────────┬─────────┘
         │ MCP Protocol
┌────────▼─────────┐
│  FastMCP Server  │  ← Presentation Layer (Tools, Resources, Prompts)
│                  │     Business Logic (Pipelines, Middleware, Context)
└────────┬─────────┘
         │ HTTP/REST
┌────────▼─────────┐
│    R2R Engine    │  ← Data Access Layer (Search, RAG, Knowledge Graph)
│                  │     Storage (PostgreSQL, Neo4j, Redis)
└──────────────────┘
```

---

## ⚡ Minimal Setup (30 минут)

### 1. Установка зависимостей

```bash
uv venv
source .venv/bin/activate
uv pip install fastmcp httpx python-dotenv
```

### 2. Конфигурация

Создайте `.env`:
```env
R2R_BASE_URL=http://localhost:7272
R2R_API_KEY=your_api_key_here
FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPENAPI_PARSER=true
```

### 3. Создайте сервер

Создайте `server.py`:
```python
"""Minimal FastMCP R2R Server."""
import os
import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

# Request-time authentication (CRITICAL для serverless)
class DynamicBearerAuth(httpx.Auth):
    def auth_flow(self, request: httpx.Request):
        api_key = os.getenv("R2R_API_KEY", "")
        if api_key:
            request.headers["Authorization"] = f"Bearer {api_key}"
        yield request

# Auto-generate MCP server from R2R OpenAPI
mcp = FastMCP.from_openapi(
    name="R2R MCP Server",
    spec_url=os.getenv("R2R_OPENAPI_URL", "http://localhost:7272/openapi.json"),
    base_url=os.getenv("R2R_BASE_URL", "http://localhost:7272"),
    auth=DynamicBearerAuth()
)

if __name__ == "__main__":
    mcp.run()
```

### 4. Запуск

```bash
# stdio (для Claude Desktop)
python server.py

# HTTP (для разработки)
python server.py http 8000
```

**Результат:** 81 R2R endpoints → 114 auto-generated MCP components (Resources + Tools)

---

## 🚀 Основные паттерны

### Pattern 1: Enhanced Tool с Context

```python
from fastmcp import Context

@mcp.tool()
async def enhanced_search(
    query: str,
    limit: int = 10,
    ctx: Context | None = None
) -> dict:
    """Search R2R with progress and AI analysis."""
    if ctx:
        await ctx.info(f"Searching: {query}")
        await ctx.report_progress(0, 100, "Searching...")

    # R2R search
    async with httpx.AsyncClient(auth=DynamicBearerAuth()) as client:
        response = await client.post(
            f"{os.getenv('R2R_BASE_URL')}/v3/retrieval/search",
            json={"query": query, "limit": limit}
        )

    if ctx:
        await ctx.report_progress(50, 100, "Analyzing...")

        # AI analysis
        analysis = await ctx.sample(
            f"Analyze these search results: {response.json()}"
        )

        await ctx.report_progress(100, 100, "Completed")

        return {
            "results": response.json(),
            "analysis": analysis.text
        }

    return response.json()
```

**Преимущества:**
- ✅ Progress reporting (ctx.report_progress)
- ✅ Context logging (ctx.info/debug/error)
- ✅ LLM sampling (ctx.sample)

---

### Pattern 2: Pipeline Composition

```python
from src.pipelines import Pipeline

@mcp.tool()
async def research_pipeline(query: str, ctx: Context) -> dict:
    """Multi-step research: search → analyze → summarize."""
    pipeline = Pipeline(ctx)

    return await (
        pipeline
        .add_step("search", search_function, query=query)
        .add_step("analyze", analyze_function)
        .add_step("summarize", summarize_function)
        .execute()
    )
```

**Преимущества:**
- ✅ Chainable operations (fluent interface)
- ✅ Result propagation (previous_results)
- ✅ Context propagation (automatic)

---

### Pattern 3: Middleware для cross-cutting concerns

```python
from fastmcp import Middleware

class LoggingMiddleware(Middleware):
    async def on_call_tool(self, ctx, tool_name: str, arguments: dict):
        logger.info(f"Tool: {tool_name}, Args: {arguments}")
        result = await super().on_call_tool(ctx, tool_name, arguments)
        logger.info(f"Tool {tool_name} completed")
        return result

mcp.add_middleware(LoggingMiddleware)
```

**Типовые middleware:**
- Logging (запись всех операций)
- Caching (кэширование результатов)
- Rate Limiting (ограничение частоты запросов)
- Authentication (проверка прав доступа)

---

## 📊 Разделение ответственности

| Компонент | Ответственность | Технология |
|-----------|----------------|-----------|
| **Presentation** | Tools, Resources, Prompts (LLM interface) | FastMCP |
| **Business Logic** | Pipelines, Middleware, Context | FastMCP |
| **Data Access** | HTTP Client, OpenAPI auto-generation | FastMCP |
| **RAG Backend** | Search, RAG, Knowledge Graph, Agent | R2R |
| **Storage** | PostgreSQL, Neo4j, Redis | R2R |

---

## 🎓 Когда использовать что?

### Используйте R2R напрямую:
- ❌ **Нет LLM интеграции** (простой REST API)
- ❌ **Backend для frontend** (React/Vue.js)
- ❌ **Batch processing** (массовая загрузка документов)
- ❌ **Analytics** (прямые SQL запросы)

```python
from r2r import R2RClient

client = R2RClient("http://localhost:7272")
results = client.retrieval.search(query="machine learning")
```

### Используйте FastMCP + R2R:
- ✅ **LLM интеграция** (Claude Desktop, OpenAI)
- ✅ **Autonomous agents** (tool calling)
- ✅ **Complex workflows** (pipelines)
- ✅ **Progress reporting** (UI feedback)
- ✅ **AI-enhanced analysis** (ctx.sample)
- ✅ **Middleware** (logging, caching, rate limiting)

```python
from fastmcp import FastMCP, Context

mcp = FastMCP.from_openapi(
    spec_url="http://localhost:7272/openapi.json",
    auth=DynamicBearerAuth()
)

@mcp.tool()
async def enhanced_rag(query: str, ctx: Context) -> dict:
    # Progress + R2R + AI analysis
    ...
```

---

## 🔗 Дальнейшее изучение

### Основная документация

- **[R2R ↔ FastMCP Integration Analysis](./R2R_FASTMCP_INTEGRATION.md)** - 1,600+ строк comprehensive guide:
  - Архитектурная совместимость
  - Функциональные пересечения
  - Migration paths
  - Production patterns
  - Практические примеры

### Архитектурные паттерны

- **[FastMCP Layered Architecture](./fastmcp/09-layered-architecture.md)** - Functional composition patterns
- **[R2R Search & RAG](./r2r/03-search-and-rag.md)** - Search strategies и RAG generation

### Документация по компонентам

- **R2R Documentation:** [docs/r2r/README.md](./r2r/README.md) (8 разделов)
- **FastMCP Documentation:** [docs/fastmcp/README.md](./fastmcp/README.md) (8 разделов)
- **Claude Code Documentation:** [docs/claude_code/README.md](./claude_code/README.md) (13 разделов)

---

## 💡 Ключевые insights

### 1. OpenAPI Auto-generation

```python
# 81 R2R endpoints → 114 MCP components автоматически
mcp = FastMCP.from_openapi(spec_url="...")

# Семантическая маршрутизация:
# - GET с {params} → RESOURCE_TEMPLATE
# - GET без params → RESOURCE
# - POST/PUT/DELETE → TOOL
```

### 2. DynamicBearerAuth (CRITICAL для serverless)

```python
# ❌ НЕПРАВИЛЬНО - импорт на module level
API_KEY = os.getenv("R2R_API_KEY")

# ✅ ПРАВИЛЬНО - request-time чтение
class DynamicBearerAuth(httpx.Auth):
    def auth_flow(self, request):
        api_key = os.getenv("R2R_API_KEY", "")
        if api_key:
            request.headers["Authorization"] = f"Bearer {api_key}"
        yield request
```

**Почему важно:**
- FastMCP Cloud инжектит env vars ПОСЛЕ импорта модулей
- Request-time authentication читает key при каждом запросе
- Работает в serverless окружениях (Vercel, AWS Lambda, etc.)

### 3. Functional Composition > OOP Hierarchies

```python
# ❌ Classical OOP (НЕ применимо в FastMCP)
class SearchService:
    def search(self, query: str) -> dict: ...

class SearchController:
    def __init__(self, service: SearchService): ...

# ✅ Functional Composition (идиоматичный FastMCP)
@mcp.tool()
async def search(query: str, ctx: Context) -> dict:
    # Прямая композиция через pipelines
    pipeline = Pipeline(ctx)
    return await pipeline.add_step(...).execute()
```

---

## 🎯 Next Steps

### Для новых проектов:
1. ✅ Используйте этот quickstart для minimal setup
2. ✅ Добавьте enhanced tools по мере необходимости
3. ✅ Внедряйте middleware для logging/caching
4. ✅ Используйте pipelines для complex workflows

### Для миграции:
1. ✅ Сохраните R2R backend без изменений
2. ✅ Создайте FastMCP сервер с OpenAPI auto-generation
3. ✅ Постепенно добавляйте custom tools
4. ✅ Тестируйте каждый phase

### Production deployment:
1. ✅ FastMCP Cloud (самый простой способ)
2. ✅ Docker/Kubernetes (для self-hosting)
3. ✅ Serverless (AWS Lambda, Vercel)

---

**Версия:** 1.0
**Последнее обновление:** 2025-11-27
**Время чтения:** 5 минут
**Готово к использованию:** ✅
