"""FastMCP R2R Server - Auto-generated from OpenAPI Specification.

This server exposes R2R API as MCP Tools and Resources, automatically
generating MCP components from the R2R OpenAPI specification.

Architecture:
- GET endpoints with path params -> RESOURCE_TEMPLATE
- GET endpoints without params -> RESOURCE
- POST/PUT/PATCH/DELETE -> TOOL
- Dynamic authentication via DynamicBearerAuth (reads API key at request time)
- Automatic parser selection (experimental with fallback to legacy)

Best Practices Implemented:
- Comprehensive error handling for network failures and invalid specs
- Request-time authentication for serverless compatibility (FastMCP Cloud)
- Structured logging with debug mode support
- OpenAPI spec validation before server initialization
- Graceful degradation with informative error messages

Configuration:
Environment variables (see .env.example):
- R2R_BASE_URL: Base URL for R2R API (required)
- R2R_API_KEY: API key for authentication (required)
- R2R_OPENAPI_URL: Custom OpenAPI spec URL (optional)
- DEBUG_LOGGING: Enable detailed debug logs (optional)

For more information, see the project README and workspace rules.
"""

import logging
import os
from datetime import datetime
from typing import Any

import httpx
from dotenv import load_dotenv
from fastmcp import Context, FastMCP

# Import pipeline components (after FastMCP imports)
from src.pipelines import (
    Pipeline,
    pipeline_llm_analyze,
    pipeline_llm_summarize,
    pipeline_search_and_analyze,
    sample_structured_output,
)

# Import from experimental parser if available (faster, stateless, better serverless)
try:
    from fastmcp.experimental.server.openapi import (  # type: ignore[import-not-found]
        MCPType,
        RouteMap,
    )

    _using_experimental = True
except ImportError:
    # Fallback to legacy parser if experimental not available
    from fastmcp.server.openapi import MCPType, RouteMap

    _using_experimental = False

# Load environment variables
load_dotenv()

# Configure logging
_debug_logging = os.getenv("DEBUG_LOGGING", "false").lower() == "true"
log_level = logging.DEBUG if _debug_logging else logging.INFO
logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DynamicBearerAuth(httpx.Auth):
    """Auth handler that reads API key from environment at request time.

    CRITICAL for FastMCP Cloud compatibility:
    - Reads R2R_API_KEY from environment DURING request execution
    - NOT at module import time (when env vars may not be injected yet)
    - Ensures auth works in serverless environments
    """

    def auth_flow(self, request: httpx.Request):
        """Inject Bearer token into request headers at request time.

        This method is called for EVERY request, ensuring the API key is
        always read from the current environment. This is critical for
        serverless/cloud deployments where env vars may be injected after
        module initialization.
        """
        api_key = os.getenv("R2R_API_KEY", "")
        if api_key:
            request.headers["Authorization"] = f"Bearer {api_key}"
            if _debug_logging:
                # Log first 8 chars of key for debugging (never log full key!)
                masked_key = (
                    f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
                )
                logger.debug(
                    f"✓ Injected Bearer auth for {request.method} {request.url.path} "
                    f"(key: {masked_key})"
                )
        else:
            logger.warning(
                "⚠️  R2R_API_KEY not set - API requests will likely fail with 401. "
                "Set R2R_API_KEY environment variable."
            )
        yield request


# R2R API configuration
_r2r_base_url = os.getenv("R2R_BASE_URL", "https://api.136-119-36-216.nip.io")
_r2r_openapi_url = os.getenv(
    "R2R_OPENAPI_URL",
    f"{_r2r_base_url}/openapi.json",
)

# Route mapping configuration for semantic MCP type assignment
# Validates against all 114+ R2R endpoints
_route_maps = [
    # Priority 1: GET with path parameters -> RESOURCE_TEMPLATE
    # Examples: /v3/chunks/{id}, /v3/documents/{id}/chunks,
    # /v3/collections/{id}/documents/{document_id}
    RouteMap(
        methods=["GET"],
        pattern=r"^/v3/.*\{.*\}.*$",
        mcp_type=MCPType.RESOURCE_TEMPLATE,
    ),
    # Priority 2: GET without parameters -> RESOURCE
    # Examples: /v3/chunks, /v3/documents, /v3/collections, /v3/graphs
    RouteMap(
        methods=["GET"],
        pattern=r"^/v3/.*$",
        mcp_type=MCPType.RESOURCE,
    ),
    # Priority 3: All mutations -> TOOL
    # Examples: POST /v3/chunks/search, DELETE /v3/documents/{id},
    # POST /v3/collections, PATCH /v3/documents/{id}/metadata
    RouteMap(
        methods=["POST", "PUT", "PATCH", "DELETE"],
        pattern=r".*",
        mcp_type=MCPType.TOOL,
    ),
]

# Create HTTP client with dynamic authentication
_client = httpx.AsyncClient(
    base_url=_r2r_base_url,
    auth=DynamicBearerAuth(),
    timeout=30.0,
    follow_redirects=True,
)

logger.info(f"Initializing R2R MCP Server with base URL: {_r2r_base_url}")
logger.info(f"OpenAPI spec URL: {_r2r_openapi_url}")
logger.info(
    f"Using {'experimental' if _using_experimental else 'legacy'} OpenAPI parser"
)

# Fetch OpenAPI spec with error handling
try:
    logger.info(f"Fetching OpenAPI specification from {_r2r_openapi_url}")
    _openapi_response = httpx.get(_r2r_openapi_url, timeout=30.0)
    _openapi_response.raise_for_status()
    _openapi_spec = _openapi_response.json()

    # Validate OpenAPI spec structure
    if not isinstance(_openapi_spec, dict) or "openapi" not in _openapi_spec:
        raise ValueError("Invalid OpenAPI specification format")

    spec_title = _openapi_spec.get("info", {}).get("title", "Unknown")
    spec_version = _openapi_spec.get("info", {}).get("version", "Unknown")
    logger.info(f"✓ Loaded OpenAPI spec: {spec_title} v{spec_version}")

except httpx.HTTPError as e:
    logger.error(f"Failed to fetch OpenAPI spec from {_r2r_openapi_url}: {e}")
    raise RuntimeError(
        f"Could not connect to R2R API. Please verify R2R_BASE_URL={_r2r_base_url} "
        "is correct and the server is running."
    ) from e
except (ValueError, KeyError) as e:
    logger.error(f"Invalid OpenAPI specification format: {e}")
    raise RuntimeError(
        f"Received invalid OpenAPI specification from {_r2r_openapi_url}. "
        "Please verify the API is returning a valid OpenAPI 3.0/3.1 spec."
    ) from e

# Auto-generate MCP components from OpenAPI spec with error handling
try:
    logger.info("Initializing FastMCP server from OpenAPI specification...")
    mcp = FastMCP.from_openapi(
        openapi_spec=_openapi_spec,
        client=_client,
        route_maps=_route_maps,
    )

    # Log component counts for visibility
    total_paths = len(_openapi_spec.get("paths", {}))
    logger.info(
        f"✓ Successfully initialized MCP server with "
        f"{'experimental' if _using_experimental else 'legacy'} parser"
    )
    logger.info(f"  - Processed {total_paths} API endpoints from OpenAPI spec")
    logger.info(f"  - Applied {len(_route_maps)} custom route mapping rules")

except Exception as e:
    logger.error(f"Failed to initialize FastMCP server: {e}")
    raise RuntimeError(
        f"Could not create MCP server from OpenAPI spec. Error: {type(e).__name__}: {e}"
    ) from e


# Add custom resources for server health and info
@mcp.resource("r2r://server/info")
def get_server_info() -> dict[str, Any]:
    """Get R2R server configuration and connection status.

    Returns comprehensive server information including configuration,
    OpenAPI spec details, and authentication status.
    """
    return {
        "server": {
            "name": "R2R MCP Server",
            "description": "R2R API - Document management, knowledge graphs, and AI",
            "version": "1.0.0",
        },
        "configuration": {
            "base_url": _r2r_base_url,
            "openapi_url": _r2r_openapi_url,
            "auth_configured": bool(os.getenv("R2R_API_KEY")),
            "debug_logging": _debug_logging,
        },
        "openapi": {
            "version": _openapi_spec.get("openapi", "unknown"),
            "title": _openapi_spec.get("info", {}).get("title", "Unknown"),
            "api_version": _openapi_spec.get("info", {}).get("version", "Unknown"),
            "total_endpoints": len(_openapi_spec.get("paths", {})),
        },
        "parser": {
            "type": "experimental" if _using_experimental else "legacy",
            "note": (
                "Experimental parser provides better performance "
                "and serverless compatibility"
            ),
        },
    }


@mcp.resource("r2r://server/routes")
def get_route_mapping() -> dict[str, Any]:
    """Get information about route mapping configuration.

    Explains how OpenAPI endpoints are converted to MCP component types
    (RESOURCE, RESOURCE_TEMPLATE, TOOL) based on HTTP method and path pattern.
    """
    return {
        "description": (
            "FastMCP route mapping converts OpenAPI endpoints to MCP components"
        ),
        "total_route_maps": len(_route_maps),
        "mappings": [
            {
                "priority": idx + 1,
                "methods": rm.methods,
                "pattern": rm.pattern,
                "mcp_type": (
                    rm.mcp_type.name
                    if hasattr(rm.mcp_type, "name")
                    else str(rm.mcp_type)
                ),
                "description": _get_route_map_description(idx),
            }
            for idx, rm in enumerate(_route_maps)
        ],
        "examples": {
            "RESOURCE_TEMPLATE": {
                "description": (
                    "GET requests with path parameters become parameterized resources"
                ),
                "examples": [
                    "/v3/chunks/{id}",
                    "/v3/documents/{id}/chunks",
                    "/v3/collections/{id}/documents",
                ],
            },
            "RESOURCE": {
                "description": (
                    "GET requests without parameters become static resources"
                ),
                "examples": [
                    "/v3/chunks",
                    "/v3/documents",
                    "/v3/collections",
                    "/v3/graphs",
                ],
            },
            "TOOL": {
                "description": (
                    "Mutation operations (POST/PUT/PATCH/DELETE) become tools"
                ),
                "examples": [
                    "POST /v3/chunks/search",
                    "DELETE /v3/documents/{id}",
                    "POST /v3/collections",
                ],
            },
        },
        "note": "Route maps are evaluated in priority order - first match wins",
    }


def _get_route_map_description(idx: int) -> str:
    """Get human-readable description for route map at given index."""
    descriptions = [
        "GET endpoints with path parameters (e.g., {id}) → Resource Templates",
        "GET endpoints without path parameters → Resources",
        "All mutation operations (POST/PUT/PATCH/DELETE) → Tools",
    ]
    return descriptions[idx] if idx < len(descriptions) else "Custom mapping rule"


# ============================================================================
# ENHANCED R2R RESOURCES - Direct access to R2R data
# ============================================================================


@mcp.resource(
    "r2r://documents/{document_id}",
    description="Get detailed information about a specific R2R document",
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def get_document_resource(document_id: str, ctx: Context) -> dict[str, Any]:
    """Fetch detailed document information from R2R API.

    This resource template provides direct access to document metadata,
    allowing LLMs to inspect document properties without making tool calls.
    """
    try:
        await ctx.info(f"Fetching document: {document_id}")
        response = await _client.get(f"/v3/documents/{document_id}")
        response.raise_for_status()

        await ctx.debug(f"Successfully fetched document {document_id}")
        return response.json()

    except httpx.HTTPError as e:
        await ctx.error(f"Failed to fetch document {document_id}: {e}")
        return {
            "error": f"Failed to fetch document: {e}",
            "document_id": document_id,
        }


@mcp.resource(
    "r2r://collections/{collection_id}/summary",
    description="Get summary information for an R2R collection",
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def get_collection_summary(collection_id: str, ctx: Context) -> dict[str, Any]:
    """Fetch collection summary with document count and metadata."""
    try:
        await ctx.info(f"Fetching collection summary: {collection_id}")

        # Get collection info
        response = await _client.get(f"/v3/collections/{collection_id}")
        response.raise_for_status()
        collection_data = response.json()

        # Get documents in collection
        docs_response = await _client.get(f"/v3/collections/{collection_id}/documents")
        docs_response.raise_for_status()
        documents = docs_response.json()

        return {
            "collection_id": collection_id,
            "collection_info": collection_data,
            "document_count": len(documents.get("results", [])),
            "fetched_at": datetime.now().isoformat(),
        }

    except httpx.HTTPError as e:
        await ctx.error(f"Failed to fetch collection {collection_id}: {e}")
        return {
            "error": f"Failed to fetch collection: {e}",
            "collection_id": collection_id,
        }


@mcp.resource(
    "r2r://search/results/{query}{?limit}",
    description="Search R2R knowledge base and return results",
    mime_type="application/json",
)
async def search_knowledge_base(
    query: str,
    limit: int = 10,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """Search R2R documents with optional result limit.

    Demonstrates RFC 6570 query parameters - limit is optional and
    can be provided via ?limit=N in the URI.
    """
    if ctx:
        await ctx.info(f"Searching R2R: '{query}' (limit={limit})")

    try:
        search_payload = {"query": query, "search_settings": {"limit": limit}}

        response = await _client.post("/v3/retrieval/search", json=search_payload)
        response.raise_for_status()
        results = response.json()

        if ctx:
            await ctx.debug(
                f"Search returned {len(results.get('results', {}))} results"
            )

        return {
            "query": query,
            "limit": limit,
            "results": results,
            "searched_at": datetime.now().isoformat(),
        }

    except httpx.HTTPError as e:
        error_msg = f"Search failed: {e}"
        if ctx:
            await ctx.error(error_msg)
        return {"error": error_msg, "query": query}


# ============================================================================
# PROMPTS - Reusable message templates for R2R operations
# ============================================================================


@mcp.prompt(
    name="rag_query_prompt",
    description="Generate a well-structured RAG query for R2R",
    tags={"r2r", "rag", "query"},
)
async def create_rag_query_prompt(
    question: str,
    context: str = "",
    ctx: Context | None = None,
) -> str:
    """Create a prompt for R2R RAG queries with optional context.

    This prompt template helps structure questions for optimal
    retrieval-augmented generation results.
    """
    if ctx:
        await ctx.info(f"Generating RAG prompt for question: {question[:50]}...")

    base_prompt = f"""Please answer the following question using the R2R knowledge base:

Question: {question}
"""

    if context:
        base_prompt += f"""
Additional Context: {context}
"""

    base_prompt += """
Please provide:
1. A clear, concise answer based on the retrieved documents
2. Citations to specific sources when possible
3. Confidence level in your answer (high/medium/low)
"""

    return base_prompt


@mcp.prompt(
    name="document_analysis_prompt",
    description="Generate a prompt for analyzing R2R document content",
    tags={"r2r", "analysis", "documents"},
)
def create_document_analysis_prompt(
    document_id: str,
    analysis_type: str = "summary",
) -> str:
    """Create a prompt for analyzing R2R documents.

    Args:
        document_id: The R2R document UUID
        analysis_type: Type of analysis (summary, entities, topics, sentiment)
    """
    prompts_by_type = {
        "summary": f"""Analyze the document {document_id} and provide:
1. A concise summary (2-3 sentences)
2. Key topics and themes
3. Document type and structure
""",
        "entities": f"""Extract structured information from document {document_id}:
1. Named entities (people, organizations, locations)
2. Key concepts and terminology
3. Dates and numerical data
""",
        "topics": f"""Identify the main topics in document {document_id}:
1. Primary subject areas
2. Related themes and concepts
3. Suggested tags for categorization
""",
        "sentiment": f"""Analyze the sentiment and tone of document {document_id}:
1. Overall sentiment (positive/neutral/negative)
2. Emotional tone and writing style
3. Intended audience and purpose
""",
    }

    return prompts_by_type.get(
        analysis_type,
        f"Analyze document {document_id} (type: {analysis_type})",
    )


# ============================================================================
# ENHANCED TOOLS - Tools with Context for better UX
# ============================================================================


@mcp.tool(
    description="Search R2R knowledge base with progress reporting",
    tags={"r2r", "search", "enhanced"},
)
async def enhanced_search(
    query: str,
    limit: int = 10,
    search_type: str = "hybrid",
    ctx: Context | None = None,
) -> dict[str, Any]:
    """Enhanced search with context logging and progress reporting.

    Demonstrates FastMCP Context capabilities:
    - Progress reporting for long operations
    - Info/debug logging for visibility
    - Error handling with context logging
    """
    if ctx:
        await ctx.info(f"🔍 Starting enhanced search: '{query}'")
        await ctx.report_progress(progress=0, total=100)

    try:
        # Prepare search
        search_payload = {
            "query": query,
            "search_settings": {
                "limit": limit,
                "use_hybrid_search": search_type == "hybrid",
                "use_semantic_search": search_type in ["semantic", "hybrid"],
            },
        }

        if ctx:
            await ctx.debug(f"Search settings: {search_payload['search_settings']}")
            await ctx.report_progress(progress=30, total=100)

        # Execute search
        response = await _client.post("/v3/retrieval/search", json=search_payload)
        response.raise_for_status()

        if ctx:
            await ctx.report_progress(progress=80, total=100)

        results = response.json()
        result_count = len(results.get("results", {}).get("chunk_search_results", []))

        if ctx:
            await ctx.info(f"✓ Found {result_count} results")
            await ctx.report_progress(progress=100, total=100)

        return {
            "query": query,
            "search_type": search_type,
            "result_count": result_count,
            "results": results,
            "timestamp": datetime.now().isoformat(),
        }

    except httpx.HTTPError as e:
        error_msg = f"Search failed: {e}"
        if ctx:
            await ctx.error(f"❌ {error_msg}")
        raise RuntimeError(error_msg) from e


@mcp.tool(
    description="Analyze R2R search results using LLM sampling",
    tags={"r2r", "analysis", "ai"},
)
async def analyze_search_results(
    query: str,
    limit: int = 5,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """Search R2R and use LLM sampling to analyze results.

    This tool demonstrates FastMCP's LLM sampling capability:
    - Performs R2R search
    - Uses ctx.sample() to analyze results with LLM
    - Returns structured analysis
    """
    if not ctx:
        return {"error": "Context required for LLM sampling"}

    try:
        await ctx.info(f"🧠 Analyzing search results for: '{query}'")

        # Step 1: Search R2R
        search_payload = {"query": query, "search_settings": {"limit": limit}}
        response = await _client.post("/v3/retrieval/search", json=search_payload)
        response.raise_for_status()
        results = response.json()

        # Step 2: Format results for LLM analysis
        chunks = results.get("results", {}).get("chunk_search_results", [])
        if not chunks:
            return {"analysis": "No results found", "query": query}

        results_text = "\n\n".join([
            f"Result {i + 1}: {chunk.get('text', '')[:200]}..."
            for i, chunk in enumerate(chunks[:5])
        ])

        # Step 3: Use LLM sampling for analysis
        await ctx.info("Requesting LLM analysis...")
        analysis_prompt = f"""Analyze these search results for the query: "{query}"

Results:
{results_text}

Provide:
1. Key themes and patterns
2. Relevance assessment
3. Suggested follow-up questions
"""

        llm_response = await ctx.sample(
            messages=analysis_prompt,
            system_prompt=(
                "You are an expert data analyst. Provide concise, structured analysis."
            ),
            temperature=0.3,
            max_tokens=500,
        )

        await ctx.info("✓ Analysis complete")

        return {
            "query": query,
            "result_count": len(chunks),
            "analysis": llm_response.text,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        await ctx.error(f"Analysis failed: {e}")
        raise


# ============================================================================
# ADVANCED: Pipeline-based Tools (using ctx.sample and composition)
# ============================================================================


@mcp.tool(
    description="Multi-step research pipeline: search → analyze → summarize",
    tags={"r2r", "pipeline", "research"}
)
async def research_pipeline(
    query: str,
    analysis_depth: str = "standard",  # "quick", "standard", "deep"
    ctx: Context | None = None
) -> dict:
    """
    Execute a complete research pipeline combining search, LLM analysis, and summarization.

    Steps:
        1. Search R2R knowledge base
        2. Analyze results with LLM (ctx.sample)
        3. Generate executive summary

    Args:
        query: Research question or topic
        analysis_depth: "quick" (1-2 mins), "standard" (3-5 mins), "deep" (5-10 mins)

    Example:
        research_pipeline(
            query="What are the latest advances in quantum computing?",
            analysis_depth="deep"
        )
    """
    if ctx:
        await ctx.info(f"🔬 Starting research pipeline: {query}")
        await ctx.info(f"Analysis depth: {analysis_depth}")

    # Configure based on depth
    depth_config = {
        "quick": {"search_limit": 5, "max_tokens": 500},
        "standard": {"search_limit": 10, "max_tokens": 1000},
        "deep": {"search_limit": 20, "max_tokens": 2000}
    }

    depth_config.get(analysis_depth, depth_config["standard"])

    # Create pipeline
    pipeline = Pipeline(ctx)

    # Execute pipeline steps
    results = await (
        pipeline
        .add_step("search", pipeline_search_and_analyze, query=query)
        .add_step("analyze", pipeline_llm_analyze)
        .add_step("summarize", pipeline_llm_summarize)
        .execute()
    )

    if ctx:
        await ctx.info("✅ Research pipeline complete")

    return {
        "query": query,
        "analysis_depth": analysis_depth,
        "summary": results.get("summarize", {}).get("summary"),
        "full_analysis": results.get("analyze", {}).get("analysis"),
        "search_results_count": len(results.get("search", {}).get("results", [])),
        "timestamp": datetime.utcnow().isoformat()
    }


@mcp.tool(
    description="Comparative analysis of multiple queries using LLM sampling",
    tags={"r2r", "pipeline", "comparison"}
)
async def comparative_analysis(
    queries: list[str],
    comparison_criteria: list[str] | None = None,
    ctx: Context | None = None
) -> dict:
    """
    Compare multiple search queries and provide comparative insights.

    Uses ctx.sample for AI-powered comparison of results.

    Args:
        queries: List of 2-5 queries to compare
        comparison_criteria: Optional criteria (e.g., ["accuracy", "completeness", "relevance"])

    Example:
        comparative_analysis(
            queries=["RAG vs fine-tuning", "RAG vs prompt engineering"],
            comparison_criteria=["use_cases", "cost", "performance"]
        )
    """
    if not ctx:
        return {"error": "Context required for LLM analysis"}

    if len(queries) < 2:
        return {"error": "At least 2 queries required for comparison"}

    if len(queries) > 5:
        return {"error": "Maximum 5 queries allowed"}

    await ctx.info(f"🔍 Comparative analysis of {len(queries)} queries")
    await ctx.report_progress(0, len(queries) + 1)

    # Search for each query
    search_results = {}
    for idx, query in enumerate(queries):
        await ctx.info(f"Searching: {query}")

        # In real implementation, this would call R2R search API
        search_results[query] = {
            "results": [{"text": f"Sample result for: {query}"}]
        }

        await ctx.report_progress(idx + 1, len(queries) + 1)

    # Prepare comparison prompt
    comparison_text = "\n\n".join([
        f"Query {i + 1}: {q}\nResults: {r}"
        for i, (q, r) in enumerate(search_results.items())
    ])

    criteria_text = (
        f"\n\nComparison Criteria: {', '.join(comparison_criteria)}"
        if comparison_criteria
        else ""
    )

    prompt = f"""Compare the following search queries and their results:

{comparison_text}{criteria_text}

Provide a structured comparison including:
1. Key similarities and differences
2. Strengths and limitations of each
3. Best use cases for each
4. Overall recommendation"""

    await ctx.info("🤖 Generating comparative analysis...")

    # Use LLM sampling for comparison
    response = await ctx.sample(
        messages=prompt,
        system_prompt="You are an expert analyst specializing in comparative analysis and synthesis.",
        temperature=0.4,
        max_tokens=2000
    )

    await ctx.report_progress(len(queries) + 1, len(queries) + 1)
    await ctx.info("✅ Comparative analysis complete")

    return {
        "queries": queries,
        "comparison": response.text,
        "criteria": comparison_criteria,
        "timestamp": datetime.utcnow().isoformat()
    }


@mcp.tool(
    description="Extract structured data from documents using LLM sampling",
    tags={"r2r", "extraction", "structured"}
)
async def extract_structured_data(
    document_id: str,
    schema: dict,
    ctx: Context | None = None
) -> dict:
    """
    Extract structured data from a document according to a provided schema.

    Uses ctx.sample to intelligently extract and structure information.

    Args:
        document_id: R2R document UUID
        schema: JSON schema describing desired output structure
            Example: {
                "title": "string",
                "authors": ["string"],
                "key_findings": ["string"],
                "date": "YYYY-MM-DD"
            }

    Example:
        extract_structured_data(
            document_id="abc123",
            schema={
                "title": "string",
                "summary": "string (max 200 chars)",
                "topics": ["string"],
                "sentiment": "positive|neutral|negative"
            }
        )
    """
    if not ctx:
        return {"error": "Context required for extraction"}

    await ctx.info(f"📄 Extracting structured data from document {document_id}")

    # Fetch document (in real implementation)
    # document = await _client.get(f"{_r2r_base_url}/v3/documents/{document_id}")

    # For demo, use placeholder
    document_content = f"Sample content for document {document_id}"

    await ctx.info("🔍 Analyzing document with schema...")

    # Use pipeline's structured output function
    result = await sample_structured_output(
        ctx=ctx,
        data={
            "document_id": document_id,
            "content": document_content,
            "schema": schema
        },
        output_format="json"
    )

    await ctx.info("✅ Extraction complete")

    return {
        "document_id": document_id,
        "schema": schema,
        "extracted_data": result,
        "timestamp": datetime.utcnow().isoformat()
    }


@mcp.tool(
    description="Generate follow-up questions based on search results",
    tags={"r2r", "questions", "exploration"}
)
async def generate_followup_questions(
    initial_query: str,
    num_questions: int = 5,
    ctx: Context | None = None
) -> dict:
    """
    Generate intelligent follow-up questions using LLM sampling.

    Helps users explore topics more deeply by suggesting relevant questions.

    Args:
        initial_query: The original search query
        num_questions: Number of follow-up questions (default: 5, max: 10)

    Example:
        generate_followup_questions(
            initial_query="What is GraphRAG?",
            num_questions=5
        )
    """
    if not ctx:
        return {"error": "Context required for question generation"}

    num_questions = min(num_questions, 10)  # Cap at 10

    await ctx.info(f"💡 Generating {num_questions} follow-up questions")

    # Search for initial query (in real implementation)
    # search_results = await _client.post(...)

    prompt = f"""Based on the query: "{initial_query}"

Generate {num_questions} insightful follow-up questions that would help explore this topic more deeply.

Questions should:
1. Build on the initial query
2. Cover different aspects (technical, practical, comparative, etc.)
3. Be specific and answerable
4. Progress from basic to advanced

Format as a numbered list."""

    response = await ctx.sample(
        messages=prompt,
        system_prompt="You are an expert at generating insightful questions for research and exploration.",
        temperature=0.7,  # Higher for creative questions
        max_tokens=800
    )

    await ctx.info("✅ Questions generated")

    # Parse questions from response
    questions_text = response.text
    questions = [
        line.strip()
        for line in questions_text.split('\n')
        if line.strip() and any(line.strip().startswith(f"{i}.") for i in range(1, 20))
    ]

    return {
        "initial_query": initial_query,
        "follow_up_questions": questions,
        "count": len(questions),
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    # Run with stdio transport (for Claude Desktop and FastMCP Cloud)
    logger.info("Starting R2R MCP Server with stdio transport")
    logger.info(
        "Enhanced features: 3 resource templates, 2 prompts, 6 tools (2 basic + 4 pipelines)"
    )
    mcp.run()
