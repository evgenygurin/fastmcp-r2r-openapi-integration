# R2R MCP Server Development Roadmap

**Based on R2R RAG analysis (max_tokens=4000, 20-25 sources per query)**

This roadmap outlines the development path to make our FastMCP R2R server production-ready, based on extensive analysis via R2R RAG queries of R2R and FastMCP documentation.

---

## 📊 Current State

### Auto-Generated (from OpenAPI)
- ✅ 114 MCP routes from 81 R2R API endpoints
- ✅ Route mapping: GET → Resources/Templates, POST/PUT/DELETE → Tools
- ✅ Dynamic Bearer authentication for serverless compatibility
- ✅ Experimental parser support with fallback

### Custom Components
- ✅ 2 Static Resources (server/info, server/routes)
- ✅ 3 Resource Templates (documents, collections, search with RFC 6570)
- ✅ 2 Prompts (rag_query, document_analysis)
- ✅ 2 Enhanced Tools (enhanced_search, analyze_search_results)

### FastMCP Features Used
- ✅ Context integration (logging, progress, sampling)
- ✅ LLM sampling in tools
- ✅ Resource annotations
- ✅ Error handling with context

---

## 🎯 Priority 1: Knowledge Graph & GraphRAG

### Why Important
Knowledge graphs enhance search accuracy and context understanding by identifying entities, relationships, and communities in documents.

### Features to Add

#### 1.1 Entity & Relationship Tools

**Resource Templates:**
```python
@mcp.resource(
    "r2r://documents/{document_id}/entities",
    description="View extracted entities from a document"
)
async def get_document_entities(document_id: str, ctx: Context) -> dict:
    """Fetch entities extracted from a specific document."""
    await ctx.info(f"Fetching entities for document {document_id}")
    
    response = await _client.get(
        f"{_r2r_base_url}/v3/documents/{document_id}/entities"
    )
    entities = response.json()
    
    await ctx.info(f"Found {len(entities.get('results', []))} entities")
    return {
        "document_id": document_id,
        "entities": entities,
        "count": len(entities.get("results", []))
    }

@mcp.resource(
    "r2r://documents/{document_id}/relationships",
    description="View extracted relationships from a document"
)
async def get_document_relationships(document_id: str, ctx: Context) -> dict:
    """Fetch relationships extracted from a specific document."""
    # Similar implementation
```

**Tool - Extract Knowledge Graph:**
```python
@mcp.tool(
    description="Extract entities and relationships from a document",
    tags={"r2r", "knowledge-graph", "extraction"}
)
async def extract_knowledge_graph(
    document_id: str,
    entity_types: list[str] | None = None,
    relation_types: list[str] | None = None,
    ctx: Context | None = None
) -> dict:
    """
    Extract knowledge graph from a document.
    
    Args:
        document_id: R2R document UUID
        entity_types: Types of entities to extract (e.g., ["Person", "Organization"])
        relation_types: Types of relationships (e.g., ["WORKS_FOR", "LOCATED_IN"])
    """
    if ctx:
        await ctx.info(f"Starting knowledge graph extraction for {document_id}")
        await ctx.report_progress(0, 100)
    
    payload = {"document_id": document_id}
    if entity_types:
        payload["entity_types"] = entity_types
    if relation_types:
        payload["relation_types"] = relation_types
    
    if ctx:
        await ctx.report_progress(30, 100)
    
    response = await _client.post(
        f"{_r2r_base_url}/v3/documents/{document_id}/extract",
        json=payload
    )
    
    if ctx:
        await ctx.report_progress(100, 100)
        await ctx.info("✓ Knowledge graph extraction complete")
    
    return response.json()
```

#### 1.2 Graph Search Tool

```python
@mcp.tool(
    description="Search knowledge graph for entities and relationships",
    tags={"r2r", "graph", "search"}
)
async def graph_search(
    query: str,
    entity_types: list[str] | None = None,
    limit: int = 10,
    ctx: Context | None = None
) -> dict:
    """
    Search the knowledge graph for entities and their relationships.
    
    Example:
        graph_search("technologies used by OpenAI", entity_types=["Technology"])
    """
    if ctx:
        await ctx.info(f"Searching graph: {query}")
    
    response = await _client.post(
        f"{_r2r_base_url}/v3/retrieval/search",
        json={
            "query": query,
            "search_settings": {
                "graph_settings": {
                    "enabled": True
                },
                "limit": limit
            }
        }
    )
    
    results = response.json()
    graph_results = results.get("graph_search_results", [])
    
    if ctx:
        await ctx.info(f"Found {len(graph_results)} graph results")
    
    return {
        "query": query,
        "graph_results": graph_results,
        "count": len(graph_results)
    }
```

#### 1.3 Community Detection

**Tool - Build Communities:**
```python
@mcp.tool(
    description="Build communities in knowledge graph using Leiden algorithm",
    tags={"r2r", "graph", "communities"}
)
async def build_graph_communities(
    collection_id: str,
    max_iterations: int = 10,
    ctx: Context | None = None
) -> dict:
    """
    Detect and build communities in the knowledge graph.
    
    Communities are densely connected groups of entities.
    """
    if ctx:
        await ctx.info(f"Building communities for collection {collection_id}")
        await ctx.report_progress(0, 100)
    
    response = await _client.post(
        f"{_r2r_base_url}/v3/graphs/{collection_id}/communities/build",
        json={"max_iterations": max_iterations}
    )
    
    if ctx:
        await ctx.report_progress(100, 100)
        await ctx.info("✓ Community detection complete")
    
    return response.json()

@mcp.resource(
    "r2r://graphs/{collection_id}/communities",
    description="View communities in a knowledge graph"
)
async def get_graph_communities(collection_id: str, ctx: Context) -> dict:
    """List communities detected in a collection's knowledge graph."""
    response = await _client.get(
        f"{_r2r_base_url}/v3/graphs/{collection_id}/communities"
    )
    return response.json()
```

#### 1.4 Graph-Enhanced RAG

**Tool - GraphRAG Query:**
```python
@mcp.tool(
    description="RAG query with knowledge graph integration",
    tags={"r2r", "rag", "graph"}
)
async def graphrag_query(
    query: str,
    collection_ids: list[str] | None = None,
    use_communities: bool = True,
    ctx: Context | None = None
) -> dict:
    """
    Perform RAG query enhanced with knowledge graph context.
    
    Combines vector search with graph search for richer context.
    """
    if ctx:
        await ctx.info(f"GraphRAG query: {query}")
        await ctx.report_progress(0, 100)
    
    search_settings = {
        "use_hybrid_search": True,
        "graph_settings": {
            "enabled": True,
            "kg_search_type": "local"  # or "global" for community-based
        },
        "limit": 20
    }
    
    if collection_ids:
        search_settings["filters"] = {
            "collection_ids": {"$overlap": collection_ids}
        }
    
    if ctx:
        await ctx.report_progress(30, 100)
    
    response = await _client.post(
        f"{_r2r_base_url}/v3/retrieval/rag",
        json={
            "query": query,
            "search_settings": search_settings,
            "rag_generation_config": {
                "model": "openai/gpt-4o-mini",
                "temperature": 0.7,
                "max_tokens": 1500
            }
        }
    )
    
    if ctx:
        await ctx.report_progress(100, 100)
    
    result = response.json()
    
    if ctx:
        chunk_count = len(result.get("chunk_search_results", []))
        graph_count = len(result.get("graph_search_results", []))
        await ctx.info(f"✓ Retrieved {chunk_count} chunks + {graph_count} graph results")
    
    return result
```

**Implementation Priority:** HIGH  
**Estimated Effort:** 2-3 days  
**Dependencies:** R2R with graph extraction enabled

---

## 🤖 Priority 2: Agent & Agentic RAG

### Why Important
Agents enable multi-step reasoning, tool use, and conversational interactions, making the system more intelligent and autonomous.

### Features to Add

#### 2.1 Conversational Agent

**Tool - Agent Query:**
```python
@mcp.tool(
    description="Engage with R2R conversational agent",
    tags={"r2r", "agent", "conversation"}
)
async def agent_query(
    message: str,
    conversation_id: str | None = None,
    mode: str = "rag",  # "rag" or "research"
    use_tools: list[str] | None = None,
    ctx: Context | None = None
) -> dict:
    """
    Interact with R2R agent for complex queries.
    
    Modes:
        - "rag": Standard RAG with retrieval
        - "research": Deep analysis with reasoning tools
    
    Tools (for research mode):
        - "search_file_knowledge": Search documents
        - "web_search": Search web
        - "reasoning": Deep reasoning
        - "critique": Critical analysis
    """
    if ctx:
        await ctx.info(f"Agent query ({mode} mode): {message[:50]}...")
    
    payload = {
        "message": {
            "role": "user",
            "content": message
        },
        "mode": mode,
        "search_mode": "advanced"
    }
    
    if conversation_id:
        payload["conversation_id"] = conversation_id
    
    if use_tools:
        if mode == "rag":
            payload["rag_tools"] = use_tools
        else:
            payload["research_tools"] = use_tools
    
    response = await _client.post(
        f"{_r2r_base_url}/v3/retrieval/agent",
        json=payload
    )
    
    result = response.json()
    
    if ctx:
        await ctx.info(f"✓ Agent response: {len(result.get('messages', []))} messages")
    
    return result
```

#### 2.2 Research Mode with Extended Thinking

**Tool - Research Query:**
```python
@mcp.tool(
    description="Deep research query with multi-step reasoning",
    tags={"r2r", "research", "reasoning"}
)
async def research_query(
    query: str,
    thinking_budget: int = 2048,
    enable_critique: bool = True,
    ctx: Context | None = None
) -> dict:
    """
    Perform deep research with extended thinking and critique.
    
    Extended thinking shows step-by-step reasoning process.
    """
    if ctx:
        await ctx.info(f"Research query: {query}")
        await ctx.info(f"Thinking budget: {thinking_budget} tokens")
    
    payload = {
        "message": {
            "role": "user",
            "content": query
        },
        "mode": "research",
        "research_generation_config": {
            "extended_thinking": True,
            "thinking_budget": thinking_budget,
            "max_tokens": 2000,
            "temperature": 0.4
        },
        "research_tools": ["rag", "reasoning"]
    }
    
    if enable_critique:
        payload["research_tools"].append("critique")
    
    response = await _client.post(
        f"{_r2r_base_url}/v3/retrieval/agent",
        json=payload
    )
    
    result = response.json()
    
    if ctx:
        # Extract thinking/reasoning from response
        messages = result.get("messages", [])
        reasoning_steps = [m for m in messages if m.get("type") == "thinking"]
        await ctx.info(f"✓ Research complete: {len(reasoning_steps)} reasoning steps")
    
    return result
```

#### 2.3 Conversation Management

**Resource Templates:**
```python
@mcp.resource(
    "r2r://conversations/{conversation_id}",
    description="Get conversation details and history"
)
async def get_conversation(conversation_id: str, ctx: Context) -> dict:
    """Retrieve conversation history and metadata."""
    response = await _client.get(
        f"{_r2r_base_url}/v3/conversations/{conversation_id}"
    )
    return response.json()

@mcp.resource(
    "r2r://conversations/{conversation_id}/messages",
    description="Get all messages in a conversation"
)
async def get_conversation_messages(conversation_id: str, ctx: Context) -> dict:
    """Retrieve all messages from a conversation."""
    response = await _client.get(
        f"{_r2r_base_url}/v3/conversations/{conversation_id}/messages"
    )
    return response.json()
```

**Tool - Create Conversation:**
```python
@mcp.tool(
    description="Create a new conversation",
    tags={"r2r", "conversation"}
)
async def create_conversation(
    name: str | None = None,
    ctx: Context | None = None
) -> dict:
    """Create a new conversation for multi-turn interactions."""
    payload = {}
    if name:
        payload["name"] = name
    
    response = await _client.post(
        f"{_r2r_base_url}/v3/conversations",
        json=payload
    )
    
    result = response.json()
    
    if ctx:
        conv_id = result.get("id")
        await ctx.info(f"✓ Created conversation: {conv_id}")
    
    return result
```

**Implementation Priority:** MEDIUM-HIGH  
**Estimated Effort:** 3-4 days  
**Dependencies:** R2R agent endpoints enabled

---

## ⚡ Priority 3: Production Best Practices

### Why Important
Production systems need robust error handling, performance optimization, monitoring, and testing.

### Features to Add

#### 3.1 Error Handling Middleware

**Implementation:**
```python
from fastmcp.server.middleware.error_handling import (
    ErrorHandlingMiddleware,
    RetryMiddleware
)

# Add after FastMCP initialization
mcp.add_middleware(ErrorHandlingMiddleware(
    include_traceback=True,  # For debugging
    transform_error=lambda e: {
        "error": str(e),
        "type": type(e).__name__,
        "timestamp": datetime.utcnow().isoformat()
    },
    on_error=lambda e: logger.error(f"MCP Error: {e}")
))

# Add retry for transient failures
mcp.add_middleware(RetryMiddleware(
    max_retries=3,
    retry_errors=(httpx.ConnectError, httpx.TimeoutError),
    backoff_factor=1.5
))
```

#### 3.2 Caching Layer

**Implementation:**
```python
from functools import lru_cache
from datetime import datetime, timedelta

# In-memory cache with TTL
_cache = {}
_cache_ttl = {}

def cached_resource(ttl_seconds: int = 300):
    """Decorator for caching resource responses."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Create cache key
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            
            # Check cache
            if cache_key in _cache:
                if datetime.now() < _cache_ttl[cache_key]:
                    logger.debug(f"Cache hit: {cache_key}")
                    return _cache[cache_key]
                else:
                    # Expired
                    del _cache[cache_key]
                    del _cache_ttl[cache_key]
            
            # Fetch and cache
            result = await func(*args, **kwargs)
            _cache[cache_key] = result
            _cache_ttl[cache_key] = datetime.now() + timedelta(seconds=ttl_seconds)
            
            return result
        
        return wrapper
    return decorator

# Use in resources
@mcp.resource("r2r://server/info")
@cached_resource(ttl_seconds=60)  # Cache for 1 minute
async def get_server_info(ctx: Context | None = None) -> dict:
    # Implementation...
```

#### 3.3 Rate Limiting

**Implementation:**
```python
from fastmcp.server.middleware.rate_limiting import RateLimitMiddleware

# Add rate limiting
mcp.add_middleware(RateLimitMiddleware(
    requests_per_minute=60,
    burst_size=10,
    on_limit_exceeded=lambda: logger.warning("Rate limit exceeded")
))
```

#### 3.4 Monitoring & Metrics

**Implementation:**
```python
import time
from collections import defaultdict

# Simple metrics tracking
_metrics = {
    "requests": defaultdict(int),
    "errors": defaultdict(int),
    "latencies": defaultdict(list)
}

def track_metrics(operation: str):
    """Decorator to track operation metrics."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            _metrics["requests"][operation] += 1
            
            try:
                result = await func(*args, **kwargs)
                latency = time.time() - start_time
                _metrics["latencies"][operation].append(latency)
                return result
            except Exception as e:
                _metrics["errors"][operation] += 1
                raise
        
        return wrapper
    return decorator

# Add metrics resource
@mcp.resource("r2r://server/metrics")
async def get_metrics(ctx: Context | None = None) -> dict:
    """Get server metrics and statistics."""
    return {
        "requests": dict(_metrics["requests"]),
        "errors": dict(_metrics["errors"]),
        "latencies": {
            op: {
                "count": len(latencies),
                "avg": sum(latencies) / len(latencies) if latencies else 0,
                "max": max(latencies) if latencies else 0
            }
            for op, latencies in _metrics["latencies"].items()
        }
    }
```

#### 3.5 Health Check

**Implementation:**
```python
@mcp.resource("r2r://health")
async def health_check(ctx: Context | None = None) -> dict:
    """Health check endpoint for monitoring."""
    try:
        # Check R2R API connectivity
        response = await _client.get(
            f"{_r2r_base_url}/health",
            timeout=5.0
        )
        r2r_healthy = response.status_code == 200
    except Exception as e:
        r2r_healthy = False
    
    return {
        "status": "healthy" if r2r_healthy else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            "r2r_api": "ok" if r2r_healthy else "failed",
            "auth_configured": bool(os.getenv("R2R_API_KEY"))
        }
    }
```

#### 3.6 Testing Framework

**Create `tests/test_server.py`:**
```python
import pytest
from src.server import mcp, _client

@pytest.mark.asyncio
async def test_server_info_resource():
    """Test server info resource."""
    result = await mcp.call_resource("r2r://server/info")
    assert "server" in result
    assert result["server"]["name"] == "R2R MCP Server"

@pytest.mark.asyncio
async def test_enhanced_search_tool():
    """Test enhanced search tool."""
    result = await mcp.call_tool("enhanced_search", {
        "query": "test query",
        "limit": 5
    })
    assert "results" in result
    assert "query" in result

@pytest.mark.asyncio
async def test_graphrag_query():
    """Test GraphRAG query tool."""
    result = await mcp.call_tool("graphrag_query", {
        "query": "machine learning",
        "use_communities": True
    })
    assert "chunk_search_results" in result or "graph_search_results" in result

# Run tests
# pytest tests/ -v --asyncio-mode=auto
```

**Implementation Priority:** HIGH  
**Estimated Effort:** 3-4 days  
**Dependencies:** None (can be implemented incrementally)

---

## 🔄 Priority 4: Advanced Search & Retrieval

### Features to Add

#### 4.1 Hybrid Search with Custom Weights

```python
@mcp.tool(
    description="Hybrid search with configurable weights",
    tags={"r2r", "search", "hybrid"}
)
async def hybrid_search(
    query: str,
    semantic_weight: float = 5.0,
    fulltext_weight: float = 1.0,
    rrf_k: int = 50,
    limit: int = 10,
    ctx: Context | None = None
) -> dict:
    """
    Hybrid search combining semantic and full-text search.
    
    Args:
        semantic_weight: Weight for semantic search (default: 5.0)
        fulltext_weight: Weight for full-text search (default: 1.0)
        rrf_k: Reciprocal Rank Fusion parameter (default: 50)
    """
    if ctx:
        await ctx.info(f"Hybrid search: {query}")
        await ctx.debug(f"Weights - semantic: {semantic_weight}, fulltext: {fulltext_weight}")
    
    response = await _client.post(
        f"{_r2r_base_url}/v3/retrieval/search",
        json={
            "query": query,
            "search_settings": {
                "use_hybrid_search": True,
                "hybrid_settings": {
                    "semantic_weight": semantic_weight,
                    "full_text_weight": fulltext_weight,
                    "rrf_k": rrf_k,
                    "full_text_limit": 200
                },
                "limit": limit
            }
        }
    )
    
    return response.json()
```

#### 4.2 HyDE & RAG-Fusion

```python
@mcp.tool(
    description="Advanced search using HyDE or RAG-Fusion strategies",
    tags={"r2r", "search", "advanced"}
)
async def advanced_search(
    query: str,
    strategy: str = "hyde",  # "hyde" or "rag_fusion"
    num_sub_queries: int = 5,
    limit: int = 10,
    ctx: Context | None = None
) -> dict:
    """
    Advanced search with query expansion strategies.
    
    Strategies:
        - "hyde": Hypothetical Document Embeddings
        - "rag_fusion": Multi-query fusion with RRF
    """
    if ctx:
        await ctx.info(f"Advanced search ({strategy}): {query}")
    
    response = await _client.post(
        f"{_r2r_base_url}/v3/retrieval/search",
        json={
            "query": query,
            "search_settings": {
                "search_strategy": strategy,
                "num_sub_queries": num_sub_queries,
                "limit": limit
            }
        }
    )
    
    return response.json()
```

#### 4.3 Filtered Search

```python
@mcp.tool(
    description="Search with metadata filtering",
    tags={"r2r", "search", "filter"}
)
async def filtered_search(
    query: str,
    filters: dict,
    limit: int = 10,
    ctx: Context | None = None
) -> dict:
    """
    Search with complex metadata filtering.
    
    Filter examples:
        - {"document_type": {"$eq": "pdf"}}
        - {"metadata.year": {"$gt": 2020}}
        - {"$and": [{"category": {"$eq": "tech"}}, {"status": {"$in": ["active"]}}]}
    
    Operators: $eq, $neq, $gt, $gte, $lt, $lte, $like, $in, $nin, $and, $or
    """
    if ctx:
        await ctx.info(f"Filtered search: {query}")
        await ctx.debug(f"Filters: {filters}")
    
    response = await _client.post(
        f"{_r2r_base_url}/v3/retrieval/search",
        json={
            "query": query,
            "search_settings": {
                "use_hybrid_search": True,
                "filters": filters,
                "limit": limit
            }
        }
    )
    
    return response.json()
```

**Implementation Priority:** MEDIUM  
**Estimated Effort:** 2 days  
**Dependencies:** R2R with search features enabled

---

## 📦 Priority 5: Document Management

### Features to Add

#### 5.1 Bulk Document Operations

```python
@mcp.tool(
    description="Upload multiple documents to R2R",
    tags={"r2r", "documents", "bulk"}
)
async def bulk_upload_documents(
    files: list[dict],  # [{"path": "...", "metadata": {...}}]
    collection_ids: list[str] | None = None,
    ingestion_mode: str = "hi-res",
    ctx: Context | None = None
) -> dict:
    """
    Upload multiple documents in batch.
    
    Ingestion modes:
        - "hi-res": Comprehensive parsing and enrichment
        - "fast": Speed-focused ingestion
        - "custom": Custom configuration
    """
    if ctx:
        await ctx.info(f"Bulk upload: {len(files)} documents")
        await ctx.report_progress(0, len(files))
    
    results = []
    for idx, file_info in enumerate(files):
        # Upload each file
        with open(file_info["path"], "rb") as f:
            response = await _client.post(
                f"{_r2r_base_url}/v3/documents",
                files={"file": f},
                data={
                    "metadata": json.dumps(file_info.get("metadata", {})),
                    "collection_ids": json.dumps(collection_ids or []),
                    "ingestion_mode": ingestion_mode
                }
            )
            results.append(response.json())
        
        if ctx:
            await ctx.report_progress(idx + 1, len(files))
    
    if ctx:
        await ctx.info(f"✓ Uploaded {len(results)} documents")
    
    return {"uploaded": len(results), "results": results}
```

#### 5.2 Document Status Tracking

```python
@mcp.resource(
    "r2r://documents/{document_id}/status",
    description="Track document processing status"
)
async def get_document_status(document_id: str, ctx: Context) -> dict:
    """Get document ingestion and processing status."""
    response = await _client.get(
        f"{_r2r_base_url}/v3/documents/{document_id}"
    )
    
    doc = response.json()
    
    return {
        "document_id": document_id,
        "status": doc.get("status"),
        "ingestion_status": doc.get("ingestion_status"),
        "extraction_status": doc.get("extraction_status"),
        "created_at": doc.get("created_at"),
        "updated_at": doc.get("updated_at")
    }
```

**Implementation Priority:** LOW-MEDIUM  
**Estimated Effort:** 1-2 days

---

## 🎓 Priority 6: User & Collection Management

### Features to Add

#### 6.1 Collection Tools

```python
@mcp.tool(
    description="Create a new collection",
    tags={"r2r", "collections"}
)
async def create_collection(
    name: str,
    description: str | None = None,
    ctx: Context | None = None
) -> dict:
    """Create a new document collection."""
    response = await _client.post(
        f"{_r2r_base_url}/v3/collections",
        json={
            "name": name,
            "description": description
        }
    )
    
    result = response.json()
    
    if ctx:
        await ctx.info(f"✓ Created collection: {result.get('id')}")
    
    return result

@mcp.tool(
    description="Add document to collection",
    tags={"r2r", "collections"}
)
async def add_document_to_collection(
    document_id: str,
    collection_id: str,
    ctx: Context | None = None
) -> dict:
    """Add a document to a collection."""
    response = await _client.post(
        f"{_r2r_base_url}/v3/collections/{collection_id}/documents/{document_id}"
    )
    
    if ctx:
        await ctx.info(f"✓ Added document to collection")
    
    return response.json()
```

**Implementation Priority:** LOW  
**Estimated Effort:** 1 day

---

## 📈 Implementation Plan

### Phase 1: Knowledge Graph (Weeks 1-2)
- [ ] Entity & relationship resource templates
- [ ] Knowledge graph extraction tool
- [ ] Graph search tool
- [ ] Community detection tools
- [ ] GraphRAG query tool

### Phase 2: Agents & Conversations (Weeks 3-4)
- [ ] Agent query tool
- [ ] Research mode with extended thinking
- [ ] Conversation management resources
- [ ] Conversation tools (create, update, delete)

### Phase 3: Production Features (Weeks 5-6)
- [ ] Error handling middleware
- [ ] Caching layer
- [ ] Rate limiting
- [ ] Monitoring & metrics
- [ ] Health check endpoint
- [ ] Testing framework

### Phase 4: Advanced Search (Week 7)
- [ ] Hybrid search tool
- [ ] HyDE & RAG-Fusion
- [ ] Filtered search
- [ ] Search analytics

### Phase 5: Document Management (Week 8)
- [ ] Bulk upload
- [ ] Status tracking
- [ ] Collection management

---

## 🧪 Testing Strategy

### Unit Tests
```bash
pytest tests/unit/ -v
```

### Integration Tests
```bash
pytest tests/integration/ -v --asyncio-mode=auto
```

### Load Tests
```bash
locust -f tests/load/locustfile.py
```

### MCP Inspector
```bash
fastmcp inspect src/server.py
```

---

## 📊 Success Metrics

### Performance
- [ ] < 100ms response time for cached resources
- [ ] < 500ms for simple searches
- [ ] < 2s for complex GraphRAG queries
- [ ] > 99% uptime

### Quality
- [ ] > 90% test coverage
- [ ] Zero linting errors
- [ ] All type hints valid
- [ ] Documentation complete

### Features
- [ ] 20+ custom components (beyond auto-generated)
- [ ] GraphRAG fully functional
- [ ] Agent capabilities working
- [ ] Production middleware enabled

---

## 🔗 References

### R2R Documentation
- Knowledge Graphs: https://r2r-docs.sciphi.ai/documentation/graphs
- Agent: https://r2r-docs.sciphi.ai/documentation/agent
- Search: https://r2r-docs.sciphi.ai/documentation/search-and-rag

### FastMCP Documentation
- Resources: https://gofastmcp.com/servers/resources
- Context: https://gofastmcp.com/servers/context
- Middleware: https://gofastmcp.com/servers/middleware
- Testing: https://gofastmcp.com/servers/testing

---

## 📝 Notes

This roadmap is based on extensive R2R RAG analysis with:
- **4 RAG queries** with max_tokens=4000
- **20-25 sources per query**
- Total of ~80 unique R2R/FastMCP documentation sources
- Focus on production-ready features and real-world patterns

Update this document as features are implemented and new requirements emerge.
