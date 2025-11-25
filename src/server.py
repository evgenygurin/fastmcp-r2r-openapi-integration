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
R2R_API_KEY = os.getenv("R2R_API_KEY")
R2R_TIMEOUT = float(os.getenv("R2R_TIMEOUT", "30.0"))
DEBUG_LOGGING = os.getenv("DEBUG_LOGGING", "false").lower() == "true"

# CRITICAL: Validate API key is present
if not R2R_API_KEY:
    raise ValueError(
        "R2R_API_KEY environment variable is required. "
        "Set it in FastMCP Cloud Environment Variables or in .env file locally."
    )

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

response = httpx.get(openapi_url, timeout=30.0)
response.raise_for_status()
openapi_spec = response.json()

# Create HTTP client with authentication
headers = {}
if R2R_API_KEY:
    headers["Authorization"] = f"Bearer {R2R_API_KEY}"
else:
    raise ValueError("R2R_API_KEY must be set to authenticate with R2R API")

# Log headers for debugging (without exposing full key)
if DEBUG_LOGGING:
    auth_header = headers.get("Authorization", "NOT SET")
    if auth_header != "NOT SET":
        masked = f"Bearer {R2R_API_KEY[:10]}...{R2R_API_KEY[-10:]}"
        logging.debug(f"Authorization header: {masked}")
    else:
        logging.debug("Authorization header: NOT SET")

client = httpx.AsyncClient(
    base_url=R2R_BASE_URL,
    headers=headers,
    timeout=R2R_TIMEOUT,
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
    client=client,
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
