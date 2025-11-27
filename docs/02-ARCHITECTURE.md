[← Back to Documentation Index](./README.md)

# Architecture & Core Concepts

**Глубокое понимание архитектуры** FastMCP + R2R интеграции: ключевые паттерны, layered design, и production-ready решения.

---

## 📑 Содержание

1. [4-Layer Architecture](#-1-4-layer-architecture)
2. [DynamicBearerAuth Pattern](#-2-dynamicbearerauth-pattern)
3. [ctx.sample Patterns](#-3-ctxsample-patterns---llm-operations)
4. [Pipeline Composition](#-4-pipeline-composition--middleware)
5. [OpenAPI Auto-Generation](#-5-openapi-auto-generation)
6. [Key Insights](#-key-insights)
7. [Practical Recommendations](#-practical-recommendations)

---

## 🏛️ 1. 4-Layer Architecture

### Overview

FastMCP + R2R образуют **4-layer stack** где каждый слой имеет четкую ответственность:

```text
┌─────────────────────────────────────────────────────────────┐
│                    LLM (Claude, GPT-4)                      │
│                                                             │
└───────────────────────┬─────────────────────────────────────┘
                        │ MCP Protocol (stdio/HTTP)
┌───────────────────────▼─────────────────────────────────────┐
│   LAYER 1: Presentation (FastMCP)                           │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ @mcp.tool() - Actions LLM can perform               │   │
│   │ @mcp.resource() - Data LLM can read                 │   │
│   │ @mcp.prompt() - Templates LLM can use               │   │
│   └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│   LAYER 2: Business Logic (FastMCP)                        │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ Pipeline - Multi-step workflows                     │   │
│   │ Middleware - Auth, logging, caching                 │   │
│   │ Context - Dependency injection, ctx.sample()        │   │
│   └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│   LAYER 3: Data Access (FastMCP → R2R)                     │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ httpx.AsyncClient - HTTP client                     │   │
│   │ DynamicBearerAuth - Request-time auth               │   │
│   │ OpenAPI Auto-Gen - Semantic routing                 │   │
│   └─────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API (HTTPS)
┌────────────────────────▼────────────────────────────────────┐
│   LAYER 4: RAG Backend (R2R)                                │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ Documents - Ingestion, metadata, search             │   │
│   │ Knowledge Graph - Entities, relationships           │   │
│   │ Agent - Reasoning, tool calling                     │   │
│   │ Collections - Multi-tenancy, access control         │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
│   Storage: PostgreSQL + pgvector + Neo4j + Redis           │
└─────────────────────────────────────────────────────────────┘
```

### Separation of Concerns

| Layer | Responsibility | Technology | примеры |
|-------|----------------|------------|---------|
| **Presentation** | LLM Interface | FastMCP decorators | `@mcp.tool()`, `@mcp.resource()` |
| **Business Logic** | Orchestration | FastMCP Context | Pipelines, Middleware, ctx.sample |
| **Data Access** | HTTP Communication | httpx | DynamicBearerAuth, OpenAPI routing |
| **RAG Backend** | Data & Computation | R2R | Search, RAG, Knowledge Graph, Agent |

**Ключевой принцип:**
- **FastMCP** = Presentation + Business Logic (LLM интерфейс)
- **R2R** = Data Access + Backend (RAG engine)

### Responsibilities Matrix

| Функция | R2R | FastMCP | Владелец |
|---------|-----|---------|----------|
| Document Ingestion | ✅ Core | ➡️ Proxy | R2R |
| Vector Search | ✅ Core | ➡️ Proxy | R2R |
| Knowledge Graph | ✅ Core | ➡️ Proxy | R2R |
| RAG Generation | ✅ Core | ➡️ Proxy | R2R |
| Agent (Reasoning) | ✅ Core | ➡️ Proxy | R2R |
| MCP Protocol | ❌ | ✅ Core | FastMCP |
| Tools/Resources | ❌ | ✅ Core | FastMCP |
| Middleware | ❌ | ✅ Core | FastMCP |
| Pipeline Composition | ❌ | ✅ Core | FastMCP |
| Context (DI) | ❌ | ✅ Core | FastMCP |

**Вывод**: Минимальное дублирование, четкое разделение ответственности.

---

## 🔐 2. DynamicBearerAuth Pattern

### The Problem

**Serverless окружения** (FastMCP Cloud, AWS Lambda, Google Cloud Functions) инжектят environment variables **ПОСЛЕ импорта модулей**.

Traditional approach fails:

```python
# ❌ НЕ РАБОТАЕТ в serverless
API_KEY = os.getenv("R2R_API_KEY")  # Empty string при импорте!

_client = httpx.AsyncClient(
    headers={"Authorization": f"Bearer {API_KEY}"}  # ❌ Пустой ключ
)
```

**Почему**: В serverless, env vars устанавливаются runtime после того как модуль уже импортирован.

### The Solution

**Request-time authentication** - читаем API key WHEN needed, NOT when imported:

```python
class DynamicBearerAuth(httpx.Auth):
    """Auth handler reading API key at REQUEST TIME.

    CRITICAL for serverless compatibility:
    - Reads R2R_API_KEY during request execution
    - NOT at module import time (when env vars uninitialized)
    - Ensures auth works in FastMCP Cloud, Lambda, etc.
    """

    def auth_flow(self, request: httpx.Request):
        """Inject Bearer token at request time."""
        # ✅ Читаем API key ЗДЕСЬ, при выполнении запроса
        api_key = os.getenv("R2R_API_KEY", "")

        if api_key:
            request.headers["Authorization"] = f"Bearer {api_key}"

        yield request

# ✅ РАБОТАЕТ в serverless
_client = httpx.AsyncClient(
    base_url=os.getenv("R2R_BASE_URL", "http://localhost:7272"),
    auth=DynamicBearerAuth(),  # Auth на request-time!
    timeout=30.0,
)
```

### Architecture Significance

**Benefits:**

1. **Serverless Compatibility** ✅
   - Env vars могут быть установлены поздно
   - Работает в Lambda, Cloud Run, FastMCP Cloud

2. **Security** 🔒
   - API key никогда не хардкодится
   - Можно менять без перезапуска сервера

3. **Lazy Initialization** 🦥
   - API key читается только когда нужен
   - Нет overhead при импорте модуля

4. **httpx.Auth Interface** 🔌
   - Стандартный протокол httpx
   - Совместимо с middleware и interceptors

### Code References

**Implementation:**
- `src/server.py:75-110` - DynamicBearerAuth class definition
- `src/server.py:170` - httpx.AsyncClient initialization с DynamicBearerAuth
- `src/r2r_typed.py:174-199` - R2RTypedClient usage

**Usage:**

```python
# В любом tool/resource
async def my_tool(ctx: Context | None = None) -> dict:
    # _client автоматически использует DynamicBearerAuth
    response = await _client.post("/v3/retrieval/search", json={...})
    return response.json()
```

---

## 🤖 3. ctx.sample Patterns - LLM Operations

### Overview

FastMCP предоставляет `ctx.sample()` для **LLM-powered операций** внутри tools и resources.

**7 основных паттернов** от простых до продвинутых.

### Pattern 1: Basic Prompting

**Самый простой** - direct text generation:

```python
async def sample_basic_generation(ctx: Context, prompt: str) -> str:
    """Simple text generation without special configuration."""
    response = await ctx.sample(prompt)
    return response.text  # type: ignore[union-attr]
```

**Use Case:** Быстрая генерация без role-playing или structured output.

**Example:**
```python
result = await sample_basic_generation(ctx, "Explain quantum computing in 2 sentences")
```

---

### Pattern 2: System Prompt (Role-Based)

**Role-based** ответы через system prompt:

```python
async def sample_with_system_prompt(
    ctx: Context,
    user_message: str,
    system_role: str = "expert data analyst"
) -> str:
    """Generate role-based responses using system prompt."""
    response = await ctx.sample(
        messages=user_message,
        system_prompt=f"You are an {system_role}. Provide detailed, accurate analysis.",
        temperature=0.3,  # Lower для focused responses
        max_tokens=1000,
    )
    return response.text  # type: ignore[union-attr]
```

**Use Case:** Специализированные ответы (аналитик, юрист, инженер, переводчик).

**Example:**
```python
analysis = await sample_with_system_prompt(
    ctx,
    "Analyze this data: {...}",
    system_role="statistician"
)
```

---

### Pattern 3: Structured Output

**Запрос structured data** (JSON, markdown, YAML):

```python
async def sample_structured_output(
    ctx: Context,
    data: dict,
    output_format: str = "json"
) -> dict:
    """Request structured output from LLM."""
    prompt = f"""Analyze the following data and return results in {output_format} format:

Data: {json.dumps(data, indent=2)}

Please structure your response as valid {output_format}."""

    response = await ctx.sample(
        messages=prompt,
        temperature=0.2,  # Очень низкая для structure
        max_tokens=2000,
    )

    # Parse JSON if requested
    if output_format == "json":
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return {"raw_response": response.text}

    return {"response": response.text}
```

**Use Case:** Парсинг данных, извлечение структуры, schema generation.

**Example:**
```python
result = await sample_structured_output(
    ctx,
    {"items": [1, 2, 3], "total": 6},
    output_format="json"
)
# → {"analysis": {...}, "insights": [...]}
```

---

### Pattern 4: Multi-Turn Conversations

**Диалоги** с message history:

```python
async def sample_multi_turn_conversation(
    ctx: Context,
    conversation_history: list[dict]
) -> str:
    """Multi-turn conversations with message history.

    Args:
        conversation_history: List of {"role": "user"|"assistant", "content": "..."}
    """
    # Convert to sampling messages format
    messages = [msg["content"] for msg in conversation_history]

    response = await ctx.sample(
        messages=messages,
        temperature=0.7,
        max_tokens=1500
    )

    return response.text  # type: ignore[union-attr]
```

**Use Case:** Chatbots, диалоговые агенты, contextual assistants.

**Example:**
```python
history = [
    {"role": "user", "content": "What is RAG?"},
    {"role": "assistant", "content": "RAG stands for..."},
    {"role": "user", "content": "How does it work with R2R?"}
]
response = await sample_multi_turn_conversation(ctx, history)
```

---

### Pattern 5: Retry Logic

**Production-ready** sampling с exponential backoff:

```python
async def sample_with_retry(
    ctx: Context,
    prompt: str,
    max_retries: int = 3
) -> str:
    """Sampling with retry logic for robustness."""
    for attempt in range(max_retries):
        try:
            await ctx.debug(f"Sampling attempt {attempt + 1}/{max_retries}")

            response = await ctx.sample(
                messages=prompt,
                temperature=0.5,
                max_tokens=1000
            )

            await ctx.debug(f"✓ Success on attempt {attempt + 1}")
            return response.text  # type: ignore[union-attr]

        except Exception as e:
            await ctx.error(f"Failed attempt {attempt + 1}: {e}")

            if attempt == max_retries - 1:
                raise

            # Exponential backoff: 2^0, 2^1, 2^2 seconds
            await asyncio.sleep(2 ** attempt)

    return ""  # Should never reach here
```

**Use Case:** Production environments, rate-limited APIs, unstable connections.

**Example:**
```python
result = await sample_with_retry(ctx, "Complex analysis task")
```

---

### Pattern 6: Model Preferences

**Рекомендации** по выбору модели и параметров:

| Use Case | Model | Temperature | Max Tokens | Rationale |
|----------|-------|-------------|------------|-----------|
| **Structured output** | claude-3-5-sonnet | 0.0-0.2 | 2000-4000 | Deterministic, precise |
| **Creative writing** | claude-3-opus | 0.7-0.9 | 4000+ | High creativity |
| **Code generation** | claude-3-5-sonnet | 0.2-0.4 | 4000-8000 | Balance accuracy/variety |
| **Data analysis** | claude-3-5-sonnet | 0.3-0.5 | 2000-4000 | Analytical, focused |
| **Summarization** | claude-3-haiku | 0.3 | 1000-2000 | Fast, cost-effective |

**Example:**
```python
# For structured output (low temperature)
response = await ctx.sample(
    messages="Extract entities from text",
    temperature=0.1,  # ← Very deterministic
    max_tokens=2000
)

# For creative tasks (high temperature)
response = await ctx.sample(
    messages="Write a creative story",
    temperature=0.8,  # ← More creative
    max_tokens=4000
)
```

---

### Pattern 7: Advanced Message Types

**Complex structures** with SamplingMessage:

```python
from fastmcp.types import SamplingMessage

# Advanced message with metadata
messages = [
    SamplingMessage(
        role="user",
        content="Analyze this data",
        metadata={"source": "api", "timestamp": "2025-11-27"}
    )
]

response = await ctx.sample(messages=messages)
```

**Use Case:** Когда нужны metadata, tool calls, или complex message structures.

### Code References

**Implementation:** `src/pipelines.py:46-160` (7 функций)

**Usage в проекте:**
- `src/server.py:670-964` - Enhanced tools используют patterns 1, 2, 3, 5

---

## 🔄 4. Pipeline Composition & Middleware

### Pipeline Architecture

**Цель:** Multi-step workflows с automatic result passing, error handling, progress tracking.

#### Base Pipeline Class

```python
class Pipeline:
    """Chain multiple operations with context tracking.

    Example:
        pipeline = Pipeline(ctx)
        result = await (
            pipeline
            .add_step("search", search_documents, query="AI")
            .add_step("analyze", analyze_results)
            .add_step("summarize", summarize_findings)
            .execute()
        )
    """

    def __init__(self, ctx: Context | None = None):
        self.ctx = ctx
        self.steps: list[dict] = []
        self.results: dict[str, Any] = {}

    def add_step(self, name: str, func: Callable, **kwargs) -> "Pipeline":
        """Add a step to the pipeline."""
        self.steps.append({"name": name, "func": func, "kwargs": kwargs})
        return self  # ← Chainable!

    async def execute(self) -> dict[str, Any]:
        """Execute all pipeline steps in order."""
        if self.ctx:
            await self.ctx.info(f"🔄 Starting {len(self.steps)} steps")
            await self.ctx.report_progress(0, len(self.steps))

        for idx, step in enumerate(self.steps):
            name = step["name"]
            func = step["func"]
            kwargs = step["kwargs"]

            if self.ctx:
                await self.ctx.info(f"⚙️ Step {idx + 1}: {name}")

            try:
                # Auto-inject context if function accepts it
                if "ctx" in func.__code__.co_varnames:
                    kwargs["ctx"] = self.ctx

                # Pass previous results
                kwargs["previous_results"] = self.results

                # Execute step
                result = await func(**kwargs)
                self.results[name] = result

                if self.ctx:
                    await self.ctx.report_progress(idx + 1, len(self.steps))
                    await self.ctx.debug(f"✓ Step {name} complete")

            except Exception as e:
                if self.ctx:
                    await self.ctx.error(f"❌ Step {name} failed: {e}")
                raise

        if self.ctx:
            await self.ctx.info(f"✅ Pipeline complete: {len(self.results)} results")

        return self.results
```

**Key Features:**
- ✅ **Chainable API** - `add_step().add_step().execute()`
- ✅ **Auto context injection** - `ctx` передается автоматически
- ✅ **Result passing** - каждый step получает `previous_results`
- ✅ **Progress tracking** - `ctx.report_progress()`
- ✅ **Error handling** - exceptions с context logging

#### ConditionalPipeline

**Условное выполнение** шагов:

```python
class ConditionalPipeline:
    """Pipeline with conditional step execution.

    Example:
        pipeline = ConditionalPipeline(ctx)
        pipeline.add_step("search", search_func)
        pipeline.add_step(
            "deep_analysis",
            expensive_llm_call,
            condition=lambda r: len(r["search"]["results"]) > 10
        )
        results = await pipeline.execute()
    """

    def add_step(
        self,
        name: str,
        func: Callable,
        condition: Callable | None = None,  # ← NEW!
        **kwargs
    ) -> "ConditionalPipeline":
        """Add a conditional step.

        Args:
            name: Step identifier
            func: Function to execute
            condition: Optional function(results: dict) -> bool
            **kwargs: Arguments for function
        """
        self.steps.append({
            "name": name,
            "func": func,
            "condition": condition,
            "kwargs": kwargs,
        })
        return self

    async def execute(self) -> dict[str, Any]:
        """Execute pipeline with conditional steps."""
        for step in self.steps:
            condition = step["condition"]

            # Check condition before execution
            if condition and not condition(self.results):
                if self.ctx:
                    await self.ctx.info(f"⏭️ Skipping {step['name']} (condition not met)")
                continue

            # Execute if condition passes (or no condition)
            # ... (same as Pipeline)
```

**Use Case:**
```python
pipeline = ConditionalPipeline(ctx)
pipeline.add_step("search", search_docs)
pipeline.add_step(
    "detailed_analysis",
    expensive_operation,
    condition=lambda r: len(r["search"]["results"]) > 10  # Only if много результатов
)
```

### Middleware Architecture

**Hook-based interception** для cross-cutting concerns.

#### Middleware Hierarchy

```text
Request Flow:
    │
    ├─→ on_message (lowest level)
    │       ↓
    ├─→ on_request
    │       ↓
    ├─→ on_call_tool / on_read_resource / on_get_prompt (parallel)
    │       ↓
    ├─→ Handler execution
    │       ↓
    ├─→ on_call_tool / on_read_resource / on_get_prompt (after)
    │       ↓
    ├─→ on_request (after)
    │       ↓
    └─→ on_message (after)
```

#### Creating Middleware

```python
from fastmcp import Middleware

class LoggingMiddleware(Middleware):
    async def on_request(self, request, call_next):
        """Log all requests."""
        logger.info(f"Request: {request.method}")

        # Call next middleware/handler
        response = await call_next(request)

        logger.info(f"Response: {response.status}")
        return response

    async def on_call_tool(self, tool_call, call_next):
        """Intercept tool calls."""
        logger.info(f"Tool: {tool_call.name}")

        # Modify tool call if needed
        if tool_call.name == "sensitive_operation":
            if not self.check_permissions():
                raise PermissionError("Access denied")

        result = await call_next(tool_call)
        return result

# Attach to server
mcp = FastMCP("MyServer")
mcp.add_middleware(LoggingMiddleware())
```

**Use Cases:**
- 🔐 **Authentication** - verify API keys, JWT tokens
- 📝 **Logging** - request/response logging
- ⏱️ **Rate Limiting** - throttle requests
- ✅ **Input Validation** - validate parameters
- 📊 **Metrics** - collect usage statistics

### Advanced Pipeline Patterns

#### Pattern: Fallback

```python
async def pipeline_with_fallback(
    primary_func: Callable,
    fallback_func: Callable,
    ctx: Context | None = None,
    **kwargs
) -> Any:
    """Execute function with fallback on error."""
    try:
        if ctx:
            await ctx.info("⚡ Attempting primary operation")

        result = await primary_func(ctx=ctx, **kwargs)

        if ctx:
            await ctx.info("✓ Primary operation successful")

        return result

    except Exception as e:
        if ctx:
            await ctx.error(f"❌ Primary failed: {e}")
            await ctx.info("🔄 Falling back to alternative")

        try:
            result = await fallback_func(ctx=ctx, **kwargs)

            if ctx:
                await ctx.info("✓ Fallback successful")

            return result

        except Exception as fallback_error:
            if ctx:
                await ctx.error(f"❌ Fallback also failed: {fallback_error}")
            raise
```

**Use Case:** Resilient systems - expensive LLM vs simple rules.

#### Pattern: Caching

```python
_pipeline_cache: dict[str, Any] = {}

async def cached_pipeline_step(
    cache_key: str,
    func: Callable,
    ttl_seconds: int = 300,
    ctx: Context | None = None,
    **kwargs
) -> Any:
    """Execute pipeline step with caching."""
    # Check cache
    if cache_key in _pipeline_cache:
        cached_result, cached_time = _pipeline_cache[cache_key]
        age = (datetime.utcnow() - cached_time).total_seconds()

        if age < ttl_seconds:
            if ctx:
                await ctx.info(f"📦 Cache hit: {cache_key} (age: {age:.1f}s)")
            return cached_result
        else:
            if ctx:
                await ctx.debug(f"🗑️ Cache expired: {cache_key}")
            del _pipeline_cache[cache_key]

    # Execute function
    if ctx:
        await ctx.info(f"🔄 Executing (cache miss): {cache_key}")

    if "ctx" in func.__code__.co_varnames:
        kwargs["ctx"] = ctx

    result = await func(**kwargs)

    # Store in cache
    _pipeline_cache[cache_key] = (result, datetime.utcnow())

    if ctx:
        await ctx.debug(f"💾 Cached result: {cache_key}")

    return result
```

**Use Case:** Expensive API calls, LLM operations, database queries.

### Code References

**Implementation:**
- `src/pipelines.py:169-248` - Pipeline base class
- `src/pipelines.py:413-480` - ConditionalPipeline
- `src/pipelines.py:487-531` - Fallback pattern
- `src/pipelines.py:538-589` - Caching pattern

---

## 🔧 5. OpenAPI Auto-Generation

### Overview

FastMCP автоматически генерирует MCP серверы из OpenAPI спецификаций через **semantic routing**.

**Преимущества:**
- ✅ Автоматическая генерация Tools/Resources/ResourceTemplates
- ✅ Поддержка 100+ endpoints без ручного кода
- ✅ Обновление через `make update-spec`

### Basic Usage

```python
from fastmcp import FastMCP
import httpx

# Load OpenAPI spec
spec = httpx.get("https://api.example.com/openapi.json").json()

# Auto-generate MCP server
mcp = FastMCP.from_openapi(
    openapi_spec=spec,
    client=httpx.AsyncClient(
        base_url="https://api.example.com",
        auth=DynamicBearerAuth()  # ← Request-time auth!
    )
)
```

### Route Mapping Rules

**DEFAULT_ROUTE_MAPPINGS** (порядок КРИТИЧЕН - first match wins):

```python
from fastmcp.openapi import RouteMap, RouteType

DEFAULT_ROUTE_MAPPINGS = [
    # Rule 1: GET с path parameters → ResourceTemplate
    RouteMap(
        methods=["GET"],
        pattern=r".*\{.*\}.*",  # Regex: contains {param}
        route_type=RouteType.RESOURCE_TEMPLATE
    ),
    # Example: GET /v3/documents/{id} → r2r://documents/{id}

    # Rule 2: GET без parameters → Resource
    RouteMap(
        methods=["GET"],
        pattern=r".*",
        route_type=RouteType.RESOURCE
    ),
    # Example: GET /v3/documents → r2r://documents

    # Rule 3: Все остальные методы → Tool
    RouteMap(
        methods=["POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"],
        pattern=r".*",
        route_type=RouteType.TOOL
    ),
    # Example: POST /v3/retrieval/search → search_chunks_v3_chunks_search_post
]
```

### Component Type Mapping

| HTTP Pattern | MCP Component | URI Schema | Example |
|--------------|---------------|------------|---------|
| `GET /api/{id}` | ResourceTemplate | `api://{id}` | `r2r://documents/{document_id}` |
| `GET /api/list` | Resource | `api://list` | `r2r://documents` |
| `POST /api/create` | Tool | Function call | `create_document_v3_documents_post()` |
| `DELETE /api/{id}` | Tool | Function call | `delete_document_by_id_v3_documents(id)` |

### Custom Route Mapping

```python
from fastmcp.openapi import RouteMap, RouteType

# Override defaults
custom_mappings = [
    # Exclude health endpoints
    RouteMap(
        methods=["GET"],
        pattern=r".*/health.*",
        route_type=RouteType.EXCLUDE
    ),

    # Force specific endpoint to be a Tool
    RouteMap(
        methods=["GET"],
        pattern=r".*/v3/analytics/.*",
        route_type=RouteType.TOOL
    ),

    # All other defaults apply after custom rules
    *DEFAULT_ROUTE_MAPPINGS
]

mcp = FastMCP.from_openapi(
    openapi_spec=spec,
    client=client,
    route_mappings=custom_mappings  # ← Custom rules
)
```

### Semantic Routing Logic

**Принцип:** HTTP semantics → MCP component type

- **GET** operations = **Read data** → Resources (data for LLM to read)
- **POST/PUT/DELETE** = **Write operations** → Tools (actions LLM can perform)
- **Path parameters** = **Template patterns** → ResourceTemplates (parameterized access)

**Example из R2R API:**

```python
# Project route mappings (src/server.py:121-145)
ROUTE_MAPPINGS = [
    # GET /v3/documents/{id} → r2r://documents/{id} (ResourceTemplate)
    RouteMap(
        methods=["GET"],
        pattern=r"/v3/.*\{.*\}.*",
        route_type=RouteType.RESOURCE_TEMPLATE,
    ),

    # GET /v3/documents → r2r://documents (Resource)
    RouteMap(
        methods=["GET"],
        pattern=r"/v3/.*",
        route_type=RouteType.RESOURCE,
    ),

    # POST /v3/retrieval/search → search_app_v3_retrieval_search_post (Tool)
    RouteMap(
        methods=["POST", "PUT", "PATCH", "DELETE"],
        pattern=r".*",
        route_type=RouteType.TOOL,
    ),
]
```

**Result:** Из 100+ R2R API endpoints автоматически создано:
- **60+ Tools** - POST/PUT/DELETE operations
- **25+ Resources** - GET list operations
- **15+ Resource Templates** - GET by ID operations

### Code References

**Implementation:** `src/server.py:121-145` - Route mapping config

**Auto-generated components:** `src/server.py:150-200` - FastMCP.from_openapi() call

---

## 🎯 Key Insights

### 1. Request-Time Authentication is Critical

**Problem:** Serverless окружения инжектят env vars поздно.

**Solution:** `DynamicBearerAuth` читает API ключ при выполнении запроса.

**Impact:** Позволяет деплой на FastMCP Cloud, AWS Lambda, Google Cloud Functions.

### 2. ctx.sample Enables LLM-Native Tools

**Capability:** Tools могут использовать LLM для analysis, generation, reasoning.

**Patterns:** 7 основных типов от basic prompting до multi-turn conversations.

**Impact:** Трансформация статических tools в интеллектуальные агенты.

### 3. Pipeline Composition Reduces Boilerplate

**Problem:** Multi-step workflows требуют много error handling и logging кода.

**Solution:** `Pipeline` и `ConditionalPipeline` инкапсулируют паттерны.

**Impact:** Код становится декларативным (`add_step → execute`).

### 4. OpenAPI Auto-Generation is Production-Ready

**Capability:** Автоматическая генерация из OpenAPI specs.

**Semantic Routing:** Умное маппинг HTTP → MCP components.

**Impact:** Создание MCP сервера из любого REST API за минуты, не часы.

### 5. Middleware Enables Cross-Cutting Concerns

**Pattern:** Hook-based interception (`on_request` → `on_call_tool` → handler).

**Use Cases:** Auth, logging, rate limiting, input validation, metrics.

**Impact:** Separation of concerns, reusable middleware components.

---

## 🚀 Practical Recommendations

### For Serverless Deployment

1. **ВСЕГДА используй DynamicBearerAuth** для API credentials
2. **Избегай module-level** чтения env vars (`API_KEY = os.getenv(...)`)
3. **Тестируй в облаке рано** - локальные тесты не покажут проблемы инициализации
4. **Используй experimental parser**:
   ```bash
   FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPENAPI_PARSER=true
   ```

### For LLM-Powered Tools

1. **System prompts** для role-based behavior:
   ```python
   system_prompt="You are an expert data analyst"
   ```
2. **Низкая temperature** (0.0-0.3) для structured output
3. **Retry logic обязателен** для production (exponential backoff)
4. **Multi-turn conversations** для complex tasks

### For Pipeline Design

1. **Prefer composition** over inheritance
2. **ConditionalPipeline** для conditional execution
3. **Caching** для expensive operations:
   ```python
   cache_key=f"search:{query}"
   ttl_seconds=600
   ```
4. **Fallback handlers** для resilience

### For OpenAPI Integration

1. **Custom route mappings** для exclude patterns:
   ```python
   RouteMap(pattern=r".*/health.*", route_type=RouteType.EXCLUDE)
   ```
2. **First match wins** - порядок RouteMap критичен
3. **Test semantic routing** перед production деплоем
4. **Monitor auto-generated** - проверь что маппинг корректный

---

## 📚 References

### Primary Sources (R2R Knowledge Base)

1. **Document `e9cf5e5c`** (09-layered-architecture.md)
   - DynamicBearerAuth implementation
   - Request-time vs import-time authentication
   - Serverless compatibility patterns

2. **Document `302419b0`** (FastMCP documentation)
   - ctx.sample methods and parameters
   - Middleware creation and hooks
   - Pipeline composition patterns

3. **Document `4fadedb8`** (OpenAPI integration)
   - RouteMap system
   - Semantic routing rules
   - Component type mapping

### Local Code

1. **src/server.py**
   - Lines 75-110: DynamicBearerAuth class
   - Lines 121-145: Route mapping config
   - Lines 328-964: Custom components

2. **src/r2r_typed.py**
   - Lines 30-168: TypedDict definitions
   - Lines 174-606: R2RTypedClient (type-safe wrapper)

3. **src/pipelines.py**
   - Lines 46-160: ctx.sample patterns
   - Lines 169-248: Pipeline base
   - Lines 413-480: ConditionalPipeline
   - Lines 487-589: Advanced patterns

---

[← Previous: Quick Start](./01-QUICKSTART.md) | [Next: Patterns Guide →](./03-PATTERNS.md)
