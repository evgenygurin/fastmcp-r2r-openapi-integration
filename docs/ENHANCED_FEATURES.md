# Enhanced R2R MCP Server Features

This document describes the custom enhancements added to the R2R MCP server beyond the auto-generated OpenAPI components.

## 📊 Component Summary

### Auto-Generated (from OpenAPI)
- **81 API endpoints** from R2R OpenAPI specification
- **114 MCP routes** automatically mapped:
  - GET with path params → Resource Templates
  - GET without params → Resources  
  - POST/PUT/PATCH/DELETE → Tools

### Custom Enhancements
- **2 Static Resources** - Server introspection
- **3 Resource Templates** - Dynamic R2R data access
- **2 Prompts** - Reusable message templates
- **2 Enhanced Tools** - Context-aware operations

---

## 📁 Custom Resources

### `r2r://server/info`
**Type:** Static Resource  
**Description:** Server configuration and status information

**Returns:**
```json
{
  "server": {
    "name": "R2R MCP Server",
    "description": "R2R API - Document management, knowledge graphs, and AI",
    "version": "1.0.0"
  },
  "configuration": {
    "base_url": "https://api.example.com",
    "openapi_url": "https://api.example.com/openapi.json",
    "auth_configured": true,
    "debug_logging": false
  },
  "openapi": {
    "version": "3.1.0",
    "title": "FastAPI",
    "api_version": "0.1.0",
    "total_endpoints": 81
  },
  "parser": {
    "type": "experimental",
    "note": "Experimental parser provides better performance..."
  }
}
```

### `r2r://server/routes`
**Type:** Static Resource  
**Description:** Route mapping configuration details

**Returns:** Information about how OpenAPI endpoints are converted to MCP components, including:
- Mapping rules and priorities
- Examples for each MCP type (RESOURCE, RESOURCE_TEMPLATE, TOOL)
- Explanations of routing logic

---

## 📄 Resource Templates

Resource templates provide dynamic, parameterized access to R2R data without making explicit API calls.

### `r2r://documents/{document_id}`
**Type:** Resource Template  
**Annotations:** `readOnlyHint: true`, `idempotentHint: true`

**Description:** Fetch detailed document information from R2R API

**Parameters:**
- `document_id` (string) - R2R document UUID

**Example Usage:**
```
r2r://documents/9fbe403b-c682-4cf7-8d3e-91a3d27c8452
```

**Returns:**
```json
{
  "id": "...",
  "metadata": {...},
  "status": "...",
  "created_at": "...",
  ...
}
```

**Features:**
- ✅ Context logging for debugging
- ✅ Error handling with descriptive messages
- ✅ Read-only and idempotent (safe to cache)

### `r2r://collections/{collection_id}/summary`
**Type:** Resource Template  
**Annotations:** `readOnlyHint: true`, `idempotentHint: true`

**Description:** Get collection summary with document count

**Parameters:**
- `collection_id` (string) - R2R collection UUID

**Example Usage:**
```
r2r://collections/122fdf6a-e116-546b-a8f6-e4cb2e2c0a09/summary
```

**Returns:**
```json
{
  "collection_id": "...",
  "collection_info": {...},
  "document_count": 42,
  "fetched_at": "2025-11-25T12:00:00"
}
```

**Features:**
- ✅ Aggregates collection metadata and document count
- ✅ Context logging for visibility
- ✅ Timestamp for cache invalidation

### `r2r://search/results/{query}{?limit}`
**Type:** Resource Template (RFC 6570)  
**MIME Type:** `application/json`

**Description:** Search R2R knowledge base with optional result limit

**Parameters:**
- `query` (string, required) - Search query
- `limit` (integer, optional) - Max results (default: 10)

**Example Usage:**
```
r2r://search/results/machine learning
r2r://search/results/quantum computing?limit=20
```

**Returns:**
```json
{
  "query": "machine learning",
  "limit": 10,
  "results": {
    "results": {
      "chunk_search_results": [...]
    }
  },
  "searched_at": "2025-11-25T12:00:00"
}
```

**Features:**
- ✅ RFC 6570 query parameters (`{?limit}`)
- ✅ Optional context logging
- ✅ Flexible result limits

---

## 💬 Prompts

Prompts provide reusable message templates that LLMs can use for consistent interactions.

### `rag_query_prompt`
**Tags:** `r2r`, `rag`, `query`

**Description:** Generate well-structured RAG queries for R2R

**Parameters:**
- `question` (string, required) - The question to ask
- `context` (string, optional) - Additional context

**Example Usage:**
```python
# Via MCP client
prompt_result = await client.get_prompt("rag_query_prompt", {
    "question": "What is quantum computing?",
    "context": "Focus on applications in cryptography"
})
```

**Generated Prompt:**
```
Please answer the following question using the R2R knowledge base:

Question: What is quantum computing?

Additional Context: Focus on applications in cryptography

Please provide:
1. A clear, concise answer based on the retrieved documents
2. Citations to specific sources when possible
3. Confidence level in your answer (high/medium/low)
```

**Features:**
- ✅ Context injection for logging
- ✅ Optional context parameter for specialized queries
- ✅ Structured output format

### `document_analysis_prompt`
**Tags:** `r2r`, `analysis`, `documents`

**Description:** Generate prompts for analyzing R2R documents

**Parameters:**
- `document_id` (string, required) - R2R document UUID
- `analysis_type` (string, optional) - Type of analysis (default: "summary")
  - `summary` - Concise summary with key topics
  - `entities` - Extract named entities and concepts
  - `topics` - Identify main themes
  - `sentiment` - Analyze sentiment and tone

**Example Usage:**
```python
# Summary analysis
prompt = await client.get_prompt("document_analysis_prompt", {
    "document_id": "abc123",
    "analysis_type": "entities"
})
```

**Features:**
- ✅ Multiple analysis types
- ✅ Structured prompts for consistent results
- ✅ No context dependency (synchronous)

---

## 🔧 Enhanced Tools

Custom tools that leverage FastMCP Context for advanced capabilities.

### `enhanced_search`
**Tags:** `r2r`, `search`, `enhanced`

**Description:** Search R2R knowledge base with progress reporting

**Parameters:**
- `query` (string, required) - Search query
- `limit` (integer, optional) - Max results (default: 10)
- `search_type` (string, optional) - Search strategy: "hybrid", "semantic", "fulltext" (default: "hybrid")

**Example Usage:**
```python
result = await client.call_tool("enhanced_search", {
    "query": "machine learning",
    "limit": 20,
    "search_type": "hybrid"
})
```

**Returns:**
```json
{
  "query": "machine learning",
  "search_type": "hybrid",
  "result_count": 15,
  "results": {...},
  "timestamp": "2025-11-25T12:00:00"
}
```

**Features:**
- ✅ **Progress Reporting:** Real-time progress updates (0% → 30% → 80% → 100%)
- ✅ **Context Logging:** Info/debug messages visible in client
- ✅ **Error Handling:** Descriptive error messages with context
- ✅ **Flexible Search:** Supports hybrid, semantic, and fulltext modes

**Progress Events:**
```
0%   - Search initiated
30%  - Search payload prepared
80%  - API request complete
100% - Results processed
```

### `analyze_search_results`
**Tags:** `r2r`, `analysis`, `ai`

**Description:** Search R2R and analyze results using LLM sampling

**Parameters:**
- `query` (string, required) - Search query
- `limit` (integer, optional) - Max results (default: 5)

**Example Usage:**
```python
result = await client.call_tool("analyze_search_results", {
    "query": "quantum computing applications",
    "limit": 5
})
```

**Returns:**
```json
{
  "query": "quantum computing applications",
  "result_count": 5,
  "analysis": "Key themes: quantum algorithms, cryptography, simulation...",
  "timestamp": "2025-11-25T12:00:00"
}
```

**Features:**
- ✅ **LLM Sampling:** Uses `ctx.sample()` to analyze search results
- ✅ **Multi-Step Process:**
  1. Search R2R knowledge base
  2. Format results for LLM analysis
  3. Request LLM analysis via sampling
  4. Return structured analysis
- ✅ **Context Logging:** Tracks each step
- ✅ **AI-Powered Insights:** Identifies themes, patterns, follow-up questions

**LLM Sampling Configuration:**
```python
await ctx.sample(
    messages=analysis_prompt,
    system_prompt="You are an expert data analyst...",
    temperature=0.3,      # Low for consistency
    max_tokens=500        # Concise analysis
)
```

---

## 🎯 FastMCP Features Demonstrated

### 1. Context Integration
All custom components use `Context` for enhanced capabilities:

```python
async def my_resource(param: str, ctx: Context) -> dict:
    await ctx.info("Starting operation...")      # Visible to client
    await ctx.debug("Internal detail...")        # Debug-level logging
    await ctx.report_progress(50, 100)           # Progress bar
    result = await ctx.sample("Analyze this...")  # LLM sampling
    await ctx.error("Something failed")          # Error logging
    return result
```

**Benefits:**
- Real-time feedback to users
- Debug visibility without affecting output
- Progress tracking for long operations
- LLM capabilities within tools

### 2. RFC 6570 URI Templates
Resource templates support advanced URI patterns:

```python
# Simple parameter
"r2r://documents/{document_id}"

# Multiple parameters  
"r2r://collections/{collection_id}/summary"

# Query parameters (RFC 6570)
"r2r://search/results/{query}{?limit}"
```

**Query Parameters:**
- Defined with `{?param}` syntax
- Must have default values in function
- Automatically type-converted
- Example: `?limit=20` → `limit: int = 20`

### 3. Resource Annotations
Hint to clients about resource behavior:

```python
@mcp.resource(
    "r2r://documents/{id}",
    annotations={
        "readOnlyHint": True,      # No side effects
        "idempotentHint": True     # Multiple reads safe
    }
)
```

**Benefits:**
- Helps clients with caching decisions
- Improves UX with appropriate UI elements
- Reduces unnecessary re-fetches

### 4. LLM Sampling
Tools can request LLM analysis from the client:

```python
response = await ctx.sample(
    messages="Analyze this data...",
    system_prompt="You are an expert...",
    temperature=0.3,
    max_tokens=500
)
analysis = response.text
```

**Use Cases:**
- Analyze search results
- Generate summaries
- Extract insights
- Transform data

---

## 🚀 Usage Examples

### Claude Desktop Integration

Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "r2r": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/fastapi-r2r-openapi-integration",
        "run",
        "python",
        "-m",
        "src.server"
      ],
      "env": {
        "R2R_BASE_URL": "http://localhost:7272",
        "R2R_API_KEY": "your_api_key"
      }
    }
  }
}
```

### Example Interactions

**Using Resource Templates:**
```
User: Show me document abc123
Claude: [Reads r2r://documents/abc123]
        Here's the document information...
```

**Using Prompts:**
```
User: Help me query R2R about quantum computing
Claude: [Uses rag_query_prompt]
        "Please answer the following question using the R2R knowledge base:
         Question: What is quantum computing?..."
```

**Using Enhanced Search:**
```
User: Search for "machine learning" with progress
Claude: [Calls enhanced_search tool]
        🔍 Starting enhanced search...
        [Progress: ████░░░░░░ 30%]
        [Progress: ████████░░ 80%]
        ✓ Found 15 results
```

**Using LLM Analysis:**
```
User: Analyze search results for "quantum algorithms"
Claude: [Calls analyze_search_results]
        🧠 Analyzing search results...
        Requesting LLM analysis...
        ✓ Analysis complete
        
        Key themes: quantum algorithms, optimization, cryptography...
```

---

## 🛠️ Development

### Testing Custom Components

```bash
# Inspect server components
fastmcp inspect src/server.py

# Test with HTTP transport
make run-http

# Enable debug logging
echo "DEBUG_LOGGING=true" >> .env
make run
```

### Adding New Components

**Resource Template:**
```python
@mcp.resource(
    "r2r://your-template/{param}",
    description="Your description",
    annotations={"readOnlyHint": True}
)
async def your_resource(param: str, ctx: Context) -> dict:
    await ctx.info(f"Fetching {param}")
    # Your implementation
    return {"data": "..."}
```

**Prompt:**
```python
@mcp.prompt(
    name="your_prompt",
    description="Your prompt description",
    tags={"r2r", "custom"}
)
async def your_prompt(param: str, ctx: Context | None = None) -> str:
    if ctx:
        await ctx.info("Generating prompt...")
    return f"Your prompt template with {param}"
```

**Enhanced Tool:**
```python
@mcp.tool(
    description="Your tool description",
    tags={"r2r", "custom"}
)
async def your_tool(param: str, ctx: Context | None = None) -> dict:
    if ctx:
        await ctx.info("Starting operation...")
        await ctx.report_progress(0, 100)
    
    # Your implementation
    
    if ctx:
        await ctx.report_progress(100, 100)
    
    return {"result": "..."}
```

---

## 📚 References

- [FastMCP Documentation](https://gofastmcp.com)
- [R2R Documentation](https://r2r-docs.sciphi.ai)
- [MCP Specification](https://modelcontextprotocol.io)
- [RFC 6570 URI Templates](https://datatracker.ietf.org/doc/html/rfc6570)

---

## 🔍 Technical Details

### Context Capabilities Used

| Feature | Resource Templates | Prompts | Tools |
|---------|-------------------|---------|-------|
| Logging | ✅ | ✅ | ✅ |
| Progress | ❌ | ❌ | ✅ |
| Sampling | ❌ | ❌ | ✅ |
| Error Handling | ✅ | ✅ | ✅ |

### Error Handling Pattern

All custom components use consistent error handling:

```python
try:
    await ctx.info("Operation starting...")
    # ... operation ...
    await ctx.debug("Success")
    return result
except httpx.HTTPError as e:
    await ctx.error(f"API error: {e}")
    return {"error": str(e)}
except Exception as e:
    await ctx.error(f"Unexpected error: {e}")
    raise  # Re-raise for client error handling
```

### Performance Considerations

- **Resource Templates:** Executed on-demand (lazy evaluation)
- **Context Logging:** Only when context is provided (optional)
- **Progress Reporting:** Minimal overhead, updates at key milestones
- **LLM Sampling:** Only in `analyze_search_results` tool

---

## 🎓 Learning Resources

### FastMCP Patterns

1. **Resource Templates:** [docs](https://gofastmcp.com/servers/resources#resource-templates)
2. **Context API:** [docs](https://gofastmcp.com/servers/context)
3. **Prompts:** [docs](https://gofastmcp.com/servers/prompts)
4. **LLM Sampling:** [docs](https://gofastmcp.com/servers/sampling)

### R2R API Endpoints

Based on study via R2R MCP search:

**Core Categories:**
- `/v3/documents` - Document management
- `/v3/collections` - Collection organization
- `/v3/graphs` - Knowledge graph operations
- `/v3/retrieval/search` - Vector/hybrid search
- `/v3/retrieval/rag` - Retrieval-augmented generation
- `/v3/retrieval/agent` - Conversational agent
- `/v3/users` - User management
- `/v3/chunks` - Chunk operations

**Key Features:**
- Hybrid search (semantic + full-text)
- Knowledge graph integration
- RAG-Fusion for better retrieval
- Graph entity extraction
- Conversation management

---

## 📝 Changelog

### v1.1.0 - Enhanced Features
- Added 3 resource templates for direct R2R data access
- Added 2 prompts for RAG and document analysis
- Added 2 enhanced tools with Context integration
- Implemented LLM sampling in `analyze_search_results`
- Added RFC 6570 query parameter support
- Enhanced error handling with context logging

### v1.0.0 - Initial Release
- Auto-generated MCP server from R2R OpenAPI spec
- 114 routes mapped from 81 endpoints
- Dynamic Bearer authentication
- Experimental parser support
- Custom server info resources
