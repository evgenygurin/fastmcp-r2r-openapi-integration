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
from typing import Any

import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP

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


if __name__ == "__main__":
    # Run with stdio transport (for Claude Desktop and FastMCP Cloud)
    logger.info("Starting R2R MCP Server with stdio transport")
    mcp.run()
