# Многослойная архитектура FastMCP приложений

## 📖 Концепция

FastMCP реализует **функциональную многослойную архитектуру** для создания MCP серверов, где каждый слой имеет четкую ответственность и взаимодействует через композицию функций, а не через иерархии классов.

### Базовая четырехуровневая модель

```text
┌─────────────────────────────────────────┐
│         Presentation Layer              │  ← Tools, Resources, Prompts
│  (MCP Components - LLM Interface)       │
├─────────────────────────────────────────┤
│         Business Logic Layer            │  ← Middleware, Pipelines, Context
│  (Processing, Auth, Validation)         │
├─────────────────────────────────────────┤
│         Data Access Layer               │  ← HTTP Clients, OpenAPI, Databases
│  (External APIs, Storage)               │
├─────────────────────────────────────────┤
│         Transport Layer                 │  ← stdio / HTTP / SSE
│  (Communication Protocol)               │
└─────────────────────────────────────────┘
```

## 🎯 Слои архитектуры

### 1. Presentation Layer (Слой представления)

**Ответственность:** Интерфейс для LLM - определяет ЧТО доступно.

**Компоненты:**
- **Tools** - действия, которые может выполнить LLM
- **Resources** - данные для чтения
- **Prompts** - переиспользуемые шаблоны

**Пример:**

```python
from fastmcp import FastMCP, Context

mcp = FastMCP("My Server")

@mcp.tool(
    description="Enhanced search with progress reporting",
    tags={"search", "rag"}
)
async def enhanced_search(
    query: str,
    limit: int = 10,
    use_hybrid_search: bool = True,
    ctx: Context | None = None
) -> dict[str, Any]:
    """Semantic search with progress and context logging."""
    if ctx:
        await ctx.info(f"Starting search for: {query}")
        await ctx.report_progress(0, 100, "Initializing search...")

    # Делегация к business logic layer
    response = await _client.post(
        "/v3/retrieval/search",
        json={
            "query": query,
            "limit": limit,
            "use_hybrid_search": use_hybrid_search
        }
    )

    if ctx:
        await ctx.report_progress(100, 100, "Search completed")

    return response.json()
```

**Лучшие практики:**
- ✅ Детальные docstrings для LLM понимания
- ✅ Строгая типизация (`type hints`)
- ✅ Опциональный `Context`: `ctx: Context | None = None`
- ✅ Annotations для подсказок: `readOnlyHint`, `destructiveHint`, `idempotentHint`
- ✅ Минимум бизнес-логики (делегация к pipelines)

**Что НЕ делать:**
- ❌ Сложная бизнес-логика в tools
- ❌ Прямые database/HTTP запросы (используй data access layer)
- ❌ Хардкодинг credentials

---

### 2. Business Logic Layer (Слой бизнес-логики)

**Ответственность:** Обработка, валидация, трансформация данных - определяет КАК выполняется логика.

**Компоненты:**
- **Middleware** - pipeline обработки запросов
- **Pipelines** - композиция операций
- **Context** - dependency injection
- **Validators** - проверка данных

#### 2.1 Middleware (Цепочка обработки)

```python
from fastmcp.server.middleware import Middleware, MiddlewareContext

class LoggingMiddleware(Middleware):
    async def on_call_tool(self, context: MiddlewareContext, call_next):
        start_time = datetime.now()
        tool_name = getattr(context.message, "name", "unknown")

        logger.info(f"→ Tool call started: {tool_name}")

        try:
            result = await call_next(context)
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"✓ Tool completed: {tool_name} ({duration:.2f}s)")
            return result
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(f"✗ Tool failed: {tool_name} ({duration:.2f}s) - {e}")
            raise

# Добавление middleware
mcp.add_middleware(LoggingMiddleware())
```

**Execution flow:**

```text
Request
   ↓
Middleware 1 → before (Logging)
   ↓
Middleware 2 → before (Authentication)
   ↓
Middleware 3 → before (Validation)
   ↓
Handler (Tool/Resource)
   ↓
Middleware 3 → after (Transform response)
   ↓
Middleware 2 → after (Audit)
   ↓
Middleware 1 → after (Metrics)
   ↓
Response
```

#### 2.2 Pipelines (Композиция операций)

```python
class Pipeline:
    """Chainable async operations."""

    def __init__(self, ctx: Context | None = None):
        self.ctx = ctx
        self.steps: list[tuple[str, callable, dict]] = []
        self._results: dict[str, Any] = {}

    def add_step(
        self,
        name: str,
        func: callable,
        **kwargs
    ) -> "Pipeline":
        """Add step to pipeline (chainable)."""
        self.steps.append((name, func, kwargs))
        return self  # Fluent interface

    async def execute(self) -> dict[str, Any]:
        """Execute all steps sequentially."""
        for step_name, func, kwargs in self.steps:
            if self.ctx:
                await self.ctx.info(f"Pipeline step: {step_name}")

            # Context propagation
            if "ctx" in func.__code__.co_varnames:
                kwargs["ctx"] = self.ctx

            # Result propagation
            if "previous_results" in func.__code__.co_varnames:
                kwargs["previous_results"] = self._results

            # Execute step
            self._results[step_name] = await func(**kwargs)

        return self._results

# Использование
pipeline = Pipeline(ctx)
results = await (
    pipeline
    .add_step("search", pipeline_search, query="AI safety")
    .add_step("analyze", pipeline_analyze)
    .add_step("summarize", pipeline_summarize)
    .execute()
)
```

#### 2.3 Context (Dependency Injection)

```python
@mcp.tool
async def advanced_tool(query: str, ctx: Context) -> dict:
    """Tool with full context access."""

    # List resources
    resources = await ctx.list_resources()

    # Read specific resource
    content = await ctx.read_resource("resource://config")

    # LLM sampling
    analysis = await ctx.sample(
        messages=f"Analyze: {query}",
        system_prompt="You are a data analyst",
        temperature=0.3
    )

    # Logging
    await ctx.info(f"Processed query: {query}")
    await ctx.debug(f"Found {len(resources)} resources")

    # Progress reporting
    await ctx.report_progress(50, 100)

    return {
        "query": query,
        "analysis": analysis.text,
        "resources_count": len(resources)
    }
```

---

### 3. Data Access Layer (Слой доступа к данным)

**Ответственность:** Взаимодействие с внешними системами - определяет ГДЕ хранятся данные.

**Компоненты:**
- **HTTP Clients** - API запросы
- **OpenAPI Integration** - auto-generated clients
- **Databases** - persistence
- **Authentication** - credentials management

#### 3.1 DynamicBearerAuth (Request-time authentication)

```python
import httpx
import os

class DynamicBearerAuth(httpx.Auth):
    """Auth handler that reads API key at REQUEST TIME.

    КРИТИЧНО для FastMCP Cloud/serverless:
    - Читает R2R_API_KEY при ВЫПОЛНЕНИИ запроса
    - НЕ при импорте модуля (когда env vars могут быть не инжектированы)
    """

    def auth_flow(self, request: httpx.Request):
        """Inject Bearer token at request time."""
        api_key = os.getenv("R2R_API_KEY", "")
        if api_key:
            request.headers["Authorization"] = f"Bearer {api_key}"
        yield request

# Create HTTP client
_client = httpx.AsyncClient(
    base_url="https://api.example.com",
    auth=DynamicBearerAuth(),  # ← Request-time auth
    timeout=30.0
)
```

**Почему request-time важно:**
- ✅ Serverless/cloud окружения инжектят env vars ПОСЛЕ импорта модуля
- ✅ Secrets rotation без перезапуска
- ✅ Multi-tenancy с разными credentials

#### 3.2 OpenAPI Auto-generation

```python
from fastmcp import FastMCP
import httpx

# Загрузка OpenAPI spec
spec = httpx.get("https://api.example.com/openapi.json").json()

# Создание HTTP client
client = httpx.AsyncClient(
    base_url="https://api.example.com",
    auth=DynamicBearerAuth()
)

# Auto-generate MCP server from OpenAPI
mcp = FastMCP.from_openapi(
    openapi_spec=spec,
    client=client,
    route_maps=[
        # GET with params → RESOURCE_TEMPLATE
        RouteMap(
            methods=["GET"],
            pattern=r"^/v3/.*\{.*\}.*$",
            mcp_type=MCPType.RESOURCE_TEMPLATE,
        ),
        # GET without params → RESOURCE
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
    ]
)
```

---

### 4. Transport Layer (Слой транспорта)

**Ответственность:** Коммуникация между клиентом и сервером.

**Типы транспортов:**
- **stdio** - локальное использование (Claude Desktop)
- **HTTP** - удаленный доступ
- **SSE** - streaming responses

```python
# stdio transport (local)
if __name__ == "__main__":
    mcp.run(transport="stdio")

# HTTP transport (remote)
if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
```

---

## 🏛️ Организация кода

### Простое приложение (Single-file)

```text
my_server.py
├── Presentation: @mcp.tool decorators
├── Business Logic: function implementations
├── Data Access: httpx.AsyncClient
└── Transport: mcp.run()
```

```python
# my_server.py
from fastmcp import FastMCP, Context
import httpx

mcp = FastMCP("Simple Server")

# Data Access Layer
_api_client = httpx.AsyncClient(base_url="https://api.example.com")

# Utils
def validate_input(value: str) -> bool:
    return len(value) >= 3

# Presentation Layer
@mcp.tool
async def get_data(resource_id: int, ctx: Context | None = None) -> dict:
    """Get data from external API."""
    if ctx:
        await ctx.info(f"Fetching resource {resource_id}")

    if resource_id < 1:
        raise ValueError("Invalid resource_id")

    response = await _api_client.get(f"/resources/{resource_id}")
    return response.json()

# Transport Layer
if __name__ == "__main__":
    mcp.run()
```

---

### Модульное приложение (Multi-file)

```text
src/
├── server.py              # Main entry point
├── presentation/
│   ├── tools.py           # @mcp.tool definitions
│   ├── resources.py       # @mcp.resource definitions
│   └── prompts.py         # @mcp.prompt definitions
├── business_logic/
│   ├── middleware.py      # Auth, logging, validation
│   ├── pipelines.py       # Multi-step workflows
│   └── transformers.py    # Data transformation
├── data_access/
│   ├── clients.py         # HTTP/DB clients
│   └── auth.py            # Authentication handlers
└── utils/
    ├── formatters.py      # Pure functions
    └── validators.py      # Input validation
```

**server.py (Entrypoint):**

```python
from fastmcp import FastMCP
from src.presentation import tools, resources
from src.business_logic.middleware import LoggingMiddleware, AuthMiddleware
from src.data_access.clients import get_api_client

# Initialize server
mcp = FastMCP("Production Server")

# Add middleware (business logic layer)
mcp.add_middleware(LoggingMiddleware())
mcp.add_middleware(AuthMiddleware())

# Initialize data access
api_client = get_api_client()

# Register components (presentation layer)
tools.register_all(mcp, api_client)
resources.register_all(mcp, api_client)

# Transport
if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
```

**presentation/tools.py:**

```python
from fastmcp import FastMCP, Context

def register_all(mcp: FastMCP, api_client):
    """Register all tools."""

    @mcp.tool
    async def search(query: str, ctx: Context | None = None) -> dict:
        """Search resources."""
        from src.business_logic.pipelines import search_pipeline

        return await search_pipeline(
            query=query,
            client=api_client,
            ctx=ctx
        )
```

**business_logic/pipelines.py:**

```python
from fastmcp import Context

async def search_pipeline(
    query: str,
    client,
    ctx: Context | None = None
) -> dict:
    """Multi-step search pipeline."""
    results = {}

    # Step 1: Search
    if ctx:
        await ctx.info("Step 1: Searching...")

    search_results = await client.post(
        "/search",
        json={"query": query}
    )
    results["search"] = search_results.json()

    # Step 2: Analyze with LLM
    if ctx:
        await ctx.info("Step 2: Analyzing...")

        analysis = await ctx.sample(
            messages=f"Analyze search results: {results['search']}",
            temperature=0.3
        )
        results["analysis"] = analysis.text

    return results
```

---

## ❌ Что НЕ использовать (классические паттерны)

### Controllers → НЕ НУЖНЫ

FastMCP Tools уже являются entry points (как контроллеры в REST API).

```python
# ❌ НЕ ДЕЛАЙ ТАК - излишняя абстракция
class SearchController:
    def __init__(self, service: SearchService):
        self.service = service

    def handle_search(self, request: SearchRequest) -> SearchResponse:
        return self.service.search(request.query)

# ✅ ДЕЛАЙ ТАК - Tools = Controllers
@mcp.tool
async def search(query: str) -> dict:
    """Direct and simple."""
    response = await _client.post("/search", json={"query": query})
    return response.json()
```

---

### Services → ЗАМЕНЯЮТСЯ на Pipelines

```python
# ❌ НЕ ДЕЛАЙ ТАК - OOP overhead
class SearchService:
    def __init__(self, repo: SearchRepository):
        self.repo = repo

    def search(self, query: str) -> List[Result]:
        results = self.repo.search(query)
        return self._filter(results)

# ✅ ДЕЛАЙ ТАК - Functional composition
async def search_pipeline(query: str, ctx: Context) -> dict:
    """Pipeline function instead of Service class."""
    results = await _client.post("/search", json={"query": query})
    filtered = filter_results(results.json())

    if ctx:
        analysis = await ctx.sample(f"Analyze: {filtered}")
        return {"results": filtered, "analysis": analysis.text}

    return {"results": filtered}
```

---

### Repositories → HTTP Clients напрямую

```python
# ❌ НЕ ДЕЛАЙ ТАК - излишняя абстракция для REST API
class SearchRepository:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    def search(self, query: str) -> List[Document]:
        response = self.client.post("/search", json={"query": query})
        return response.json()

# ✅ ДЕЛАЙ ТАК - Direct HTTP client
_client = httpx.AsyncClient(base_url="https://api.example.com")

@mcp.tool
async def search(query: str) -> dict:
    response = await _client.post("/search", json={"query": query})
    return response.json()
```

---

## 🟡 Когда классы УМЕСТНЫ

### Service Pattern - для сложной domain logic

```python
# ✅ УМЕСТНО: Complex domain logic со state
class GraphAnalysisService:
    """Service для complex graph algorithms."""

    def __init__(self, ctx: Context):
        self.ctx = ctx
        self._graph_cache = {}

    async def analyze_community_structure(
        self,
        collection_id: str
    ) -> dict:
        """Complex multi-step graph analysis."""
        entities = await self._fetch_entities(collection_id)
        graph = self._build_graph(entities)
        communities = self._leiden_algorithm(graph)

        analysis = await self.ctx.sample(
            f"Analyze communities: {communities}"
        )

        return {
            "communities": communities,
            "analysis": analysis.text
        }

    def _build_graph(self, entities):
        import networkx as nx
        # Complex graph building logic
        ...

    def _leiden_algorithm(self, graph):
        # Complex community detection
        ...
```

**Используй Service ТОЛЬКО если:**
- ✅ Сложная domain logic с state
- ✅ Композиция нескольких источников данных
- ✅ Сложные алгоритмы (graph analysis, ML inference)

---

### Repository Pattern - для complex data access

```python
# ✅ УМЕСТНО: Multiple data sources с fallback
class MultiSourceRepository:
    """Repository для complex data access patterns."""

    def __init__(
        self,
        primary_client: httpx.AsyncClient,
        fallback_client: httpx.AsyncClient
    ):
        self.primary = primary_client
        self.fallback = fallback_client
        self._cache = {}

    async def search_with_fallback(self, query: str) -> dict:
        """Search with caching and fallback."""
        # Check cache
        if query in self._cache:
            return self._cache[query]

        # Try primary
        try:
            result = await self.primary.post("/search", json={"query": query})
            self._cache[query] = result.json()
            return result.json()
        except httpx.HTTPError:
            pass

        # Fallback to secondary
        result = await self.fallback.post("/search", json={"query": query})
        return result.json()
```

**Используй Repository ТОЛЬКО если:**
- ✅ Multiple data sources с fallback logic
- ✅ Complex caching strategies
- ✅ Database access (PostgreSQL, MongoDB)

---

## 📊 Сравнительная таблица

| Паттерн | Traditional Backend | FastMCP | Когда использовать |
|---------|---------------------|---------|-------------------|
| **Controllers** | ✅ Обязательно | ❌ НЕ нужны | НИКОГДА (есть Tools) |
| **Services** | ✅ Обязательно | 🟡 Редко | Сложная domain logic |
| **Repositories** | ✅ Обязательно | 🟡 Редко | Multiple data sources |
| **Pipelines** | ❌ Редко | ✅ Основной | Multi-step workflows |
| **Middleware** | 🟡 Опционально | ✅ Основной | Cross-cutting concerns |
| **Utils** | ✅ Всегда | ✅ Всегда | Pure functions |

---

## ✅ Лучшие практики

### По слоям

**Presentation Layer:**
- ✅ Детальные docstrings
- ✅ Строгая типизация
- ✅ Опциональный Context: `ctx: Context | None = None`
- ✅ Минимум бизнес-логики
- ❌ Прямые HTTP/DB запросы

**Business Logic Layer:**
- ✅ Pipeline functions для multi-step
- ✅ Middleware для cross-cutting concerns
- ✅ Context для dependency injection
- ✅ Async/await для I/O
- ❌ Сложные class hierarchies

**Data Access Layer:**
- ✅ Request-time authentication (DynamicBearerAuth)
- ✅ Async HTTP clients
- ✅ Error handling и retry logic
- ❌ Module-level credentials
- ❌ Синхронные клиенты

---

## 🎯 Правило выбора подхода

```python
# 1. Простая операция (1-5 строк) → прямой код
@mcp.tool
async def simple_op(param: str) -> dict:
    return await _client.get(f"/api/{param}")

# 2. Multi-step (2-5 шагов) → pipeline function
@mcp.tool
async def complex_op(param: str, ctx: Context) -> dict:
    return await my_pipeline(param, ctx)

# 3. Очень сложная logic (>100 строк, state) → Service class
@mcp.tool
async def very_complex_op(param: str, ctx: Context) -> dict:
    service = ComplexService(ctx)
    return await service.do_complex_thing(param)
```

---

## 🚀 Эвристика выбора

```text
Операция выполняется за 1-5 строк?
  → Прямой код в tool

Операция требует 2-5 шагов?
  → Pipeline function

Операция требует state, сложные алгоритмы, >100 строк?
  → Service class

Работаешь с внешним API?
  → HTTP client напрямую

Работаешь с БД + кэширование + fallback?
  → Repository pattern
```

---

## 📝 Итоговые рекомендации

### Для 90% FastMCP проектов:

```text
✅ Используй:
- Tools/Resources/Prompts (вместо controllers)
- Pipeline functions (вместо services)
- HTTP Clients напрямую (вместо repositories)
- Middleware (для cross-cutting)
- Utils (для helpers)

❌ НЕ используй:
- Controllers (есть Tools)
- Service classes (есть Pipeline functions)
- Repository classes (для простых REST API)
- DTO classes (если не нужна сложная валидация)
```

### Для сложных проектов (10%):

```text
🟡 Можешь использовать:
- Service classes (для complex domain logic)
- Repository pattern (для multiple data sources)
- Dependency injection (через Context или globals)
```

---

## 🎓 Ключевая идея

**FastMCP favors functional composition over object hierarchies.**

Используй классы ТОЛЬКО когда функций недостаточно. В 90% случаев функции + pipelines + middleware достаточно для элегантного и поддерживаемого кода.

---

## 📚 См. также

- [Tools](./02-tools.md) - Создание инструментов для LLM
- [Middleware](./07-middleware-error-handling.md) - Cross-cutting concerns
- [Deployment](./06-deployment-configuration.md) - Production patterns
- [FastAPI Integration](./08-fastapi-openapi.md) - OpenAPI auto-generation
