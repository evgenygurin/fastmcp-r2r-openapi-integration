# R2R ↔ FastMCP: Полный анализ интеграции и симбиоза

**Comprehensive analysis of integration points, transition paths, and symbiotic patterns**

---

## 📑 Оглавление

1. [Введение](#-введение)
2. [Архитектурная совместимость](#-архитектурная-совместимость)
3. [Функциональные пересечения](#-функциональные-пересечения)
4. [Возможности перехода](#-возможности-перехода)
5. [Симбиоз: Лучшие практики](#-симбиоз-лучшие-практики)
6. [Законченность решения](#-законченность-решения)
7. [Production Patterns](#-production-patterns)
8. [Практические примеры](#-практические-примеры)
9. [Сравнительный анализ](#-сравнительный-анализ)

---

## 🎯 Введение

**R2R (RAG to Riches)** и **FastMCP** - две системы, которые при совместном использовании образуют мощную платформу для создания production-ready RAG-приложений.

### Ключевой принцип интеграции

```text
┌──────────────────────────────────────────────────────┐
│                   LLM (Claude, GPT)                  │
│                                                      │
└──────────────────┬───────────────────────────────────┘
                   │ MCP Protocol
┌──────────────────▼───────────────────────────────────┐
│                   FastMCP Server                     │  ← Presentation Layer
│  (Tools, Resources, Prompts)                         │     (LLM Interface)
│                                                      │
│  ┌────────────────────────────────────────────────┐ │
│  │ Business Logic Layer                           │ │
│  │ - Pipelines (composition)                      │ │
│  │ - Middleware (auth, logging, caching)          │ │
│  │ - Context (dependency injection)               │ │
│  └────────────┬───────────────────────────────────┘ │
└───────────────┼──────────────────────────────────────┘
                │ HTTP/REST API
┌───────────────▼──────────────────────────────────────┐
│                    R2R Engine                        │  ← Data Access Layer
│  (Documents, Search, RAG, Knowledge Graph)           │     (RAG Backend)
│                                                      │
│  ┌────────────────────────────────────────────────┐ │
│  │ Storage Layer                                  │ │
│  │ - PostgreSQL (pgvector)                        │ │
│  │ - Neo4j (knowledge graph)                      │ │
│  │ - Redis (caching)                              │ │
│  └────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────┘
```

**Separation of Concerns:**
- **FastMCP**: Интерфейс для LLM (MCP сервер)
- **R2R**: Движок для RAG (Backend система)

---

## 🏗️ Архитектурная совместимость

### 1. Четырехслойная модель интеграции

```text
┌─────────────────────────────────────────┐
│  Presentation Layer (FastMCP)           │
│  - Tools (@mcp.tool)                    │
│  - Resources (@mcp.resource)            │
│  - Prompts (@mcp.prompt)                │
├─────────────────────────────────────────┤
│  Business Logic Layer (FastMCP)         │
│  - Pipelines (composition)              │
│  - Middleware (auth, logging)           │
│  - Context (dependency injection)       │
├─────────────────────────────────────────┤
│  Data Access Layer (FastMCP → R2R)      │
│  - httpx.AsyncClient                    │
│  - DynamicBearerAuth                    │
│  - OpenAPI auto-generation              │
├─────────────────────────────────────────┤
│  RAG Backend Layer (R2R)                │
│  - Documents (ingestion, search)        │
│  - Knowledge Graph (entities, relations)│
│  - Agent (reasoning, tools)             │
│  - Collections (organization)           │
└─────────────────────────────────────────┘
```

### 2. Семантическая маршрутизация (OpenAPI → MCP)

FastMCP автоматически конвертирует R2R OpenAPI спецификацию в MCP компоненты по следующим правилам:

```python
# Route mapping order (FIRST MATCH WINS)
_route_maps = [
    # GET с path parameters → RESOURCE_TEMPLATE
    RouteMap(
        methods=["GET"],
        pattern=r"^/v3/.*\{.*\}.*$",  # e.g., /v3/documents/{id}
        mcp_type=MCPType.RESOURCE_TEMPLATE,
    ),

    # GET без parameters → RESOURCE
    RouteMap(
        methods=["GET"],
        pattern=r"^/v3/.*$",           # e.g., /v3/documents
        mcp_type=MCPType.RESOURCE,
    ),

    # POST/PUT/PATCH/DELETE → TOOL
    RouteMap(
        methods=["POST", "PUT", "PATCH", "DELETE"],
        pattern=r".*",                 # Any endpoint
        mcp_type=MCPType.TOOL,
    ),
]
```

**Принцип:**
- **Read operations (GET)** → Данные для чтения LLM
- **Write operations (POST/PUT/DELETE)** → Действия, которые может выполнить LLM

### 3. DynamicBearerAuth: Критический паттерн для serverless

**Проблема:** FastMCP Cloud и serverless окружения инжектят env vars ПОСЛЕ импорта модулей.

**Решение:** Request-time authentication (читает API key при каждом запросе, НЕ при импорте).

```python
class DynamicBearerAuth(httpx.Auth):
    """Auth handler that reads API key from environment at request time.

    CRITICAL for FastMCP Cloud compatibility:
    - Reads R2R_API_KEY DURING request execution
    - NOT at module import time
    - Ensures auth works in serverless environments
    """

    def auth_flow(self, request: httpx.Request):
        """Inject Bearer token at request time."""
        api_key = os.getenv("R2R_API_KEY", "")
        if api_key:
            request.headers["Authorization"] = f"Bearer {api_key}"
        yield request

# Global async client with dynamic auth
_client = httpx.AsyncClient(
    base_url=os.getenv("R2R_BASE_URL", "http://localhost:7272"),
    auth=DynamicBearerAuth(),  # ← Authentication на request-time!
    timeout=30.0,
)
```

**Почему это важно:**
1. **Serverless compatibility** - env vars инжектятся после импорта
2. **Security** - API key никогда не хардкодится
3. **Flexibility** - можно менять API key без перезапуска сервера

---

## 🔗 Функциональные пересечения

### Матрица ответственности

| Функция | R2R | FastMCP | Кто владелец? |
|---------|-----|---------|---------------|
| **Document Ingestion** | ✅ Core | ➡️ Proxy | R2R |
| **Vector Search** | ✅ Core | ➡️ Proxy | R2R |
| **Knowledge Graph** | ✅ Core | ➡️ Proxy | R2R |
| **RAG Generation** | ✅ Core | ➡️ Proxy | R2R |
| **Agent (Reasoning)** | ✅ Core | ➡️ Proxy | R2R |
| **MCP Protocol** | ❌ | ✅ Core | FastMCP |
| **LLM Interface (Tools/Resources)** | ❌ | ✅ Core | FastMCP |
| **Middleware (Logging, Auth)** | ❌ | ✅ Core | FastMCP |
| **Pipeline Composition** | ❌ | ✅ Core | FastMCP |
| **Context Dependency Injection** | ❌ | ✅ Core | FastMCP |
| **Authentication (JWT/OAuth)** | ✅ Built-in | ✅ Built-in | Both (разные уровни) |
| **HTTP Transport** | ✅ Server | ✅ Client | Both |
| **Caching** | ✅ Built-in | ✅ Middleware | Both (разные слои) |

### Взаимодополняемость

**R2R предоставляет:**
- 🗂️ Document management (upload, metadata, deletion)
- 🔍 Advanced search (semantic, fulltext, hybrid, graph)
- 🧠 RAG with streaming generation
- 🕸️ Knowledge Graph (entities, relationships, communities)
- 🤖 Agent with reasoning (research mode, tool calling)
- 📚 Collections (multi-tenancy, access control)
- 📊 Analytics (usage, performance)

**FastMCP предоставляет:**
- 🎨 Presentation Layer для LLM (Tools, Resources, Prompts)
- 🔄 Pipeline composition (chainable async operations)
- 🛡️ Middleware (auth, logging, caching, rate limiting)
- 📦 Context (dependency injection)
- 🧪 Testing framework (async-friendly)
- 🚀 Deployment (stdio, HTTP, SSE, FastMCP Cloud)
- 🔧 OpenAPI auto-generation (REST API → MCP)

**Дублирование функциональности:**
- Минимальное (разные уровни абстракции)
- Оба предоставляют HTTP сервер, но для разных целей:
  - R2R: REST API для RAG операций
  - FastMCP: MCP сервер для LLM интеграции

---

## 🔄 Возможности перехода

### 1. От чистого R2R к R2R + FastMCP

**Сценарий:** У вас есть R2R backend, нужно добавить MCP интерфейс для LLM.

**Шаги:**

1. **Создайте FastMCP сервер с OpenAPI auto-generation:**

```python
from fastmcp import FastMCP

# Auto-generate MCP components from R2R OpenAPI
mcp = FastMCP.from_openapi(
    name="R2R MCP Server",
    spec_url="http://localhost:7272/openapi.json",
    base_url="http://localhost:7272",
    route_maps=[
        # GET с params → RESOURCE_TEMPLATE
        RouteMap(
            methods=["GET"],
            pattern=r"^/v3/.*\{.*\}.*$",
            mcp_type=MCPType.RESOURCE_TEMPLATE,
        ),
        # GET без params → RESOURCE
        RouteMap(
            methods=["GET"],
            pattern=r"^/v3/.*$",
            mcp_type=MCPType.RESOURCE,
        ),
        # POST/PUT/DELETE → TOOL
        RouteMap(
            methods=["POST", "PUT", "PATCH", "DELETE"],
            pattern=r".*",
            mcp_type=MCPType.TOOL,
        ),
    ],
    auth=DynamicBearerAuth(),
)
```

2. **Добавьте кастомные enhanced tools (опционально):**

```python
@mcp.tool(
    description="Enhanced search with progress and AI analysis",
    tags={"search", "ai"}
)
async def enhanced_search(
    query: str,
    limit: int = 10,
    ctx: Context | None = None
) -> dict[str, Any]:
    """Search with progress reporting and LLM analysis."""
    if ctx:
        await ctx.report_progress(0, 100, "Searching R2R...")

    # Вызов R2R API
    response = await _client.post(
        "/v3/retrieval/search",
        json={"query": query, "limit": limit}
    )

    if ctx:
        await ctx.report_progress(50, 100, "Analyzing results...")

        # AI analysis с ctx.sample
        analysis = await ctx.sample(
            prompt=f"Analyze these search results: {response.json()}"
        )

        await ctx.report_progress(100, 100, "Completed")

    return {
        "results": response.json(),
        "analysis": analysis.text if ctx else None
    }
```

3. **Запустите сервер:**

```bash
# stdio для Claude Desktop
python -m src.server

# HTTP для разработки
python -m src.server http 8000
```

**Результат:** R2R backend остается без изменений, FastMCP предоставляет MCP интерфейс.

---

### 2. Модульный переход (поэтапное внедрение)

**Phase 1: Basic MCP Integration**
```python
# Только auto-generated components (Resources + Tools)
mcp = FastMCP.from_openapi(
    spec_url="http://localhost:7272/openapi.json",
    # ... route maps
)
```

**Phase 2: Add Custom Tools**
```python
# Добавление enhanced tools с Context
@mcp.tool()
async def custom_tool(param: str, ctx: Context) -> dict:
    # Custom logic + R2R calls
    ...
```

**Phase 3: Add Middleware**
```python
# Middleware для logging, caching, rate limiting
from fastmcp import Middleware

class LoggingMiddleware(Middleware):
    async def on_request(self, ctx):
        logger.info(f"Request: {ctx.method} {ctx.path}")
        return await super().on_request(ctx)

mcp.add_middleware(LoggingMiddleware)
```

**Phase 4: Add Pipelines**
```python
# Pipeline composition для complex workflows
from src.pipelines import Pipeline

@mcp.tool()
async def research_pipeline(query: str, ctx: Context) -> dict:
    pipeline = Pipeline(ctx)
    return await (
        pipeline
        .add_step("search", pipeline_search_and_analyze, query=query)
        .add_step("analyze", pipeline_llm_analyze)
        .add_step("summarize", pipeline_llm_summarize)
        .execute()
    )
```

**Преимущества поэтапного перехода:**
- ✅ Низкий риск (каждый phase независим)
- ✅ Быстрая отдача (Phase 1 готов за 30 минут)
- ✅ Постепенное обучение команды
- ✅ Простая откатка (вернуться на предыдущую phase)

---

### 3. Migration Path: REST API → MCP

**До (прямые REST вызовы):**
```python
# Клиент напрямую вызывает R2R REST API
import requests

def search(query: str) -> dict:
    response = requests.post(
        "http://localhost:7272/v3/retrieval/search",
        json={"query": query},
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    return response.json()
```

**После (через MCP):**
```python
# LLM вызывает MCP tool, который проксирует к R2R
from fastmcp import Context

@mcp.tool()
async def search(
    query: str,
    ctx: Context | None = None
) -> dict[str, Any]:
    """Search R2R knowledge base."""
    if ctx:
        await ctx.info(f"Searching: {query}")

    response = await _client.post(
        "/v3/retrieval/search",
        json={"query": query}
    )

    return response.json()
```

**Преимущества MCP подхода:**
- 🎯 LLM может вызывать tools автономно
- 📊 Progress reporting (ctx.report_progress)
- 🔍 Context logging (ctx.info/debug/error)
- 🧠 LLM sampling (ctx.sample) внутри tool
- 🔄 Pipeline composition (chainable operations)

---

## 🤝 Симбиоз: Лучшие практики

### 1. FastMCP как MCP интерфейс, R2R как RAG backend

**Идеальная архитектура:**

```text
┌──────────────────────────────────────────┐
│              LLM (Claude)                │
│                                          │
└──────────────┬───────────────────────────┘
               │ MCP Protocol
┌──────────────▼───────────────────────────┐
│          FastMCP Server                  │
│                                          │
│  Tools:                                  │
│  - search(query)         ────────┐       │
│  - rag(question)          ─────┐ │       │
│  - agent(message)          ───┐│ │       │
│  - upload_document(file)    ─┐││ │       │
│                               │││ │       │
│  Resources:                   │││ │       │
│  - r2r://documents/{id}    ─┐ │││ │       │
│  - r2r://collections       ─┼┐│││ │       │
│                             ││││││ │       │
│  Pipelines:                 ││││││ │       │
│  - research_pipeline()      ││││││ │       │
│  - comparative_analysis()   ││││││ │       │
└─────────────────────────────┼┼┼┼┼┼─┘
               │              ││││││
               │ HTTP/REST    ││││││
┌──────────────▼──────────────▼▼▼▼▼▼─────────┐
│              R2R Backend                    │
│                                             │
│  POST /v3/retrieval/search  ◄──────────────┤
│  POST /v3/retrieval/rag     ◄────────────┤ │
│  POST /v3/retrieval/agent   ◄──────────┤ │ │
│  POST /v3/documents         ◄────────┤ │ │ │
│  GET  /v3/documents/{id}    ◄──────┤ │ │ │ │
│  GET  /v3/collections       ◄────┤ │ │ │ │ │
│                                  │ │ │ │ │ │
│  Storage:                        │ │ │ │ │ │
│  - PostgreSQL (pgvector)         │ │ │ │ │ │
│  - Neo4j (knowledge graph)       │ │ │ │ │ │
│  - Redis (caching)               │ │ │ │ │ │
└──────────────────────────────────┴─┴─┴─┴─┴─┘
```

### 2. Middleware для cross-cutting concerns

**Logging Middleware:**
```python
from fastmcp import Middleware

class LoggingMiddleware(Middleware):
    async def on_call_tool(self, ctx, tool_name: str, arguments: dict):
        logger.info(f"Tool: {tool_name}, Args: {arguments}")
        start_time = time.time()

        result = await super().on_call_tool(ctx, tool_name, arguments)

        elapsed = time.time() - start_time
        logger.info(f"Tool {tool_name} completed in {elapsed:.2f}s")

        return result
```

**Caching Middleware:**
```python
from datetime import datetime, timedelta

_cache: dict[str, tuple[Any, datetime]] = {}
_cache_ttl = timedelta(minutes=5)

class CachingMiddleware(Middleware):
    async def on_call_tool(self, ctx, tool_name: str, arguments: dict):
        # Cache key
        cache_key = f"{tool_name}:{json.dumps(arguments, sort_keys=True)}"

        # Check cache
        if cache_key in _cache:
            result, timestamp = _cache[cache_key]
            if datetime.now() - timestamp < _cache_ttl:
                logger.debug(f"Cache HIT: {cache_key}")
                return result

        # Cache MISS
        result = await super().on_call_tool(ctx, tool_name, arguments)
        _cache[cache_key] = (result, datetime.now())

        return result
```

**Rate Limiting Middleware:**
```python
from collections import defaultdict
import asyncio

_rate_limits: dict[str, list[float]] = defaultdict(list)
_max_requests_per_minute = 60

class RateLimitMiddleware(Middleware):
    async def on_call_tool(self, ctx, tool_name: str, arguments: dict):
        client_id = ctx.request_id or "default"
        now = time.time()

        # Cleanup old requests
        _rate_limits[client_id] = [
            t for t in _rate_limits[client_id]
            if now - t < 60  # Last 60 seconds
        ]

        # Check rate limit
        if len(_rate_limits[client_id]) >= _max_requests_per_minute:
            raise Exception("Rate limit exceeded: 60 requests/minute")

        # Record request
        _rate_limits[client_id].append(now)

        return await super().on_call_tool(ctx, tool_name, arguments)
```

### 3. Pipeline Composition для complex workflows

**Паттерн: Search → Analyze → Summarize**

```python
from src.pipelines import Pipeline

@mcp.tool(
    description="Research pipeline with AI analysis",
    tags={"research", "ai"}
)
async def research_pipeline(
    query: str,
    ctx: Context | None = None
) -> dict[str, Any]:
    """Multi-step research workflow."""
    pipeline = Pipeline(ctx)

    results = await (
        pipeline
        .add_step(
            "search",
            pipeline_search_and_analyze,
            query=query,
            limit=10
        )
        .add_step(
            "analyze",
            pipeline_llm_analyze,
            # previous_results передается автоматически
        )
        .add_step(
            "summarize",
            pipeline_llm_summarize,
            # previous_results передается автоматически
        )
        .execute()
    )

    return {
        "query": query,
        "search_results": results["search"],
        "analysis": results["analyze"],
        "summary": results["summarize"]
    }
```

**Pipeline Step Implementation:**

```python
async def pipeline_search_and_analyze(
    query: str,
    limit: int = 10,
    ctx: Context | None = None,
    previous_results: dict | None = None
) -> dict[str, Any]:
    """Search R2R and return results."""
    if ctx:
        await ctx.info(f"Searching R2R: {query}")
        await ctx.report_progress(0, 100, "Searching...")

    response = await _client.post(
        "/v3/retrieval/search",
        json={
            "query": query,
            "limit": limit,
            "use_hybrid_search": True
        }
    )

    if ctx:
        await ctx.report_progress(100, 100, "Search completed")

    return response.json()

async def pipeline_llm_analyze(
    ctx: Context | None = None,
    previous_results: dict | None = None
) -> dict[str, Any]:
    """AI analysis of search results."""
    if not ctx:
        return {"error": "Context required for LLM sampling"}

    search_results = previous_results.get("search") if previous_results else {}

    await ctx.info("Analyzing search results with AI...")
    await ctx.report_progress(0, 100, "AI analysis...")

    # LLM sampling
    response = await ctx.sample(
        messages=[
            {"role": "user", "content": f"Analyze these search results and identify key themes: {json.dumps(search_results)}"}
        ],
        temperature=0.2
    )

    await ctx.report_progress(100, 100, "Analysis completed")

    try:
        analysis = json.loads(response.text)
    except json.JSONDecodeError:
        analysis = {"raw_response": response.text}

    return analysis

async def pipeline_llm_summarize(
    ctx: Context | None = None,
    previous_results: dict | None = None
) -> dict[str, Any]:
    """Executive summary of analysis."""
    if not ctx:
        return {"error": "Context required for LLM sampling"}

    analysis = previous_results.get("analyze") if previous_results else {}

    await ctx.info("Creating executive summary...")
    await ctx.report_progress(0, 100, "Summarizing...")

    response = await ctx.sample(
        messages=[
            {"role": "user", "content": f"Create an executive summary (2-3 sentences) of this analysis: {json.dumps(analysis)}"}
        ],
        temperature=0.3
    )

    await ctx.report_progress(100, 100, "Summary completed")

    return {
        "summary": response.text,
        "timestamp": datetime.now().isoformat()
    }
```

### 4. R2R Configuration Best Practices

**Environment Variables:**
```env
# R2R Backend
R2R_BASE_URL=http://localhost:7272
R2R_API_KEY=your_api_key_here
R2R_TIMEOUT=30.0

# FastMCP Server
FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPENAPI_PARSER=true
DEBUG_LOGGING=false

# Optional: R2R OpenAPI spec URL
R2R_OPENAPI_URL=${R2R_BASE_URL}/openapi.json
```

**R2R Search Settings (default для production):**
```json
{
  "use_hybrid_search": true,
  "search_strategy": "vanilla",
  "limit": 10,
  "chunk_settings": {
    "enabled": true,
    "index_measure": "cosine_distance"
  },
  "graph_settings": {
    "enabled": true
  },
  "hybrid_settings": {
    "full_text_weight": 1.0,
    "semantic_weight": 5.0,
    "rrf_k": 50
  }
}
```

**R2R Agent Settings (research mode):**
```json
{
  "mode": "research",
  "tools": ["rag", "reasoning", "critique", "python_executor"],
  "max_tokens": 4000,
  "temperature": 0.1,
  "thinking_budget": 4096
}
```

---

## ✅ Законченность решения

### Что дает комбинация FastMCP + R2R?

**1. Полноценное RAG-приложение "из коробки":**

```text
✅ Document Management
   - Upload (FastMCP tool → R2R POST /v3/documents)
   - Metadata (FastMCP resource → R2R GET /v3/documents/{id})
   - Deletion (FastMCP tool → R2R DELETE /v3/documents/{id})

✅ Search & Retrieval
   - Semantic search (vector similarity)
   - Full-text search (keyword matching)
   - Hybrid search (combined scoring)
   - Graph search (entity relationships)

✅ RAG Generation
   - Context-aware responses
   - Citation tracking
   - Streaming support
   - Multi-turn conversations

✅ Knowledge Graph
   - Entity extraction
   - Relationship detection
   - Community detection
   - Graph-enhanced RAG (GraphRAG)

✅ Agent Reasoning
   - Research mode (extended thinking)
   - Tool calling (Python executor, web search)
   - Multi-step reasoning
   - Critique and refinement

✅ Multi-tenancy
   - Collections (organize documents)
   - User management
   - Access control

✅ Production Features
   - Authentication (JWT/Bearer)
   - Middleware (logging, caching, rate limiting)
   - Error handling
   - Monitoring
   - Streaming
```

**2. Developer Experience:**

```python
# Minimal setup (30 minutes)
from fastmcp import FastMCP

mcp = FastMCP.from_openapi(
    spec_url="http://localhost:7272/openapi.json",
    auth=DynamicBearerAuth()
)

if __name__ == "__main__":
    mcp.run()
```

**3. Гибкость и расширяемость:**

```python
# Custom tools (добавить свою логику)
@mcp.tool()
async def custom_search(query: str, ctx: Context) -> dict:
    # Custom pre-processing
    enhanced_query = preprocess(query)

    # R2R search
    results = await _client.post("/v3/retrieval/search", ...)

    # Custom post-processing
    return postprocess(results)

# Middleware (cross-cutting concerns)
mcp.add_middleware(LoggingMiddleware)
mcp.add_middleware(CachingMiddleware)
mcp.add_middleware(RateLimitMiddleware)

# Pipelines (complex workflows)
@mcp.tool()
async def research_pipeline(query: str, ctx: Context) -> dict:
    pipeline = Pipeline(ctx)
    return await pipeline.add_step(...).execute()
```

---

## 🎯 Production Patterns

### Pattern 1: Auto-generated + Custom Tools

**Проблема:** OpenAPI auto-generation дает базовую функциональность, но нужны enhanced tools.

**Решение:** Комбинируйте auto-generated и custom tools.

```python
# Auto-generate basic tools
mcp = FastMCP.from_openapi(
    spec_url="http://localhost:7272/openapi.json",
    route_maps=[...],
    auth=DynamicBearerAuth()
)

# Add custom enhanced tools
@mcp.tool(
    description="Enhanced search with AI analysis and progress reporting"
)
async def enhanced_search(
    query: str,
    limit: int = 10,
    ctx: Context | None = None
) -> dict[str, Any]:
    """Search with progress and AI analysis."""
    # ... implementation ...

@mcp.tool(
    description="Research pipeline: search → analyze → summarize"
)
async def research_pipeline(
    query: str,
    ctx: Context | None = None
) -> dict[str, Any]:
    """Multi-step research workflow."""
    # ... implementation ...
```

**Результат:**
- ✅ Базовые tools из OpenAPI (быстро, без кода)
- ✅ Enhanced tools с Context (progress, logging, LLM sampling)
- ✅ Pipeline tools (complex workflows)

---

### Pattern 2: Resource Templates для динамических данных

**Проблема:** Нужен доступ к документам по ID через Resources (не Tools).

**Решение:** Resource Templates с URI parameters.

```python
from fastmcp import ResourceTemplate

@mcp.resource_template(
    uri_template="r2r://documents/{document_id}",
    name="R2R Document",
    description="Get R2R document metadata by ID",
    annotations={"readOnlyHint": True}
)
async def r2r_document_resource(
    document_id: str,
    ctx: Context | None = None
) -> str:
    """Fetch document metadata from R2R."""
    if ctx:
        await ctx.info(f"Fetching document: {document_id}")

    try:
        response = await _client.get(f"/v3/documents/{document_id}")
        document = response.json()

        return json.dumps(document, indent=2)
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to fetch document: {e}")
        return json.dumps({"error": str(e)})
```

**Использование из LLM:**
```python
# LLM может прочитать документ через resource
content = await client.read_resource("r2r://documents/uuid-here")
```

---

### Pattern 3: Prompts для reusable templates

**Проблема:** Одинаковые промпты повторяются в разных tools.

**Решение:** Centralized prompt management.

```python
@mcp.prompt(
    name="rag_query_prompt",
    description="Structured prompt for RAG queries"
)
async def rag_query_prompt(query: str, context: str = "") -> list[dict]:
    """Generate structured RAG query prompt."""
    return [
        {
            "role": "system",
            "content": "You are a helpful assistant that answers questions based on provided context."
        },
        {
            "role": "user",
            "content": f"""Question: {query}

Context: {context}

Please provide a detailed, accurate answer based solely on the context provided."""
        }
    ]

@mcp.prompt(
    name="document_analysis_prompt",
    description="Analyze document content"
)
async def document_analysis_prompt(
    document: str,
    analysis_type: str = "summary"
) -> list[dict]:
    """Generate document analysis prompt."""
    prompts = {
        "summary": "Provide a concise summary of the document.",
        "entities": "Extract all key entities (people, organizations, locations).",
        "topics": "Identify main topics and themes.",
        "sentiment": "Analyze the sentiment and tone."
    }

    instruction = prompts.get(analysis_type, prompts["summary"])

    return [
        {
            "role": "user",
            "content": f"""Document:
{document}

Task: {instruction}"""
        }
    ]
```

**Использование:**
```python
# LLM может получить prompt template
prompt = await client.get_prompt("rag_query_prompt", arguments={"query": "What is R2R?"})
```

---

### Pattern 4: Middleware Chaining

**Проблема:** Нужно логирование, кэширование, rate limiting одновременно.

**Решение:** Middleware chain (onion model).

```python
# Middleware order (execution order)
mcp.add_middleware(LoggingMiddleware)      # Outer layer
mcp.add_middleware(RateLimitMiddleware)    # Middle layer
mcp.add_middleware(CachingMiddleware)      # Inner layer

# Execution flow:
# Request
#   ↓
# LoggingMiddleware.on_request (before)
#   ↓
# RateLimitMiddleware.on_request (before)
#   ↓
# CachingMiddleware.on_request (before)
#   ↓
# Tool Execution
#   ↓
# CachingMiddleware.on_request (after)
#   ↓
# RateLimitMiddleware.on_request (after)
#   ↓
# LoggingMiddleware.on_request (after)
#   ↓
# Response
```

---

### Pattern 5: Conditional Pipelines

**Проблема:** Workflow зависит от промежуточных результатов.

**Решение:** ConditionalPipeline с branches.

```python
from src.pipelines import ConditionalPipeline

@mcp.tool()
async def smart_search(
    query: str,
    ctx: Context | None = None
) -> dict[str, Any]:
    """Smart search with conditional analysis."""
    pipeline = ConditionalPipeline(ctx)

    # Step 1: Search
    pipeline.add_step("search", pipeline_search_and_analyze, query=query)

    # Step 2: Conditional branch
    async def check_relevance(previous_results: dict) -> bool:
        """Check if results are relevant."""
        results = previous_results.get("search", {})
        # Check if top result score > 0.8
        return results.get("results", [{}])[0].get("score", 0) > 0.8

    # High relevance → quick summary
    pipeline.add_conditional_step(
        "high_relevance_summary",
        pipeline_llm_summarize,
        condition=check_relevance
    )

    # Low relevance → deep analysis
    pipeline.add_conditional_step(
        "low_relevance_analysis",
        pipeline_llm_analyze,
        condition=lambda r: not await check_relevance(r)
    )

    return await pipeline.execute()
```

---

## 💡 Практические примеры

### Example 1: Minimal FastMCP + R2R Setup

**Время реализации:** 30 минут

```python
"""Minimal FastMCP R2R Server - Auto-generated from OpenAPI."""
import os
from dotenv import load_dotenv
from fastmcp import FastMCP
import httpx

load_dotenv()

# Dynamic authentication (request-time)
class DynamicBearerAuth(httpx.Auth):
    def auth_flow(self, request: httpx.Request):
        api_key = os.getenv("R2R_API_KEY", "")
        if api_key:
            request.headers["Authorization"] = f"Bearer {api_key}"
        yield request

# Auto-generate MCP server from OpenAPI
mcp = FastMCP.from_openapi(
    name="R2R MCP Server",
    spec_url=os.getenv("R2R_OPENAPI_URL", "http://localhost:7272/openapi.json"),
    base_url=os.getenv("R2R_BASE_URL", "http://localhost:7272"),
    auth=DynamicBearerAuth()
)

if __name__ == "__main__":
    mcp.run()
```

**Результат:**
- ✅ 81 R2R endpoints → 114 auto-generated MCP routes
- ✅ Resources для GET endpoints (read-only data)
- ✅ Tools для POST/PUT/DELETE (actions)

---

### Example 2: Enhanced Search Tool

**Добавление AI анализа и progress reporting:**

```python
@mcp.tool(
    description="Enhanced search with AI analysis",
    tags={"search", "ai"}
)
async def enhanced_search(
    query: str,
    limit: int = 10,
    use_hybrid_search: bool = True,
    ctx: Context | None = None
) -> dict[str, Any]:
    """Search R2R with progress and AI analysis."""
    if ctx:
        await ctx.info(f"Starting search: {query}")
        await ctx.report_progress(0, 100, "Searching R2R...")

    # R2R search
    response = await _client.post(
        "/v3/retrieval/search",
        json={
            "query": query,
            "limit": limit,
            "use_hybrid_search": use_hybrid_search,
            "search_strategy": "vanilla"
        }
    )

    results = response.json()

    if ctx:
        await ctx.report_progress(50, 100, "Analyzing results...")

        # AI analysis
        analysis = await ctx.sample(
            messages=[{
                "role": "user",
                "content": f"Analyze these search results and identify key themes: {json.dumps(results)}"
            }],
            temperature=0.2
        )

        await ctx.report_progress(100, 100, "Completed")

        return {
            "query": query,
            "results": results,
            "analysis": analysis.text
        }

    return results
```

---

### Example 3: Research Pipeline

**Multi-step workflow: Search → Analyze → Summarize**

```python
from src.pipelines import Pipeline

@mcp.tool(
    description="Research pipeline with AI analysis",
    tags={"research", "ai"}
)
async def research_pipeline(
    query: str,
    max_results: int = 10,
    ctx: Context | None = None
) -> dict[str, Any]:
    """Multi-step research workflow."""
    pipeline = Pipeline(ctx)

    results = await (
        pipeline
        .add_step(
            "search",
            pipeline_search_and_analyze,
            query=query,
            limit=max_results
        )
        .add_step("analyze", pipeline_llm_analyze)
        .add_step("summarize", pipeline_llm_summarize)
        .execute()
    )

    return {
        "query": query,
        "timestamp": datetime.now().isoformat(),
        "search_results": results["search"],
        "analysis": results["analyze"],
        "summary": results["summarize"]
    }
```

**Использование из Claude:**
```bash
User: Research "machine learning best practices" in the knowledge base

Claude: Let me use the research pipeline...
[Calls research_pipeline tool]

Result:
- Found 10 relevant documents
- Key themes: model evaluation, data preprocessing, hyperparameter tuning
- Summary: Best practices include cross-validation, feature engineering,
          and proper train/test splitting.
```

---

### Example 4: Comparative Analysis Tool

**Сравнение двух queries через R2R:**

```python
@mcp.tool(
    description="Compare search results for two queries",
    tags={"comparison", "ai"}
)
async def comparative_analysis(
    query1: str,
    query2: str,
    limit: int = 5,
    ctx: Context | None = None
) -> dict[str, Any]:
    """Compare search results for two queries."""
    if ctx:
        await ctx.info(f"Comparing: '{query1}' vs '{query2}'")
        await ctx.report_progress(0, 100, "Searching...")

    # Search 1
    response1 = await _client.post(
        "/v3/retrieval/search",
        json={"query": query1, "limit": limit}
    )

    if ctx:
        await ctx.report_progress(30, 100, "First search completed")

    # Search 2
    response2 = await _client.post(
        "/v3/retrieval/search",
        json={"query": query2, "limit": limit}
    )

    if ctx:
        await ctx.report_progress(60, 100, "Both searches completed")

    results1 = response1.json()
    results2 = response2.json()

    if ctx:
        await ctx.report_progress(80, 100, "Analyzing differences...")

        # AI comparative analysis
        comparison = await ctx.sample(
            messages=[{
                "role": "user",
                "content": f"""Compare these two sets of search results:

Query 1: {query1}
Results 1: {json.dumps(results1)}

Query 2: {query2}
Results 2: {json.dumps(results2)}

Identify:
1. Overlapping documents
2. Unique aspects of each query
3. Key differences in retrieved content"""
            }],
            temperature=0.2
        )

        await ctx.report_progress(100, 100, "Analysis completed")

        return {
            "query1": query1,
            "query2": query2,
            "results1": results1,
            "results2": results2,
            "comparison": comparison.text
        }

    return {
        "query1": query1,
        "query2": query2,
        "results1": results1,
        "results2": results2
    }
```

---

## 📊 Сравнительный анализ

### R2R vs FastMCP: Когда использовать что?

| Критерий | R2R | FastMCP | Рекомендация |
|----------|-----|---------|--------------|
| **Document Ingestion** | ✅ Native | 🔄 Proxy to R2R | Use R2R directly |
| **Search (semantic/hybrid)** | ✅ Native | 🔄 Proxy to R2R | Use R2R via FastMCP tool |
| **RAG Generation** | ✅ Native | 🔄 Proxy + enhance | Use R2R via FastMCP tool + ctx.sample |
| **Knowledge Graph** | ✅ Native | 🔄 Proxy to R2R | Use R2R via FastMCP tool |
| **Agent Reasoning** | ✅ Native | 🔄 Proxy + enhance | Use R2R agent OR FastMCP ctx.sample |
| **MCP Interface** | ❌ | ✅ Native | Use FastMCP |
| **LLM Tools/Resources** | ❌ | ✅ Native | Use FastMCP |
| **Middleware** | ❌ | ✅ Native | Use FastMCP |
| **Pipeline Composition** | ❌ | ✅ Native | Use FastMCP |
| **Progress Reporting** | ❌ | ✅ Native (Context) | Use FastMCP ctx.report_progress |
| **LLM Sampling in tools** | ❌ | ✅ Native (Context) | Use FastMCP ctx.sample |
| **Authentication** | ✅ JWT/Bearer | ✅ JWT/OAuth | Both (R2R: API, FastMCP: MCP) |
| **Caching** | ✅ Built-in | ✅ Middleware | Both (different layers) |
| **Deployment** | ✅ Docker/K8s | ✅ stdio/HTTP/Cloud | Both (different purposes) |

### Когда использовать только R2R?

**Сценарии:**
- Простой REST API без LLM интеграции
- Backend для существующего frontend приложения
- Batch processing (ingestion, graph building)
- Analytics и reporting (прямые SQL запросы к PostgreSQL)

**Пример:**
```python
# Прямой Python SDK
from r2r import R2RClient

client = R2RClient("http://localhost:7272")

# Upload documents
client.documents.create(file=open("doc.pdf", "rb"))

# Search
results = client.retrieval.search(query="machine learning")

# RAG
answer = client.retrieval.rag(query="What is RAG?")
```

### Когда использовать FastMCP + R2R?

**Сценарии:**
- LLM интеграция (Claude Desktop, OpenAI, etc.)
- Autonomous agents с tool calling
- Complex workflows (pipelines)
- Progress reporting для UI
- AI-enhanced analysis (ctx.sample)
- Middleware requirements (logging, caching, rate limiting)

**Пример:**
```python
# FastMCP MCP Server
from fastmcp import FastMCP

mcp = FastMCP.from_openapi(
    spec_url="http://localhost:7272/openapi.json",
    auth=DynamicBearerAuth()
)

@mcp.tool()
async def enhanced_rag(query: str, ctx: Context) -> dict:
    # Progress reporting
    await ctx.report_progress(0, 100, "Searching...")

    # R2R RAG
    response = await _client.post("/v3/retrieval/rag", ...)

    await ctx.report_progress(50, 100, "Analyzing...")

    # AI enhancement
    analysis = await ctx.sample(...)

    await ctx.report_progress(100, 100, "Completed")

    return {"answer": response.json(), "analysis": analysis.text}
```

### Когда использовать обе системы параллельно?

**Сценарии:**
- R2R для batch ingestion + FastMCP для query/RAG
- R2R REST API для frontend + FastMCP MCP для LLM agents
- R2R analytics dashboard + FastMCP conversational interface

**Архитектура:**
```text
┌────────────────┐        ┌────────────────┐
│   Frontend     │────────│  LLM (Claude)  │
│   (React)      │  REST  │                │
└────────┬───────┘        └────────┬───────┘
         │                         │ MCP
         │                         │
┌────────▼────────┐       ┌────────▼────────┐
│   R2R REST API  │       │  FastMCP Server │
│   (Direct)      │       │  (MCP)          │
└────────┬────────┘       └────────┬────────┘
         │                         │
         │ HTTP                    │ HTTP
         └────────┬────────────────┘
                  │
         ┌────────▼────────┐
         │   R2R Backend   │
         │   (Shared)      │
         └─────────────────┘
```

---

## 🎓 Заключение

### Ключевые выводы

1. **FastMCP и R2R - комплементарные системы:**
   - FastMCP: Интерфейс для LLM (MCP сервер)
   - R2R: Движок для RAG (Backend система)

2. **Архитектурная совместимость:**
   - Четырехслойная модель (Presentation → Business Logic → Data Access → R2R Backend)
   - OpenAPI auto-generation (REST API → MCP components)
   - DynamicBearerAuth (request-time authentication для serverless)

3. **Функциональная взаимодополняемость:**
   - R2R предоставляет: documents, search, RAG, knowledge graph, agent
   - FastMCP предоставляет: MCP interface, pipelines, middleware, Context

4. **Простота перехода:**
   - Модульный подход (Phase 1 → Phase 4)
   - Низкий риск (каждый phase независим)
   - Быстрая отдача (minimal setup за 30 минут)

5. **Production-ready паттерны:**
   - Auto-generated + custom tools
   - Resource templates для dynamic data
   - Prompts для reusable templates
   - Middleware chaining (logging, caching, rate limiting)
   - Pipeline composition (complex workflows)

6. **Законченность решения:**
   - Полноценное RAG-приложение из коробки
   - Гибкость и расширяемость
   - Production features (auth, monitoring, error handling)

### Рекомендации

**Для новых проектов:**
1. Начните с minimal FastMCP + R2R setup (30 минут)
2. Добавьте custom enhanced tools по мере необходимости
3. Внедряйте middleware для cross-cutting concerns
4. Используйте pipelines для complex workflows

**Для миграции:**
1. Сохраните существующий R2R backend без изменений
2. Создайте FastMCP сервер с OpenAPI auto-generation
3. Постепенно добавляйте enhanced tools и middleware
4. Тестируйте каждый phase перед переходом к следующему

**Для production:**
1. Используйте DynamicBearerAuth для serverless compatibility
2. Добавьте middleware (logging, caching, rate limiting)
3. Настройте monitoring и alerting
4. Оптимизируйте search settings (hybrid search, vanilla strategy)
5. Используйте research mode для complex queries

---

## 📚 Ссылки

### Документация

- **FastMCP:** [gofastmcp.com](https://gofastmcp.com)
  - `docs/fastmcp/README.md` - Навигационный hub (8 разделов)
  - `docs/fastmcp/09-layered-architecture.md` - Архитектурные паттерны

- **R2R:** [r2r-docs.sciphi.ai](https://r2r-docs.sciphi.ai/)
  - `docs/r2r/README.md` - Навигационный hub (8 разделов)
  - `docs/r2r/03-search-and-rag.md` - Search & RAG capabilities

- **Model Context Protocol:** [modelcontextprotocol.io](https://modelcontextprotocol.io)

### Production Code

- `src/server.py` - FastMCP R2R Server implementation
  - Lines 75-110: DynamicBearerAuth (CRITICAL for serverless)
  - Lines 121-145: Route mapping rules
  - Lines 328-519: Resource templates & Prompts
  - Lines 526-964: Enhanced tools & Pipeline tools

- `src/pipelines.py` - Pipeline patterns
  - Lines 28-160: ctx.sample patterns (7 types)
  - Lines 167-248: Pipeline base class
  - Lines 256-373: LLM-powered pipeline steps

### Configuration

- `.env.example` - Configuration template
- `.claude/config/.env` - R2R CLI credentials
- `openapi.json` - R2R OpenAPI 3.1 spec

---

**Версия документа:** 1.0
**Последнее обновление:** 2025-11-27
**Авторы:** Based on R2R Agent analysis + FastMCP/R2R documentation + Production code examples
