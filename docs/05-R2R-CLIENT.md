[← Back to Documentation Index](./README.md)

# R2R Client vs httpx: Comprehensive Analysis

**Should we use R2R Python SDK (R2RClient) instead of direct HTTP calls?**

---

## 📑 Содержание

1. [Введение](#-введение)
2. [Текущий подход (httpx)](#-текущий-подход-httpx)
3. [Альтернативный подход (R2RClient)](#-альтернативный-подход-r2rclient)
4. [Сравнительный анализ](#-сравнительный-анализ)
5. [Проблема DynamicBearerAuth](#-проблема-dynamicbearerauth)
6. [Гибридный подход](#-гибридный-подход)
7. [Рекомендации](#-рекомендации)
8. [Практические примеры](#-практические-примеры)

---

## 🎯 Введение

При интеграции FastMCP с R2R API возникает фундаментальный вопрос: использовать ли **прямые HTTP вызовы через httpx** или **официальный R2R Python SDK**?

### Контекст

**Текущий подход:** Direct HTTP calls с `httpx.AsyncClient` + `DynamicBearerAuth`

```python
_client = httpx.AsyncClient(
    base_url=os.getenv("R2R_BASE_URL"),
    auth=DynamicBearerAuth(),  # Request-time authentication
    timeout=30.0
)

# Usage
response = await _client.post(
    "/v3/retrieval/search",
    json={"query": "...", "limit": 10}
)
```

**Альтернативный подход:** R2R Python SDK

```python
from r2r import R2RClient

client = R2RClient(base_url="http://localhost:7272")

# Usage
results = await client.retrieval.search(query="...", limit=10)
```

---

## 🔧 Текущий подход (httpx)

### Архитектура

```python
# src/server.py (current implementation)
import httpx
from dotenv import load_dotenv

class DynamicBearerAuth(httpx.Auth):
    """Request-time authentication (CRITICAL для serverless)."""

    def auth_flow(self, request: httpx.Request):
        api_key = os.getenv("R2R_API_KEY", "")
        if api_key:
            request.headers["Authorization"] = f"Bearer {api_key}"
        yield request

# Global async client
_client = httpx.AsyncClient(
    base_url=os.getenv("R2R_BASE_URL", "http://localhost:7272"),
    auth=DynamicBearerAuth(),
    timeout=30.0
)

# Usage in tools
@mcp.tool()
async def search(query: str, limit: int = 10) -> dict:
    response = await _client.post(
        "/v3/retrieval/search",
        json={"query": query, "limit": limit}
    )
    return response.json()
```

### Преимущества httpx подхода

#### 1. **Полный контроль над HTTP запросами**

```python
# Можем точно контролировать каждый аспект запроса
response = await _client.post(
    "/v3/retrieval/search",
    json={
        "query": query,
        "limit": limit,
        "use_hybrid_search": True,
        "search_settings": {
            "hybrid_settings": {
                "full_text_weight": 1.0,
                "semantic_weight": 5.0
            }
        }
    },
    headers={"X-Custom-Header": "value"},
    timeout=60.0  # Custom timeout для этого запроса
)
```

#### 2. **DynamicBearerAuth для serverless**

```python
# КРИТИЧНО: API key читается при КАЖДОМ запросе
# НЕ при импорте модуля
class DynamicBearerAuth(httpx.Auth):
    def auth_flow(self, request: httpx.Request):
        # Читает R2R_API_KEY в момент выполнения запроса
        api_key = os.getenv("R2R_API_KEY", "")
        if api_key:
            request.headers["Authorization"] = f"Bearer {api_key}"
        yield request
```

**Почему это важно:**
- FastMCP Cloud инжектит env vars ПОСЛЕ импорта модулей
- Serverless окружения (AWS Lambda, Vercel) могут инжектить env vars динамически
- Request-time auth гарантирует работу в любом окружении

#### 3. **OpenAPI Auto-generation совместимость**

```python
# FastMCP.from_openapi() использует httpx внутренне
mcp = FastMCP.from_openapi(
    spec_url="http://localhost:7272/openapi.json",
    base_url="http://localhost:7272",
    auth=DynamicBearerAuth()  # ← Прямая интеграция с httpx.Auth
)
```

**Преимущество:** Единый подход для auto-generated и custom tools.

#### 4. **Минимальные зависимости**

```toml
# pyproject.toml
dependencies = [
    "fastmcp>=2.13.0",
    "httpx>=0.27.0",
    "python-dotenv>=1.0.0"
]
```

**3 зависимости** - минималистичный подход.

#### 5. **Прозрачность и отладка**

```python
# Видим точно что отправляется и что приходит
response = await _client.post("/v3/retrieval/search", json=payload)

print(f"Request: POST {_client.base_url}/v3/retrieval/search")
print(f"Payload: {json.dumps(payload, indent=2)}")
print(f"Response: {response.status_code} - {response.text}")
```

### Недостатки httpx подхода

#### 1. **Отсутствие type hints**

```python
# Нет автокомплита, нет type checking
response = await _client.post(
    "/v3/retrieval/search",
    json={"query": query}  # Какие поля доступны? Какие типы?
)

result = response.json()  # dict[str, Any] - нет structure
```

#### 2. **Ручная обработка ошибок**

```python
# Нужно вручную обрабатывать HTTP errors
try:
    response = await _client.post("/v3/retrieval/search", json=payload)
    response.raise_for_status()  # Вручную!
    return response.json()
except httpx.HTTPStatusError as e:
    # Ручная обработка 4xx/5xx
    raise Exception(f"R2R API error: {e.response.text}")
except httpx.RequestError as e:
    # Ручная обработка network errors
    raise Exception(f"Network error: {e}")
```

#### 3. **Поддержка API changes**

```python
# Если R2R API изменится, нужно вручную обновлять все вызовы
# Нет гарантии совместимости
response = await _client.post(
    "/v3/retrieval/search",  # Что если endpoint переименуется?
    json={"query": query}    # Что если параметры изменятся?
)
```

#### 4. **Дублирование логики**

```python
# Каждый tool должен повторять одну и ту же логику
@mcp.tool()
async def search(query: str) -> dict:
    try:
        response = await _client.post("/v3/retrieval/search", ...)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        # Повторяется в каждом tool
        raise

@mcp.tool()
async def rag(query: str) -> dict:
    try:
        response = await _client.post("/v3/retrieval/rag", ...)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        # Та же логика
        raise
```

---

## 📦 Альтернативный подход (R2RClient)

### Архитектура

```python
from r2r import R2RClient

# Initialize client
client = R2RClient(base_url="http://localhost:7272")

# Optional: login with credentials
# client.users.login("email@example.com", "password")

# Usage
results = await client.retrieval.search(query="machine learning", limit=10)
```

### Преимущества R2RClient

#### 1. **Structured API с type hints**

```python
# R2RClient предоставляет type-safe методы
from r2r import R2RClient

client = R2RClient(base_url="http://localhost:7272")

# Autocomplete и type checking работают!
results = client.retrieval.search(
    query="machine learning",  # str
    limit=10,                  # int
    use_hybrid_search=True     # bool
)
# results имеет известную структуру
```

**Преимущества:**
- ✅ IDE autocomplete
- ✅ Type checking (mypy, pyright)
- ✅ Меньше ошибок на этапе разработки

#### 2. **Высокоуровневые методы**

```python
# Documents
client.documents.create(file_path="doc.pdf")
client.documents.extract(document_id="uuid")

# Collections
collection = client.collections.create(
    name="research_papers",
    description="AI research collection"
)
client.collections.add_document(
    collection_id=collection["collection_id"],
    document_id="doc_uuid"
)

# Knowledge Graph
graph = client.collections.get_graph(collection_id="uuid")
results = client.collections.query_graph(
    collection_id="uuid",
    query="MATCH (p:Person)-[:WROTE]->(w:Work) RETURN p, w"
)

# RAG
answer = client.retrieval.rag(
    query="What is RAG?",
    max_tokens=4000
)

# Agent
response = client.retrieval.agent(
    message={"role": "user", "content": "Analyze this..."},
    mode="research"
)
```

#### 3. **Built-in error handling**

```python
# R2RClient обрабатывает HTTP errors внутренне
try:
    results = client.retrieval.search(query="...")
except R2RException as e:
    # Structured exception с деталями
    print(f"R2R error: {e.message}")
    print(f"Error type: {e.error_type}")
    print(f"Status code: {e.status_code}")
```

#### 4. **API версионирование**

```python
# R2R SDK отслеживает изменения API
# Обновление SDK гарантирует совместимость
pip install --upgrade r2r

# Ваш код продолжает работать после обновления API
results = client.retrieval.search(query="...")
```

#### 5. **Меньше boilerplate кода**

```python
# Было (httpx):
@mcp.tool()
async def search(query: str, limit: int = 10) -> dict:
    try:
        response = await _client.post(
            "/v3/retrieval/search",
            json={"query": query, "limit": limit}
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise Exception(f"R2R error: {e.response.text}")
    except httpx.RequestError as e:
        raise Exception(f"Network error: {e}")

# Стало (R2RClient):
@mcp.tool()
async def search(query: str, limit: int = 10) -> dict:
    return client.retrieval.search(query=query, limit=limit)
```

### Недостатки R2RClient

#### 1. **ПРОБЛЕМА: Отсутствие request-time authentication**

```python
# R2RClient инициализируется на module level
from r2r import R2RClient

# ❌ API key читается при ИМПОРТЕ модуля!
client = R2RClient(
    base_url=os.getenv("R2R_BASE_URL"),
    api_key=os.getenv("R2R_API_KEY")  # ← Читается СЕЙЧАС!
)

# Проблема: FastMCP Cloud инжектит env vars ПОСЛЕ импорта
# Результат: client.api_key = None (или старое значение)
```

**CRITICAL для serverless:** R2RClient НЕ поддерживает request-time auth из коробки.

#### 2. **Дополнительная зависимость**

```toml
# Было:
dependencies = ["fastmcp", "httpx", "python-dotenv"]

# Стало:
dependencies = ["fastmcp", "httpx", "python-dotenv", "r2r"]
```

**Проблема:** R2R SDK может тянуть свои зависимости (httpx, pydantic, etc.), увеличивая размер деплоя.

#### 3. **Меньше контроля над HTTP запросами**

```python
# httpx: полный контроль
response = await _client.post(
    "/v3/retrieval/search",
    json=payload,
    headers={"X-Custom-Header": "value"},
    timeout=60.0,
    follow_redirects=True
)

# R2RClient: ограниченные опции
results = client.retrieval.search(
    query="...",
    limit=10
    # Нельзя добавить custom headers
    # Нельзя изменить timeout для конкретного запроса
)
```

#### 4. **Sync vs Async API**

```python
# R2RClient может НЕ поддерживать async/await
# (Нужно проверить документацию)

# Если sync-only:
results = client.retrieval.search(query="...")  # Blocking call!

# В async context:
@mcp.tool()
async def search(query: str) -> dict:
    # ❌ Blocking call в async функции!
    results = client.retrieval.search(query=query)
    return results

# Нужен workaround:
import asyncio
from concurrent.futures import ThreadPoolExecutor

@mcp.tool()
async def search(query: str) -> dict:
    loop = asyncio.get_event_loop()
    results = await loop.run_in_executor(
        ThreadPoolExecutor(),
        lambda: client.retrieval.search(query=query)
    )
    return results
```

**Проблема:** Если R2RClient sync-only, нужны workarounds для async context.

#### 5. **Abstraction leak**

```python
# R2RClient скрывает детали HTTP запросов
# Сложнее отладить проблемы:
# - Какой именно endpoint вызывается?
# - Какой payload отправляется?
# - Какие headers добавляются?

# С httpx все прозрачно:
response = await _client.post(
    "/v3/retrieval/search",  # ← Видим endpoint
    json={"query": "..."}    # ← Видим payload
)
```

---

## 📊 Сравнительный анализ

### Матрица сравнения

| Критерий | httpx + DynamicBearerAuth | R2RClient | Победитель |
|----------|---------------------------|-----------|------------|
| **Request-time auth** | ✅ Поддерживается (DynamicBearerAuth) | ❌ Module-level только | **httpx** |
| **Serverless compatibility** | ✅ Полная | ❌ Проблемы с env vars | **httpx** |
| **Type hints / autocomplete** | ❌ dict[str, Any] | ✅ Structured types | **R2RClient** |
| **Error handling** | ❌ Ручная | ✅ Built-in | **R2RClient** |
| **API versioning** | ❌ Ручная синхронизация | ✅ SDK updates | **R2RClient** |
| **Boilerplate code** | ❌ Много | ✅ Минимум | **R2RClient** |
| **Контроль над HTTP** | ✅ Полный | ❌ Ограниченный | **httpx** |
| **Dependencies** | ✅ Минимальные (3) | ❌ Дополнительная | **httpx** |
| **Async/await support** | ✅ Native | ⚠️ Зависит от SDK | **httpx** |
| **Отладка** | ✅ Прозрачная | ❌ Abstraction leak | **httpx** |
| **OpenAPI auto-gen compatibility** | ✅ Прямая интеграция | ❌ Несовместимо | **httpx** |
| **Maintenance** | ❌ Ручная | ✅ SDK updates | **R2RClient** |

### Оценка по категориям

**Production-critical (serverless compatibility):**
- ✅ **httpx wins** - DynamicBearerAuth КРИТИЧЕН для FastMCP Cloud

**Developer Experience:**
- ✅ **R2RClient wins** - Type hints, autocomplete, less boilerplate

**Debugging & Control:**
- ✅ **httpx wins** - Прозрачность, полный контроль

**Maintenance:**
- ✅ **R2RClient wins** - SDK updates синхронизируют с API changes

**Integration with FastMCP:**
- ✅ **httpx wins** - OpenAPI auto-generation использует httpx

---

## ⚠️ Проблема DynamicBearerAuth

### Почему R2RClient не работает out-of-the-box?

```python
# R2RClient инициализация (типичный паттерн)
from r2r import R2RClient

client = R2RClient(
    base_url=os.getenv("R2R_BASE_URL"),
    api_key=os.getenv("R2R_API_KEY")  # ← Проблема!
)
```

**Что происходит:**

1. **Module import time:**
   ```python
   # Python импортирует модуль
   import src.server  # ← R2RClient() вызывается ЗДЕСЬ
   ```

2. **FastMCP Cloud инжектит env vars:**
   ```python
   # ПОСЛЕ импорта модулей
   os.environ["R2R_API_KEY"] = "actual_key_from_cloud"
   ```

3. **Результат:**
   ```python
   # client.api_key = None (или старое значение)
   # Все запросы fail с "Invalid token or API key"
   ```

### Решение: Wrapper для request-time auth

Можем создать wrapper вокруг R2RClient:

```python
class DynamicR2RClient:
    """R2RClient wrapper с request-time authentication."""

    def __init__(self):
        # НЕ инициализируем client в __init__!
        self._client: R2RClient | None = None

    def _get_client(self) -> R2RClient:
        """Get or create client with current env vars."""
        # Читаем env vars при КАЖДОМ вызове
        base_url = os.getenv("R2R_BASE_URL", "http://localhost:7272")
        api_key = os.getenv("R2R_API_KEY", "")

        # Создаем новый client с актуальными credentials
        return R2RClient(base_url=base_url, api_key=api_key)

    # Proxy все методы
    @property
    def retrieval(self):
        return self._get_client().retrieval

    @property
    def documents(self):
        return self._get_client().documents

    @property
    def collections(self):
        return self._get_client().collections

# Usage
client = DynamicR2RClient()

@mcp.tool()
async def search(query: str) -> dict:
    # Создает новый R2RClient с актуальным API key
    return client.retrieval.search(query=query)
```

**Проблема с этим подходом:**
- ❌ Создает новый client при каждом вызове (performance overhead)
- ❌ Теряет connection pooling (каждый client = новый httpx.Client)
- ❌ Сложный proxy pattern (нужно проксировать все методы)

---

## 🔀 Гибридный подход

### Вариант 1: httpx для FastMCP, R2RClient для standalone scripts

```python
# src/server.py - FastMCP MCP сервер
# Использует httpx + DynamicBearerAuth для serverless compatibility
import httpx

class DynamicBearerAuth(httpx.Auth):
    def auth_flow(self, request):
        api_key = os.getenv("R2R_API_KEY", "")
        if api_key:
            request.headers["Authorization"] = f"Bearer {api_key}"
        yield request

_client = httpx.AsyncClient(auth=DynamicBearerAuth())

@mcp.tool()
async def search(query: str) -> dict:
    response = await _client.post("/v3/retrieval/search", ...)
    return response.json()
```

```python
# scripts/batch_ingest.py - Standalone script для batch processing
# Использует R2RClient для удобства
from r2r import R2RClient

client = R2RClient(base_url="http://localhost:7272")

# Batch upload documents
for file_path in documents:
    client.documents.create(file_path=file_path)
```

**Преимущества:**
- ✅ FastMCP сервер работает в serverless (httpx)
- ✅ Scripts удобны для разработки (R2RClient)
- ✅ Правильный инструмент для правильной задачи

**Недостатки:**
- ❌ Две разные системы для одного API
- ❌ Нужно поддерживать оба подхода

---

### Вариант 2: R2RClient с DynamicAuth wrapper (только для non-serverless)

```python
# Используем R2RClient только если НЕ serverless
import os

USE_R2R_CLIENT = os.getenv("USE_R2R_CLIENT", "false").lower() == "true"

if USE_R2R_CLIENT:
    # Local development - используем R2RClient
    from r2r import R2RClient

    client = R2RClient(
        base_url=os.getenv("R2R_BASE_URL"),
        api_key=os.getenv("R2R_API_KEY")
    )

    @mcp.tool()
    async def search(query: str) -> dict:
        return client.retrieval.search(query=query)
else:
    # Production / serverless - используем httpx
    _client = httpx.AsyncClient(auth=DynamicBearerAuth())

    @mcp.tool()
    async def search(query: str) -> dict:
        response = await _client.post("/v3/retrieval/search", ...)
        return response.json()
```

**Преимущества:**
- ✅ Local dev удобен (R2RClient)
- ✅ Production работает (httpx)

**Недостатки:**
- ❌ Сложность (conditional imports)
- ❌ Два code paths для тестирования
- ❌ Потенциальные bugs из-за расхождений

---

### Вариант 3: Typed wrappers вокруг httpx (лучшее из обоих миров)

```python
# src/r2r_typed.py - Typed wrappers вокруг httpx
from typing import TypedDict, Literal
import httpx

class SearchRequest(TypedDict, total=False):
    query: str
    limit: int
    use_hybrid_search: bool
    search_strategy: Literal["vanilla", "hyde", "rag_fusion"]

class SearchResult(TypedDict):
    id: str
    text: str
    score: float
    metadata: dict

class R2RTypedClient:
    """Type-safe wrapper around httpx client."""

    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def search(
        self,
        query: str,
        limit: int = 10,
        use_hybrid_search: bool = True
    ) -> list[SearchResult]:
        """Type-safe search method."""
        response = await self._client.post(
            "/v3/retrieval/search",
            json={
                "query": query,
                "limit": limit,
                "use_hybrid_search": use_hybrid_search
            }
        )
        response.raise_for_status()
        data = response.json()

        # Type checking и validation
        return data.get("results", [])

    async def rag(
        self,
        query: str,
        max_tokens: int = 4000
    ) -> str:
        """Type-safe RAG method."""
        response = await self._client.post(
            "/v3/retrieval/rag",
            json={"query": query, "max_tokens": max_tokens}
        )
        response.raise_for_status()
        data = response.json()
        return data.get("answer", "")

# Usage
_http_client = httpx.AsyncClient(auth=DynamicBearerAuth())
r2r = R2RTypedClient(_http_client)

@mcp.tool()
async def search(query: str, limit: int = 10) -> list[SearchResult]:
    return await r2r.search(query=query, limit=limit)  # ← Type-safe!
```

**Преимущества:**
- ✅ Type hints (IDE autocomplete, mypy checking)
- ✅ DynamicBearerAuth (serverless compatibility)
- ✅ Полный контроль над HTTP (httpx)
- ✅ Прозрачность (видим что отправляется)
- ✅ Меньше boilerplate (typed wrappers)

**Недостатки:**
- ❌ Нужно поддерживать typed wrappers вручную
- ❌ При изменении R2R API нужно обновлять TypedDicts

---

## 💡 Рекомендации

### TL;DR

**Для FastMCP MCP серверов:**
- ✅ **Используйте httpx + DynamicBearerAuth** (текущий подход)
- ⚠️ **НЕ используйте R2RClient** без request-time auth wrapper

**Для standalone scripts:**
- ✅ **Используйте R2RClient** для удобства
- ✅ Batch processing, data migration, testing

**Гибридный подход:**
- ✅ **Typed wrappers** вокруг httpx (лучшее из обоих миров)

---

### Detailed Recommendations

#### 1. Для Production FastMCP Servers

**Оставайтесь на httpx + DynamicBearerAuth:**

```python
# src/server.py - Production-ready approach
import httpx
from dotenv import load_dotenv

class DynamicBearerAuth(httpx.Auth):
    """Request-time authentication (CRITICAL)."""
    def auth_flow(self, request: httpx.Request):
        api_key = os.getenv("R2R_API_KEY", "")
        if api_key:
            request.headers["Authorization"] = f"Bearer {api_key}"
        yield request

_client = httpx.AsyncClient(
    base_url=os.getenv("R2R_BASE_URL"),
    auth=DynamicBearerAuth(),
    timeout=30.0
)
```

**Причины:**
- ✅ Serverless compatibility (FastMCP Cloud, AWS Lambda, Vercel)
- ✅ OpenAPI auto-generation compatibility
- ✅ Минимальные зависимости
- ✅ Полный контроль и прозрачность

---

#### 2. Добавьте Typed Wrappers для Developer Experience

```python
# src/r2r_typed.py - Type-safe wrappers (NEW)
from typing import TypedDict, Literal
import httpx

class SearchParams(TypedDict, total=False):
    query: str
    limit: int
    use_hybrid_search: bool

class RAGParams(TypedDict, total=False):
    query: str
    max_tokens: int
    stream: bool

class R2RTypedClient:
    """Type-safe wrapper around httpx AsyncClient."""

    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def search(self, **params: SearchParams) -> dict:
        """Semantic search with type hints."""
        response = await self._client.post(
            "/v3/retrieval/search",
            json=params
        )
        response.raise_for_status()
        return response.json()

    async def rag(self, **params: RAGParams) -> dict:
        """RAG with type hints."""
        response = await self._client.post(
            "/v3/retrieval/rag",
            json=params
        )
        response.raise_for_status()
        return response.json()

# Usage
r2r = R2RTypedClient(_client)

@mcp.tool()
async def search(query: str, limit: int = 10) -> dict:
    return await r2r.search(query=query, limit=limit)  # ← Type-safe!
```

**Преимущества:**
- ✅ Type hints для IDE
- ✅ Сохраняет DynamicBearerAuth
- ✅ Минимальный overhead

---

#### 3. Используйте R2RClient для Standalone Scripts

```python
# scripts/batch_ingest.py - Batch processing script
from r2r import R2RClient
import os

client = R2RClient(
    base_url=os.getenv("R2R_BASE_URL"),
    api_key=os.getenv("R2R_API_KEY")
)

# Batch upload
documents = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
for doc in documents:
    print(f"Uploading {doc}...")
    result = client.documents.create(file_path=doc)
    print(f"✓ Uploaded: {result['document_id']}")
```

**Use cases:**
- Batch document ingestion
- Data migration scripts
- Testing utilities
- Admin tools

---

#### 4. НЕ смешивайте подходы в одном файле

```python
# ❌ ПЛОХО - два разных подхода в одном файле
from r2r import R2RClient
import httpx

r2r_client = R2RClient(...)
http_client = httpx.AsyncClient(...)

@mcp.tool()
async def search_v1(query: str):
    return r2r_client.retrieval.search(query=query)

@mcp.tool()
async def search_v2(query: str):
    response = await http_client.post("/v3/retrieval/search", ...)
    return response.json()
```

```python
# ✅ ХОРОШО - один подход, typed wrapper
_client = httpx.AsyncClient(auth=DynamicBearerAuth())
r2r = R2RTypedClient(_client)

@mcp.tool()
async def search(query: str):
    return await r2r.search(query=query)
```

---

## 🎯 Практические примеры

### Пример 1: Current Approach (httpx + DynamicBearerAuth)

```python
# src/server.py - Production approach
import os
import httpx
from fastmcp import FastMCP, Context

class DynamicBearerAuth(httpx.Auth):
    def auth_flow(self, request: httpx.Request):
        api_key = os.getenv("R2R_API_KEY", "")
        if api_key:
            request.headers["Authorization"] = f"Bearer {api_key}"
        yield request

_client = httpx.AsyncClient(
    base_url=os.getenv("R2R_BASE_URL"),
    auth=DynamicBearerAuth(),
    timeout=30.0
)

mcp = FastMCP("R2R MCP Server")

@mcp.tool()
async def search(
    query: str,
    limit: int = 10,
    ctx: Context | None = None
) -> dict:
    """Search R2R knowledge base."""
    if ctx:
        await ctx.info(f"Searching: {query}")
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
        await ctx.report_progress(100, 100, "Completed")

    return response.json()

if __name__ == "__main__":
    mcp.run()
```

**Status:** ✅ Production-ready, serverless compatible

---

### Пример 2: R2RClient Approach (NOT RECOMMENDED для serverless)

```python
# src/server_r2r_client.py - R2RClient approach (NOT RECOMMENDED)
import os
from r2r import R2RClient
from fastmcp import FastMCP, Context

# ❌ ПРОБЛЕМА: API key читается при импорте
client = R2RClient(
    base_url=os.getenv("R2R_BASE_URL"),
    api_key=os.getenv("R2R_API_KEY")  # ← Module-level init!
)

mcp = FastMCP("R2R MCP Server")

@mcp.tool()
async def search(
    query: str,
    limit: int = 10,
    ctx: Context | None = None
) -> dict:
    """Search R2R knowledge base."""
    if ctx:
        await ctx.info(f"Searching: {query}")

    # ⚠️ Может не работать если async не поддерживается
    results = client.retrieval.search(query=query, limit=limit)

    return results

if __name__ == "__main__":
    mcp.run()
```

**Status:** ❌ NOT serverless compatible, ⚠️ async support unclear

---

### Пример 3: Typed Wrapper (RECOMMENDED for best DX)

```python
# src/r2r_typed.py - Type-safe wrapper
from typing import TypedDict, Any
import httpx

class SearchParams(TypedDict, total=False):
    query: str
    limit: int
    use_hybrid_search: bool
    search_strategy: str

class R2RTypedClient:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def search(
        self,
        query: str,
        limit: int = 10,
        use_hybrid_search: bool = True
    ) -> dict[str, Any]:
        """Type-safe search method."""
        response = await self._client.post(
            "/v3/retrieval/search",
            json={
                "query": query,
                "limit": limit,
                "use_hybrid_search": use_hybrid_search
            }
        )
        response.raise_for_status()
        return response.json()

    async def rag(
        self,
        query: str,
        max_tokens: int = 4000
    ) -> dict[str, Any]:
        """Type-safe RAG method."""
        response = await self._client.post(
            "/v3/retrieval/rag",
            json={"query": query, "max_tokens": max_tokens}
        )
        response.raise_for_status()
        return response.json()

# src/server.py - Usage
from src.r2r_typed import R2RTypedClient

_http_client = httpx.AsyncClient(auth=DynamicBearerAuth())
r2r = R2RTypedClient(_http_client)

@mcp.tool()
async def search(
    query: str,
    limit: int = 10,
    ctx: Context | None = None
) -> dict:
    """Search with type hints."""
    if ctx:
        await ctx.info(f"Searching: {query}")
        await ctx.report_progress(0, 100, "Searching...")

    results = await r2r.search(query=query, limit=limit)  # ← Type-safe!

    if ctx:
        await ctx.report_progress(100, 100, "Completed")

    return results
```

**Status:** ✅ Best of both worlds (types + serverless)

---

## 🎓 Заключение

### Итоговая рекомендация

**Для FastMCP MCP серверов:**

1. ✅ **Оставайтесь на httpx + DynamicBearerAuth** для production
2. ✅ **Добавьте typed wrappers** для улучшения DX
3. ✅ **Используйте R2RClient** только для standalone scripts

**Почему:**
- **Serverless compatibility** - CRITICAL для FastMCP Cloud
- **OpenAPI auto-generation** - единый подход для всех tools
- **Control & debugging** - прозрачность HTTP запросов
- **Minimal dependencies** - меньше bloat

**Typed wrappers дают:**
- ✅ Type hints (IDE autocomplete)
- ✅ Меньше boilerplate
- ✅ Сохраняют все преимущества httpx

### Next Steps

1. ⚠️ **НЕ мигрируйте на R2RClient** без решения проблемы request-time auth
2. ✅ **Рассмотрите добавление typed wrappers** для улучшения DX
3. ✅ **Используйте R2RClient** для batch scripts и admin tools
4. ✅ **Документируйте** выбор подхода для команды

---

**Версия:** 1.0
**Последнее обновление:** 2025-11-27
**Статус:** Recommendation - KEEP httpx approach

---

[← Previous: Features Guide](./04-FEATURES.md) | [Next: Deployment Guide →](./06-DEPLOYMENT.md)
