[← Back to Documentation Index](./README.md)

# Quick Start Guide

**5-минутный старт** с FastMCP + R2R integration. Этот гайд поможет запустить MCP сервер и подключить его к Claude Desktop.

---

## 🚀 5-Minute Setup

### Prerequisites

- **Python 3.10+**
- **Claude Desktop** (latest version)
- **R2R API** credentials (base URL + API key)
- **uv** package manager (рекомендуется) или pip

### Quick Installation

```bash
# 1. Clone repository
git clone <repository-url>
cd fastapi-r2r-openapi-integration

# 2. Create virtual environment (рекомендуется uv)
uv venv
source .venv/bin/activate  # или .venv\Scripts\activate на Windows

# 3. Install dependencies
uv pip install -e .

# 4. Configure environment
cp .env.example .env
# Отредактируй .env - добавь R2R_BASE_URL и R2R_API_KEY

# 5. Test server
./start.sh
# Должен вывести: "✓ Successfully initialized MCP server..."
```

### Quick Configuration

**Claude Desktop Config** (`~/Library/Application Support/Claude/claude_desktop_config.json` на macOS):

```json
{
  "mcpServers": {
    "r2r": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/fastapi-r2r-openapi-integration",
        "run",
        "python",
        "-m",
        "src.server"
      ],
      "env": {
        "R2R_BASE_URL": "https://your-r2r-api.com",
        "R2R_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

**ВАЖНО**: Используй **абсолютные пути** в `--directory`.

### Quick Verification

1. Перезапусти Claude Desktop
2. Проверь наличие MCP сервера в интерфейсе
3. Попробуй простой запрос:
   ```bash
   Search R2R knowledge base for "machine learning"
   ```

**Если работает** - сервер настроен корректно!

---

## 📦 Detailed Installation

### Step 1: Python Environment Setup

#### Option A: Using uv (Recommended)

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Activate
source .venv/bin/activate  # Linux/macOS
# или
.venv\Scripts\activate     # Windows

# Install project
uv pip install -e .

# Install dev dependencies (optional)
uv pip install -e ".[dev]"
```

#### Option B: Using pip

```bash
# Create virtual environment
python -m venv .venv

# Activate
source .venv/bin/activate  # Linux/macOS
# или
.venv\Scripts\activate     # Windows

# Install project
pip install -e .

# Install dev dependencies (optional)
pip install -e ".[dev]"
```

### Step 2: Environment Configuration

Create `.env` file in project root:

```bash
# R2R API Configuration
R2R_BASE_URL=https://api.your-r2r-instance.com
R2R_API_KEY=your_api_key_here

# Optional: Custom OpenAPI spec URL
R2R_OPENAPI_URL=https://api.your-r2r-instance.com/openapi.json

# Optional: Request timeout in seconds (default: 30.0)
R2R_TIMEOUT=30.0

# Optional: Enable debug logging (default: false)
DEBUG_LOGGING=false

# IMPORTANT: Enable experimental OpenAPI parser (recommended)
FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPENAPI_PARSER=true
```

**Где взять credentials**:
- `R2R_BASE_URL` - URL вашего R2R API server
- `R2R_API_KEY` - API key из R2R admin panel

### Step 3: Test Server Locally

```bash
# Run server in stdio mode (default for Claude Desktop)
./start.sh

# Expected output:
# ✓ Loaded OpenAPI spec: N endpoints
# ✓ Successfully initialized MCP server with X tools, Y resources, Z prompts
```

**Alternative: HTTP mode** (для тестирования вне Claude Desktop):

```bash
# HTTP transport
./start.sh http 0.0.0.0 8000

# Streamable HTTP (recommended for production)
./start.sh streamable-http 0.0.0.0 8000
```

### Step 4: Claude Desktop Integration

#### Locate Config File

**macOS**:
```text
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows**:
```text
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux**:
```text
~/.config/Claude/claude_desktop_config.json
```

#### Add MCP Server Configuration

```json
{
  "mcpServers": {
    "r2r": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/yourname/path/to/fastapi-r2r-openapi-integration",
        "run",
        "python",
        "-m",
        "src.server"
      ],
      "env": {
        "R2R_BASE_URL": "https://api.your-r2r-instance.com",
        "R2R_API_KEY": "your_api_key_here",
        "FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPENAPI_PARSER": "true"
      }
    }
  }
}
```

**Critical Notes**:
- Use **absolute paths** for `--directory`
- Environment variables в `env` block override `.env` file
- `FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPENAPI_PARSER` - recommended for better performance

#### Alternative: Using pip instead of uv

```json
{
  "mcpServers": {
    "r2r": {
      "command": "/absolute/path/to/.venv/bin/python",
      "args": [
        "-m",
        "src.server"
      ],
      "env": {
        "R2R_BASE_URL": "https://api.your-r2r-instance.com",
        "R2R_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Step 5: Verify Integration

1. **Restart Claude Desktop** полностью (quit и reopen)

2. **Check MCP Connection**:
   - Открой Claude Desktop
   - Проверь наличие MCP indicator в интерфейсе
   - Должен показать "r2r" сервер с зеленым статусом

3. **Test Basic Functionality**:

```bash
User: Search the R2R knowledge base for documents about "API integration"

Expected Response:
Claude should use the enhanced_search tool and return search results
```

4. **Test Advanced Features**:

```bash
User: Analyze the top 5 search results for "machine learning" and summarize key insights

Expected Response:
Claude should use analyze_search_results tool and provide structured analysis
```

---

## 🎯 Core Concepts Overview

### DynamicBearerAuth Pattern

**Problem**: FastMCP Cloud и serverless окружения инжектят environment variables ПОСЛЕ импорта модулей.

**Solution**: Request-time authentication

```python
class DynamicBearerAuth(httpx.Auth):
    def auth_flow(self, request: httpx.Request):
        # Читает API key при КАЖДОМ запросе, НЕ при импорте!
        api_key = os.getenv("R2R_API_KEY", "")
        if api_key:
            request.headers["Authorization"] = f"Bearer {api_key}"
        yield request
```

**Почему это важно**:
- ✅ Работает в serverless (AWS Lambda, FastMCP Cloud)
- ✅ Позволяет менять credentials без перезапуска
- ✅ Совместимо с OpenAPI auto-generation

### OpenAPI Auto-Generation

**Semantic Routing** - автоматическое определение типа MCP component:

```python
# GET с {params} → RESOURCE_TEMPLATE
GET /v3/documents/{id}           # → r2r://documents/{id}

# GET без params → RESOURCE
GET /v3/documents                # → r2r://documents

# POST/PUT/DELETE → TOOL
POST /v3/retrieval/search        # → search_chunks_v3_chunks_search_post
```

**Преимущества**:
- Автоматическая генерация из OpenAPI spec
- Поддержка 100+ endpoints без ручного кода
- Обновление через `make update-spec`

### ctx.sample Patterns

**LLM-powered операции** через FastMCP Context:

```python
# Basic generation
response = await ctx.sample("Explain quantum computing")

# With system prompt
response = await ctx.sample(
    messages="Analyze this data",
    system_prompt="You are an expert data analyst",
    temperature=0.3
)

# Structured output
response = await ctx.sample(
    messages=f"Return JSON: {data}",
    temperature=0.2
)
```

**7 паттернов** доступны - см. [Patterns Guide](./03-PATTERNS.md).

### Pipeline Composition

**Multi-step workflows** с передачей результатов:

```python
pipeline = Pipeline(ctx)
results = await (
    pipeline
    .add_step("search", search_func, query="AI")
    .add_step("analyze", analyze_func)
    .add_step("summarize", summarize_func)
    .execute()
)
```

**Подробнее** в [Patterns Guide](./03-PATTERNS.md#pattern-2-pipeline-composition).

---

## 🔧 First Steps

### Example 1: Basic Search

```bash
User: Search for "FastMCP patterns" in the knowledge base

Claude will:
1. Use enhanced_search tool
2. Query R2R API with hybrid search
3. Return top results with metadata
```

### Example 2: RAG Query

```text
User: What is DynamicBearerAuth and why is it important?

Claude will:
1. Use rag_app_v3_retrieval_rag_post tool
2. Search relevant documentation
3. Generate answer with citations
```

### Example 3: Advanced Analysis

```bash
User: Compare search strategies in R2R: vanilla vs hyde vs rag_fusion

Claude will:
1. Use comparative_analysis tool
2. Perform multiple searches
3. LLM-powered comparison
4. Structured summary
```

### Example 4: Document Upload

```text
User: Upload this PDF to R2R knowledge base

Claude will:
1. Use create_document_v3_documents_post tool
2. Upload file with metadata
3. Trigger ingestion pipeline
4. Return document ID
```

---

## 🐛 Troubleshooting

### Issue: Server не запускается

**Symptom**: `./start.sh` fails with import errors

**Solution**:
```bash
# Reinstall dependencies
uv pip install -e .

# Check Python version
python --version  # Should be 3.10+

# Check environment
cat .env  # Verify R2R_BASE_URL and R2R_API_KEY are set
```

### Issue: Claude Desktop не видит MCP server

**Symptom**: No "r2r" server in MCP list

**Solutions**:
1. **Проверь абсолютные пути** в `claude_desktop_config.json`
2. **Перезапусти Claude Desktop** полностью (quit + reopen)
3. **Проверь логи**: Claude Desktop → Help → Show Logs
4. **Тест вручную**:
   ```bash
   cd /path/to/project
   ./start.sh
   # Должно работать без ошибок
   ```

### Issue: Tools не работают

**Symptom**: Claude says "I cannot use that tool"

**Solutions**:
1. **Проверь API credentials** в `.env` или `claude_desktop_config.json`
2. **Тест R2R API вручную**:
   ```bash
   curl -H "Authorization: Bearer $R2R_API_KEY" \
        "$R2R_BASE_URL/v3/system/settings"
   # Should return 200 OK
   ```
3. **Проверь OpenAPI spec**:
   ```bash
   make update-spec
   ./start.sh
   # Check output for "Successfully initialized"
   ```

### Issue: Slow performance

**Symptom**: Tools take too long to respond

**Solutions**:
1. **Enable experimental parser**:
   ```bash
   FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPENAPI_PARSER=true
   ```
2. **Adjust timeout**:
   ```bash
   R2R_TIMEOUT=60.0  # Increase if needed
   ```
3. **Check R2R server health**:
   ```bash
   curl "$R2R_BASE_URL/v3/system/health"
   ```

### Issue: "500 Internal Server Error" from R2R

**Symptom**: Tools return HTTP 500 errors

**Common Causes**:
1. **VertexAI/LiteLLM configuration** на R2R server
2. **Invalid API key**
3. **R2R server downtime**

**Solutions**:
1. Check R2R server logs
2. Verify API key is valid and not expired
3. Try different search strategy (use `vanilla` instead of `hyde`)
4. Contact R2R server administrator

---

## 📚 Next Steps

### For New Users
✅ **You're ready!** Try interacting with Claude Desktop using MCP tools.

**Recommended Next**:
- [Architecture Guide](./02-ARCHITECTURE.md) - понять core concepts
- [Features Guide](./04-FEATURES.md) - изучить custom components

### For Developers
**Learn Advanced Patterns**:
- [Patterns Guide](./03-PATTERNS.md) - ctx.sample и pipelines
- [R2R Client Guide](./05-R2R-CLIENT.md) - type-safe integration

### For Production Deployment
**Deploy to Cloud**:
- [Deployment Guide](./06-DEPLOYMENT.md) - FastMCP Cloud, Docker, monitoring

---

## 🔗 Useful Resources

### Documentation
- [R2R API Documentation](https://r2r-docs.sciphi.ai/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [MCP Specification](https://modelcontextprotocol.io/)

### Project Files
- [CLAUDE.md](../CLAUDE.md) - Claude Code instructions
- [pyproject.toml](../pyproject.toml) - Dependencies
- [Makefile](../Makefile) - Development commands

### Quick Commands
```bash
make dev        # Install dev dependencies
make lint       # Run ruff linting
make fix        # Auto-fix issues
make run        # Run server (stdio)
make run-http   # Run server (HTTP)
```

---

[Next: Architecture Guide →](./02-ARCHITECTURE.md)
