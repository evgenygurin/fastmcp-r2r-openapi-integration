# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🎯 Обзор проекта

**Гибридный репозиторий**, объединяющий документацию и производственный MCP сервер:

### Компоненты

1. **Документация** (docs/) - Унифицированное руководство (7 разделов):
   - **01-QUICKSTART.md** - Быстрый старт за 5 минут
   - **02-ARCHITECTURE.md** - Архитектура и core concepts
   - **03-PATTERNS.md** - ctx.sample и pipeline patterns
   - **04-FEATURES.md** - Custom MCP components
   - **05-R2R-CLIENT.md** - Type-safe R2R integration
   - **06-DEPLOYMENT.md** - Production deployment
   - **07-ROADMAP.md** - Development priorities

2. **MCP Сервер** (src/) - Production FastMCP implementation:
   - **server.py** - Auto-generated MCP components from R2R OpenAPI
   - **r2r_typed.py** - Type-safe wrapper around httpx for R2R API
   - **pipelines.py** - Advanced ctx.sample patterns and tool composition
   - Supports stdio (Claude Desktop) and HTTP (development) transports

3. **R2R Integration** (.claude/scripts/) - Bash CLI для R2R API:
   - Модульная архитектура (8 команд, 48 подкоманд)
   - Slash commands интеграция с Claude Code

### Архитектурные особенности

**OpenAPI → MCP Auto-generation:**
- Experimental parser (fastmcp.experimental.server.openapi) с fallback на legacy
- Semantic routing: GET с params → RESOURCE_TEMPLATE, GET без params → RESOURCE, POST/PUT/DELETE → TOOL
- DynamicBearerAuth для serverless compatibility (читает API_KEY при выполнении запроса)

## 📁 Структура проекта

```text
fastapi-r2r-openapi-integration/
├── src/                           # 🐍 Python MCP Server
│   ├── __init__.py
│   ├── server.py                  # Main entrypoint (970 строк)
│   │                              # - Auto-generation from OpenAPI
│   │                              # - DynamicBearerAuth (request-time API key)
│   │                              # - 3 resource templates, 2 prompts, 6 tools
│   ├── r2r_typed.py               # Type-safe R2R client (661 строка)
│   │                              # - TypedDicts for requests/responses
│   │                              # - 13 typed methods (search, rag, agent, etc.)
│   │                              # - Maintains DynamicBearerAuth compatibility
│   └── pipelines.py               # Advanced patterns (663 строки)
│                                  # - ctx.sample patterns (7 типов)
│                                  # - Pipeline composition (4 класса)
│                                  # - Caching, retry, fallback
├── docs/                          # 📚 Документация
│   ├── README.md                  # Навигационный hub
│   ├── 01-QUICKSTART.md           # Быстрый старт (5 минут)
│   ├── 02-ARCHITECTURE.md         # Core concepts & patterns
│   ├── 03-PATTERNS.md             # ctx.sample & pipelines
│   ├── 04-FEATURES.md             # Custom MCP components
│   ├── 05-R2R-CLIENT.md           # Type-safe integration
│   ├── 06-DEPLOYMENT.md           # Production deployment
│   ├── 07-ROADMAP.md              # Development priorities
│   └── REORGANIZATION_PLAN.md     # Reorganization plan
├── .claude/                       # ⚙️ Claude Code Integration
│   ├── scripts/                   # Модульная CLI для R2R API
│   │   ├── r2r                    # Main dispatcher
│   │   ├── lib/common.sh          # Shared config (43 lines)
│   │   ├── commands/              # 8 modules (48 subcommands)
│   │   │   ├── search.sh, rag.sh, agent.sh
│   │   │   ├── docs.sh, collections.sh, conversation.sh
│   │   │   ├── graph.sh, analytics.sh
│   │   ├── examples.sh, workflows.sh, quick.sh, aliases.sh
│   │   └── README.md
│   ├── commands/                  # 15 slash commands
│   │   ├── r2r*.md (9)            # R2R operations
│   │   └── cc*.md (6)             # Claude Code docs
│   ├── agents/ (3)                # Specialized agents
│   ├── hooks/SessionStart/        # check-r2r.md
│   └── config/.env                # R2R_BASE_URL, API_KEY
├── pyproject.toml                 # uv + ruff + mypy config
├── Makefile                       # Development commands
├── start.sh                       # Entrypoint с .env auto-load
├── openapi.json                   # R2R OpenAPI 3.1 spec
└── .env.example                   # Template configuration
```

## 🔧 Основные команды

### Python MCP Server Development

**Setup и установка:**
```bash
# Создание venv и установка зависимостей
uv venv
source .venv/bin/activate  # или .venv\Scripts\activate на Windows
uv pip install -e .

# Dev dependencies (ruff, mypy)
uv pip install -e ".[dev]"
# или
make dev
```

**Запуск сервера (предпочтительный способ - через start.sh):**
```bash
# stdio transport (для Claude Desktop)
./start.sh
# или
make run

# HTTP transport (для разработки/тестирования)
./start.sh http 0.0.0.0 8000
# или
make run-http

# Streamable HTTP (рекомендуется для production)
./start.sh streamable-http 0.0.0.0 8000
# или
make run-streamable
```

**ВАЖНО:** `start.sh` автоматически загружает переменные из `.env`:
```bash
# start.sh делает это автоматически:
set -a && source .env && set +a
uv run python -m src.server "$@"
```

**Качество кода:**
```bash
# Линтинг
uv run ruff check .
make lint

# Автоисправление + форматирование
uv run ruff check --fix .
uv run ruff format .
make fix

# Type checking
uv run mypy src/
```

**Обновление OpenAPI спецификации:**
```bash
# Скачать свежую спецификацию из R2R API
make update-spec
# или вручную:
curl -o openapi.json http://localhost:7272/openapi.json
# или с кастомным URL:
R2R_BASE_URL=<url> make update-spec
```

### R2R API Integration (через bash скрипты)

**Конфигурация:** `.claude/config/.env`
```bash
R2R_BASE_URL=<your-r2r-api-url>
API_KEY=<your-api-key>
```

**Модульный CLI (8 команд, 48 подкоманд):**

```bash
# Core commands
.claude/scripts/r2r search "query" --limit 5
.claude/scripts/r2r rag "question" --max-tokens 8000
.claude/scripts/r2r agent "query" --mode research --thinking

# Management commands
.claude/scripts/r2r docs list -l 10 -q
.claude/scripts/r2r collections create -n "Name" -d "Description"
.claude/scripts/r2r conversation list
.claude/scripts/r2r graph entities <collection_id> -l 50
.claude/scripts/r2r analytics system
```

**Slash команды Claude Code (15):**

```bash
# Core Operations
/r2r-search "query" [limit]
/r2r-rag "question" [max_tokens]
/r2r-agent "message" [mode]
/r2r-collections [action]
/r2r-upload <file> [collection_id]

# Helper Scripts
/r2r-quick <task> [args]      # ask, status, up, col, continue, etc.
/r2r-workflows <workflow>     # upload, create-collection, research, etc.
/r2r-examples [category]      # search, rag, agent, docs, etc.

# Claude Code Documentation
/cc                           # Quick reference
/cc-hooks                     # Hooks documentation
/cc-commands                  # Custom commands guide
/cc-mcp                       # MCP integration
/cc-subagents                 # Subagents guide
/cc-setup                     # Installation guide
```

**Helper Scripts:**

```bash
# Quick Tasks (.claude/scripts/quick.sh)
./quick.sh ask "query"        # Search + RAG answer
./quick.sh status             # System status
./quick.sh up file.pdf        # Quick upload

# Workflows (.claude/scripts/workflows.sh)
./workflows.sh upload paper.pdf
./workflows.sh create-collection "Name" "Desc" *.pdf
./workflows.sh research "query"

# Aliases (.claude/scripts/aliases.sh - source в .bashrc/.zshrc)
source .claude/scripts/aliases.sh
rs "query"   # r2r search
rr "q"       # r2r rag
ra "msg"     # r2r agent
```

### Работа с документацией

```bash
# Поиск по содержимому (ВСЕГДА используй rg вместо grep)
rg "search term" docs/
rg "DynamicBearerAuth" docs/
rg "ctx.sample" docs/

# Поиск файлов (ВСЕГДА используй fd вместо find)
fd -e md . docs/
fd "README" docs/

# Статистика
fd -e md . docs | wc -l           # Количество файлов (9)
du -sh docs/                       # Общий размер (~200KB)
```

## 🏗️ Архитектура

### MCP Server Architecture (src/)

**Ключевая проблема:** FastMCP Cloud и serverless окружения инжектят env vars ПОСЛЕ импорта модулей.

**Решение - DynamicBearerAuth (server.py:75-110):**
```python
class DynamicBearerAuth(httpx.Auth):
    def auth_flow(self, request: httpx.Request):
        # Читает R2R_API_KEY при КАЖДОМ запросе
        # НЕ при импорте модуля!
        api_key = os.getenv("R2R_API_KEY", "")
        if api_key:
            request.headers["Authorization"] = f"Bearer {api_key}"
        yield request
```

**OpenAPI Auto-generation Pattern:**
1. Fetch spec from `R2R_OPENAPI_URL` (default: `$R2R_BASE_URL/openapi.json`)
2. Validate structure (`openapi` field, `info`, `paths`)
3. Apply route mappings (3 правила в порядке приоритета):
   - `GET /v3/.*\{.*\}.*` → RESOURCE_TEMPLATE (например `/v3/documents/{id}`)
   - `GET /v3/.*` → RESOURCE (например `/v3/documents`)
   - `POST|PUT|PATCH|DELETE .*` → TOOL
4. Auto-generate FastMCP components: `mcp = FastMCP.from_openapi(...)`

**Custom Components (добавлены вручную поверх auto-generated):**
- 3 Resource Templates: `r2r://documents/{id}`, `r2r://collections/{id}/summary`, `r2r://search/results/{query}{?limit}`
- 2 Prompts: `rag_query_prompt`, `document_analysis_prompt`
- 6 Tools: `enhanced_search`, `analyze_search_results`, `research_pipeline`, `comparative_analysis`, `extract_structured_data`, `generate_followup_questions`

**Pipelines Architecture (pipelines.py):**

7 ctx.sample patterns:
1. `sample_basic_generation` - простая генерация
2. `sample_with_system_prompt` - с role-based промптами
3. `sample_structured_output` - JSON/markdown output
4. `sample_multi_turn_conversation` - multi-turn диалоги
5. `sample_with_retry` - retry logic с exponential backoff
6. `pipeline_llm_analyze` - AI анализ результатов
7. `pipeline_llm_summarize` - executive summary

4 Pipeline classes:
1. `Pipeline` - базовая композиция (add_step → execute)
2. `ConditionalPipeline` - условное выполнение шагов
3. `pipeline_with_fallback` - primary/fallback pattern
4. `cached_pipeline_step` - кэширование с TTL

Паттерн использования:
```python
pipeline = Pipeline(ctx)
results = await (
    pipeline
    .add_step("search", pipeline_search_and_analyze, query="AI")
    .add_step("analyze", pipeline_llm_analyze)
    .add_step("summarize", pipeline_llm_summarize)
    .execute()
)
```

**R2R Typed Client Architecture (r2r_typed.py):**

Type-safe wrapper around httpx для улучшения developer experience при сохранении DynamicBearerAuth.

**Преимущества над raw httpx:**
- ✅ Type hints и IDE autocomplete
- ✅ TypedDicts для requests/responses
- ✅ Меньше boilerplate кода
- ✅ Сохраняет DynamicBearerAuth (serverless compatible)

**Преимущества над R2R Python SDK:**
- ✅ Request-time authentication (работает в serverless)
- ✅ Полный контроль над HTTP запросами
- ✅ OpenAPI auto-generation compatibility
- ✅ Минимальные зависимости

Компоненты:
- **13 TypedDicts** для requests: `SearchRequest`, `RAGRequest`, `AgentRequest`, etc.
- **13 TypedDicts** для responses: `SearchResponse`, `RAGResponse`, `AgentResponse`, etc.
- **13 typed методов**: `search()`, `rag()`, `agent()`, `create_document()`, `get_document()`, `list_documents()`, `delete_document()`, `create_collection()`, `list_collections()`, `get_collection()`, `get_collection_documents()`, `health()`, `request()`
- **2 helper функции**: `format_search_results()`, `extract_citations()`

Паттерн использования:
```python
from src.r2r_typed import R2RTypedClient

# Инициализация с DynamicBearerAuth
_client = httpx.AsyncClient(auth=DynamicBearerAuth(), base_url=R2R_BASE_URL)
r2r = R2RTypedClient(_client)

# Type-safe вызовы с autocomplete
results = await r2r.search(query="machine learning", limit=10)
answer = await r2r.rag(query="What is RAG?", max_tokens=4000)
response = await r2r.agent(message="Analyze this", mode="research")
```

**Важно:** `response.json()` возвращает `Any`, поэтому используем `# type: ignore[no-any-return]` вместо `cast()` - честный подход без runtime overhead.

### Документация - три независимых раздела

Каждая технология имеет:
- **README.md** - навигационный hub со структурой разделов
- **NN-section-name.md** - пронумерованные разделы (01-08 или 01-13)
- **Единый стиль** - эмодзи в H2, практические примеры, русский текст + английские термины

### R2R Integration Architecture

```text
┌─────────────────┐
│  Claude Code    │  Slash Commands (15)
│  (Frontend)     │  /r2r-* (9) + /cc-* (6)
└────────┬────────┘
         │
┌────────▼────────┐
│ Modular CLI     │  r2r dispatcher → commands/*.sh
│  (Middleware)   │  + helpers: examples, workflows, quick, aliases
└────────┬────────┘
         │ curl + jq → JSON
┌────────▼────────┐
│      R2R        │  $R2R_BASE_URL
│   (Backend)     │  8 команд, 48 подкоманд
└─────────────────┘
```

**Важно:**
- Ранее использовался FastMCP bridge (MCP сервер), но удален в пользу прямых bash скриптов
- Монолитные r2r_client.sh и r2r_advanced.sh заменены модульной структурой commands/
- **Используется jq для формирования JSON** - избегает проблем с экранированием и валидностью

### R2R API Defaults

Конфигурация в `lib/common.sh`:
```bash
DEFAULT_LIMIT=3                    # Результатов поиска
DEFAULT_MAX_TOKENS=4000            # Токенов для генерации
DEFAULT_MODE="research"            # Agent mode (research/rag)
DEFAULT_SEARCH_STRATEGY="vanilla"  # ⚠️ ТОЛЬКО vanilla работает
```

**⚠️ Известная проблема:** Search strategies `hyde` и `rag_fusion` не работают из-за ошибки конфигурации VertexAI на R2R сервере. См. `.claude/SEARCH_STRATEGIES.md` для деталей.

## 🚫 Запрещенные действия

### Для документации (docs/)
1. **НЕ меняй** язык документации на английский без явного запроса
2. **НЕ удаляй** эмодзи из заголовков - это часть стиля документации
3. **НЕ создавай** .cursorrules, AGENTS.md и подобные файлы - используй только CLAUDE.md

### Для Python кода (src/)
1. **НЕ импортируй API_KEY на module level** - используй только DynamicBearerAuth паттерн
   ```python
   # ❌ НЕПРАВИЛЬНО - импорт на module level
   API_KEY = os.getenv("R2R_API_KEY")

   # ✅ ПРАВИЛЬНО - request-time чтение
   class DynamicBearerAuth(httpx.Auth):
       def auth_flow(self, request):
           api_key = os.getenv("R2R_API_KEY", "")
           ...
   ```

2. **НЕ добавляй type annotations для Context** если используется `| None`:
   ```python
   # ✅ ПРАВИЛЬНО
   async def tool(ctx: Context | None = None) -> dict:

   # ❌ НЕПРАВИЛЬНО
   async def tool(ctx: Optional[Context] = None) -> dict:
   ```

3. **НЕ изменяй route mapping порядок** - first match wins:
   ```python
   # Порядок КРИТИЧЕН:
   # 1. GET с {params} → RESOURCE_TEMPLATE
   # 2. GET без params → RESOURCE
   # 3. POST/PUT/DELETE → TOOL
   ```

4. **НЕ используй** синхронные HTTP calls - только async (httpx.AsyncClient)

### Общие
5. **НЕ используй** grep, find, cat - используй rg, fd, bat (современные альтернативы)
6. **НЕ добавляй** dependencies без обоснования - проект минималистичный (3 deps: fastmcp, httpx, python-dotenv)

## ✅ Обязательные практики

### При работе с Python кодом (src/)

1. **ВСЕГДА используй async/await** для I/O операций:
   ```python
   # ✅ ПРАВИЛЬНО
   async def fetch_data(ctx: Context | None = None):
       response = await _client.get("/endpoint")

   # ❌ НЕПРАВИЛЬНО
   def fetch_data():
       response = requests.get("/endpoint")
   ```

2. **ВСЕГДА используй Context для logging и progress**:
   ```python
   async def tool(ctx: Context | None = None):
       if ctx:
           await ctx.info("Starting operation...")
           await ctx.report_progress(0, 100)
           # ... операция
           await ctx.report_progress(100, 100)
   ```

3. **ВСЕГДА обрабатывай отсутствие Context**:
   ```python
   # ✅ ПРАВИЛЬНО
   if ctx:
       await ctx.info("Message")

   # ❌ НЕПРАВИЛЬНО - может упасть если ctx is None
   await ctx.info("Message")
   ```

4. **Type hints обязательны** для всех публичных функций:
   ```python
   async def process_data(
       data: dict[str, Any],
       ctx: Context | None = None
   ) -> dict[str, Any]:
       ...
   ```

5. **Следуй Ruff rules** (E, W, F, I, B, C4, SIM, UP, RUF):
   - Line length: 88 symbols
   - Trailing commas: обязательны
   - Import sorting: автоматически через ruff
   - Python 3.10+ синтаксис (используй `|` для Union)

6. **Error handling с контекстом**:
   ```python
   try:
       result = await operation()
   except Exception as e:
       if ctx:
           await ctx.error(f"Operation failed: {e}")
       raise  # или return fallback
   ```

### При работе с документацией (docs/)

1. **ВСЕГДА используй Read tool перед редактированием** существующих файлов
2. **Сохраняй структуру** - не меняй порядок разделов без необходимости
3. **Проверяй внутренние ссылки** - относительные пути должны работать
4. **Обновляй table of contents** в README.md при изменении заголовков
5. **Следуй нумерации** - 01-NN-section-name.md для последовательности
6. **Используй эмодзи в H2** - 🎯, 📁, 🔍, ⚙️, 📚, 🔗, ⚠️, ✅, ❌

### При работе с R2R API (bash scripts)

1. **Загружай .env** перед curl запросами:
   ```bash
   bash -c 'source .claude/config/.env && curl ...'
   ```
2. **Используй vanilla стратегию** - hyde и rag_fusion не работают
3. **Hybrid search включен по умолчанию** во всех скриптах
4. **Research mode** предпочтительнее RAG mode для сложных запросов
5. **Используй jq для JSON** - избегает проблем с экранированием:
   ```bash
   # ✅ ПРАВИЛЬНО
   PAYLOAD=$(jq -n --arg q "$query" '{query: $q}')

   # ❌ НЕПРАВИЛЬНО
   PAYLOAD="{\"query\": \"$query\"}"
   ```

### Git workflow

```bash
# Коммиты ВСЕГДА одной строкой, БЕЗ подписей Co-Authored-By
git commit -m "docs(r2r): add hybrid search examples"
git commit -m "fix(scripts): correct API endpoint URL"
git commit -m "feat(commands): add /r2r-upload slash command"
```

**Типы:** `docs`, `fix`, `feat`, `refactor`, `chore`

## 📋 R2R Quick Reference

### API Endpoints (v3)

```sql
POST /v3/retrieval/search          # Hybrid search (semantic + fulltext)
POST /v3/retrieval/rag             # RAG with generation
POST /v3/retrieval/agent           # Multi-turn agent

POST /v3/documents                 # Create document
GET  /v3/documents                 # List documents
DELETE /v3/documents/{id}          # Delete document

POST /v3/collections               # Create collection
GET  /v3/collections               # List collections
POST /v3/collections/{id}/documents  # Add document to collection

POST /v3/graphs/{id}/pull          # Sync knowledge graph
POST /v3/graphs/{id}/entities      # Create entity
```

### Search Settings

```json
{
  "use_hybrid_search": true,         // ✅ Работает с vanilla
  "search_strategy": "vanilla",      // ⚠️ hyde, rag_fusion - НЕ работают
  "limit": 3,
  "filters": {
    "collection_ids": {"$overlap": ["collection_id"]}
  }
}
```

### RAG Generation Config

```json
{
  "max_tokens": 4000,
  "model": "openai/gpt-4.1",
  "temperature": 0.1,
  "stream": false
}
```

### Agent Modes

| Mode | Tools | Use Case |
|------|-------|----------|
| **research** | rag, reasoning, critique, python_executor | Сложный анализ, multi-step reasoning |
| **rag** | search_file_knowledge, get_file_content, web_search | Простые factual queries |

## 🔍 Типичные задачи

### Поиск информации в документации

```bash
# Найти примеры использования конкретного API
rg "client.documents.create" docs/

# Найти все Python примеры
rg "```python" docs/

# Найти разделы про аутентификацию
fd -e md authentication docs/
```

### Добавление нового раздела документации

1. Определи следующий номер: `ls docs/*.md | grep -E '^[0-9]{2}-' | sort`
2. Создай файл: `docs/08-NEW-SECTION.md` (следующий номер)
3. Добавь навигацию:
   - В начало: `[← Back to Documentation Index](./README.md)`
   - В конец: Previous/Next ссылки
4. Обнови `docs/README.md` - добавь в table of contents
5. Коммит: `git commit -m "docs: add section 08 - new topic"`

### Обновление существующего раздела

1. Читай перед редактированием: `Read` tool на файл
2. Сохраняй структуру заголовков
3. Проверь внутренние ссылки после изменений
4. Обнови README.md если меняешь заголовки

### Тестирование R2R интеграции

```bash
# Проверка доступности API (модульный CLI)
.claude/scripts/r2r search "test" 1

# Проверка JSON output
.claude/scripts/r2r search --json "test" 1 | jq .

# Проверка slash команды
/r2r-search "R2R documentation"

# Проверка agent mode
/r2r-agent "What is R2R?"
```

## 🐛 Troubleshooting

### R2R API Issues

**Проблема:** RAG запрос возвращает `null`

**Решение:**
1. Проверь `.claude/SEARCH_STRATEGIES.md`
2. Убедись что `DEFAULT_SEARCH_STRATEGY="vanilla"`
3. Проверь `.claude/config/.env` на наличие `API_KEY`

**Проблема:** "API_KEY not set in .env file"

**Решение:**
```bash
# Создай .claude/config/.env
cat > .claude/config/.env << 'EOF'
R2R_BASE_URL=<your-r2r-api-url>
API_KEY=<your-api-key>
EOF
```

### Документация Issues

**Проблема:** Внутренние ссылки не работают

**Решение:** Используй относительные пути от текущей директории:
```markdown
[Quick Start](./01-QUICKSTART.md)    # ✅ Правильно
[Quick Start](/docs/01-QUICKSTART)   # ❌ Не работает в GitHub
```

**Проблема:** Inconsistent нумерация файлов

**Решение:**
```bash
# Проверь последовательность
ls docs/*.md | grep -E '^docs/[0-9]{2}-' | sort
# Должно быть: 01, 02, 03, ..., 07 без пропусков
```

## 📚 Ссылки на важные файлы

### Python MCP Server
- `src/server.py:75-110` - DynamicBearerAuth (КРИТИЧНО для serverless)
- `src/server.py:121-145` - Route mapping rules (порядок важен!)
- `src/server.py:170` - R2RTypedClient инициализация
- `src/server.py:214-248` - Custom resources (`r2r://server/info`, `r2r://server/routes`)
- `src/server.py:328-432` - Resource templates (3 шт)
- `src/server.py:439-519` - Prompts (2 шт)
- `src/server.py:526-663` - Enhanced tools (2 базовых)
- `src/server.py:670-964` - Pipeline tools (4 advanced)
- `src/r2r_typed.py:30-110` - TypedDicts для requests (SearchRequest, RAGRequest, AgentRequest, etc.)
- `src/r2r_typed.py:115-168` - TypedDicts для responses (SearchResponse, RAGResponse, AgentResponse, etc.)
- `src/r2r_typed.py:174-199` - R2RTypedClient class definition
- `src/r2r_typed.py:204-368` - Retrieval methods (search, rag, agent)
- `src/r2r_typed.py:373-478` - Document methods (create, get, list, delete)
- `src/r2r_typed.py:483-550` - Collection methods (create, list, get, get_documents)
- `src/r2r_typed.py:555-606` - Utility & low-level methods (health, request)
- `src/r2r_typed.py:613-661` - Helper functions (format_search_results, extract_citations)
- `src/pipelines.py:30-38` - extract_text() helper для response.text
- `src/pipelines.py:46-160` - ctx.sample patterns (7 типов)
- `src/pipelines.py:167-248` - Pipeline base class
- `src/pipelines.py:256-373` - LLM-powered pipeline steps
- `pyproject.toml:25-35` - Ruff configuration
- `Makefile` - Development commands
- `start.sh` - Entrypoint с auto .env loading

### Конфигурация
- `.env.example` - Template (ВАЖНО: `FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPENAPI_PARSER=true`)
- `.claude/config/.env` - API credentials для bash scripts
- `openapi.json` - R2R OpenAPI 3.1 spec

### Bash R2R Integration
- `.claude/scripts/r2r` - main CLI dispatcher
- `.claude/scripts/lib/common.sh:24-27` - Default settings (LIMIT=3, MAX_TOKENS=4000, MODE=research, STRATEGY=vanilla)
- `.claude/scripts/commands/` - 8 modular commands (48 subcommands)
- `.claude/scripts/` - Helper scripts (examples, workflows, quick, aliases)
- `.claude/docs/SEARCH_STRATEGIES.md` - Troubleshooting для hyde/rag_fusion

### Claude Code Integration
- `.claude/commands/` - 15 slash commands (9 R2R + 6 Claude Code docs)
- `.claude/agents/` - 3 specialized agents
- `.claude/hooks/SessionStart/` - API health check

### Документация
- `docs/README.md` - Навигационный hub
- `docs/01-QUICKSTART.md` - Быстрый старт (5 минут)
- `docs/02-ARCHITECTURE.md` - DynamicBearerAuth, ctx.sample, pipelines, OpenAPI
- `docs/03-PATTERNS.md` - Advanced patterns (ctx.sample, pipelines)
- `docs/04-FEATURES.md` - Custom MCP components
- `docs/05-R2R-CLIENT.md` - Type-safe R2R integration (httpx vs SDK)
- `docs/06-DEPLOYMENT.md` - FastMCP Cloud, Docker
- `docs/07-ROADMAP.md` - Development priorities
- `docs/REORGANIZATION_PLAN.md` - Documentation reorganization plan

## 🎯 Ключевые принципы

### Для Python кода (src/)
1. **DynamicBearerAuth is CRITICAL** - читай API_KEY при каждом запросе, НЕ при импорте
2. **Async everywhere** - все I/O операции async/await (httpx.AsyncClient)
3. **Use R2RTypedClient** - предпочитай `r2r.search()` вместо `_client.post("/v3/retrieval/search")` для type safety
4. **Context optional** - всегда `ctx: Context | None = None` и проверяй `if ctx:`
5. **Type hints обязательны** - все публичные функции должны иметь type annotations
6. **Ruff compliance** - line length 88, trailing commas, Python 3.10+ syntax (`|` вместо `Union`)
7. **Honest type ignores** - используй `# type: ignore[no-any-return]` вместо `cast()` для `response.json()`
8. **Minimal dependencies** - только fastmcp, httpx, python-dotenv

### Для документации (docs/)
9. **Русский + English** - текст на русском, код/термины/API на английском
10. **Эмодзи в заголовках** - часть стиля, не удаляй
11. **Консистентность** - следуй существующему стилю во всех файлах
12. **Нумерация файлов** - 01-NN-section-name.md для последовательности

### Для R2R Integration (bash scripts)
13. **Vanilla strategy only** - hyde и rag_fusion не работают (см. .claude/docs/SEARCH_STRATEGIES.md)
14. **jq for JSON** - избегает проблем с экранированием и валидностью
15. **Research mode** - предпочтительнее RAG mode для сложных запросов
16. **Hybrid search** - включен по умолчанию (use_hybrid_search: true)

### Общие
17. **Современные инструменты** - rg вместо grep, fd вместо find, bat вместо cat
18. **Одна строка коммитов** - без подписей Co-Authored-By, краткие описания
19. **Read before Edit** - всегда читай файл перед редактированием

## 🔬 Типичные сценарии разработки

### Добавление нового MCP Tool

1. Определи нужен ли Context (`ctx: Context | None = None`)
2. Добавь в `src/server.py` или `src/pipelines.py`
3. Используй декоратор `@mcp.tool()`:
   ```python
   @mcp.tool(
       description="Tool description",
       tags={"category", "type"}
   )
   async def my_tool(
       param: str,
       ctx: Context | None = None
   ) -> dict[str, Any]:
       if ctx:
           await ctx.info("Starting tool...")

       try:
           result = await some_operation(param)
           return {"result": result}
       except Exception as e:
           if ctx:
               await ctx.error(f"Failed: {e}")
           raise
   ```
4. Запусти `make lint` и `make fix`
5. Тестируй через `./start.sh`

### Добавление нового Pipeline Pattern

1. Добавь в `src/pipelines.py`
2. Следуй существующим паттернам (7 ctx.sample типов, 4 pipeline классов)
3. Используй `Pipeline` или `ConditionalPipeline` базовый класс
4. Документируй с примерами использования:
   ```python
   async def my_pipeline_step(
       ctx: Context | None = None,
       previous_results: dict | None = None
   ) -> dict:
       """Pipeline step description.

       Example:
           pipeline = Pipeline(ctx)
           result = await (
               pipeline
               .add_step("step1", my_pipeline_step)
               .execute()
           )
       """
   ```

### Обновление OpenAPI spec и тестирование

```bash
# 1. Скачай новую спецификацию
make update-spec

# 2. Проверь что сервер инициализируется
./start.sh

# 3. Проверь логи на ошибки парсинга:
# - "✓ Loaded OpenAPI spec: ..."
# - "✓ Successfully initialized MCP server..."
# - "Processed N API endpoints..."

# 4. Если experimental parser fails, fallback на legacy автоматический
```

### Debugging FastMCP Cloud Issues

**Проблема:** Tool/Resource не работает в FastMCP Cloud, но работает локально.

**Решение:**
1. Проверь что используется `DynamicBearerAuth` (НЕ module-level API_KEY)
2. Проверь логи: `DEBUG_LOGGING=true` в env vars
3. Убедись что `R2R_API_KEY` и `R2R_BASE_URL` установлены в FastMCP Cloud env vars
4. Проверь что experimental parser включен: `FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPENAPI_PARSER=true`
