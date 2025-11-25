"""R2R MCP Server - FastMCP integration for R2R API."""

import logging
import os

import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP

# Use experimental OpenAPI parser for better performance and serverless compatibility
# 100-200ms faster startup, stateless request building, better OpenAPI compliance
try:
    from fastmcp.experimental.server.openapi import MCPType, RouteMap
except ImportError:
    # Fallback to legacy parser if experimental not available
    from fastmcp.server.openapi import MCPType, RouteMap

# Load environment variables from .env file (local development only)
# In production (FastMCP Cloud), environment variables are set directly
load_dotenv()

# Configuration
R2R_BASE_URL = os.getenv("R2R_BASE_URL", "http://localhost:7272")
R2R_API_KEY = os.getenv("R2R_API_KEY", "")
R2R_TIMEOUT = float(os.getenv("R2R_TIMEOUT", "30.0"))
DEBUG_LOGGING = os.getenv("DEBUG_LOGGING", "false").lower() == "true"

# Note: API key validation moved to runtime to allow build-time inspection

# Enable debug logging if requested
if DEBUG_LOGGING:
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("fastmcp.server.openapi").setLevel(logging.DEBUG)
    logging.getLogger("fastmcp.experimental.server.openapi").setLevel(logging.DEBUG)

# Load OpenAPI specification from R2R API directly
# This ensures we always have the latest API specification
openapi_url = f"{R2R_BASE_URL}/openapi.json"

# Log configuration for debugging (mask API key)
if DEBUG_LOGGING:
    masked_key = f"{R2R_API_KEY[:10]}...{R2R_API_KEY[-10:]}" if R2R_API_KEY else "NOT SET"
    logging.debug(f"R2R_BASE_URL: {R2R_BASE_URL}")
    logging.debug(f"R2R_API_KEY: {masked_key}")
    logging.debug(f"R2R_TIMEOUT: {R2R_TIMEOUT}")

# Load OpenAPI spec (public endpoint, no auth needed)
try:
    response = httpx.get(openapi_url, timeout=30.0)
    response.raise_for_status()
    openapi_spec = response.json()
except Exception as e:
    # If we can't load from API, try to use local file as fallback
    import json
    from pathlib import Path

    local_spec = Path(__file__).parent.parent / "openapi.json"
    if local_spec.exists():
        with open(local_spec) as f:
            openapi_spec = json.load(f)
    else:
        raise RuntimeError(f"Failed to load OpenAPI spec from {openapi_url}: {e}") from e

# Function to create HTTP client with authentication
# This is called lazily to ensure environment variables are available
def _create_client() -> httpx.AsyncClient:
    """Create HTTP client with authentication headers."""
    # Re-read environment variables to ensure we get runtime values
    api_key = os.getenv("R2R_API_KEY", "")
    base_url = os.getenv("R2R_BASE_URL", "http://localhost:7272")
    timeout = float(os.getenv("R2R_TIMEOUT", "30.0"))
    debug = os.getenv("DEBUG_LOGGING", "false").lower() == "true"

    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
        # Log headers for debugging (without exposing full key)
        if debug:
            masked = f"Bearer {api_key[:10]}...{api_key[-10:]}"
            logging.debug(f"Authorization header: {masked}")
    elif debug:
        logging.warning("R2R_API_KEY not set - API calls will fail with 401 Unauthorized")

    return httpx.AsyncClient(
        base_url=base_url,
        headers=headers,
        timeout=timeout,
    )


# Define semantic route mappings for R2R API
route_maps = [
    # === RESOURCES (GET without modifications) ===
    # Single item retrieval - ResourceTemplate (parametrized)
    RouteMap(
        methods=["GET"],
        pattern=r"^/v3/(chunks|documents|collections|conversations)/\{id\}$",
        mcp_type=MCPType.RESOURCE_TEMPLATE,
    ),
    RouteMap(
        methods=["GET"],
        pattern=r"^/v3/documents/\{id\}/download$",
        mcp_type=MCPType.RESOURCE_TEMPLATE,
    ),
    # List operations - Resources (read-only collections)
    RouteMap(
        methods=["GET"],
        pattern=r"^/v3/(chunks|documents|collections|conversations|entities|relationships|communities)$",
        mcp_type=MCPType.RESOURCE,
    ),
    # === TOOLS (All modifications and complex operations) ===
    # Search operations
    RouteMap(
        methods=["POST"],
        pattern=r".*/search$",
        mcp_type=MCPType.TOOL,
    ),
    # Create, Update, Delete operations
    RouteMap(
        methods=["POST", "PUT", "PATCH", "DELETE"],
        pattern=r".*",
        mcp_type=MCPType.TOOL,
    ),
    # Graph operations
    RouteMap(
        methods=["POST"],
        pattern=r"^/v3/(documents/\{id\}/(extract|deduplicate)|graphs/.*/communities/build)$",
        mcp_type=MCPType.TOOL,
    ),
    # Export operations
    RouteMap(
        methods=["POST"],
        pattern=r".*/export$",
        mcp_type=MCPType.TOOL,
    ),
    # Health check as resource
    RouteMap(
        methods=["GET"],
        pattern=r"^/health$",
        mcp_type=MCPType.RESOURCE,
    ),
]

# Create MCP server from OpenAPI specification
# Using experimental parser for:
# - 100-200ms faster startup (no code generation)
# - Stateless request building with openapi-core
# - Better serverless compatibility
mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=_create_client(),  # Create client with runtime environment variables
    name="R2R API MCP Server",
    route_maps=route_maps,
    tags={"r2r", "knowledge-graph", "document-management", "rag"},
)


if __name__ == "__main__":
    import sys

    # Support both stdio and HTTP transports
    transport = sys.argv[1] if len(sys.argv) > 1 else "stdio"

    if transport == "http":
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
        mcp.run(transport="http", port=port)
    else:
        mcp.run(transport="stdio")
