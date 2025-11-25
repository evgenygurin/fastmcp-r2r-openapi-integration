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

# Custom Auth class that reads API key at request time
class DynamicBearerAuth(httpx.Auth):
    """Auth handler that reads API key from environment at request time."""

    def auth_flow(self, request: httpx.Request):
        """Add Authorization header dynamically for each request."""
        # Read API key at REQUEST TIME, not at initialization time
        api_key = os.getenv("R2R_API_KEY", "")
        debug = os.getenv("DEBUG_LOGGING", "false").lower() == "true"

        if api_key:
            request.headers["Authorization"] = f"Bearer {api_key}"
            if debug:
                masked = f"Bearer {api_key[:10]}...{api_key[-10:]}"
                logging.debug(f"[Request] Authorization header: {masked}")
        elif debug:
            logging.warning("[Request] R2R_API_KEY not set - request will fail with 401")

        yield request


# Function to create HTTP client with dynamic authentication
def _create_client() -> httpx.AsyncClient:
    """Create HTTP client with dynamic authentication that reads env vars per request."""
    base_url = os.getenv("R2R_BASE_URL", "http://localhost:7272")
    timeout = float(os.getenv("R2R_TIMEOUT", "30.0"))
    debug = os.getenv("DEBUG_LOGGING", "false").lower() == "true"

    if debug:
        api_key = os.getenv("R2R_API_KEY", "")
        masked_key = f"{api_key[:10]}...{api_key[-10:]}" if api_key else "NOT SET"
        logging.debug(f"[Init] Creating client with base_url={base_url}")
        logging.debug(f"[Init] API key status: {masked_key}")

    # Use custom auth that reads API key at REQUEST time
    return httpx.AsyncClient(
        base_url=base_url,
        auth=DynamicBearerAuth(),
        timeout=timeout,
    )


# Define semantic route mappings for R2R API
# Based on analysis of 114 routes across 11 categories
# IMPORTANT: FastMCP checks patterns in order - first match wins
# More specific patterns MUST come before general ones
# See: https://gofastmcp.com/integrations/openapi
route_maps = [  # type: ignore
    # GET requests with path parameters -> RESOURCE_TEMPLATE
    RouteMap(
        methods=["GET"],
        pattern=r".*\{.*\}.*",
        mcp_type=MCPType.RESOURCE_TEMPLATE,  # type: ignore
    ),
    # All other GET requests -> RESOURCE
    RouteMap(
        methods=["GET"],
        pattern=r".*",
        mcp_type=MCPType.RESOURCE,  # type: ignore
    ),
    # POST/PUT/PATCH/DELETE default to TOOL (implicit)
]

# Create MCP server from OpenAPI specification
# Lazy initialization function to ensure environment variables are loaded
def _create_mcp_server():
    """Create MCP server with runtime environment variables."""
    # Create client with current environment variables
    client = _create_client()

    # Using experimental parser for:
    # - 100-200ms faster startup (no code generation)
    # - Stateless request building with openapi-core
    # - Better serverless compatibility
    return FastMCP.from_openapi(
        openapi_spec=openapi_spec,
        client=client,
        name="R2R API MCP Server",
        route_maps=route_maps,  # type: ignore
    )


# Create server instance (will be initialized lazily when accessed)
mcp = _create_mcp_server()


if __name__ == "__main__":
    import sys

    # Support multiple transports: stdio, http, streamable-http
    # stdio - for Claude Desktop
    # streamable-http - recommended for production (efficient bidirectional streaming)
    # http - legacy HTTP transport
    transport = sys.argv[1] if len(sys.argv) > 1 else "stdio"

    if transport in ["http", "streamable-http"]:
        # HTTP/Streamable HTTP transport
        host = sys.argv[2] if len(sys.argv) > 2 else "0.0.0.0"
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 8000

        print(f"🚀 Starting R2R MCP Server")
        print(f"   Transport: {transport}")
        print(f"   Host: {host}")
        print(f"   Port: {port}")
        print(f"   Endpoint: http://{host}:{port}/mcp")
        print(f"   Health: http://{host}:{port}/health")
        print()

        mcp.run(
            transport=transport,  # type: ignore
            host=host,
            port=port,
            log_level="INFO",
        )
    else:
        # STDIO transport for Claude Desktop
        mcp.run(transport="stdio")
