### Integrate FastMCP Server into an Existing FastAPI Application

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/http.mdx

This code demonstrates how to seamlessly add a FastMCP server to an existing FastAPI application. It defines a FastMCP server with a sample tool and mounts it at a dedicated `/mcp` path, allowing both the original FastAPI endpoints and the FastMCP tools to coexist within the same application instance.

```python
from fastapi import FastAPI
from fastmcp import FastMCP

# Your existing API
api = FastAPI()

@api.get("/api/status")
def status():
    return {"status": "ok"}

# Create your MCP server
mcp = FastMCP("API Tools")

@mcp.tool
def query_database(query: str) -> dict:
    """Run a database query"""
    return {"result": "data"}

# Mount MCP at /mcp
api.mount("/mcp", mcp.http_app())

# Run with: uvicorn app:api --host 0.0.0.0 --port 8000
```

--------------------------------

### Create FastMCP Proxy Server from Client - Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

Creates a FastMCP proxy server from an existing FastMCP Client instance. Accepts additional settings as keyword arguments and returns a FastMCPProxy instance that wraps the provided client for proxy operations.

```python
from_client(cls, client: Client[ClientTransportT], **settings: Any) -> FastMCPProxy
```

--------------------------------

### Test FastMCP Servers In-Memory with Client (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/README.md

This snippet provides an example of using the `fastmcp.Client` for efficient in-memory testing of a `FastMCP` server instance. By passing the `FastMCP` object directly to the client, it establishes a direct connection, eliminating the need for process management or network calls during tests.

```python
from fastmcp import FastMCP, Client

mcp = FastMCP("My MCP Server")

async def main():
    # Connect via in-memory transport
    async with Client(mcp) as client:
        # ... use the client
```

--------------------------------

### Manage Path Parameters in FastMCP Client Calls

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openapi.mdx

FastMCP ensures the integrity of path parameters by filtering out `None` values and validating that all required path parameters are provided. If a required path parameter is missing or set to `None`, FastMCP raises a clear error, preventing malformed requests.

```python
# ✅ This works
await client.call_tool("get_user", {"user_id": 123})

# ❌ This raises: "Missing required path parameters: {'user_id'}"
await client.call_tool("get_user", {"user_id": None})
```

--------------------------------

### Generate FastMCP Servers from OpenAPI Specification or FastAPI App (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/server.mdx

Shows how FastMCP can automatically create server instances from existing API definitions. It covers generating a FastMCP server from an OpenAPI specification using `FastMCP.from_openapi()` and from a FastAPI application using `FastMCP.from_fastapi()`, simplifying the integration of existing APIs.

```python
import httpx
from fastmcp import FastMCP

# From OpenAPI spec
spec = httpx.get("https://api.example.com/openapi.json").json()
mcp = FastMCP.from_openapi(openapi_spec=spec, client=httpx.AsyncClient())

# From FastAPI app
from fastapi import FastAPI
app = FastAPI()
mcp = FastMCP.from_fastapi(app=app)
```

--------------------------------

### Initialize FastMCP and Component Manager

Source: https://github.com/jlowin/fastmcp/blob/main/src/fastmcp/contrib/component_manager/README.md

This Python code demonstrates how to set up a FastMCP server and integrate the Component Manager module. It initializes a FastMCP application instance and then calls `set_up_component_manager` to register the necessary component management routes.

```python
from fastmcp import FastMCP
from fastmcp.contrib.component_manager import set_up_component_manager

mcp = FastMCP(name="Component Manager", instructions="This is a test server with component manager.")
set_up_component_manager(server=mcp)
```

--------------------------------

### Create FastMCP Server from Client URL in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-cli-run.mdx

Instantiates a FastMCP server instance by connecting to a remote URL. Takes a URL string as input and returns a configured FastMCP server that acts as a client proxy to the remote server.

```python
def create_client_server(url: str) -> Any:
    """Create a FastMCP server from a client URL.
    
    Args:
        url: The URL to connect to
    
    Returns:
        A FastMCP server instance
    """
    pass
```

--------------------------------

### Install FastMCP using uv

Source: https://github.com/jlowin/fastmcp/blob/main/README.md

This command demonstrates how to install the FastMCP library using the `uv` package manager, which is the recommended method for installation. This sets up FastMCP for building and managing Model Context Protocol (MCP) servers.

```bash
uv pip install fastmcp
```

--------------------------------

### Call FastMCP Server Tools using Gemini SDK (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/gemini.mdx

This asynchronous Python script demonstrates how to connect to a FastMCP server and use its tools via the Google Gemini SDK. It instantiates a `Client` for the FastMCP server, enters its connection context, and then passes the `mcp_client.session` to the Gemini API's `generate_content` method. The Gemini model then calls the FastMCP tool (e.g., `roll_dice`) based on the prompt. Requires `fastmcp` and `google-genai` packages.

```python
from fastmcp import Client
from google import genai
import asyncio

mcp_client = Client("server.py")
gemini_client = genai.Client()

async def main():    
    async with mcp_client:
        response = await gemini_client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents="Roll 3 dice!",
            config=genai.types.GenerateContentConfig(
                temperature=0,
                tools=[mcp_client.session],  # Pass the FastMCP client session
            ),
        )
        print(response.text)

if __name__ == "__main__":
    asyncio.run(main())
```

--------------------------------

### Define Minimal FastMCP Server in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/fastmcp-cloud.mdx

This Python code defines a minimal FastMCP server instance. It initializes a `FastMCP` object with a server name and registers a simple tool named `hello`. This tool accepts a string `name` as input and returns a personalized greeting, illustrating the basic structure of a server file compatible with FastMCP Cloud.

```python
from fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.tool
def hello(name: str) -> str:
    return f"Hello, {name}!"
```

--------------------------------

### POST /server/run/streamable-http

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

Initiates the FastMCP server using Streamable HTTP transport.

```APIDOC
## POST /server/run/streamable-http

### Description
Run the server using Streamable HTTP transport.

### Method
POST

### Endpoint
/server/run/streamable-http

### Parameters
- **host** (str) - Optional - Host address to bind to
- **port** (int) - Optional - Port to bind to
- **log_level** (str) - Optional - Log level for the server
- **path** (str) - Optional - Path for the endpoint
- **uvicorn_config** (dict[str, Any]) - Optional - Additional configuration for the Uvicorn server

### Response
#### Success Response (200)
- **status** (None) - Server started successfully, returns no content.
```

--------------------------------

### Test FastMCP Server Functionality Using In-Memory Transport

Source: https://github.com/jlowin/fastmcp/blob/main/CLAUDE.md

This Python code demonstrates how to test a FastMCP server directly using an in-memory transport. It instantiates `FastMCP` and `Client` with the server object, bypassing network complexities for isolated and efficient testing of tool calls like `greet`.

```python
mcp = FastMCP("TestServer")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Direct connection - no network complexity
async with Client(mcp) as client:
    result = await client.call_tool("greet", {"name": "World"})
```

--------------------------------

### Tag FastMCP Components for Filtering in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/server.mdx

This example demonstrates how to assign tags to FastMCP components (like tools) using the `tags` parameter in their decorators. These tags enable selective exposure of components based on include/exclude rules configured on the FastMCP server instance.

```python
@mcp.tool(tags={"public", "utility"})
def public_tool() -> str:
    return "This tool is public"

@mcp.tool(tags={"internal", "admin"})
def admin_tool() -> str:
    return "This tool is for admins only"
```

--------------------------------

### Return a List of Images using FastMCP Media Helper (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/tools.mdx

Illustrates how a FastMCP tool can return multiple images by returning a list of `fastmcp.utilities.types.Image` objects. FastMCP processes each item in the list, converting them into individual MCP `ImageContent` blocks for a comprehensive response.

```python
from fastmcp.utilities.types import Image, Audio, File

@mcp.tool
def get_multiple_charts() -> list[Image]:
    """Return multiple charts."""
    return [Image(path="chart1.png"), Image(path="chart2.png")]
```

--------------------------------

### Define a FastMCP Tool for LLM Actions

Source: https://github.com/jlowin/fastmcp/blob/main/README.md

This example demonstrates how to define a 'tool' using the `@mcp.tool` decorator in FastMCP. Tools are Python functions that allow LLMs to perform actions, such as computations or API calls. FastMCP automatically generates a schema from the function's type hints and docstring.

```python
@mcp.tool
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers."""
    return a * b
```

--------------------------------

### Upgrade FastMCP Import Statement

Source: https://github.com/jlowin/fastmcp/blob/main/docs/getting-started/installation.mdx

Demonstrates the code change required when upgrading from the official MCP SDK's FastMCP 1.0 to FastMCP 2.0. The primary change involves updating the import statement for the FastMCP class.

```python
# Before
# from mcp.server.fastmcp import FastMCP

# After
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")
```

--------------------------------

### Create Nested FastMCP Mounts within Starlette Applications

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/http.mdx

This example illustrates how to build complex routing hierarchies by nesting Starlette applications, with a FastMCP server mounted deep within. An `inner_app` mounts the FastMCP server, which is then mounted by the main `app`, making the FastMCP accessible via a multi-segment path like `/outer/inner/mcp/`.

```python
from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount

# Create your FastMCP server
mcp = FastMCP("MyServer")

# Create the ASGI app
mcp_app = mcp.http_app(path='/mcp')

# Create nested application structure
inner_app = Starlette(routes=[Mount("/inner", app=mcp_app)])
app = Starlette(
    routes=[Mount("/outer", app=inner_app)],
    lifespan=mcp_app.lifespan,
)
```

--------------------------------

### Create FastMCP Server from OpenAPI Specification - Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

Creates a FastMCP server instance from an OpenAPI specification dictionary. Accepts custom route maps, route mapping functions, component functions, MCP names, tags, and additional settings. Returns a FastMCPOpenAPI or FastMCPOpenAPINew instance with an httpx AsyncClient for HTTP operations.

```python
from_openapi(cls, openapi_spec: dict[str, Any], client: httpx.AsyncClient, route_maps: list[RouteMap] | list[RouteMapNew] | None = None, route_map_fn: OpenAPIRouteMapFn | OpenAPIRouteMapFnNew | None = None, mcp_component_fn: OpenAPIComponentFn | OpenAPIComponentFnNew | None = None, mcp_names: dict[str, str] | None = None, tags: set[str] | None = None, **settings: Any) -> FastMCPOpenAPI | FastMCPOpenAPINew
```

--------------------------------

### Create FastMCP Server from FastAPI Application - Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

Creates a FastMCP server instance from an existing FastAPI application. Supports custom route maps, mapping functions, component functions, MCP names, httpx client configuration, tags, and additional settings. Returns a FastMCPOpenAPI or FastMCPOpenAPINew instance integrated with the FastAPI app.

```python
from_fastapi(cls, app: Any, name: str | None = None, route_maps: list[RouteMap] | list[RouteMapNew] | None = None, route_map_fn: OpenAPIRouteMapFn | OpenAPIRouteMapFnNew | None = None, mcp_component_fn: OpenAPIComponentFn | OpenAPIComponentFnNew | None = None, mcp_names: dict[str, str] | None = None, httpx_client_kwargs: dict[str, Any] | None = None, tags: set[str] | None = None, **settings: Any) -> FastMCPOpenAPI | FastMCPOpenAPINew
```

--------------------------------

### Mount FastMCP Server as Sub-application in Starlette (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/http.mdx

This code snippet demonstrates the initial steps for integrating a FastMCP server as a sub-application within an existing Starlette web framework. By importing `FastMCP`, `Starlette`, and `Mount`, developers can expose MCP capabilities alongside their current API endpoints, sharing the same domain and infrastructure.

```python
from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount
```

--------------------------------

### Start FastMCP Server as Async Task (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-utilities-tests.mdx

This Python asynchronous context manager launches a FastMCP server as an asyncio task within the same process. It's the recommended method for in-process asynchronous testing, avoiding issues common with subprocess management. It takes a FastMCP server instance and optional parameters for port, transport type, path, and host.

```python
run_server_async(server: FastMCP, port: int | None = None, transport: Literal['http', 'streamable-http', 'sse'] = 'http', path: str = '/mcp', host: str = '127.0.0.1') -> AsyncGenerator[str, None]
```

--------------------------------

### FastMCP Server Name Property

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

Returns the name of the FastMCP server instance as a string.

```python
def name(self) -> str
```

--------------------------------

### Create FastMCP Server from MCP Configuration in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-cli-run.mdx

Generates a FastMCP server instance from an MCP configuration file. Accepts a Path object pointing to the configuration file and returns a typed FastMCP server ready for execution.

```python
def create_mcp_config_server(mcp_config_path: Path) -> FastMCP[None]:
    """Create a FastMCP server from a MCPConfig."""
    pass
```

--------------------------------

### Verify FastMCP Installation

Source: https://github.com/jlowin/fastmcp/blob/main/docs/getting-started/installation.mdx

Checks if FastMCP is installed correctly by running the 'fastmcp version' command. This command displays the installed versions of FastMCP, MCP, Python, and the platform information.

```bash
fastmcp version
```

--------------------------------

### Configure FastMCP Client with Asynchronous Callback Handlers (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/client.mdx

This Python example demonstrates how to initialize the `fastmcp.Client` with asynchronous callback functions for handling server log messages (`log_handler`), monitoring operation progress (`progress_handler`), and responding to LLM sampling requests (`sampling_handler`). It also shows setting a default request timeout. Dependencies include `fastmcp`.

```python
from fastmcp import Client
from fastmcp.client.logging import LogMessage

async def log_handler(message: LogMessage):
    print(f"Server log: {message.data}")

async def progress_handler(progress: float, total: float | None, message: str | None):
    print(f"Progress: {progress}/{total} - {message}")

async def sampling_handler(messages, params, context):
    # Integrate with your LLM service here
    return "Generated response"

client = Client(
    "my_mcp_server.py",
    log_handler=log_handler,
    progress_handler=progress_handler,
    sampling_handler=sampling_handler,
    timeout=30.0
)
```

--------------------------------

### Capture FastMCP Logs (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-utilities-tests.mdx

This Python context manager facilitates capturing logs from FastMCP loggers, even when log propagation is disabled. It's useful for testing logging behavior within FastMCP applications.

```python
caplog_for_fastmcp(caplog)
```

--------------------------------

### Configure FastMCP dependencies in Python (deprecated)

Source: https://github.com/jlowin/fastmcp/blob/main/examples/fastmcp_config_demo/README.md

This Python code snippet shows the deprecated method of declaring server dependencies directly within the FastMCP server instantiation. As of FastMCP 2.11.4, this approach is no longer recommended and has been replaced by `fastmcp.json` configuration.

```python
mcp = FastMCP("Demo Server", dependencies=["pyautogui", "Pillow"])
```

--------------------------------

### Define FastMCP Tool Arguments with Python Type Annotations

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/tools.mdx

This snippet illustrates how FastMCP automatically uses standard Python type annotations in function signatures to define and validate tool arguments. It demonstrates defining parameters with basic types, default values, and optional types, which are then translated into MCP schemas. FastMCP supports a wide range of types, including Pydantic models.

```python
@mcp.tool
def analyze_text(
    text: str,
    max_tokens: int = 100,
    language: str | None = None
) -> dict:
    """Analyze the provided text."""
    # Implementation...
```

--------------------------------

### Run FastMCP Server Synchronously in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

This method starts the FastMCP server in a synchronous blocking manner. Similar to `run_async`, it allows specifying a `transport` protocol and a `show_banner` flag, plus extra transport arguments. This function blocks until the server stops and does not return a value.

```python
run(self, transport: Transport | None = None, show_banner: bool = True, **transport_kwargs: Any) -> None
```

--------------------------------

### Setup Auth0 OAuth Protection with FastMCP

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-auth-providers-auth0.mdx

Demonstrates how to integrate Auth0 for OAuth protection within a FastMCP application. Requires the `fastmcp` library and the `Auth0Provider` class. This example shows the initialization of the `Auth0Provider` with necessary credentials and its subsequent use in creating a FastMCP instance.

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.auth0 import Auth0Provider

# Simple Auth0 OAuth protection
auth = Auth0Provider(
    config_url="https://auth0.config.url",
    client_id="your-auth0-client-id",
    client_secret="your-auth0-client-secret",
    audience="your-auth0-api-audience",
    base_url="http://localhost:8000",
)

mcp = FastMCP("My Protected Server", auth=auth)
```

--------------------------------

### Convert FastAPI App to FastMCP Server (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/fastapi.mdx

This snippet demonstrates the simplest way to convert an existing FastAPI application into a FastMCP server. It utilizes the `FastMCP.from_fastapi` method, requiring the FastAPI app instance as input, and then runs the converted MCP server.

```python
# Assumes the FastAPI app from above is already defined
from fastmcp import FastMCP

# Convert to MCP server
mcp = FastMCP.from_fastapi(app=app)

if __name__ == "__main__":
    mcp.run()
```

--------------------------------

### Run FastMCP Server in Separate Process (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-utilities-tests.mdx

This Python context manager starts a FastMCP server in an isolated process, providing its URL for testing. It automatically terminates the server process upon exiting the context. It requires a function to create and run the server, and supports arguments for host, port, and server function parameters.

```python
run_server_in_process(server_fn: Callable[..., None], *args: Any, **kwargs: Any) -> Generator[str, None, None]
```

--------------------------------

### Run FastMCP Server with Inferred Instance (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

Demonstrates how to run a FastMCP server by letting `fastmcp run` automatically detect a `mcp`, `server`, or `app` variable in a specified Python file. This method requires the server instance to be directly assigned to one of these predefined variable names.

```python
from fastmcp import FastMCP

mcp = FastMCP("MyServer")
```

```bash
fastmcp run server.py
```

--------------------------------

### Protecting a Server with Google OAuth

Source: https://github.com/jlowin/fastmcp/blob/main/README.md

This Python snippet demonstrates how to protect a FastMCP server using Google OAuth. It initializes a GoogleProvider with client credentials and then creates a FastMCP instance with this authentication provider. This is the primary method for enabling enterprise-grade authentication on your FastMCP server.

```python
from fastmcp.server.auth.providers.google import GoogleProvider

auth = GoogleProvider(client_id="...", client_secret="...", base_url="https://myserver.com")
mcp = FastMCP("Protected Server", auth=auth)
```

--------------------------------

### Define FastMCP Prompt with Typed Arguments and Auto-Conversion

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/prompts.mdx

Demonstrates how FastMCP allows defining prompt functions with complex type annotations like `list[int]` and `dict[str, str]` in Python. FastMCP automatically handles conversion from JSON string arguments provided by MCP clients and generates clear JSON schema descriptions for these arguments.

```python
@mcp.prompt
def analyze_data(
    numbers: list[int],
    metadata: dict[str, str], 
    threshold: float
) -> str:
    """Analyze numerical data."""
    avg = sum(numbers) / len(numbers)
    return f"Average: {avg}, above threshold: {avg > threshold}"
```

```json
{
  "name": "analyze_data",
  "description": "Analyze numerical data.",
  "arguments": [
    {
      "name": "numbers",
      "description": "Provide as a JSON string matching the following schema: {\"items\":{\"type\":\"integer\"},\"type\":\"array\"}",
      "required": true
    },
    {
      "name": "metadata", 
      "description": "Provide as a JSON string matching the following schema: {\"additionalProperties\":{\"type\":\"string\"},\"type\":\"object\"}",
      "required": true
    },
    {
      "name": "threshold",
      "description": "Provide as a JSON string matching the following schema: {\"type\":\"number\"}",
      "required": true
    }
  ]
}
```

--------------------------------

### Verify FastMCP Server Reachability with Ping in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/client.mdx

Shows how to use the `ping()` method to check if the FastMCP server is reachable. This is a basic health check for server connectivity.

```python
async with client:
    await client.ping()
    print("Server is reachable")
```

--------------------------------

### Configure Advanced Rate Limiting Middleware in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

These Python examples demonstrate configuring FastMCP's built-in rate limiting middleware. The first uses a token bucket algorithm with configurable requests per second and burst capacity. The second uses a sliding window approach for precise time-based control.

```python
from fastmcp.server.middleware.rate_limiting import (
    RateLimitingMiddleware, 
    SlidingWindowRateLimitingMiddleware
)

# Token bucket rate limiting (allows controlled bursts)
mcp.add_middleware(RateLimitingMiddleware(
    max_requests_per_second=10.0,
    burst_capacity=20
))

# Sliding window rate limiting (precise time-based control)
mcp.add_middleware(SlidingWindowRateLimitingMiddleware(
    max_requests=100,
    window_minutes=1
))
```

--------------------------------

### Call an MCP Server Tool Using FastMCP Client in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/getting-started/welcome.mdx

This Python asynchronous function uses the `fastmcp.Client` to connect to an MCP server at `https://gofastmcp.com/mcp`. It then calls a remote tool named 'SearchFastMcp' with a query argument and prints the result. This demonstrates how to programmatically interact with an MCP server's exposed tools.

```python
import asyncio
from fastmcp import Client

async def main():
    async with Client("https://gofastmcp.com/mcp") as client:
        result = await client.call_tool(
            name="SearchFastMcp", 
            arguments={"query": "deploy a FastMCP server"}
        )
    print(result)

asyncio.run(main())
```

--------------------------------

### Remove Tool from FastMCP Server

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

This method removes a specified tool from the FastMCP server by its name. If the tool is not found, a `NotFoundError` will be raised.

```python
remove_tool(self, name: str) -> None
```

--------------------------------

### Run `fastmcp dev` within a specified project directory

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

Execute the `fastmcp dev` command and its associated server file within a particular project directory. The `--project` flag directs `fastmcp` to operate relative to the given path.

```bash
fastmcp dev server.py --project /path/to/project
```

--------------------------------

### Combine Multiple FastAPI and FastMCP Lifespans (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/fastapi.mdx

When a FastAPI application already has its own lifespan for setup and teardown, this snippet demonstrates how to combine it with the FastMCP application's lifespan. It utilizes `asynccontextmanager` to create a new, unified lifespan function that gracefully manages the startup and shutdown processes of both the main FastAPI application and the mounted FastMCP server, ensuring all resources are properly initialized and released.

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastmcp import FastMCP

# Your existing lifespan
@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # Startup
    print("Starting up the app...")
    # Initialize database, cache, etc.
    yield
    # Shutdown
    print("Shutting down the app...")

# Create MCP server
mcp = FastMCP("Tools")
mcp_app = mcp.http_app(path='/mcp')

# Combine both lifespans
@asynccontextmanager
async def combined_lifespan(app: FastAPI):
    # Run both lifespans
    async with app_lifespan(app):
        async with mcp_app.lifespan(app):
            yield
```

--------------------------------

### Call FastMCP Server via OpenAI Responses API

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openai.mdx

This Python script demonstrates how to interact with a deployed FastMCP server using the OpenAI Python SDK and the Responses API. It initializes an OpenAI client, configures a tool of type "mcp" pointing to the server's public URL, and then sends an input query to trigger the tool. Users need to replace `https://your-server-url.com` with the actual URL where their FastMCP server is exposed.

```python
from openai import OpenAI

# Your server URL (replace with your actual URL)
url = 'https://your-server-url.com'

client = OpenAI()

resp = client.responses.create(
    model="gpt-4.1",
    tools=[
        {
            "type": "mcp",
            "server_label": "dice_server",
            "server_url": f"{url}/mcp/",
            "require_approval": "never",
        },
    ],
    input="Roll a few dice!",
)

print(resp.output_text)
```

--------------------------------

### Initialize a FastMCP Server Instance

Source: https://github.com/jlowin/fastmcp/blob/main/README.md

This Python code snippet shows how to create a new instance of the `FastMCP` server. The `FastMCP` object serves as the central application for defining tools, resources, and prompts, and it can be configured with a unique name.

```python
from fastmcp import FastMCP

# Create a server instance
mcp = FastMCP(name="MyAssistantServer")
```

--------------------------------

### Define a FastMCP Tool with Python Decorator

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/tools.mdx

This example shows how to register a Python function as a tool in FastMCP using the `@mcp.tool` decorator. It initializes a FastMCP instance and defines an `add` function that takes two integers and returns their sum. FastMCP automatically derives the tool's name, description from the docstring, and input schema from type annotations, making it callable by an LLM.

```python
from fastmcp import FastMCP

mcp = FastMCP(name="CalculatorServer")

@mcp.tool
def add(a: int, b: int) -> int:
    """Adds two integer numbers together."""
    return a + b
```

--------------------------------

### Leveraging LLM Sampling with FastMCP Context (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/context.mdx

Explains how to request text generation from the client's LLM using `ctx.sample()`, useful for integrating AI capabilities within your tools. This allows dynamic content generation or data analysis leveraging large language models.

```python
response = await ctx.sample("Analyze this data", temperature=0.7)
```

--------------------------------

### Define a FastMCP Tool using Python Decorator

Source: https://github.com/jlowin/fastmcp/blob/main/docs/updates.mdx

This Python code demonstrates the 'naked' decorator usage introduced in FastMCP 2.7 for defining a tool. It shows how to register a simple 'add' function as a FastMCP tool using the `@mcp.tool` decorator, making it accessible for integration with LLMs or other clients. An initialized `FastMCP` instance named `mcp` is a prerequisite for using this decorator.

```python
mcp = FastMCP()

@mcp.tool
def add(a: int, b: int) -> int:
    return a + b
```

--------------------------------

### Define a Basic FastMCP Server with a Tool in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/getting-started/welcome.mdx

This Python code initializes a FastMCP server, named 'Demo 🚀', and defines a simple tool `add` that takes two integers and returns their sum. The tool is exposed via the `@mcp.tool` decorator, making it accessible to LLM applications. The script includes a standard `if __name__ == "__main__"` block to run the MCP server when executed directly.

```python
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    mcp.run()
```

--------------------------------

### POST /server/run/http

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

Initiates the FastMCP server using HTTP transport, allowing configuration of host, port, logging, and Uvicorn settings.

```APIDOC
## POST /server/run/http

### Description
Initiates the FastMCP server using HTTP transport.

### Method
POST

### Endpoint
/server/run/http

### Parameters
- **transport** (Literal['http', 'streamable-http', 'sse']) - Optional - Transport protocol to use - either "streamable-http" (default) or "sse"
- **host** (str) - Optional - Host address to bind to (defaults to settings.host)
- **port** (int) - Optional - Port to bind to (defaults to settings.port)
- **log_level** (str) - Optional - Log level for the server (defaults to settings.log_level)
- **path** (str) - Optional - Path for the endpoint (defaults to settings.streamable_http_path or settings.sse_path)
- **uvicorn_config** (dict[str, Any]) - Optional - Additional configuration for the Uvicorn server
- **middleware** (list[ASGIMiddleware]) - Optional - A list of middleware to apply to the app
- **json_response** (bool) - Optional - Whether to use JSON response format (defaults to settings.json_response)
- **stateless_http** (bool) - Optional - Whether to use stateless HTTP (defaults to settings.stateless_http)

### Response
#### Success Response (200)
- **status** (None) - Server started successfully, returns no content.
```

--------------------------------

### Registering Static Methods with FastMCP Decorators (Not Recommended)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/decorating-methods.mdx

This approach demonstrates directly decorating a static method with a FastMCP decorator. While it technically 'works' because `@staticmethod` converts the method into a regular function that FastMCP can process, it is not recommended as the FastMCP decorator will not return a callable staticmethod.

```python
from fastmcp import FastMCP

mcp = FastMCP()

class MyClass:
    @mcp.tool
    @staticmethod
    def utility(x, y):
        return x + y
```

--------------------------------

### FastMCP.from_openapi()

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openapi.mdx

This section details how to initialize an FastMCP server by providing an OpenAPI specification and an HTTP client. FastMCP will automatically convert the API endpoints into MCP components.

```APIDOC
## Class Method FastMCP.from_openapi()

### Description
Convert an OpenAPI specification into an MCP server instance. This method streamlines the process of exposing existing APIs to AI models via the MCP protocol.

### Method/Function
`FastMCP.from_openapi(openapi_spec, client, name=None, timeout=None)`

### Parameters
#### Arguments
- **openapi_spec** (dict) - Required - The loaded OpenAPI specification as a Python dictionary.
- **client** (httpx.AsyncClient) - Required - An instance of `httpx.AsyncClient` configured to interact with the target API. This client will be used for all API calls made by the MCP server.
- **name** (str) - Optional - A human-readable name for the generated MCP server.
- **timeout** (float) - Optional - A timeout in seconds for all requests made by the internal HTTP client used by FastMCP.

### Request Example
```python
import httpx
from fastmcp import FastMCP

# Create an HTTP client for your API
client = httpx.AsyncClient(base_url="https://api.example.com")

# Load your OpenAPI spec 
# In a real application, this might come from a file or a live endpoint
openapi_spec = httpx.get("https://api.example.com/openapi.json").json()

# Create the MCP server
mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
    name="My API Server"
)

if __name__ == "__main__":
    mcp.run()
```

### Response
#### Success Response (FastMCP Instance)
Returns an initialized `FastMCP` server instance, ready to be run.
```python
# mcp is an instance of FastMCP, configured from the OpenAPI spec
# mcp.run() starts the server
```
```

--------------------------------

### FastMCP Server Settings Property

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

Returns the Settings object associated with the FastMCP server instance. Used to access server configuration and settings.

```python
def settings(self) -> Settings
```

--------------------------------

### Return a Single Image using FastMCP Media Helper (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/tools.mdx

This example demonstrates how a FastMCP tool can return a single `fastmcp.utilities.types.Image` object. FastMCP automatically converts this helper class into an appropriate MCP `ImageContent` block, simplifying media handling for developers.

```python
from fastmcp.utilities.types import Image, Audio, File

@mcp.tool
def get_chart() -> Image:
    """Generate a chart image."""
    return Image(path="chart.png")
```

--------------------------------

### Retrieve FastMCP Server Icons in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

This method provides a list of icon objects configured for the FastMCP server. It takes no parameters and returns a list of `mcp.types.Icon` instances.

```python
icons(self) -> list[mcp.types.Icon]
```

--------------------------------

### Instantiate FastMCP Server in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/server.mdx

This code demonstrates how to create basic instances of the FastMCP server. It shows how to initialize a server with just a name and how to include an 'instructions' string to guide client interactions.

```python
from fastmcp import FastMCP

# Create a basic server instance
mcp = FastMCP(name="MyAssistantServer")

# You can also add instructions for how to interact with the server
mcp_with_instructions = FastMCP(
    name="HelpfulAssistant",
    instructions="""
        This server provides data analysis tools.
        Call get_average() to analyze numerical data.
    """,
)
```

--------------------------------

### Run Async Streamable HTTP Server in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

This function asynchronously launches a server utilizing the Streamable HTTP transport protocol. It supports detailed configuration including host, port, log level, endpoint path, and custom Uvicorn settings. The function aims to efficiently serve streamable HTTP content with controlled server parameters.

```python
run_streamable_http_async(self, host: str | None = None, port: int | None = None, log_level: str | None = None, path: str | None = None, uvicorn_config: dict[str, Any] | None = None) -> None
```

--------------------------------

### Instantiate FastMCP application in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/http.mdx

This Python snippet demonstrates how to create a FastMCP application instance and generate its HTTP application component. The `path` argument specifies the internal MCP protocol endpoint, ensuring operational routes are correctly generated.

```python
mcp = FastMCP("Protected Server", auth=auth)
mcp_app = mcp.http_app(path=MCP_PATH)
```

--------------------------------

### Running FastMCP Server with Streamable HTTP Transport

Source: https://github.com/jlowin/fastmcp/blob/main/README.md

This Python code configures and runs a FastMCP server using the streamable HTTP transport. It specifies the local host address and port, along with a custom path for the MCP endpoint. This is recommended for web deployments.

```python
mcp.run(transport="http", host="127.0.0.1", port=8000, path="/mcp")
```

--------------------------------

### Run a FastMCP server using the FastMCP CLI

Source: https://github.com/jlowin/fastmcp/blob/main/docs/getting-started/quickstart.mdx

Launch a FastMCP server using the `fastmcp run` command, specifying the server's Python file and object. The CLI supports different transports, allowing execution with default `stdio` or explicitly setting `http` with a port.

```bash
fastmcp run my_server.py:mcp
```

```bash
fastmcp run my_server.py:mcp --transport http --port 8000
```

--------------------------------

### Interact with Multi-Server FastMCP Client (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/client.mdx

Demonstrates how to create and interact with a `fastmcp.Client` configured with multiple MCP servers from a dictionary. It shows how to call tools and read resources, automatically prefixing operations with the respective server names as defined in the configuration.

```python
config = {
    "mcpServers": {
        "weather": {"url": "https://weather-api.example.com/mcp"},
        "assistant": {"command": "python", "args": ["./assistant_server.py"]}
    }
}

client = Client(config)

async with client:
    # Tools are prefixed with server names
    weather_data = await client.call_tool("weather_get_forecast", {"city": "London"})
    response = await client.call_tool("assistant_answer_question", {"question": "What's the capital of France?"})
    
    # Resources use prefixed URIs
    icons = await client.read_resource("weather://weather/icons/sunny")
    templates = await client.read_resource("resource://assistant/templates/list")
```

--------------------------------

### Create FastMCP Client and Interact (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/client.mdx

Demonstrates how to initialize a `fastmcp.Client` with different server sources (in-memory, HTTP, local script) and perform basic operations like `ping`, `list_tools`, `list_resources`, `list_prompts`, and `call_tool` within an `async with` context manager for proper connection management. Requires `asyncio` for execution.

```python
import asyncio
from fastmcp import Client, FastMCP

# In-memory server (ideal for testing)
server = FastMCP("TestServer")
client = Client(server)

# HTTP server
client = Client("https://example.com/mcp")

# Local Python script
client = Client("my_mcp_server.py")

async def main():
    async with client:
        # Basic server interaction
        await client.ping()
        
        # List available operations
        tools = await client.list_tools()
        resources = await client.list_resources()
        prompts = await client.list_prompts()
        
        # Execute operations
        result = await client.call_tool("example_tool", {"param": "value"})
        print(result)

asyncio.run(main())
```

--------------------------------

### Display FastMCP Version Information

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

Displays version information about FastMCP and related components. An optional flag can be used to copy the version information to the clipboard.

```bash
fastmcp version
```

```bash
fastmcp version --copy
```

--------------------------------

### FastMCP Client Automatic Transport Inference (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/client.mdx

Illustrates how the `fastmcp.Client` automatically infers the appropriate transport mechanism (in-memory, Python Stdio, HTTP) based on the provided server source during client instantiation. This simplifies client setup for various MCP server types.

```python
from fastmcp import Client, FastMCP

# Examples of transport inference
client_memory = Client(FastMCP("TestServer"))
client_script = Client("./server.py") 
client_http = Client("https://api.example.com/mcp")
```

--------------------------------

### Run FastMCP Server with Uvicorn

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/http.mdx

Configure Uvicorn to run your FastMCP application. Basic configuration specifies the host and port, while production deployments benefit from using multiple workers for improved performance and reliability.

```bash
# Run with basic configuration
uvicorn app:app --host 0.0.0.0 --port 8000

# Run with multiple workers for production
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

--------------------------------

### PUT /client/sampling_callback

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-client.mdx

Configures the callback function to handle sampling requests from the MCP server. This allows the client to provide dynamic sampling logic.

```APIDOC
## PUT /client/sampling_callback

### Description
Configures the callback function to handle sampling requests from the MCP server. This allows the client to provide dynamic sampling logic.

### Method
PUT

### Endpoint
/client/sampling_callback

### Parameters
#### Path Parameters
- No path parameters.

#### Query Parameters
- No query parameters.

#### Request Body
- **sampling_callback** (ClientSamplingHandler) - Required - The handler function to be invoked for sampling requests.

### Request Example
{
  "sampling_callback": "my_sampling_function_reference"
}

### Response
#### Success Response (200)
- No response body. Indicates successful update.

#### Response Example
{}
```

--------------------------------

### Install FastMCP Server in Gemini CLI using `fastmcp install`

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/gemini-cli.mdx

This command uses the FastMCP CLI to automatically install and configure a server defined in `server.py` within Gemini CLI. It handles dependency management and internal Gemini CLI configuration.

```bash
fastmcp install gemini-cli server.py
```

--------------------------------

### Add FastMCP Server with User Scope using Gemini CLI

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/gemini-cli.mdx

This command registers a FastMCP server named 'my-server' with the Gemini CLI under the current user's scope. It uses 'uv' for environment management and runs 'server.py' through the 'fastmcp' framework.

```bash
gemini mcp add my-server --scope user uv -- run --with fastmcp fastmcp run server.py
```

--------------------------------

### Run FastMCP server from command line

Source: https://github.com/jlowin/fastmcp/blob/main/examples/fastmcp_config_demo/README.md

These bash commands illustrate various ways to run a FastMCP server using the `fastmcp` CLI tool. It covers auto-detection of `fastmcp.json` in the current directory, explicit file specification, and running in development mode with the Inspector UI.

```bash
# Auto-detect fastmcp.json in current directory
cd examples/mcp_server_config_demo
fastmcp run

# Or specify the config file explicitly
fastmcp run examples/mcp_server_config_demo/fastmcp.json

# Or use development mode with the Inspector UI
fastmcp dev examples/mcp_server_config_demo/fastmcp.json
```

--------------------------------

### Create Dynamic MCP Resource Template for User Profiles using FastMCP in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/tutorials/mcp.mdx

Illustrates creating a dynamic resource template with URL parameters. The template uses curly braces to define variable segments in the URI (e.g., {user_id}), allowing clients to request specific resources like 'users://42/profile'. This pattern enables dynamic data retrieval based on runtime parameters.

```python
from fastmcp import FastMCP

mcp = FastMCP()

# This template provides user data for any given user ID
@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: str) -> dict:
    """Returns the profile for a specific user."""
    # Fetch user from a database...
    return {"id": user_id, "name": "Zaphod Beeblebrox"}
```

--------------------------------

### Create FastMCP Proxy Server with Backend Configuration - Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

Creates a FastMCP proxy server for a given backend. The backend can be an existing Client instance, ClientTransport, FastMCP server, FastMCP1Server, URL, Path, MCPConfig, dictionary, or string. This method provides flexible proxy creation by mirroring the Client constructor's convenience.

```python
as_proxy(cls, backend: Client[ClientTransportT] | ClientTransport | FastMCP[Any] | FastMCP1Server | AnyUrl | Path | MCPConfig | dict[str, Any] | str, **settings: Any) -> FastMCPProxy
```

--------------------------------

### Basic FastMCP Server Installation

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/mcp-json-configuration.mdx

Demonstrates the simplest FastMCP server installation that generates an MCP JSON configuration. The output shows the standard uv command structure with FastMCP as a dependency. The configuration can be directly added to MCP client configuration files.

```bash
fastmcp install mcp-json dice_server.py
```

```json
{
  "Dice Server": {
    "command": "uv",
    "args": [
      "run",
      "--with",
      "fastmcp",
      "fastmcp", 
      "run",
      "/home/user/dice_server.py"
    ]
  }
}
```

--------------------------------

### Define a Dynamic FastMCP Resource Template

Source: https://github.com/jlowin/fastmcp/blob/main/README.md

This example shows how to create a dynamic 'resource template' with the `@mcp.resource` decorator. By including placeholders like `{user_id}` in the URI, clients can request specific data subsets, and the associated Python function receives these parameters to fetch the relevant information.

```python
@mcp.resource("users://{user_id}/profile")
def get_profile(user_id: int):
    # Fetch profile for user_id...
    return {"name": f"User {user_id}", "status": "active"}
```

--------------------------------

### Deploy FastMCP with Environment Variable

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/http.mdx

Example of how to set an environment variable (MCP_AUTH_TOKEN) when starting the Uvicorn server to pass sensitive configuration to the FastMCP application.

```bash
MCP_AUTH_TOKEN=secret uvicorn app:app --host 0.0.0.0 --port 8000
```

--------------------------------

### Implement Basic FastMCP Elicitation Handler in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/elicitation.mdx

This Python code defines an asynchronous function `basic_elicitation_handler` that serves as a custom handler for FastMCP elicitation requests. It prints server messages, takes user input, and returns an `ElicitResult` for non-acceptance or a structured response using `response_type` for acceptance, demonstrating interaction with a FastMCP server.

```python
from fastmcp import Client
from fastmcp.client.elicitation import ElicitResult

async def basic_elicitation_handler(message: str, response_type: type, params, context):
    print(f"Server asks: {message}")
    
    # Simple text input for demonstration
    user_response = input("Your response: ")
    
    if not user_response:
        # For non-acceptance, use ElicitResult explicitly
        return ElicitResult(action="decline")
    
    # Use the response_type dataclass to create a properly structured response
    # FastMCP handles the conversion from JSON schema to Python type
    # Return data directly - FastMCP will implicitly accept the elicitation
    return response_type(value=user_response)

client = Client(
    "my_mcp_server.py", 
    elicitation_handler=basic_elicitation_handler
)
```

--------------------------------

### Access FastMCP Server Resources in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/client.mdx

Illustrates how to list and read data from server-side resources. Resources can be static files or templated data sources provided by the FastMCP server.

```python
async with client:
    # List available resources
    resources = await client.list_resources()
    
    # Read a resource
    content = await client.read_resource("file:///config/settings.json")
    print(content[0].text)
```

--------------------------------

### Get a FastMCP Namespaced Logger (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-utilities-logging.mdx

This Python function retrieves a `logging.Logger` instance. The logger is automatically named and nested under the 'FastMCP.' namespace, taking a simple string `name` as an argument. It returns a fully configured logger ready for emitting messages within the FastMCP project.

```python
get_logger(name: str) -> logging.Logger
```

--------------------------------

### Configure FastMCP Client with Bearer Token String (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/auth/bearer.mdx

Shows how to initialize the FastMCP client using a Bearer token provided as a simple string. FastMCP automatically formats the token for the `Authorization` header. Ensure the token string does not include the `Bearer` prefix.

```python
from fastmcp import Client

async with Client(
    "https://fastmcp.cloud/mcp", 
    auth="<your-token>",
) as client:
    await client.ping()
```

--------------------------------

### Prompt Management API

Source: https://github.com/jlowin/fastmcp/blob/main/src/fastmcp/contrib/component_manager/README.md

Endpoints to dynamically enable or disable specific prompts within the FastMCP server at runtime.

```APIDOC
## POST /prompts/{prompt_name}/enable

### Description
Enables a specific prompt by its name within the FastMCP server.

### Method
POST

### Endpoint
/prompts/{prompt_name}/enable

### Parameters
#### Path Parameters
- **prompt_name** (string) - Required - The unique name of the prompt to enable.

### Response
#### Success Response (200)
- **message** (string) - A confirmation message, e.g., "Enabled prompt: {prompt_name}".

#### Response Example
{
  "message": "Enabled prompt: my_custom_prompt"
}

## POST /prompts/{prompt_name}/disable

### Description
Disables a specific prompt by its name within the FastMCP server.

### Method
POST

### Endpoint
/prompts/{prompt_name}/disable

### Parameters
#### Path Parameters
- **prompt_name** (string) - Required - The unique name of the prompt to disable.

### Response
#### Success Response (200)
- **message** (string) - A confirmation message, e.g., "Disabled prompt: {prompt_name}".

#### Response Example
{
  "message": "Disabled prompt: my_custom_prompt"
}
```

--------------------------------

### Add Custom Starlette Middleware to FastMCP ASGI App (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/http.mdx

This example illustrates how to integrate custom Starlette middleware, specifically `CORSMiddleware`, into a FastMCP application. By defining a list of `Middleware` objects and passing it to `mcp.http_app()`, you can apply global functionalities like CORS to your FastMCP ASGI application.

```python
from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

# Create your FastMCP server
mcp = FastMCP("MyServer")

# Define middleware
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

# Create ASGI app with middleware
http_app = mcp.http_app(middleware=middleware)
```

--------------------------------

### Run a FastMCP Server with Transport Options in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/server.mdx

This example demonstrates how to initialize a FastMCP server and run it using the `mcp.run()` method. It shows the default STDIO transport and an alternative HTTP transport configuration, useful for deploying as a web service.

```python
# my_server.py
from fastmcp import FastMCP

mcp = FastMCP(name="MyServer")

@mcp.tool
def greet(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    # This runs the server, defaulting to STDIO transport
    mcp.run()
    
    # To use a different transport, e.g., HTTP:
    # mcp.run(transport="http", host="127.0.0.1", port=9000)
```

--------------------------------

### Get FastMCP Server Website URL in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

This method returns the website URL associated with the FastMCP server. It requires no input and provides the URL as a string or None.

```python
website_url(self) -> str | None
```

--------------------------------

### Convert single MCPServerType to server and transport in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-utilities-mcp_config.mdx

This utility function converts a single `MCPServerTypes` entry, identified by a given name, into a server and a transport object. It accepts a name string and an `MCPServerTypes` object, returning a tuple consisting of the name, a `FastMCP` instance, and a `ClientTransport` instance.

```python
mcp_server_type_to_servers_and_transports(name: str, mcp_server: MCPServerTypes) -> tuple[str, FastMCP[Any], ClientTransport]
```

--------------------------------

### Get a Specific FastMCP Server Resource Template by Key in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

This method retrieves a specific resource template from the FastMCP server using its unique key. It requires a string `key` as input and returns the corresponding `ResourceTemplate` object.

```python
get_resource_template(self, key: str) -> ResourceTemplate
```

--------------------------------

### Connect to Multiple FastMCP Servers with Unified Client (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/README.md

This example demonstrates how to configure a single `fastmcp.Client` to manage connections to multiple MCP servers using a standard configuration dictionary. It defines different servers with specified URLs or commands and then shows how to access their respective tools using server prefixes.

```python
from fastmcp import Client

# Standard MCP configuration with multiple servers
config = {
    "mcpServers": {
        "weather": {"url": "https://weather-api.example.com/mcp"},
        "assistant": {"command": "python", "args": ["./assistant_server.py"]}
    }
}

# Create a client that connects to all servers
client = Client(config)

async def main():
    async with client:
        # Access tools and resources with server prefixes
        forecast = await client.call_tool("weather_get_forecast", {"city": "London"})
        answer = await client.call_tool("assistant_answer_question", {"query": "What is MCP?"})
```

--------------------------------

### Create a Basic FastMCP Logging Middleware in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

This Python code demonstrates how to create a custom FastMCP middleware by subclassing `Middleware` and implementing a simple logging mechanism. The `on_message` hook logs the method and source of all MCP messages before and after they are processed by the rest of the middleware chain, providing basic operational insight.

```python
from fastmcp import FastMCP
from fastmcp.server.middleware import Middleware, MiddlewareContext

class LoggingMiddleware(Middleware):
    """Middleware that logs all MCP operations."""
    
    async def on_message(self, context: MiddlewareContext, call_next):
        """Called for all MCP messages."""
        print(f"Processing {context.method} from {context.source}")
        
        result = await call_next(context)
        
        print(f"Completed {context.method}")
        return result
```

--------------------------------

### Compose FastMCP Servers by Mounting Subservers (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/server.mdx

Demonstrates how to combine multiple FastMCP servers into a single application using `main.mount()`. This allows for modular application design by integrating a sub-server with its own tools into a main server, making its functionalities accessible through a defined prefix.

```python
# Example: Importing a subserver
from fastmcp import FastMCP
import asyncio

main = FastMCP(name="Main")
sub = FastMCP(name="Sub")

@sub.tool
def hello(): 
    return "hi"

# Mount directly
main.mount(sub, prefix="sub")
```

--------------------------------

### Manage FastAPI Lifespan When Mounting FastMCP (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/fastapi.mdx

This code illustrates the correct way to handle lifespan management when mounting a FastMCP server to a FastAPI application. It emphasizes the necessity of passing the `lifespan` context from the FastMCP app to the FastAPI app to ensure proper initialization of the MCP server's session manager. An incorrect example, where lifespan is omitted, is also shown to highlight potential issues.

```python
# Correct - lifespan passed
mcp_app = mcp.http_app(path='/mcp')
app = FastAPI(lifespan=mcp_app.lifespan)
app.mount("/mcp", mcp_app)

# Incorrect - missing lifespan
app = FastAPI()
app.mount("/mcp", mcp.http_app())  # Session manager won't initialize
```

--------------------------------

### Test FastMCP Client with Google OAuth in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/google.mdx

This Python script demonstrates how to create an asynchronous `fastmcp` client that authenticates with a Google-protected server. It automatically handles Google OAuth, guiding the user through a browser-based login on the first connection, and then calls a protected tool to fetch user information. Dependencies include `fastmcp` and `asyncio`.

```python
from fastmcp import Client
import asyncio

async def main():
    # The client will automatically handle Google OAuth
    async with Client("http://localhost:8000/mcp", auth="oauth") as client:
        # First-time connection will open Google login in your browser
        print("✓ Authenticated with Google!")
        
        # Test the protected tool
        result = await client.call_tool("get_user_info")
        print(f"Google user: {result['email']}")
        print(f"Name: {result['name']}")

if __name__ == "__main__":
    asyncio.run(main())
```

--------------------------------

### Create Authenticated Remote FastMCP Proxy (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/claude-desktop.mdx

This Python snippet shows the initial imports required for creating an authenticated remote server proxy using `fastmcp`. It includes `FastMCP`, `Client`, and `BearerAuth` classes, indicating the setup for securely connecting to remote services through a proxy.

```python
from fastmcp import FastMCP, Client
from fastmcp.client.auth import BearerAuth
```

--------------------------------

### Run FastMCP Server Asynchronously in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

This method initiates the FastMCP server to run in an asynchronous mode. It accepts an optional `transport` protocol (e.g., 'stdio', 'sse', or 'streamable-http') and a `show_banner` flag, along with additional transport-specific keyword arguments. This function does not return a value but starts the server.

```python
run_async(self, transport: Transport | None = None, show_banner: bool = True, **transport_kwargs: Any) -> None
```

--------------------------------

### FastMCP Server Instructions Property

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

Gets or sets the instructions string for the FastMCP server. The instructions can be None if not set. The setter accepts an optional string value.

```python
def instructions(self) -> str | None
```

```python
def instructions(self, value: str | None) -> None
```

--------------------------------

### Configure FastMCP with GitHub OAuth Protection

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-auth-providers-github.mdx

This example demonstrates how to integrate the GitHub OAuth provider into a FastMCP server. It initializes the `GitHubProvider` with the necessary client ID and secret, then passes the configured authentication provider to the `FastMCP` instance, setting up basic GitHub OAuth protection for the server.

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.github import GitHubProvider

# Simple GitHub OAuth protection
auth = GitHubProvider(
    client_id="your-github-client-id",
    client_secret="your-github-client-secret"
)

mcp = FastMCP("My Protected Server", auth=auth)
```

--------------------------------

### Mount FastMCP Server in Starlette Application

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/http.mdx

This code demonstrates how to initialize a FastMCP server with a tool, convert it into an ASGI application using `mcp.http_app()`, and then mount it within a Starlette application. It's crucial to pass `mcp_app.lifespan` to the Starlette app to ensure proper initialization of the FastMCP server's session manager, especially for Streamable HTTP transport.

```python
mcp = FastMCP("MyServer")

@mcp.tool
def analyze(data: str) -> dict:
    return {"result": f"Analyzed: {data}"}

# Create the ASGI app
mcp_app = mcp.http_app(path='/mcp')

# Create a Starlette app and mount the MCP server
app = Starlette(
    routes=[
        Mount("/mcp-server", app=mcp_app),
        # Add other routes as needed
    ],
    lifespan=mcp_app.lifespan,
)
```

--------------------------------

### Retrieve Rendered Prompts from FastMCP Server in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/client.mdx

Demonstrates how to list available prompt templates and retrieve a rendered prompt by providing arguments. Prompts are reusable message templates managed by the FastMCP server.

```python
async with client:
    # List available prompts
    prompts = await client.list_prompts()
    
    # Get a rendered prompt
    messages = await client.get_prompt("analyze_data", {"data": [1, 2, 3]})
    print(messages.messages)
```

--------------------------------

### Python resource decorator for URI-based content serving in FastMCP

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

Decorator that registers functions as resources with URI-based access. Supports synchronous and asynchronous functions, parameterized URIs for templates, optional Context parameter for MCP capabilities, and multiple return types (str, bytes, JSON). Includes comprehensive metadata configuration options.

```python
resource(self, uri: str) -> Callable[[AnyFunction], Resource | ResourceTemplate]
```

--------------------------------

### Add Resource Tool Middleware to FastMCP

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

Demonstrates how to add the `ResourceToolMiddleware` to your FastMCP application. This middleware provides `list_resources` and `read_resource` tools for clients that cannot directly list or read resources.

```python
from fastmcp.server.middleware.tool_injection import ResourceToolMiddleware

mcp.add_middleware(ResourceToolMiddleware())
```

--------------------------------

### Integrate FastMCP with FastAPI Lifespan

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/fastapi.mdx

This code snippet demonstrates how to initialize a FastAPI application with a combined lifespan, ensuring that both the main application's initialization logic and the FastMCP server's session manager are properly managed. The `app.mount` call then makes the MCP server accessible at a specific path. This pattern uses nested `async with` statements to guarantee correct initialization and cleanup order for all resources.

```python
app = FastAPI(lifespan=combined_lifespan)
app.mount("/mcp", mcp_app)
```

--------------------------------

### Run and Inspect FastMCP Server

Source: https://github.com/jlowin/fastmcp/blob/main/examples/testing_demo/README.md

Commands to run and inspect a FastMCP server using the fastmcp CLI tool. The run command starts the server, while the inspect command provides details about the server's tools, resources, and prompts without starting it.

```bash
# Run the server
uv run fastmcp run server.py

# Inspect the server
uv run fastmcp inspect server.py
```

--------------------------------

### Perform In-Memory FastMCP Testing in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/development/tests.mdx

Demonstrates FastMCP's efficient in-memory testing approach, where a server instance is passed directly to the client for direct communication within the same Python process. This enables deterministic, fast tests without network overhead, simplifying debugging. The example creates a `WeatherServer` and tests its `get_temperature` tool.

```python
from fastmcp import FastMCP, Client

# Create your server
server = FastMCP("WeatherServer")

@server.tool
def get_temperature(city: str) -> dict:
    """Get current temperature for a city"""
    temps = {"NYC": 72, "LA": 85, "Chicago": 68}
    return {"city": city, "temp": temps.get(city, 70)}

async def test_weather_operations():
    # Pass server directly - no deployment needed
    async with Client(server) as client:
        result = await client.call_tool("get_temperature", {"city": "NYC"})
        assert result.data == {"city": "NYC", "temp": 72}
```

--------------------------------

### Inspect FastMCP v2.x Instance (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-utilities-inspect.mdx

This Python function extracts information from a FastMCP v2.x instance. It takes a `FastMCP[Any]` object as input and returns a `FastMCPInfo` dataclass containing the extracted data.

```python
inspect_fastmcp_v2(mcp: FastMCP[Any]) -> FastMCPInfo
```

--------------------------------

### Register FastMCP Component Methods with Server in Python

Source: https://github.com/jlowin/fastmcp/blob/main/src/fastmcp/contrib/mcp_mixin/README.md

This snippet demonstrates how to instantiate a `FastMCP` server and register all decorated methods from an `MCPMixin` component. It shows how to use the `register_all` method both with and without a `prefix`. Using a prefix is particularly useful for avoiding name collisions when multiple instances of the same component class are registered with the same `FastMCP` server.

```python
mcp_server = FastMCP()
component = MyComponent()

# Register all decorated methods with a prefix
# Useful if you will have multiple instantiated objects of the same class
# and want to avoid name collisions.
component.register_all(mcp_server, prefix="my_comp") 

# Register without a prefix
# component.register_all(mcp_server) 
```

--------------------------------

### Interact with FastMCP Server Converted from FastAPI Using Client (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/fastapi.mdx

This snippet illustrates how to interact with a FastMCP server, converted from a FastAPI app, using the `fastmcp.client.Client`. It demonstrates listing available tools and calling specific tools with parameters to test functionalities, simulating how an LLM-based application would interact with the server.

```python
# Assumes the FastAPI app from above is already defined
from fastmcp import FastMCP
from fastmcp.client import Client
import asyncio

# Convert to MCP server
mcp = FastMCP.from_fastapi(app=app)

async def demo():
    async with Client(mcp) as client:
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {[t.name for t in tools]}")
        
        # Create a product
        result = await client.call_tool(
            "create_product_products_post",
            {
                "name": "Wireless Keyboard",
                "price": 79.99,
                "category": "Electronics",
                "description": "Bluetooth mechanical keyboard"
            }
        )
        print(f"Created product: {result.data}")
        
        # List electronics under $100
        result = await client.call_tool(
            "list_products_products_get",
            {"category": "Electronics", "max_price": 100}
        )
        print(f"Affordable electronics: {result.data}")

if __name__ == "__main__":
    asyncio.run(demo())
```

--------------------------------

### Detailed Per-Operation Timing with DetailedTimingMiddleware in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-middleware-timing.mdx

The DetailedTimingMiddleware class provides enhanced timing with per-operation breakdowns for different MCP operations. It allows identification of performance bottlenecks in specific operations like tool calls, resource reads, and prompt retrievals. Each operation type has its own timing method that wraps the call_next handler.

```python
on_call_tool(self, context: MiddlewareContext, call_next: CallNext) -> Any
```

```python
on_read_resource(self, context: MiddlewareContext, call_next: CallNext) -> Any
```

```python
on_get_prompt(self, context: MiddlewareContext, call_next: CallNext) -> Any
```

--------------------------------

### Configure Strict or Flexible Input Validation in FastMCP

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/tools.mdx

FastMCP offers two input validation modes: a default flexible mode that coerces compatible types (e.g., string '10' to integer 10) for LLM compatibility, and a strict mode that rejects any type mismatches using JSON Schema validation. Strict mode ensures inputs precisely match type annotations, while flexible mode is recommended for most use cases due to its graceful handling of common LLM client behaviors.

```python
# Enable strict validation for this server
mcp = FastMCP("StrictServer", strict_input_validation=True)

@mcp.tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

# With strict_input_validation=True, sending {"a": "10", "b": "20"} will fail
# With strict_input_validation=False (default), it will be coerced to integers
```

--------------------------------

### Create a Remote FastMCP Proxy Server (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/claude-desktop.mdx

This Python script uses the `fastmcp` library to create a proxy server that forwards requests to a specified remote HTTP server. This allows users without native remote server support in Claude Desktop to integrate external services by running the proxy server locally.

```python
from fastmcp import FastMCP

# Create a proxy to a remote server
proxy = FastMCP.as_proxy(
    "https://example.com/mcp/sse", 
    name="Remote Server Proxy"
)

if __name__ == "__main__":
    proxy.run()  # Runs via STDIO for Claude Desktop
```

--------------------------------

### Modify FastMCP Tool Call Arguments and Results in Python Middleware

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

This Python snippet illustrates how to modify tool call arguments before execution and transform results afterward using a FastMCP middleware. It provides examples of ensuring positive input values for a 'calculate' tool and adding metadata to the structured content of a 'get_data' tool's result, showcasing pre- and post-processing capabilities.

```python
from fastmcp.server.middleware import Middleware, MiddlewareContext

class ToolCallMiddleware(Middleware):
    async def on_call_tool(self, context: MiddlewareContext, call_next):
        # Modify arguments before execution
        if context.message.name == "calculate":
            # Ensure positive inputs
            if context.message.arguments.get("value", 0) < 0:
                context.message.arguments["value"] = abs(context.message.arguments["value"])
        
        result = await call_next(context)
        
        # Transform result after execution
        if context.message.name == "get_data":
            # Add metadata to result
            if result.structured_content:
                result.structured_content["processed_at"] = "2024-01-01T00:00:00Z"
        
        return result
```

--------------------------------

### Running FastMCP Server with SSE Transport

Source: https://github.com/jlowin/fastmcp/blob/main/README.md

This Python code demonstrates how to run a FastMCP server using the Server-Sent Events (SSE) transport protocol. It sets the host and port for the server. This transport is useful for compatibility with existing SSE clients.

```python
mcp.run(transport="sse", host="127.0.0.1", port=8000)
```

--------------------------------

### Configure Authentication for FastMCP OpenAPI Server (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openapi.mdx

Illustrates how to apply authentication, such as a Bearer token, and set a request timeout on the `httpx.AsyncClient` that FastMCP uses. This ensures that all requests made by the generated MCP server to the underlying API are properly authenticated.

```python
import httpx
from fastmcp import FastMCP

# Bearer token authentication
api_client = httpx.AsyncClient(
    base_url="https://api.example.com",
    headers={"Authorization": "Bearer YOUR_TOKEN"}
)

# Create MCP server with authenticated client
mcp = FastMCP.from_openapi(
    openapi_spec=spec, 
    client=api_client,
    timeout=30.0  # 30 second timeout for all requests
)
```

--------------------------------

### Get a Specific FastMCP Server Prompt by Key in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

This method retrieves a specific prompt from the FastMCP server using its unique key. It requires a string `key` as input and returns the corresponding `Prompt` object.

```python
get_prompt(self, key: str) -> Prompt
```

--------------------------------

### Initialize FastMCP Server with Environment Variable-Configured Authentication (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/github.mdx

This Python snippet demonstrates how the `FastMCP` server initialization simplifies when the authentication provider and its settings are entirely configured through environment variables. The `FastMCP` instance automatically detects and utilizes the specified GitHub authentication provider, leading to cleaner and more concise application code.

```python
from fastmcp import FastMCP

# Authentication is automatically configured from environment
mcp = FastMCP(name="GitHub Secured App")

@mcp.tool
async def list_repos() -> list[str]:
    """List the authenticated user's repositories."""
    # Your tool implementation here
    pass
```

--------------------------------

### Install FastMCP Tools

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

Installs specified tools for a FastMCP server within a project directory. It takes the tool name and the server file as arguments, along with the project path.

```bash
fastmcp install cursor server.py --project /path/to/project
```

--------------------------------

### Combine Multiple FastMCP Middleware in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

This Python code demonstrates how to combine various FastMCP middleware components in a logical order for a production server. It includes Error Handling, Rate Limiting, Timing, and Logging middleware, followed by defining a tool endpoint.

```python
from fastmcp import FastMCP
from fastmcp.server.middleware.timing import TimingMiddleware
from fastmcp.server.middleware.logging import LoggingMiddleware
from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware

mcp = FastMCP("Production Server")

# Add middleware in logical order
mcp.add_middleware(ErrorHandlingMiddleware())  # Handle errors first
mcp.add_middleware(RateLimitingMiddleware(max_requests_per_second=50))
mcp.add_middleware(TimingMiddleware())  # Time actual execution
mcp.add_middleware(LoggingMiddleware())  # Log everything

@mcp.tool
def my_tool(data: str) -> str:
    return f"Processed: {data}"
```

--------------------------------

### Create FastMCP Server from OpenAPI Specification (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openapi.mdx

Demonstrates how to initialize an MCP server using FastMCP by providing an OpenAPI specification and an `httpx.AsyncClient`. The server converts API endpoints into MCP components, allowing AI models to interact with the API.

```python
import httpx
from fastmcp import FastMCP

# Create an HTTP client for your API
client = httpx.AsyncClient(base_url="https://api.example.com")

# Load your OpenAPI spec 
openapi_spec = httpx.get("https://api.example.com/openapi.json").json()

# Create the MCP server
mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
    name="My API Server"
)

if __name__ == "__main__":
    mcp.run()
```

--------------------------------

### Add Multiple Middleware to FastMCP Server

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

This example shows how to add multiple middleware components to a FastMCP server. Middleware is executed in the order it is added. The first middleware added processes requests first on the way in and last on the way out.

```python
from fastmcp import FastMCP
from fastmcp.server.middleware.authentication import AuthenticationMiddleware
from fastmcp.server.middleware.performance import PerformanceMiddleware
from fastmcp.server.middleware.logging import LoggingMiddleware

mcp = FastMCP("MyServer")

mcp.add_middleware(AuthenticationMiddleware("secret-token"))
mcp.add_middleware(PerformanceMiddleware())
mcp.add_middleware(LoggingMiddleware())
```

--------------------------------

### Configure FastMCP Server Environment Variables for Scalekit

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/scalekit.mdx

Sets up necessary environment variables for your FastMCP project's `.env` file, including Scalekit's environment URL, client ID, resource ID, and the MCP server's URL. These variables are crucial for connecting FastMCP to Scalekit.

```sh
SCALEKIT_ENVIRONMENT_URL=<YOUR_APP_ENVIRONMENT_URL>
SCALEKIT_CLIENT_ID=<YOUR_APP_CLIENT_ID> # skc_7008EXAMPLE46
SCALEKIT_RESOURCE_ID=<YOUR_APP_RESOURCE_ID> # res_926EXAMPLE5878
MCP_URL=http://localhost:8000/mcp
```

--------------------------------

### Example Test for Stateless Request Building

Source: https://github.com/jlowin/fastmcp/blob/main/src/fastmcp/experimental/server/openapi/README.md

Provides an example test function to verify the stateless nature of the RequestDirector and the speed of server initialization. It measures the time taken to initialize the FastMCPOpenAPI server and asserts that it falls within a very low threshold, indicating efficient startup.

```python
async def test_stateless_request_building():
    """Test that server works with stateless RequestDirector approach."""
    
    # Test server initialization is fast
    start_time = time.time()
    server = FastMCPOpenAPI(spec=valid_spec, client=client)
    init_time = time.time() - start_time
    assert init_time < 0.01  # Should be very fast
    
    # Verify RequestDirector functionality
    assert hasattr(server, '_director')
    assert hasattr(server, '_spec')
```

--------------------------------

### Use Built-in Timing Middleware

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

This snippet shows how to integrate FastMCP's built-in timing middleware into a server. It demonstrates adding both `TimingMiddleware` for basic request timing and `DetailedTimingMiddleware` for granular, per-operation timing.

```python
from fastmcp import FastMCP
from fastmcp.server.middleware.timing import (
    TimingMiddleware, 
    DetailedTimingMiddleware
)

mcp = FastMCP("MyServer")

# Basic timing for all requests
mcp.add_middleware(TimingMiddleware())

# Detailed per-operation timing (tools, resources, prompts)
mcp.add_middleware(DetailedTimingMiddleware())
```

--------------------------------

### Configure Authentication Headers for FastMCP Server from FastAPI (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/fastapi.mdx

This snippet shows how to integrate authentication into a FastAPI application and configure the FastMCP client to include the necessary authentication headers. It uses `httpx_client_kwargs` to pass a `headers` dictionary with an `Authorization` token when creating the FastMCP server, allowing it to interact with protected FastAPI endpoints.

```python
# Assumes the FastAPI app from above is already defined
from fastmcp import FastMCP

# Add authentication to your FastAPI app
from fastapi import Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != "secret-token":
        raise HTTPException(status_code=401, detail="Invalid authentication")
    return credentials.credentials

# Add a protected endpoint
@app.get("/admin/stats", dependencies=[Depends(verify_token)])
def get_admin_stats():
    return {
        "total_products": len(products_db),
        "categories": list(set(p.category for p in products_db.values()))
    }

# Create MCP server with authentication headers
mcp = FastMCP.from_fastapi(
    app=app,
    httpx_client_kwargs={
        "headers": {
            "Authorization": "Bearer secret-token",
        }
    }
)
```

--------------------------------

### Add Icons to FastMCP Server

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/icons.mdx

Shows how to associate icons with a FastMCP server, along with a website URL. These icons are displayed in MCP client applications to help users identify the server.

```python
from fastmcp import FastMCP
from mcp.types import Icon

mcp = FastMCP(
    name="WeatherService",
    website_url="https://weather.example.com",
    icons=[
        Icon(
            src="https://weather.example.com/icon-48.png",
            mimeType="image/png",
            sizes=["48x48"]
        ),
        Icon(
            src="https://weather.example.com/icon-96.png",
            mimeType="image/png",
            sizes=["96x96"]
        ),
    ]
)
```

--------------------------------

### Initialize FastMCP Server with Descope Authentication (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/descope.mdx

This Python code snippet demonstrates how to initialize a FastMCP server. When the required Descope authentication environment variables are properly set, the FastMCP library automatically detects and configures the authentication provider, streamlining the server setup process without explicit configuration in code.

```Python
from fastmcp import FastMCP

# Authentication is automatically configured from environment
mcp = FastMCP(name="My Descope Protected Server")
```

--------------------------------

### Example Output: FastMCP Generated Server Configuration

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/mcp-json-configuration.mdx

This JSON shows the typical output structure when using `fastmcp install mcp-json`. It provides a single server configuration with a default name, defining the command (`uv run` with `fastmcp`) and arguments, including the absolute path to the server script.

```json
{
  "My Server": {
    "command": "uv",
    "args": [
      "run",
      "--with",
      "fastmcp", 
      "fastmcp",
      "run",
      "/absolute/path/to/server.py"
    ]
  }
}
```

--------------------------------

### FastMCP ToolResult Content Field Examples (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/tools.mdx

Provides various examples for defining the `content` field within a `ToolResult` object, which represents the traditional MCP content blocks displayed to users. It showcases assigning a simple string, which FastMCP automatically converts to `TextContent`, and providing a list of diverse content blocks, such as `TextContent` and `ImageContent`, for richer output. At least one of `content` or `structured_content` must be supplied.

```python
# Simple string
ToolResult(content="Hello, world!")
```

```python
# List of content blocks
ToolResult(content=[
    TextContent(type="text", text="Result: 42"),
    ImageContent(type="image", data="base64...", mimeType="image/png")
])
```

--------------------------------

### Define a function-based MCP message handler in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/messages.mdx

This snippet demonstrates how to create a simple asynchronous function to act as a universal message handler for FastMCP clients. It processes all incoming messages, identifies their type (e.g., method), and can trigger specific actions based on notification types like 'notifications/tools/list_changed'. This approach is suitable for general message monitoring and initial setup.

```python
from fastmcp import Client

async def message_handler(message):
    """Handle all MCP messages from the server."""
    if hasattr(message, 'root'):
        method = message.root.method
        print(f"Received: {method}")
        
        # Handle specific notifications
        if method == "notifications/tools/list_changed":
            print("Tools have changed - might want to refresh tool cache")
        elif method == "notifications/resources/list_changed":
            print("Resources have changed")

client = Client(
    "my_mcp_server.py",
    message_handler=message_handler,
)
```

--------------------------------

### Create a FastMCP Proxy Server (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/server.mdx

Illustrates how to set up a FastMCP server to act as a proxy for any existing MCP server (local or remote) using `FastMCP.as_proxy`. This functionality is useful for bridging different transports or adding a frontend layer to an existing service, such as exposing a remote SSE server locally.

```python
from fastmcp import FastMCP, Client

backend = Client("http://example.com/mcp/sse")
proxy = FastMCP.as_proxy(backend, name="ProxyServer")
# Now use the proxy like any FastMCP server
```

--------------------------------

### Get a Specific FastMCP Server Resource by Key in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

This method retrieves a single resource from the FastMCP server using its unique key. It takes a string `key` as an argument and returns the corresponding `Resource` object.

```python
get_resource(self, key: str) -> Resource
```

--------------------------------

### FastMCP Proxy Server Implementation

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-proxy.mdx

The `FastMCPProxy` class enables an MCP server to act as a proxy to a remote MCP-compliant server. It utilizes specialized managers and a client factory to handle incoming requests efficiently.

```python
class FastMCPProxy:
    """A FastMCP server that acts as a proxy to a remote MCP-compliant server.
    It uses specialized managers that fulfill requests via a client factory."""
    pass
```

--------------------------------

### POST /server/run/sse

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

Initiates the FastMCP server using Server-Sent Events (SSE) transport.

```APIDOC
## POST /server/run/sse

### Description
Initiates the FastMCP server using SSE transport.

### Method
POST

### Endpoint
/server/run/sse

### Parameters
- **host** (str) - Optional - Host address to bind to
- **port** (int) - Optional - Port to bind to
- **log_level** (str) - Optional - Log level for the server
- **path** (str) - Optional - Path for the endpoint
- **uvicorn_config** (dict[str, Any]) - Optional - Additional configuration for the Uvicorn server

### Response
#### Success Response (200)
- **status** (None) - Server started successfully, returns no content.
```

--------------------------------

### Create a Parameterized FastMCP Resource Template in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/server.mdx

This example shows how to define a resource template that accepts parameters from its URI. The `{user_id}` in the URI is automatically extracted and passed as an argument to the `get_user_profile` function, allowing dynamic data retrieval.

```python
@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: int) -> dict:
    """Retrieves a user's profile by ID."""
    # The {user_id} in the URI is extracted and passed to this function
    return {"id": user_id, "name": f"User {user_id}", "status": "active"}
```

--------------------------------

### Inspect Generic FastMCP Instance (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-utilities-inspect.mdx

This Python function automatically detects and extracts information from either a FastMCP v1.x or v2.x instance. It takes a `FastMCP[Any] | FastMCP1x` object and provides a `FastMCPInfo` dataclass in return, simplifying instance inspection.

```python
inspect_fastmcp(mcp: FastMCP[Any] | FastMCP1x) -> FastMCPInfo
```

--------------------------------

### Create Reusable Prompt Template with FastMCP in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/tutorials/mcp.mdx

Demonstrates how to define a parameterized prompt using the @mcp.prompt decorator in FastMCP. The prompt template accepts a text parameter and returns formatted instructions for the LLM to summarize the provided text. This allows clients to request consistent, structured prompts for specific tasks.

```python
from fastmcp import FastMCP

mcp = FastMCP()

@mcp.prompt
def summarize_text(text_to_summarize: str) -> str:
    """Creates a prompt asking the LLM to summarize a piece of text."""
    return f"""
        Please provide a concise, one-paragraph summary of the following text:
        
        {text_to_summarize}
        """
```

--------------------------------

### Implement Simple Rate Limiting Middleware in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

This Python code defines a basic rate-limiting middleware for FastMCP. It tracks client requests using a defaultdict and limits them based on a configurable requests_per_minute threshold. It raises an McpError if the limit is exceeded.

```python
import time
from collections import defaultdict
from fastmcp.server.middleware import Middleware, MiddlewareContext
from mcp import McpError
from mcp.types import ErrorData

class SimpleRateLimitMiddleware(Middleware):
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.client_requests = defaultdict(list)
    
    async def on_request(self, context: MiddlewareContext, call_next):
        current_time = time.time()
        client_id = "default"  # In practice, extract from headers or context
        
        # Clean old requests and check limit
        cutoff_time = current_time - 60
        self.client_requests[client_id] = [
            req_time for req_time in self.client_requests[client_id]
            if req_time > cutoff_time
        ]
        
        if len(self.client_requests[client_id]) >= self.requests_per_minute:
            raise McpError(ErrorData(code=-32000, message="Rate limit exceeded"))
        
        self.client_requests[client_id].append(current_time)
        return await call_next(context)
```

--------------------------------

### Mount FastMCP Server to FastAPI Application (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/fastapi.mdx

This code demonstrates how to mount a FastMCP server as an ASGI application within an existing FastAPI framework. It involves creating a FastMCP instance, defining a tool, generating an ASGI app from the MCP server, and finally mounting it to a FastAPI application, ensuring the MCP app's lifespan is correctly passed to FastAPI.

```python
from fastmcp import FastMCP
from fastapi import FastAPI

# Create MCP server
mcp = FastMCP("Analytics Tools")

@mcp.tool
def analyze_pricing(category: str) -> dict:
    """Analyze pricing for a category."""
    products = [p for p in products_db.values() if p.category == category]
    if not products:
        return {"error": f"No products in {category}"}
    
    prices = [p.price for p in products]
    return {
        "category": category,
        "avg_price": round(sum(prices) / len(prices), 2),
        "min": min(prices),
        "max": max(prices),
    }

# Create ASGI app from MCP server
mcp_app = mcp.http_app(path='/mcp')

# Key: Pass lifespan to FastAPI
app = FastAPI(title="E-commerce API", lifespan=mcp_app.lifespan)

# Mount the MCP server
app.mount("/analytics", mcp_app)

# Now: API at /products/*, MCP at /analytics/mcp/
```

--------------------------------

### Manage FastMCP Client Connection Lifecycle in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/client.mdx

Demonstrates how to establish and close an asynchronous connection to a FastMCP server using a context manager. The connection is automatically opened upon entering and closed upon exiting the `async with` block, allowing multiple operations within the session.

```python
async def example():
    client = Client("my_mcp_server.py")
    
    # Connection established here
    async with client:
        print(f"Connected: {client.is_connected()}")
        
        # Make multiple calls within the same session
        tools = await client.list_tools()
        result = await client.call_tool("greet", {"name": "World"})
        
    # Connection closed automatically here
    print(f"Connected: {client.is_connected()}")
```

--------------------------------

### Run `fastmcp dev` with dependencies from a requirements file

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

Install dependencies for the `fastmcp dev` server by providing a `requirements.txt` file. This command ensures all specified packages are available in the testing environment.

```bash
fastmcp dev server.py --with-requirements requirements.txt
```

--------------------------------

### Initialize FastMCP Server with Auth0 Authentication in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/auth0.mdx

This Python code shows how to initialize a `FastMCP` application. It automatically picks up Auth0 authentication configuration from environment variables, simplifying secure server setup. A sample asynchronous tool `search_logs` is included to demonstrate tool registration within the `FastMCP` instance.

```python
from fastmcp import FastMCP

# Authentication is automatically configured from environment
mcp = FastMCP(name="Auth0 Secured App")

@mcp.tool
async def search_logs() -> list[str]:
    """Search the service logs."""
    # Your tool implementation here
    pass
```

--------------------------------

### Install a FastMCP Server in Claude Code using the CLI

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/claude-code.mdx

This command demonstrates the simplest way to install a FastMCP server defined in `server.py` into Claude Code. The `fastmcp install claude-code` command automatically handles configuration and dependency management, registering the server with Claude Code's MCP management system.

```bash
fastmcp install claude-code server.py
```

--------------------------------

### Install FastMCP Server Globally in Cursor (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/cursor.mdx

This command installs a FastMCP server into Cursor globally, handling configuration and dependency management automatically. Cursor will open and prompt for installation confirmation.

```bash
fastmcp install cursor server.py
```

--------------------------------

### Configure FastMCP Server Tag-Based Filtering in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/server.mdx

This snippet shows how to configure tag-based filtering when initializing a FastMCP server instance. You can specify `include_tags` to only expose components with matching tags, `exclude_tags` to hide components, or combine both for fine-grained control.

```python
# Only expose components tagged with "public"
mcp = FastMCP(include_tags={"public"})

# Hide components tagged as "internal" or "deprecated"  
mcp = FastMCP(exclude_tags={"internal", "deprecated"})

# Combine both: show admin tools but hide deprecated ones
mcp = FastMCP(include_tags={"admin"}, exclude_tags={"deprecated"})
```

--------------------------------

### Preview FastMCP Documentation Locally

Source: https://github.com/jlowin/fastmcp/blob/main/docs/development/contributing.mdx

Generates and serves the FastMCP documentation locally, allowing developers to review changes before publishing. This command ensures that all new features are properly documented and appear in the navigation.

```bash
just docs
```

--------------------------------

### Install and Setup FastMCP Server with Permit.io Middleware

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/permit.mdx

Install the permit-fastmcp package and create a FastMCP server instance, adding the PermitMcpMiddleware for authorization. This middleware requires the Permit PDP URL and an API key for authentication. The server exposes `greet` and `add` tools.

```python
from fastmcp import FastMCP
from permit_fastmcp.middleware.middleware import PermitMcpMiddleware

mcp = FastMCP("Secure FastMCP Server 🔒")

@mcp.tool
def greet(name: str) -> str:
    """Greet a user by name"""
    return f"Hello, {name}!"

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Add Permit.io authorization middleware
mcp.add_middleware(PermitMcpMiddleware(
    permit_pdp_url="http://localhost:7766",
    permit_api_key="your-permit-api-key"
))

if __name__ == "__main__":
    mcp.run(transport="http")
```

--------------------------------

### Start FastMCP Server in Shell

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/scalekit.mdx

Provides the shell command to start the FastMCP server using `uv run`. This command is typically executed in the directory containing your `server.py` file to launch the application.

```sh
uv run python server.py
```

--------------------------------

### Enable Basic Response Caching Middleware in FastMCP

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

Illustrates the basic setup for `ResponseCachingMiddleware` in FastMCP. By default, it caches call/list tools, resources, and prompts to an in-memory cache with TTL-based expiration, improving performance and reducing server load.

```python
from fastmcp.server.middleware.caching import ResponseCachingMiddleware

mcp.add_middleware(ResponseCachingMiddleware())
```

--------------------------------

### Install FastMCP Server with a `requirements.txt` File

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/gemini-cli.mdx

This command facilitates the installation of a FastMCP server while automatically managing its dependencies listed in a `requirements.txt` file, using the `--with-requirements` flag.

```bash
fastmcp install gemini-cli server.py --with-requirements requirements.txt
```

--------------------------------

### Understand FastMCP Middleware Hook Structure in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

This Python example outlines the standard structure of any FastMCP middleware hook, using the `on_message` hook as an illustration. It highlights the four key steps: pre-processing the request, continuing the middleware chain with `call_next`, post-processing the result, and finally returning the (potentially modified) result.

```python
async def on_message(self, context: MiddlewareContext, call_next):
    # 1. Pre-processing: Inspect and optionally modify the request
    print(f"Processing {context.method}")
    
    # 2. Chain continuation: Call the next middleware/handler
    result = await call_next(context)
    
    # 3. Post-processing: Inspect and optionally modify the response
    print(f"Completed {context.method}")
    
    # 4. Return the result (potentially modified)
    return result
```

--------------------------------

### Add Simple String Descriptions to FastMCP Parameters using Annotated

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/tools.mdx

To provide basic parameter metadata, FastMCP supports a concise shorthand using `typing.Annotated`. By passing a single string as the second argument to `Annotated`, you can define a description for the parameter, which is equivalent to using `Field(description=...)` but more compact for simple cases. This metadata can be used by LLMs to better understand parameter expectations.

```python
from typing import Annotated

@mcp.tool
def process_image(
    image_url: Annotated[str, "URL of the image to process"],
    resize: Annotated[bool, "Whether to resize the image"] = False,
    width: Annotated[int, "Target width in pixels"] = 800,
    format: Annotated[str, "Output image format"] = "jpeg"
) -> dict:
    """Process an image with optional resizing."""
    # Implementation...
```

--------------------------------

### Customize FastMCP Components with mcp_component_fn

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openapi.mdx

To modify MCP components after their creation, provide a `mcp_component_fn` when initializing the FastMCP server. This function is called on each component and allows in-place modifications, such as adding custom tags or altering descriptions based on component type. The function is expected to modify the component directly, and its return value is ignored.

```python
from fastmcp.server.openapi import (
    HTTPRoute, 
    OpenAPITool, 
    OpenAPIResource, 
    OpenAPIResourceTemplate,
)

# If using experimental parser, import from experimental module:
# from fastmcp.experimental.server.openapi import (
#     HTTPRoute,
#     OpenAPITool,
#     OpenAPIResource,
#     OpenAPIResourceTemplate,
# )

def customize_components(
    route: HTTPRoute, 
    component: OpenAPITool | OpenAPIResource | OpenAPIResourceTemplate,
) -> None:
    # Add custom tags to all components
    component.tags.add("openapi")
    
    # Customize based on component type
    if isinstance(component, OpenAPITool):
        component.description = f"🔧 {component.description} (via API)"
    
    if isinstance(component, OpenAPIResource):
        component.description = f"📊 {component.description}"
        component.tags.add("data")

mcp = FastMCP.from_openapi(
    openapi_spec=spec,
    client=client,
    mcp_component_fn=customize_components,
)
```

--------------------------------

### Display FastMCP Version Information with Python `version` function

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-cli-cli.mdx

This function displays version information and platform details for the FastMCP application. It provides insights into the current software build and environment.

```python
version()
```

--------------------------------

### Utilize FastMCP Context in a Tool Function in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-context.mdx

This Python example demonstrates how to integrate the `Context` object into a `fastmcp` tool function by type-hinting it as a parameter. It showcases various `Context` functionalities including logging messages (info, debug, warning, error), reporting progress, accessing resources, retrieving request information (ID, client ID), and managing request-scoped state.

```python
@server.tool
async def my_tool(x: int, ctx: Context) -> str:
    # Log messages to the client
    await ctx.info(f"Processing {x}")
    await ctx.debug("Debug info")
    await ctx.warning("Warning message")
    await ctx.error("Error message")

    # Report progress
    await ctx.report_progress(50, 100, "Processing")

    # Access resources
    data = await ctx.read_resource("resource://data")

    # Get request info
    request_id = ctx.request_id
    client_id = ctx.client_id

    # Manage state across the request
    ctx.set_state("key", "value")
    value = ctx.get_state("key")

    return str(x)
```

--------------------------------

### Manage FastMCP Server Resources with Pytest Fixtures in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/development/tests.mdx

Illustrates the use of Pytest fixtures to provide reusable FastMCP server instances for tests. It defines a `weather_server` fixture that sets up a FastMCP server with a `get_temperature` tool, which is then used by an asynchronous test to call the tool and assert its response. It also highlights the recommendation against opening FastMCP clients within fixtures.

```python
import pytest
from fastmcp import FastMCP, Client

@pytest.fixture
def weather_server():
    server = FastMCP("WeatherServer")
    
    @server.tool
    def get_temperature(city: str) -> dict:
        temps = {"NYC": 72, "LA": 85, "Chicago": 68}
        return {"city": city, "temp": temps.get(city, 70)}
    
    return server

async def test_temperature_tool(weather_server):
    async with Client(weather_server) as client:
        result = await client.call_tool("get_temperature", {"city": "LA"})
        assert result.data == {"city": "LA", "temp": 85}
```

--------------------------------

### Accessing Registered Prompts with FastMCP Context (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/context.mdx

Demonstrates how to list and retrieve prompts registered with your FastMCP server, allowing tools and middleware to discover and use available prompts programmatically. The `ctx.list_prompts()` method fetches all prompts, and `ctx.get_prompt()` retrieves a specific one, optionally with arguments. This feature requires FastMCP version 2.13.0 or higher.

```python
# List available prompts
prompts = await ctx.list_prompts()

# Get a specific prompt with arguments
result = await ctx.get_prompt("analyze_data", {"dataset": "users"})
messages = result.messages
```

--------------------------------

### Register a Python function as a FastMCP tool

Source: https://github.com/jlowin/fastmcp/blob/main/docs/getting-started/quickstart.mdx

Decorate a Python function with `@mcp.tool` to expose it as a callable tool on the FastMCP server. This allows external clients to invoke the function by name, passing arguments as required.

```python
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

--------------------------------

### Install FastMCP Server for Multiple Clients (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

Demonstrates the basic `fastmcp install` command to deploy a local FastMCP server, such as `server.py`, into different client applications like Claude Code, Claude Desktop, and Cursor. It also shows how to generate standard MCP JSON configuration for manual integration. This command relies on the server's default entrypoint detection.

```bash
fastmcp install claude-code server.py
fastmcp install claude-desktop server.py
fastmcp install cursor server.py
fastmcp install mcp-json server.py
```

--------------------------------

### Python prompt decorator for FastMCP server

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

Decorator method that registers a function or prompt by name. Returns a FunctionPrompt instance that wraps the provided function, enabling prompt-based functionality within the FastMCP framework.

```python
prompt(self, name_or_fn: AnyFunction) -> FunctionPrompt
```

--------------------------------

### FastMCP Tool with Dataclass Return Type Annotation

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/tools.mdx

This example demonstrates a FastMCP tool that returns a `dataclass` instance. FastMCP leverages the dataclass definition to automatically generate a detailed JSON output schema and populates both `content` and `structuredContent` in the MCP result, providing machine-readable data.

```python
from dataclasses import dataclass
from fastmcp import FastMCP

mcp = FastMCP()

@dataclass
class Person:
    name: str
    age: int
    email: str

@mcp.tool
def get_user_profile(user_id: str) -> Person:
    """Get a user's profile information."""
    return Person(
        name="Alice",
        age=30,
        email="alice@example.com",
    )
```

```json
{
  "properties": {
    "name": {"title": "Name", "type": "string"},
    "age": {"title": "Age", "type": "integer"},
    "email": {"title": "Email", "type": "string"}
  },
  "required": ["name", "age", "email"],
  "title": "Person",
  "type": "object"
}
```

```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"name\": \"Alice\", \"age\": 30, \"email\": \"alice@example.com\"}"
    }
  ],
  "structuredContent": {
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com"
  }
}
```

--------------------------------

### Implement Read-Only Tool with Skip Confirmation in Python FastMCP

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/chatgpt.mdx

Shows how to configure FastMCP tools with annotations to control ChatGPT confirmation prompts. Tools marked with readOnlyHint annotation skip user confirmation for non-destructive operations, while tools without annotations may require user approval. This improves user experience for safe, read-only operations.

```python
@mcp.tool(annotations={"readOnlyHint": True})
def get_status() -> str:
    """Check system status."""
    return "All systems operational"

@mcp.tool()  # No annotation - ChatGPT may ask for confirmation
def delete_item(id: str) -> str:
    """Delete an item."""
    return f"Deleted {id}"
```

--------------------------------

### Initialize FastMCP for CLI-Only Execution (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/running-server.mdx

This Python snippet presents the minimal setup for a FastMCP server intended for execution solely through the FastMCP CLI. By omitting the `if __name__ == "__main__":` block, the CLI automatically discovers the `FastMCP` instance and manages its startup. This pattern simplifies server deployment for CLI-driven workflows.

```python
from fastmcp import FastMCP

mcp = FastMCP("MyServer")
```

--------------------------------

### Get FastMCP Server Version in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

This method retrieves the current version string of the FastMCP server. It takes no arguments and returns a string representing the server's version or None if not available.

```python
version(self) -> str | None
```

--------------------------------

### Add Single Middleware to FastMCP Server

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

This snippet demonstrates how to add a single middleware to a FastMCP server. It initializes the server and then adds a LoggingMiddleware instance. This middleware will process requests flowing through the server.

```python
from fastmcp import FastMCP
from fastmcp.server.middleware.logging import LoggingMiddleware

mcp = FastMCP("MyServer")
mcp.add_middleware(LoggingMiddleware())
```

--------------------------------

### Cloning FastMCP Repository

Source: https://github.com/jlowin/fastmcp/blob/main/README.md

This bash command clones the FastMCP project repository from GitHub to the local machine. It's the first step in setting up the development environment for contributing to the project.

```bash
git clone https://github.com/jlowin/fastmcp.git 
cd fastmcp
```

--------------------------------

### Enable FastMCP Tool using cURL

Source: https://github.com/jlowin/fastmcp/blob/main/src/fastmcp/contrib/component_manager/README.md

This cURL command demonstrates how to enable a specific tool ('example_tool') on a running FastMCP server. It includes an Authorization header with a Bearer token for secured access and sets the Content-Type to application/json.

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  http://localhost:8001/tools/example_tool/enable
```

--------------------------------

### Run FastMCP Server with HTTP Transport (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/running-server.mdx

This snippet demonstrates how to configure and run a FastMCP server using the Streamable HTTP transport. By specifying `transport="http"` and providing `host` and `port`, the server becomes a web service accessible via a URL, capable of handling multiple concurrent clients. This is the recommended choice for network-based deployments.

```python
from fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.tool
def hello(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    # Start an HTTP server on port 8000
    mcp.run(transport="http", host="127.0.0.1", port=8000)
```

--------------------------------

### Configure Auth0 Credentials for FastMCP Server via Environment Variables

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/auth0.mdx

This snippet defines the necessary environment variables to integrate Auth0 authentication with a `FastMCP` server. It sets the Auth0 domain, client ID, client secret, audience, base URL, and required scopes, which `FastMCP` automatically uses for secure communication.

```bash
FASTMCP_SERVER_AUTH_AUTH0_CONFIG_URL=https://.../.well-known/openid-configuration
FASTMCP_SERVER_AUTH_AUTH0_CLIENT_ID=tv2ObNgaZAWWhhycr7Bz1LU2mxlnsmsB
FASTMCP_SERVER_AUTH_AUTH0_CLIENT_SECRET=vPYqbjemq...
FASTMCP_SERVER_AUTH_AUTH0_AUDIENCE=https://...
FASTMCP_SERVER_AUTH_AUTH0_BASE_URL=https://your-server.com
FASTMCP_SERVER_AUTH_AUTH0_REQUIRED_SCOPES=openid,email
```

--------------------------------

### Add Resource Annotations in FastMCP (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/resources.mdx

Illustrates how to add specialized metadata (annotations) to FastMCP resources using the `@mcp.resource` decorator's `annotations` parameter. These advisory hints, like `readOnlyHint` and `idempotentHint`, help client applications optimize caching, access patterns, and present appropriate UI without consuming LLM token context.

```python
@mcp.resource(
    "data://config",
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True
    }
)
def get_config() -> dict:
    """Get application configuration."""
    return {"version": "1.0", "debug": False}
```

--------------------------------

### Get Prompt (MCP)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-client.mdx

Sends a prompts/get request using the MCP protocol and returns the complete MCP protocol result, including prompt messages and metadata.

```APIDOC
## GET /prompts/get

### Description
Sends a prompts/get request using the MCP protocol and returns the complete MCP protocol result, including prompt messages and metadata.

### Method
GET

### Endpoint
/prompts/get?name={name}&arguments={arguments}

### Parameters
#### Query Parameters
- **name** (string) - Required - The name of the prompt to retrieve.
- **arguments** (dict[str, Any] | None) - Optional - Arguments to pass to the prompt. Defaults to None.

### Request Example
None

### Response
#### Success Response (200)
- **GetPromptResult** (mcp.types.GetPromptResult) - The complete response object from the protocol, containing the prompt messages and any additional metadata.

#### Response Example
```json
{
  "messages": [
    {
      "role": "user",
      "content": "string"
    }
  ],
  "metadata": {}
}
```

#### Error Handling
- `RuntimeError`: If called while the client is not connected.
```

--------------------------------

### Create FastMCP Proxy with Automatic Feature Forwarding (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/proxy.mdx

This code demonstrates how `ProxyClient` automatically forwards advanced MCP protocol features like sampling, logging, elicitation, and progress notifications between the backend server and the client. It ensures full MCP compatibility without explicit configuration.

```python
from fastmcp.server.proxy import ProxyClient

# ProxyClient automatically handles all these features
backend = ProxyClient("advanced_backend.py")
proxy = FastMCP.as_proxy(backend)

# When the backend server:
# - Requests LLM sampling -> forwarded to your client
# - Logs messages -> appear in your client
# - Reports progress -> shown in your client
# - Needs user input -> prompts your client
```

--------------------------------

### Two-Tier Refresh Token Exchange in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-auth-oauth_proxy.mdx

Exchanges FastMCP refresh token for new access token using two-tier refresh pattern. Verifies FastMCP token, retrieves and refreshes upstream token with provider, updates stored tokens, and issues new FastMCP access token while maintaining the same refresh token unless upstream rotates.

```python
def exchange_refresh_token(self, client: OAuthClientInformationFull, refresh_token: RefreshToken, scopes: list[str]) -> OAuthToken:
    """Exchange FastMCP refresh token for new FastMCP access token.
    
    Implements two-tier refresh:
    1. Verify FastMCP refresh token
    2. Look up upstream token via JTI mapping
    3. Refresh upstream token with upstream provider
    4. Update stored upstream token
    5. Issue new FastMCP access token
    6. Keep same FastMCP refresh token (unless upstream rotates)
    """
```

--------------------------------

### Install pytest-asyncio for FastMCP Testing

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/testing.mdx

Install pytest-asyncio as a development dependency to enable async test functions and fixtures. This package is required for testing FastMCP servers that use async operations.

```bash
pip install pytest-asyncio
```

--------------------------------

### Running a FastMCP Server with HTTP Transport

Source: https://github.com/jlowin/fastmcp/blob/main/README.md

This Python snippet demonstrates how to run a FastMCP server using the HTTP transport protocol. It specifies the host and port for the server to listen on, making it suitable for web deployments. This method is recommended for production environments.

```python
mcp.run(transport="http", host="0.0.0.0", port=8000)
```

--------------------------------

### Add Python Dependencies from Requirements File to FastMCP Server (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/cursor.mdx

This command shows how to install all Python dependencies listed in a `requirements.txt` file for your FastMCP server using the `--with-requirements` flag.

```bash
fastmcp install cursor server.py --with-requirements requirements.txt
```

--------------------------------

### Create MCP Tool for Weather Retrieval using FastMCP in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/tutorials/mcp.mdx

Demonstrates creating an MCP tool by decorating a Python function with @mcp.tool. This tool allows LLMs to request weather information for a specific city. The function signature and docstring define the tool's interface, and the return value provides structured data back to the client.

```python
from fastmcp import FastMCP

mcp = FastMCP()

# This function is now an MCP tool named "get_weather"
@mcp.tool
def get_weather(city: str) -> dict:
    """Gets the current weather for a specific city."""
    # In a real app, this would call a weather API
    return {"city": city, "temperature": "72F", "forecast": "Sunny"}
```

--------------------------------

### Configure Static Roots in FastMCP Client (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/roots.mdx

Sets static roots for a FastMCP client by providing a list of directory paths during client initialization. This is useful for clients with predefined resource access.

```python
from fastmcp import Client

client = Client(
    "my_mcp_server.py", 
    roots=["/path/to/root1", "/path/to/root2"]
)
```

--------------------------------

### Define Dynamic FastMCP Resources with Python `@mcp.resource` Decorator

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/resources.mdx

This Python example illustrates how to create dynamic FastMCP resources using the `@mcp.resource` decorator. It showcases defining a resource that returns a plain string and another that returns a dictionary, which FastMCP automatically serializes to JSON for clients. Resources are lazily loaded, meaning their functions execute only when their unique URIs are explicitly requested.

```python
import json
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")

# Basic dynamic resource returning a string
@mcp.resource("resource://greeting")
def get_greeting() -> str:
    """Provides a simple greeting message."""
    return "Hello from FastMCP Resources!"

# Resource returning JSON data (dict is auto-serialized)
@mcp.resource("data://config")
def get_config() -> dict:
    """Provides application configuration as JSON."""
    return {
        "theme": "dark",
        "version": "1.2.0",
        "features": ["tools", "resources"]
    }
```

--------------------------------

### Configure Advanced Error Handling and Retry Middleware in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

These Python examples show how to configure FastMCP's advanced error handling middleware. The first configures comprehensive logging, error transformation, and a custom error callback. The second sets up automatic retries with exponential backoff for specified exceptions.

```python
from fastmcp.server.middleware.error_handling import (
    ErrorHandlingMiddleware, 
    RetryMiddleware
)

# Comprehensive error logging and transformation
mcp.add_middleware(ErrorHandlingMiddleware(
    include_traceback=True,
    transform_errors=True,
    error_callback=my_error_callback
))

# Automatic retry with exponential backoff
mcp.add_middleware(RetryMiddleware(
    max_retries=3,
    retry_exceptions=(ConnectionError, TimeoutError)
))
```

--------------------------------

### Complete FastMCP Starlette application example in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/http.mdx

This comprehensive Python example demonstrates a complete FastMCP application integrated with Starlette, including OAuth authentication via GitHub. It covers defining routing constants, configuring the OAuth provider, creating the MCP server with a tool, generating HTTP apps, retrieving discovery routes, and assembling the final Starlette application for production deployment with `uvicorn`.

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.github import GitHubProvider
from starlette.applications import Starlette
from starlette.routing import Mount
import uvicorn

# Define routing structure
ROOT_URL = "http://localhost:8000"
MOUNT_PREFIX = "/api"
MCP_PATH = "/mcp"

# Create OAuth provider
auth = GitHubProvider(
    client_id="your-client-id",
    client_secret="your-client-secret",
    issuer_url=ROOT_URL,
    base_url=f"{ROOT_URL}{MOUNT_PREFIX}",
)

# Create MCP server
mcp = FastMCP("Protected Server", auth=auth)

@mcp.tool
def analyze(data: str) -> dict:
    return {"result": f"Analyzed: {data}"}

# Create MCP app
mcp_app = mcp.http_app(path=MCP_PATH)

# Get discovery routes for root level
well_known_routes = auth.get_well_known_routes(mcp_path=MCP_PATH)

# Assemble the application
app = Starlette(
    routes=[
        *well_known_routes,
        Mount(MOUNT_PREFIX, app=mcp_app),
    ],
    lifespan=mcp_app.lifespan,
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

--------------------------------

### Configure Dynamic Roots Callback in FastMCP Client (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/roots.mdx

Configures a FastMCP client to use a dynamic roots callback function. This function is invoked by the server, potentially per request, to determine the roots. It allows for context-aware root determination.

```python
from fastmcp import Client
from fastmcp.client.roots import RequestContext

async def roots_callback(context: RequestContext) -> list[str]:
    print(f"Server requested roots (Request ID: {context.request_id})")
    return ["/path/to/root1", "/path/to/root2"]

client = Client(
    "my_mcp_server.py", 
    roots=roots_callback
)
```

--------------------------------

### Implement Basic MCP Middleware with Raw __call__ Method in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

Demonstrates the fundamental way to create MCP middleware by overriding the __call__ method on the Middleware base class. This implementation receives all JSON-RPC messages regardless of type, allowing complete control over message processing. The middleware can inspect context, execute the next handler in the chain, and modify responses.

```python
from fastmcp.server.middleware import Middleware, MiddlewareContext

class RawMiddleware(Middleware):
    async def __call__(self, context: MiddlewareContext, call_next):
        # This method receives ALL messages regardless of type
        print(f"Raw middleware processing: {context.method}")
        result = await call_next(context)
        print(f"Raw middleware completed: {context.method}")
        return result
```

--------------------------------

### Display FastMCP CLI Help

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

This command shows the top-level help message for the FastMCP command-line interface, listing all available commands and their basic usage. It helps users understand the primary functionalities of the CLI.

```bash
fastmcp --help
```

--------------------------------

### Connecting to a Protected Server with OAuth

Source: https://github.com/jlowin/fastmcp/blob/main/README.md

This Python snippet shows how a client can connect to a protected FastMCP server using OAuth. It utilizes an asynchronous context manager for the Client, automatically handling the browser-based OAuth flow when 'auth="oauth"' is provided. The result of calling a protected tool is then retrieved.

```python
async with Client("https://protected-server.com/mcp", auth="oauth") as client:
    # Automatic browser-based OAuth flow
    result = await client.call_tool("protected_tool")
```

--------------------------------

### Generate LLM-Friendly API from Existing FastAPI App with FastMCP (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/fastapi.mdx

This example illustrates how to create an LLM-optimized interface alongside a regular FastAPI API using FastMCP. It involves generating an MCP server directly from an existing FastAPI app, then combining the routes and lifespan of both the original API and the new MCP application into a single, unified FastAPI instance for deployment.

```python
# Assumes the FastAPI app from above is already defined
from fastmcp import FastMCP
from fastapi import FastAPI

# 1. Generate MCP server from your API
mcp = FastMCP.from_fastapi(app=app, name="E-commerce MCP")

# 2. Create the MCP's ASGI app
mcp_app = mcp.http_app(path='/mcp')

# 3. Create a new FastAPI app that combines both sets of routes
combined_app = FastAPI(
    title="E-commerce API with MCP",
    routes=[
        *mcp_app.routes,  # MCP routes
        *app.routes,      # Original API routes
    ],
    lifespan=mcp_app.lifespan,
)

# Now you have:
# - Regular API: http://localhost:8000/products
# - LLM-friendly MCP: http://localhost:8000/mcp
# Both served from the same FastAPI application!
```

--------------------------------

### Run All Pytest Tests in FastMCP

Source: https://github.com/jlowin/fastmcp/blob/main/docs/development/contributing.mdx

Executes the entire suite of Pytest tests for the FastMCP project. It is crucial to run all tests locally before submitting a Pull Request to prevent regressions and ensure code quality.

```bash
uv run pytest
```

--------------------------------

### FastMCP Tool for Primitive Return Without Annotation

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/tools.mdx

This Python FastMCP tool calculates a sum but lacks a return type annotation. Consequently, FastMCP only produces traditional `content` and does not generate `structuredContent` for primitive types in this scenario.

```python
@mcp.tool
def calculate_sum(a: int, b: int):
    """Calculate sum without return annotation."""
    return a + b  # Returns 8
```

```json
{
  "content": [
    {
      "type": "text",
      "text": "8"
    }
  ]
}
```

--------------------------------

### Install FastMCP using uv or pip

Source: https://github.com/jlowin/fastmcp/blob/main/docs/getting-started/installation.mdx

Installs the FastMCP package using either the uv package manager or pip. Users can add it as a project dependency or install it directly. uv is recommended for managing Python environments and dependencies.

```bash
uv add fastmcp
```

```bash
uv pip install fastmcp
```

```bash
pip install fastmcp
```

--------------------------------

### Eliciting Structured Input from Clients in FastMCP (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/context.mdx

Demonstrates how to request structured input from clients during tool execution using `ctx.elicit()`, enabling interactive workflows and progressive disclosure. This feature requires FastMCP version 2.10.0 or higher.

```python
result = await ctx.elicit("Enter your name:", response_type=str)
if result.action == "accept":
    name = result.data
```

--------------------------------

### Define FastMCP internal path in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/http.mdx

This Python snippet illustrates setting the `mcp_path` parameter, which specifies the internal endpoint path for the FastMCP protocol. This path is appended to the `base_url` and should not include the mount prefix.

```python
mcp_path="/mcp" # Internal MCP path, NOT the mount prefix
```

--------------------------------

### Create FastMCP Client Fixture for Testing Tools

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/testing.mdx

Create a pytest fixture that wraps a FastMCP Server in a Client instance using FastMCPTransport. This enables fast testing of server functionality without external tools. The fixture yields an async context manager that provides a client instance for testing.

```python
import pytest
from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport

from my_project.main import mcp

@pytest.fixture
async def main_mcp_client():
    async with Client(transport=mcp) as mcp_client:
        yield mcp_client

async def test_list_tools(main_mcp_client: Client[FastMCPTransport]):
    list_tools = await main_mcp_client.list_tools()

    assert len(list_tools) == 5
```

--------------------------------

### Enable Built-in Advanced Logging Middleware in FastMCP

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

Shows how to integrate FastMCP's built-in logging middleware options: `LoggingMiddleware` for human-readable logs and `StructuredLoggingMiddleware` for JSON-formatted logs. Both support including request/response payloads.

```python
from fastmcp.server.middleware.logging import (
    LoggingMiddleware, 
    StructuredLoggingMiddleware
)

# Human-readable logging with payload support
mcp.add_middleware(LoggingMiddleware(
    include_payloads=True,
    max_payload_length=1000
))

# JSON-structured logging for log aggregation tools
mcp.add_middleware(StructuredLoggingMiddleware(include_payloads=True))
```

--------------------------------

### Override FastMCP Settings Temporarily (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-utilities-tests.mdx

This Python context manager allows temporary alteration of FastMCP application settings for testing purposes. It accepts keyword arguments for the settings to override, including support for nested configurations.

```python
temporary_settings(**kwargs: Any)
```

--------------------------------

### Add Middleware to FastMCP Server in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

This method allows adding a middleware component to the FastMCP server. It takes a `Middleware` object as an argument, which will be integrated into the server's request processing pipeline. This method does not return a value.

```python
add_middleware(self, middleware: Middleware) -> None
```

--------------------------------

### Run FastMCP Server

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/oci.mdx

This bash command starts the FastMCP server, specifying the entry point script (`server.py:mcp`), transport protocol (HTTP), and port (8000). This command should be executed after all necessary configurations and dependencies are in place.

```bash
fastmcp run server.py:mcp --transport http --port 8000
```

--------------------------------

### Integrate Google OAuth for FastMCP Server Protection

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-auth-providers-google.mdx

This code snippet demonstrates how to set up Google OAuth protection for a FastMCP server. It initializes the `GoogleProvider` with your Google API client ID and secret, then applies this authentication provider to a new `FastMCP` server instance. This configuration enables the server to use Google's OAuth flow for user authentication.

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.google import GoogleProvider

# Simple Google OAuth protection
auth = GoogleProvider(
    client_id="your-google-client-id.apps.googleusercontent.com",
    client_secret="your-google-client-secret"
)

mcp = FastMCP("My Protected Server", auth=auth)
```

--------------------------------

### Automatically Unwrapping Primitive Values from FastMCP Tools in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/tools.mdx

Explains FastMCP's automatic unwrapping of primitive values (like int, str, bool) from the `{"result": value}` structure returned by the server. It contrasts this with manual access required by other MCP clients.

```python
async with client:
    result = await client.call_tool("calculate_sum", {"a": 5, "b": 3})
    
    # FastMCP client automatically unwraps for convenience
    print(result.data)  # 8 (int) - the original value
    
    # Raw structured content shows the server-side wrapping
    print(result.structured_content)  # {"result": 8}
    
    # Other MCP clients would need to manually access ["result"]
    # value = result.structured_content["result"]  # Not needed with FastMCP!
```

--------------------------------

### Implement Recursive Tag Filtering in FastMCP (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/composition.mdx

This Python example demonstrates FastMCP's recursive tag filtering mechanism using `include_tags` across mounted servers. It sets up a subserver with tools tagged for different environments and then mounts it into a parent server with a 'production' tag filter, showcasing how tools are dynamically exposed or filtered based on their tags and the parent's policy.

```python
import asyncio
from fastmcp import FastMCP, Client

# Create a subserver with tools tagged for different environments
api_server = FastMCP(name="APIServer")

@api_server.tool(tags={"production"})
def prod_endpoint() -> str:
    """Production-ready endpoint."""
    return "Production data"

@api_server.tool(tags={"development"})
def dev_endpoint() -> str:
    """Development-only endpoint."""
    return "Debug data"

# Mount the subserver with production tag filtering at parent level
prod_app = FastMCP(name="ProductionApp", include_tags={"production"})
prod_app.mount(api_server, prefix="api")

# Test the filtering
async def test_filtering():
    async with Client(prod_app) as client:
        tools = await client.list_tools()
        print("Available tools:", [t.name for t in tools])
        # Shows: ['api_prod_endpoint']
        # The 'api_dev_endpoint' is filtered out

        # Calling the filtered tool raises an error
        try:
            await client.call_tool("api_dev_endpoint")
        except Exception as e:
            print(f"Filtered tool not accessible: {e}")

if __name__ == "__main__":
    asyncio.run(test_filtering())
```

--------------------------------

### Run fastmcp Server with StdIO Async Transport in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

The 'run_stdio_async' method initiates the fastmcp server using the standard input/output (stdio) transport mechanism. It allows control over whether to display the server banner and the log level for server operations.

```python
class Server:
    def run_stdio_async(self, show_banner: bool = True, log_level: str | None = None) -> None:
        # Implementation details...
        pass

# Example usage:
# server = Server()
# server.run_stdio_async(show_banner=True, log_level="INFO")

```

--------------------------------

### Run FastMCP Server from Factory Function (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

Illustrates running a FastMCP server instance that is returned by a factory function. This allows for executing setup code before the server starts and supports both synchronous and asynchronous functions. The function is specified using the `server.py:factory_fn` syntax.

```python
from fastmcp import FastMCP

async def create_server() -> FastMCP:
    mcp = FastMCP("MyServer")
    
    @mcp.tool
    def add(x: int, y: int) -> int:
        return x + y
    
    # Setup that runs with fastmcp run
    tool = await mcp.get_tool("add")
    tool.disable()
    
    return mcp
```

```bash
fastmcp run server.py:create_server
```

--------------------------------

### Test FastMCP Server Connection with OAuth Client

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/authkit.mdx

Async Python client that connects to a FastMCP server with OAuth authentication. Uses the Client context manager to establish authenticated connection and verifies server availability with a ping operation.

```python
from fastmcp import Client
import asyncio

async def main():
    async with Client("http://localhost:8000/mcp", auth="oauth") as client:
        assert await client.ping()

if __name__ == "__main__":
    asyncio.run(main())
```

--------------------------------

### Configure FastMCP Server Instance (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/server.mdx

Details how to apply server-specific settings directly during the initialization of a `FastMCP` instance. This includes controlling which components are exposed or hidden using `include_tags` and `exclude_tags`, and defining behavior for handling duplicate registrations of tools, resources, and prompts.

```python
from fastmcp import FastMCP

# Configure server-specific settings
mcp = FastMCP(
    name="ConfiguredServer",
    include_tags={"public", "api"},              # Only expose these tagged components
    exclude_tags={"internal", "deprecated"},     # Hide these tagged components
    on_duplicate_tools="error",                  # Handle duplicate registrations
    on_duplicate_resources="warn",
    on_duplicate_prompts="replace",
    include_fastmcp_meta=False                   # Disable FastMCP metadata for cleaner integration
)
```

--------------------------------

### Access FastMCP Server Initialization Results in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/client.mdx

Explains how the FastMCP client automatically performs an initialization handshake upon entering the context manager. It demonstrates accessing server metadata, capabilities, and instructions from the `initialize_result` property after the handshake.

```python
from fastmcp import Client, FastMCP

mcp = FastMCP(name="MyServer", instructions="Use the greet tool to say hello!")

@mcp.tool
def greet(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}!"

async with Client(mcp) as client:
    # Initialization already happened automatically
    print(f"Server: {client.initialize_result.serverInfo.name}")
    print(f"Version: {client.initialize_result.serverInfo.version}")
    print(f"Instructions: {client.initialize_result.instructions}")
    print(f"Capabilities: {client.initialize_result.capabilities.tools}")
```

--------------------------------

### Simplified FastMCP server initialization using environment variables (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/oci.mdx

This Python snippet shows the simplified FastMCP server initialization when all necessary OCI authentication configurations are provided via environment variables. It imports `FastMCP` and `get_access_token`, implying that the `FastMCP` instance would be configured implicitly through environment variable detection. This approach reduces boilerplate code and enhances security by externalizing sensitive credentials.

```python
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_access_token
```

--------------------------------

### Connect to Remote MCP Server using Streamable HTTP Transport in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/transports.mdx

Demonstrates connecting to a FastMCP server running as a web service using StreamableHttpTransport. This is the recommended transport for production deployments, supporting efficient bidirectional streaming over HTTP. The example shows basic connection and authentication using custom headers.

```python
from fastmcp.client.transports import StreamableHttpTransport

# Basic connection
transport = StreamableHttpTransport(url="https://api.example.com/mcp")
client = Client(transport)

# With custom headers for authentication
transport = StreamableHttpTransport(
    url="https://api.example.com/mcp",
    headers={
        "Authorization": "Bearer your-token-here",
        "X-Custom-Header": "value"
    }
)
client = Client(transport)
```

--------------------------------

### Define FastMCP Multi-Server Configuration (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/client.mdx

Presents an example Python dictionary structure for configuring multi-server FastMCP clients. It includes definitions for both remote HTTP/SSE servers with authentication headers and local Stdio servers with command-line arguments and environment variables.

```python
config = {
    "mcpServers": {
        "server_name": {
            # Remote HTTP/SSE server
            "transport": "http",  # or "sse" 
            "url": "https://api.example.com/mcp",
            "headers": {"Authorization": "Bearer token"},
            "auth": "oauth"  # or bearer token string
        },
        "local_server": {
            # Local stdio server
            "transport": "stdio",
            "command": "python",
            "args": ["./server.py", "--verbose"],
            "env": {"DEBUG": "true"},
            "cwd": "/path/to/server"
        }
    }
}
```

--------------------------------

### Handle Query Parameters in FastMCP Client Calls

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openapi.mdx

FastMCP automatically filters out query parameters with `None` values or empty strings when making HTTP requests. Only parameters with non-empty values are included in the final URL. This simplifies tool calls by preventing unnecessary parameters from being sent.

```python
# When calling this tool...
await client.call_tool("search_products", {
    "category": "electronics",  # ✅ Included
    "min_price": 100,           # ✅ Included  
    "max_price": None,          # ❌ Excluded
    "brand": "",                # ❌ Excluded
})

# The HTTP request will be: GET /products?category=electronics&min_price=100
```

--------------------------------

### Install FastMCP Library

Source: https://github.com/jlowin/fastmcp/blob/main/docs/tutorials/rest-api.mdx

This command installs the FastMCP Python library and its dependencies using pip. FastMCP is essential for connecting Large Language Models (LLMs) to REST APIs via OpenAPI specifications.

```bash
pip install fastmcp
```

--------------------------------

### FastAPI E-commerce API with Product Management

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/fastapi.mdx

A complete FastAPI application implementing an e-commerce product management system with CRUD operations. Includes in-memory database, Pydantic models for request/response validation, and endpoints for listing products with filtering by category and price, retrieving individual products, creating, updating, and deleting products. Demonstrates FastAPI best practices with type hints and HTTP exception handling.

```python
# Copy this FastAPI server into other code blocks in this guide

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Models
class Product(BaseModel):
    name: str
    price: float
    category: str
    description: str | None = None

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    category: str
    description: str | None = None

# Create FastAPI app
app = FastAPI(title="E-commerce API", version="1.0.0")

# In-memory database
products_db = {
    1: ProductResponse(
        id=1, name="Laptop", price=999.99, category="Electronics"
    ),
    2: ProductResponse(
        id=2, name="Mouse", price=29.99, category="Electronics"
    ),
    3: ProductResponse(
        id=3, name="Desk Chair", price=299.99, category="Furniture"
    ),
}
next_id = 4

@app.get("/products", response_model=list[ProductResponse])
def list_products(
    category: str | None = None,
    max_price: float | None = None,
) -> list[ProductResponse]:
    """List all products with optional filtering."""
    products = list(products_db.values())
    if category:
        products = [p for p in products if p.category == category]
    if max_price:
        products = [p for p in products if p.price <= max_price]
    return products

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    """Get a specific product by ID."""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return products_db[product_id]

@app.post("/products", response_model=ProductResponse)
def create_product(product: Product):
    """Create a new product."""
    global next_id
    product_response = ProductResponse(id=next_id, **product.model_dump())
    products_db[next_id] = product_response
    next_id += 1
    return product_response

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: Product):
    """Update an existing product."""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    products_db[product_id] = ProductResponse(
        id=product_id,
        **product.model_dump(),
    )
    return products_db[product_id]

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    """Delete a product."""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    del products_db[product_id]
    return {"message": "Product deleted"}
```

--------------------------------

### FastMCP Tool for Primitive Return With Annotation

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/tools.mdx

This FastMCP tool calculates a sum and includes a return type annotation (`-> int`). With the annotation, FastMCP automatically generates `structuredContent` by wrapping the primitive value in a `{"result": ...}` object, in addition to the traditional `content`.

```python
@mcp.tool
def calculate_sum(a: int, b: int) -> int:
    """Calculate sum with return annotation."""
    return a + b  # Returns 8
```

```json
{
  "content": [
    {
      "type": "text",
      "text": "8"
    }
  ],
  "structuredContent": {
    "result": 8
  }
}
```

--------------------------------

### Initialize FastMCPOpenAPI Server with Stateless Request Building

Source: https://github.com/jlowin/fastmcp/blob/main/src/fastmcp/experimental/utilities/openapi/README.md

This example demonstrates how to set up the `FastMCPOpenAPI` server using an OpenAPI specification dictionary and an `httpx.AsyncClient`. The server automatically initializes a `RequestDirector` and pre-calculates schemas, showcasing the stateless request building approach.

```python
import httpx
from fastmcp.server.openapi_new import FastMCPOpenAPI

# OpenAPI spec (can be loaded from file/URL)
openapi_spec = {...}

# Create HTTP client
async with httpx.AsyncClient() as client:
    # Create server with stateless request building
    server = FastMCPOpenAPI(
        openapi_spec=openapi_spec,
        client=client,
        name="My API Server"
    )
    
    # Server automatically creates RequestDirector and pre-calculates schemas
```

--------------------------------

### Run `fastmcp dev` with an explicit `fastmcp.json` configuration file

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

Specify a particular `fastmcp.json` file, such as `dev.fastmcp.json`, to configure and run the `fastmcp dev` server. This allows for using different configurations for various testing scenarios.

```bash
fastmcp dev dev.fastmcp.json
```

--------------------------------

### Customize FastMCP Route Mapping for FastAPI Endpoints (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/fastapi.mdx

This example demonstrates how to customize the conversion of FastAPI endpoints to MCP components using `RouteMap` and `MCPType`. It shows how to map GET requests with path parameters to `ResourceTemplates`, other GET requests to `Resources`, and implicitly POST/PUT/DELETE requests to `Tools`.

```python
# Assumes the FastAPI app from above is already defined
from fastmcp import FastMCP
from fastmcp.server.openapi import RouteMap, MCPType

# If using experimental parser, import from experimental module:
# from fastmcp.experimental.server.openapi import RouteMap, MCPType

# Custom mapping rules
mcp = FastMCP.from_fastapi(
    app=app,
    route_maps=[
        # GET with path params → ResourceTemplates
        RouteMap(
            methods=["GET"], 
            pattern=r".*\{.*\}.*", 
            mcp_type=MCPType.RESOURCE_TEMPLATE
        ),
        # Other GETs → Resources
        RouteMap(
            methods=["GET"], 
            pattern=r".*", 
            mcp_type=MCPType.RESOURCE
        ),
        # POST/PUT/DELETE → Tools (default)
    ],
)

# Now:
# - GET /products → Resource
# - GET /products/{id} → ResourceTemplate
# - POST/PUT/DELETE → Tools
```

--------------------------------

### Inspect FastMCP Server

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

Inspects a FastMCP server file to view summary information or generate detailed JSON reports in either FastMCP-specific or MCP protocol format. The output can be directed to stdout or saved to a file.

```bash
fastmcp inspect server.py
```

```bash
fastmcp inspect server.py --format fastmcp
```

```bash
fastmcp inspect server.py --format mcp -o manifest.json
```

```bash
fastmcp inspect server.py
```

```bash
# Output: 
# Server: MyServer
# Instructions: A helpful MCP server
# Version: 1.0.0
#
# Components:
#   Tools: 5
#   Prompts: 2
#   Resources: 3
#   Templates: 1
#
# Environment:
#   FastMCP: 2.0.0
#   MCP: 1.0.0
#
# Use --format [fastmcp|mcp] for complete JSON output

```

```bash
fastmcp inspect server.py --format fastmcp
```

```bash
fastmcp inspect server.py:my_server
```

```bash
fastmcp inspect server.py --format mcp
```

```bash
fastmcp inspect server.py --format fastmcp -o server-manifest.json
```

```bash
fastmcp inspect server.py:my_server --format mcp -o mcp-manifest.json
```

```bash
# Error: format required with output file
fastmcp inspect server.py -o output.json
# Error: --format is required when using -o/--output

```

--------------------------------

### Run FastMCP Server with HTTP Transport

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/authkit.mdx

Starts a FastMCP server locally using the CLI with HTTP transport on port 8000. Replace authkit_domain and base_url with actual values from your WorkOS configuration before running.

```bash
fastmcp run server.py --transport http --port 8000
```

--------------------------------

### Resource Management API

Source: https://github.com/jlowin/fastmcp/blob/main/src/fastmcp/contrib/component_manager/README.md

Endpoints to dynamically enable or disable specific resources within the FastMCP server. Supports both direct and templated URIs.

```APIDOC
## POST /resources/{uri:path}/enable

### Description
Enables a specific resource identified by its URI path within the FastMCP server. Supports template URIs.

### Method
POST

### Endpoint
/resources/{uri:path}/enable

### Parameters
#### Path Parameters
- **uri** (string) - Required - The full URI path of the resource to enable. Can be a template (e.g., example://test/{id}).

### Response
#### Success Response (200)
- **message** (string) - A confirmation message, e.g., "Enabled resource: {uri}".

#### Response Example
{
  "message": "Enabled resource: example://test/my_resource"
}

## POST /resources/{uri:path}/disable

### Description
Disables a specific resource identified by its URI path within the FastMCP server. Supports template URIs.

### Method
POST

### Endpoint
/resources/{uri:path}/disable

### Parameters
#### Path Parameters
- **uri** (string) - Required - The full URI path of the resource to disable. Can be a template (e.g., example://test/{id}).

### Response
#### Success Response (200)
- **message** (string) - A confirmation message, e.g., "Disabled resource: {uri}".

#### Response Example
{
  "message": "Disabled resource: example://test/my_resource"
}
```

--------------------------------

### Initialize FastMCP with Environment-Based Authentication

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/authkit.mdx

Simplified FastMCP server initialization that automatically loads authentication configuration from environment variables. Eliminates the need to manually instantiate AuthKitProvider when FASTMCP_SERVER_AUTH and related variables are properly configured.

```python
from fastmcp import FastMCP

# Authentication is automatically configured from environment
mcp = FastMCP(name="AuthKit Secured App")
```

--------------------------------

### Run FastMCP Server with Authorization

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/eunomia-authorization.mdx

This command starts the FastMCP server, which is now configured with the Eunomia authorization middleware. Upon startup, the server will intercept all incoming MCP requests and enforce the policies defined in `mcp_policies.json`.

```bash
python server.py
```

--------------------------------

### Specify Python Version for FastMCP Server (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/cursor.mdx

This command uses the `--python` flag to specify a particular Python version (e.g., 3.11) that the FastMCP server should use, ensuring compatibility with specific features.

```bash
fastmcp install cursor server.py --python 3.11
```

--------------------------------

### Use Prompt Tool Middleware

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

This snippet shows the integration of `PromptToolMiddleware` in FastMCP. This middleware provides compatibility for clients that cannot list or retrieve prompts directly, offering `list_prompts` and `get_prompt` tools accessible via tool calls.

```python
from fastmcp import FastMCP
from fastmcp.server.middleware.tool_injection import PromptToolMiddleware

mcp = FastMCP("MyServer")
mcp.add_middleware(PromptToolMiddleware())
```

--------------------------------

### Define a Reusable FastMCP Prompt

Source: https://github.com/jlowin/fastmcp/blob/main/README.md

This Python code defines a 'prompt' using the `@mcp.prompt` decorator. Prompts are reusable message templates designed to guide LLM interactions. This specific prompt generates a request for an LLM to summarize a given text, making it easy to standardize common LLM instructions.

```python
@mcp.prompt
def summarize_request(text: str) -> str:
    """Generate a prompt asking for a summary."""
    return f"Please summarize the following text:\n\n{text}"
```

--------------------------------

### FastMCP Tool Definition for Dictionary Return

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/tools.mdx

This example shows a FastMCP tool that returns a dictionary. FastMCP automatically converts object-like results like dictionaries into structured content, alongside traditional text content, without requiring explicit output schemas.

```python
@mcp.tool
def get_user_data(user_id: str) -> dict:
    """Get user data."""
    return {"name": "Alice", "age": 30, "active": True}
```

```json
{
  "content": [
    {
      "type": "text",
      "text": "{\n  \"name\": \"Alice\",\n  \"age\": 30,\n  \"active\": true\n}"
    }
  ],
  "structuredContent": {
    "name": "Alice",
    "age": 30,
    "active": true
  }
}
```

--------------------------------

### Configure FastMCP Azure AD Authentication Environment Variables

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/azure.mdx

These environment variables define the necessary Azure Active Directory parameters for a FastMCP server. `FASTMCP_SERVER_AUTH_AZURE_IDENTIFIER_URI` specifies the API identifier, while `FASTMCP_SERVER_AUTH_AZURE_ADDITIONAL_AUTHORIZE_SCOPES` allows requesting additional upstream permissions. Setting these variables enables automatic authentication configuration for the FastMCP application.

```shell
# FASTMCP_SERVER_AUTH_AZURE_IDENTIFIER_URI=api://your-api-id
# Request additional upstream scopes (optional)
# FASTMCP_SERVER_AUTH_AZURE_ADDITIONAL_AUTHORIZE_SCOPES=User.Read,Mail.Read
```

--------------------------------

### Start FastMCP Remote Server Proxy (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

Explains how to start a local proxy server that connects to a remote FastMCP server using its URL. This is beneficial for local testing or integrating with clients that require local connections.

```bash
fastmcp run https://example.com/mcp
```

--------------------------------

### Add Editable Python Package Dependencies to FastMCP Server (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/cursor.mdx

This command demonstrates how to install a local Python package in editable mode for your FastMCP server using the `--with-editable` flag, useful for development.

```bash
fastmcp install cursor server.py --with-editable ./my-local-package
```

--------------------------------

### Configure Descope Environment Variables for FastMCP

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/descope.mdx

This snippet defines essential environment variables in a `.env` file required for integrating Descope with a FastMCP server. It includes `DESCOPE_PROJECT_ID`, `DESCOPE_BASE_URL`, and `SERVER_URL`, which are crucial for the FastMCP server to correctly interact with Descope for authentication and token validation. These variables simplify configuration and promote secure practice by externalizing sensitive information.

```bash
DESCOPE_PROJECT_ID=P2abc...123      # Your Descope Project ID
DESCOPE_BASE_URL=https://api.descope.com   # Descope API URL
SERVER_URL=http://localhost:3000     # Your server's base URL
```

--------------------------------

### Define Basic Prompt Templates with FastMCP

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/prompts.mdx

This Python example demonstrates how to create basic prompt templates using the `@mcp.prompt` decorator. It shows how to define functions that accept parameters and return either a simple string (which FastMCP converts to a user message) or a specific `PromptMessage` object, leveraging function names and docstrings for inferred metadata.

```python
from fastmcp import FastMCP
from fastmcp.prompts.prompt import Message, PromptMessage, TextContent

mcp = FastMCP(name="PromptServer")

# Basic prompt returning a string (converted to user message automatically)
@mcp.prompt
def ask_about_topic(topic: str) -> str:
    """Generates a user message asking for an explanation of a topic."""
    return f"Can you please explain the concept of '{topic}'?"

# Prompt returning a specific message type
@mcp.prompt
def generate_code_request(language: str, task_description: str) -> PromptMessage:
    """Generates a user message requesting code generation."""
    content = f"Write a {language} function that performs the following task: {task_description}"
    return PromptMessage(role="user", content=TextContent(type="text", text=content))
```

--------------------------------

### Test FastMCP Server Network Features Using HTTP Transport

Source: https://github.com/jlowin/fastmcp/blob/main/CLAUDE.md

This Python example illustrates how to test FastMCP server functionality that explicitly involves network communication. It uses `StreamableHttpTransport` to connect a client to a server via a specified `server_url`, making it suitable for validating HTTP-specific features like `ping`.

```python
# Network testing only
async with Client(transport=StreamableHttpTransport(server_url)) as client:
    result = await client.ping()
```

--------------------------------

### Execute Tool with Timeout and Progress (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/tools.mdx

Demonstrates advanced execution of a tool ('long_running_task') with optional timeout and a progress handler. The timeout prevents execution from exceeding a specified duration, while the progress handler allows monitoring of the task's status. Requires an initialized 'client'.

```python
async with client:
    # With timeout (aborts if execution takes longer than 2 seconds)
    result = await client.call_tool(
        "long_running_task", 
        {"param": "value"}, 
        timeout=2.0
    )
    
    # With progress handler (to track execution progress)
    result = await client.call_tool(
        "long_running_task",
        {"param": "value"},
        progress_handler=my_progress_handler
    )
```

--------------------------------

### Configure FastMCP with OCI and encrypted persistent token storage (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/oci.mdx

This Python code configures a FastMCP application for production using OCI (Oracle Cloud Infrastructure) as an authentication provider. It sets up persistent and encrypted token management across server restarts by utilizing `jwt_signing_key` and `client_storage` with `FernetEncryptionWrapper` and `RedisStore`. Essential credentials and keys are loaded from environment variables to maintain security.

```python
import os
from fastmcp import FastMCP
from fastmcp.server.auth.providers.oci import OCIProvider

from key_value.aio.stores.redis import RedisStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper
from cryptography.fernet import Fernet

# Load configuration from environment
FASTMCP_SERVER_AUTH_OCI_CONFIG_URL = os.environ["FASTMCP_SERVER_AUTH_OCI_CONFIG_URL"]
FASTMCP_SERVER_AUTH_OCI_CLIENT_ID = os.environ["FASTMCP_SERVER_AUTH_OCI_CLIENT_ID"]
FASTMCP_SERVER_AUTH_OCI_CLIENT_SECRET = os.environ["FASTMCP_SERVER_AUTH_OCI_CLIENT_SECRET"]

# Production setup with encrypted persistent token storage
auth_provider = OCIProvider(
    config_url=FASTMCP_SERVER_AUTH_OCI_CONFIG_URL,
    client_id=FASTMCP_SERVER_AUTH_OCI_CLIENT_ID,
    client_secret=FASTMCP_SERVER_AUTH_OCI_CLIENT_SECRET,
    base_url="https://your-production-domain.com",

    # Production token management
    jwt_signing_key=os.environ["JWT_SIGNING_KEY"],
    client_storage=FernetEncryptionWrapper(
        key_value=RedisStore(
            host=os.environ["REDIS_HOST"],
            port=int(os.environ["REDIS_PORT"])
        ),
        fernet=Fernet(os.environ["STORAGE_ENCRYPTION_KEY"])
    )
)

mcp = FastMCP(name="Production OCI App", auth=auth_provider)
```

--------------------------------

### complete_mcp

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-client.mdx

Send a completion request to the server, returning the full MCP protocol result with completion data and metadata.

```APIDOC
## FUNCTION CALL complete_mcp

### Description
Send a completion request and return the complete MCP protocol result.

### Method
FUNCTION CALL

### Endpoint
complete_mcp

### Parameters
#### Request Body
- **ref** (mcp.types.ResourceTemplateReference | mcp.types.PromptReference) - Required - The reference to complete.
- **argument** (dict[str, str]) - Required - Arguments to pass to the completion request.
- **context_arguments** (dict[str, Any] | None) - Optional - Optional context arguments to include with the completion request.

### Request Example
```json
{
  "ref": {
    "type": "prompt",
    "name": "summarize_text"
  },
  "argument": {
    "text": "Long text to summarize..."
  },
  "context_arguments": {
    "user_id": "123"
  }
}
```

### Response
#### Success Response (200)
- **result** (mcp.types.CompleteResult) - The complete response object from the protocol, containing the completion and any additional metadata.

#### Response Example
```json
{
  "completion": {
    "text": "Summary of the text."
  },
  "metadata": {
    "tokens_used": 50
  }
}
```
```

--------------------------------

### Access FastMCP Settings Instance (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-settings.mdx

This property provides access to the FastMCP settings instance itself. It is included primarily for backwards compatibility with versions of FastMCP prior to 2.8.0. This ensures that older code accessing `fastmcp.settings.settings` continues to function as expected.

```python
settings(self) -> Self
```

--------------------------------

### Define FastMCP Resource Template with Multiple Parameters and Annotations in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/resources.mdx

Creates a GitHub repository information resource using FastMCP with a parameterized URI template containing owner and repo parameters. Includes annotations for readOnlyHint and idempotentHint to provide resource behavior hints to MCP clients.

```python
@mcp.resource(
    "repos://{owner}/{repo}/info",
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True
    }
)
def get_repo_info(owner: str, repo: str) -> dict:
    """Retrieves information about a GitHub repository."""
    # In a real implementation, this would call the GitHub API
    return {
        "owner": owner,
        "name": repo,
        "full_name": f"{owner}/{repo}",
        "stars": 120,
        "forks": 48
    }
```

--------------------------------

### Access Context via Runtime Dependency (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/context.mdx

Demonstrates retrieving the active Context object from anywhere within a server request's execution flow using the 'get_context' dependency function. This is useful when modifying function signatures to accept context is not feasible. Requires importing 'get_context' from 'fastmcp.server.dependencies'.

```python
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_context

mcp = FastMCP(name="Dependency Demo")


```

--------------------------------

### Configure Global FastMCP Settings with Environment Variables (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/server.mdx

This snippet demonstrates how to configure global FastMCP behaviors using environment variables prefixed with `FASTMCP_`. These variables allow control over aspects like logging level, error detail masking, resource prefix formatting, strict input validation, and the inclusion of FastMCP metadata, affecting the entire application's runtime.

```bash
export FASTMCP_LOG_LEVEL=DEBUG
export FASTMCP_MASK_ERROR_DETAILS=True
export FASTMCP_RESOURCE_PREFIX_FORMAT=protocol
export FASTMCP_STRICT_INPUT_VALIDATION=False
export FASTMCP_INCLUDE_FASTMCP_META=False
```

--------------------------------

### Configure FastMCP Client with BearerAuth Helper (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/auth/bearer.mdx

Demonstrates using the `BearerAuth` helper class for explicit Bearer token authentication with the FastMCP client. This approach allows for more control by directly implementing the `httpx.Auth` interface.

```python
from fastmcp import Client
from fastmcp.client.auth import BearerAuth

async with Client(
    "https://fastmcp.cloud/mcp", 
    auth=BearerAuth(token="<your-token>"),
) as client:
    await client.ping()
```

--------------------------------

### Report Basic Progress in FastMCP Tool (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/progress.mdx

Demonstrates the fundamental usage of `ctx.report_progress()` within a FastMCP tool to provide progress updates. It shows how to initialize `FastMCP`, define an asynchronous tool, iterate through items, report incremental progress, and finally, report 100% completion.

```python
from fastmcp import FastMCP, Context
import asyncio

mcp = FastMCP("ProgressDemo")

@mcp.tool
async def process_items(items: list[str], ctx: Context) -> dict:
    """Process a list of items with progress updates."""
    total = len(items)
    results = []
    
    for i, item in enumerate(items):
        # Report progress as we process each item
        await ctx.report_progress(progress=i, total=total)
        
        # Simulate processing time
        await asyncio.sleep(0.1)
        results.append(item.upper())
    
    # Report 100% completion
    await ctx.report_progress(progress=total, total=total)
    
    return {"processed": len(results), "results": results}
```

--------------------------------

### Implement Tool Injection Middleware

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

This example demonstrates how to use the `ToolInjectionMiddleware` in FastMCP. It allows injecting custom tools into the server's request lifecycle. The snippet defines a simple function `my_tool_fn`, converts it into a `Tool` object, and then adds the middleware with the tool to the server.

```python
from fastmcp import FastMCP, Tool
from fastmcp.server.middleware.tool_injection import ToolInjectionMiddleware

def my_tool_fn(a: int, b: int) -> int:
    return a + b

my_tool = Tool.from_function(fn=my_tool_fn, name="my_tool")

mcp = FastMCP("MyServer")
mcp.add_middleware(ToolInjectionMiddleware(tools=[my_tool]))
```

--------------------------------

### Configure and Access Components in Mounted FastMCP Servers

Source: https://github.com/jlowin/fastmcp/blob/main/src/fastmcp/contrib/component_manager/README.md

This example illustrates how to configure Component Manager with multiple mounted FastMCP servers, allowing different authentication scopes for each instance. It also provides cURL commands to interact with components on both the main and mounted servers, demonstrating how access is managed based on the server path and assigned scopes.

```python
mcp = FastMCP(name="Component Manager", instructions="This is a test server with component manager.", auth=auth)
set_up_component_manager(server=mcp, required_scopes=["mcp:write"])

mounted = FastMCP(name="Component Manager", instructions="This is a test server with component manager.", auth=auth)
set_up_component_manager(server=mounted, required_scopes=["mounted:write"])

mcp.mount(server=mounted, prefix="mo")
```

```bash
# Accessing the main server gives you control over both local and mounted components
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  http://localhost:8001/tools/mo_example_tool/enable
```

```bash
# Accessing the mounted server gives you control only over its own components
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  http://localhost:8002/tools/example_tool/enable
```

--------------------------------

### Create Streamable HTTP Application in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-http.mdx

This Python function provides an instance of a Streamable HTTP server application, integrated with a `FastMCP` server. It supports configuring the streamable HTTP path, an optional event store for session management, and an authentication provider. Additional options include JSON response formatting, stateless mode, debug settings, and custom routes/middleware, returning a `StarletteWithLifespan` application.

```python
create_streamable_http_app(server: FastMCP[LifespanResultT], streamable_http_path: str, event_store: EventStore | None = None, auth: AuthProvider | None = None, json_response: bool = False, stateless_http: bool = False, debug: bool = False, routes: list[BaseRoute] | None = None, middleware: list[Middleware] | None = None) -> StarletteWithLifespan
```

--------------------------------

### Add New Tools to FastMCP Server Converted from FastAPI (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/fastapi.mdx

This example shows how to extend a FastMCP server, converted from a FastAPI app, by adding new components like a tool. It uses the `@mcp.tool` decorator to register a Python function as an MCP tool, allowing the server to expose additional functionalities beyond the original FastAPI endpoints.

```python
# Assumes the FastAPI app from above is already defined
from fastmcp import FastMCP

# Convert to MCP server
mcp = FastMCP.from_fastapi(app=app)

# Add a new tool
@mcp.tool
def get_product(product_id: int) -> ProductResponse:
    """Get a product by ID."""
    return products_db[product_id]

# Run the MCP server
if __name__ == "__main__":
    mcp.run()
```

--------------------------------

### Specify Project Directory for FastMCP Server (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/cursor.mdx

This command uses the `--project` flag to specify the project directory where the FastMCP server should run. This helps `uv` discover relevant configuration files and ensures the correct virtual environment is used.

```bash
fastmcp install cursor server.py --project /path/to/my-project
```

--------------------------------

### Implement RFC 6570 Wildcard Parameters for Path Matching in FastMCP Python Resources

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/resources.mdx

Demonstrates three FastMCP resource patterns: standard single-segment parameter matching, wildcard parameter for multi-segment path capture, and mixed standard/wildcard parameters. Wildcard parameters ({param*}) can match multiple path segments including slashes, useful for hierarchical data and file paths.

```python
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")


# Standard parameter only matches one segment
@mcp.resource("files://{filename}")
def get_file(filename: str) -> str:
    """Retrieves a file by name."""
    # Will only match files://<single-segment>
    return f"File content for: {filename}"


# Wildcard parameter can match multiple segments
@mcp.resource("path://{filepath*}")
def get_path_content(filepath: str) -> str:
    """Retrieves content at a specific path."""
    # Can match path://docs/server/resources.mdx
    return f"Content at path: {filepath}"


# Mixing standard and wildcard parameters
@mcp.resource("repo://{owner}/{path*}/template.py")
def get_template_file(owner: str, path: str) -> dict:
    """Retrieves a file from a specific repository and path, but
    only if the resource ends with `template.py`"""
    # Can match repo://jlowin/fastmcp/src/resources/template.py
    return {
        "owner": owner,
        "path": path + "/template.py",
        "content": f"File at {path}/template.py in {owner}'s repository"
    }
```

--------------------------------

### Run a FastMCP server locally or remotely in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/getting-started/quickstart.mdx

Execute the FastMCP server by calling its `run()` method within an `if __name__ == "__main__"` block. Choose between `stdio` for local console interaction or `http` for remote access, specifying a port for the latter.

```python
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
```

```python
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
```

--------------------------------

### Install FastMCP Server with Local Editable Packages

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/gemini-cli.mdx

This command demonstrates how to install local Python packages in editable mode (e.g., `./my-local-package`) as dependencies for a FastMCP server using the `--with-editable` flag during installation.

```bash
fastmcp install gemini-cli server.py --with-editable ./my-local-package
```

--------------------------------

### Configure FastMCP Duplicate Prompt Handling (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/prompts.mdx

This example shows how to configure the FastMCP server's behavior when attempting to register multiple prompts with the same name. The 'on_duplicate_prompts' setting during 'FastMCP' initialization allows you to specify whether to warn, raise an error, replace, or ignore duplicate registrations, enabling custom conflict resolution.

```python
from fastmcp import FastMCP

mcp = FastMCP(
    name="PromptServer",
    on_duplicate_prompts="error"  # Raise an error if a prompt name is duplicated
)

@mcp.prompt
def greeting(): return "Hello, how can I help you today?"

# This registration attempt will raise a ValueError because
# "greeting" is already registered and the behavior is "error".
# @mcp.prompt
# def greeting(): return "Hi there! What can I do for you?"
```

--------------------------------

### Access MCP Session Context in FastMCP Tools (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/README.md

This snippet demonstrates how to inject and utilize the `Context` object within a FastMCP tool function. It showcases logging messages to the client using `ctx.info()`, reading resources from the server via `ctx.read_resource()`, and requesting LLM completions with `ctx.sample()`, ultimately returning the summarized content.

```python
from fastmcp import FastMCP, Context

mcp = FastMCP("My MCP Server")

@mcp.tool
async def process_data(uri: str, ctx: Context):
    # Log a message to the client
    await ctx.info(f"Processing {uri}...")

    # Read a resource from the server
    data = await ctx.read_resource(uri)

    # Ask client LLM to summarize the data
    summary = await ctx.sample(f"Summarize: {data.content[:500]}")

    # Return the summary
    return summary.text
```

--------------------------------

### Add Global Tags to all FastMCP Components

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openapi.mdx

This Python snippet demonstrates how to apply global tags to all `FastMCP` components generated from an OpenAPI specification. By providing a `tags` parameter to `FastMCP.from_openapi`, common categorization can be uniformly applied across all components.

```python
mcp = FastMCP.from_openapi(
    openapi_spec=spec,
    client=client,
    tags={"api-v2", "production", "external"}
)
```

--------------------------------

### Specify FastMCP Server Entrypoint for Installation (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/cursor.mdx

These commands show how to explicitly specify the FastMCP server object using the `file.py:object` notation during installation. If no object is specified, the CLI automatically looks for `mcp`, `server`, or `app`.

```bash
# These are equivalent if your server object is named 'mcp'
fastmcp install cursor server.py
fastmcp install cursor server.py:mcp

# Use explicit object name if your server has a different name
fastmcp install cursor server.py:my_custom_server
```

--------------------------------

### Run FastMCP Server with fastmcp.json (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

Details how to run a FastMCP server using a `fastmcp.json` configuration file, which can be auto-detected or explicitly specified. It also shows how to override configuration values using command-line arguments, such as `--port` or `--skip-env`.

```bash
# Auto-detect fastmcp.json in current directory
fastmcp run

# Or explicitly specify a configuration file
fastmcp run my-config.fastmcp.json
```

```bash
# Override port from config file
fastmcp run fastmcp.json --port 8080

# Skip environment setup when already in a uv environment
fastmcp run fastmcp.json --skip-env
```

--------------------------------

### Initialize FastMCP Server with Explicit ScalekitProvider in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/scalekit.mdx

Demonstrates how to create a FastMCP server in Python, explicitly using `ScalekitProvider` for OAuth integration. It requires Scalekit credentials and the MCP URL to be passed directly during provider instantiation, and defines a protected tool.

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.scalekit import ScalekitProvider

# Discovers Scalekit endpoints and set up JWT token validation
auth_provider = ScalekitProvider(
    environment_url=SCALEKIT_ENVIRONMENT_URL,    # Scalekit environment URL
    client_id=SCALEKIT_CLIENT_ID,                # OAuth client ID
    resource_id=SCALEKIT_RESOURCE_ID,            # Resource server ID
    mcp_url=SERVER_URL,                          # Is also aud claim
)

# Create FastMCP server with auth
mcp = FastMCP(name="My Scalekit Protected Server", auth=auth_provider)

@mcp.tool
def auth_status() -> dict:
    """Show Scalekit authentication status."""
    # Extract user claims from the JWT
    return {
        "message": "This tool requires authentication via Scalekit",
        "authenticated": True,
        "provider": "Scalekit"
    }
```

--------------------------------

### Implement a Custom Simple Logging Middleware for FastMCP

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

Provides an example of creating a custom logging middleware by extending FastMCP's `Middleware` class. This snippet shows how to log processing, completion, and failure of requests using `on_message`.

```python
from fastmcp.server.middleware import Middleware, MiddlewareContext

class SimpleLoggingMiddleware(Middleware):
    async def on_message(self, context: MiddlewareContext, call_next):
        print(f"Processing {context.method} from {context.source}")
        
        try:
            result = await call_next(context)
            print(f"Completed {context.method}")
            return result
        except Exception as e:
            print(f"Failed {context.method}: {e}")
            raise
```

--------------------------------

### Create Dynamic Resources with Templates in Python MCP Server

Source: https://github.com/jlowin/fastmcp/blob/main/docs/tutorials/create-mcp-server.mdx

Define resource templates using @mcp.resource with URI placeholders like {name}. FastMCP automatically maps placeholders to function parameters, enabling dynamic content generation.

```python
from fastmcp import FastMCP

mcp = FastMCP(name="My First MCP Server")

@mcp.tool
def add(a: int, b: int) -> int:
    """Adds two integer numbers together."""
    return a + b

@mcp.resource("resource://config")
def get_config() -> dict:
    """Provides the application's configuration."""
    return {"version": "1.0", "author": "MyTeam"}

@mcp.resource("greetings://{name}")
def personalized_greeting(name: str) -> str:
    """Generates a personalized greeting for the given name."""
    return f"Hello, {name}! Welcome to the MCP server."
```

--------------------------------

### Initialize a FastMCP server instance in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/getting-started/quickstart.mdx

Instantiate the `FastMCP` class with a server name to create a new MCP server object. This serves as the foundation for defining tools and running the server.

```python
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")
```

--------------------------------

### Implement Simple Timing Middleware

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

This Python code defines a basic timing middleware that measures the duration of a request. It uses `time.perf_counter` to calculate the time taken for request processing and logs the duration or any exceptions encountered.

```python
import time
from fastmcp.server.middleware import Middleware, MiddlewareContext

class SimpleTimingMiddleware(Middleware):
    async def on_request(self, context: MiddlewareContext, call_next):
        start_time = time.perf_counter()
        
        try:
            result = await call_next(context)
            duration_ms = (time.perf_counter() - start_time) * 1000
            print(f"Request {context.method} completed in {duration_ms:.2f}ms")
            return result
        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            print(f"Request {context.method} failed after {duration_ms:.2f}ms: {e}")
            raise
```

--------------------------------

### Execute a tool on fastmcp server (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-client.mdx

The `call_tool` method allows synchronous execution of a named tool on the fastmcp server. Unlike `call_tool_mcp`, this method specifically raises a `ToolError` if the tool execution fails. It takes the tool's name, optional arguments, a timeout, and a progress handler as input, returning the tool's output, which can be a dataclass, dictionary, or a list of content blocks.

```python
call_tool(self, name: str, arguments: dict[str, Any] | None = None, timeout: datetime.timedelta | float | int | None = None, progress_handler: ProgressHandler | None = None, raise_on_error: bool = True) -> CallToolResult
```

--------------------------------

### Configure FastMCP base_url in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/http.mdx

This Python snippet demonstrates how to set the `base_url` parameter for FastMCP, which defines the base URL for operational endpoints. It explicitly includes any Starlette `Mount()` path prefix to ensure correct routing.

```python
base_url="http://localhost:8000/api" # Includes mount prefix
```

--------------------------------

### List Resource Templates (MCP Protocol) in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-client.mdx

Sends a resources/listResourceTemplates request to retrieve resource templates with complete MCP protocol metadata. Returns the full protocol response object including templates and additional metadata. Requires an active client connection.

```python
list_resource_templates_mcp(self) -> mcp.types.ListResourceTemplatesResult
```

--------------------------------

### Install FastMCP Server to Claude Desktop Using CLI

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/claude-desktop.mdx

Commands for installing FastMCP servers into Claude Desktop using the fastmcp CLI tool (version 2.10.3+). Supports automatic configuration, explicit object notation using file.py:object syntax, and will auto-detect server objects named 'mcp', 'server', or 'app'. Requires Claude Desktop restart after installation to activate the MCP tools.

```bash
fastmcp install claude-desktop server.py
```

```bash
# These are equivalent if your server object is named 'mcp'
fastmcp install claude-desktop server.py
fastmcp install claude-desktop server.py:mcp

# Use explicit object name if your server has a different name
fastmcp install claude-desktop server.py:my_custom_server
```

--------------------------------

### Run `fastmcp dev` with auto-detected `fastmcp.json` configuration

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

Execute the `fastmcp dev` command without specifying a server file when a `fastmcp.json` configuration file is present in the current directory. The command automatically detects and uses this configuration to set up the server.

```bash
fastmcp dev
```

--------------------------------

### List Resource Templates (MCP)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-client.mdx

Sends a resources/listResourceTemplates request using the MCP protocol and returns the complete MCP protocol result, including resource templates and metadata.

```APIDOC
## GET /resources/listResourceTemplates (MCP)

### Description
Sends a resources/listResourceTemplates request using the MCP protocol and returns the complete MCP protocol result, including resource templates and metadata.

### Method
GET

### Endpoint
/resources/listResourceTemplates

### Parameters
None

### Request Example
None

### Response
#### Success Response (200)
- **ListResourceTemplatesResult** (mcp.types.ListResourceTemplatesResult) - The complete response object from the protocol, containing the list of resource templates and any additional metadata.

#### Response Example
```json
{
  "resourceTemplates": [
    {
      "name": "string",
      "version": "string",
      "description": "string"
    }
  ],
  "metadata": {}
}
```

#### Error Handling
- `RuntimeError`: If called while the client is not connected.
```

--------------------------------

### Define Custom HTTP Routes for FastMCP Server (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/running-server.mdx

This Python code demonstrates adding custom HTTP endpoints, such as a health check, to a FastMCP server using the `@mcp.custom_route` decorator. These routes run on the same web server as the main MCP endpoint, allowing for integrated service monitoring or simple API extensions. The custom route expects `Request` and returns `PlainTextResponse`.

```python
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

mcp = FastMCP("MyServer")

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")

@mcp.tool
def process(data: str) -> str:
    return f"Processed: {data}"

if __name__ == "__main__":
    mcp.run(transport="http")  # Health check at http://localhost:8000/health
```

--------------------------------

### Add Individual Python Package Dependencies to FastMCP Server (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/cursor.mdx

This command illustrates how to specify individual Python package dependencies for your FastMCP server using the `--with` flag. The flag can be used multiple times for different packages.

```bash
fastmcp install cursor server.py --with pandas --with requests
```

--------------------------------

### Access Context in FastMCP Tool Function (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/context.mdx

Demonstrates how to access the Context object within a FastMCP tool function. The context is automatically injected as a parameter typed 'Context' and can be used for logging and resource access. The function must be async as context methods are async.

```python
from fastmcp import FastMCP, Context

mcp = FastMCP(name="Context Demo")

@mcp.tool
async def process_file(file_uri: str, ctx: Context) -> str:
    """Processes a file, using context for logging and resource access."""
    # Context is available as the ctx parameter
    return "Processed file"

```

--------------------------------

### Install FastMCP Server from JSON Configuration File

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/mcp-json-configuration.mdx

Installs a FastMCP server using a fastmcp.json configuration file. This simplifies the installation process by centralizing all configuration options in a single file. Requires a fastmcp.json file in the current directory or specified path.

```bash
fastmcp install mcp-json fastmcp.json
```

--------------------------------

### Create FastMCP Server with Eunomia Middleware in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/eunomia-authorization.mdx

This Python code demonstrates how to initialize a FastMCP server and seamlessly integrate the Eunomia authorization middleware. It includes a sample tool definition and configures the middleware to use a policy file named `mcp_policies.json` for access control.

```python
from fastmcp import FastMCP
from eunomia_mcp import create_eunomia_middleware

# Create your FastMCP server
mcp = FastMCP("Secure MCP Server 🔒")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Add middleware to your server
middleware = create_eunomia_middleware(policy_file="mcp_policies.json")
mcp.add_middleware(middleware)

if __name__ == "__main__":
    mcp.run()
```

--------------------------------

### Configure FastMCP Descope Provider through Environment Variable

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/descope.mdx

This `bash` snippet sets the `FASTMCP_SERVER_AUTH` environment variable to `fastmcp.server.auth.providers.descope.DescopeProvider`. This configuration instructs FastMCP to automatically use Descope for authentication without explicit code instantiation, which is particularly useful for production deployments and maintaining separation of concerns. This method relies on FastMCP's ability to discover and initialize providers based on this variable.

```bash
# Use the Descope provider
FASTMCP_SERVER_AUTH=fastmcp.server.auth.providers.descope.DescopeProvider
```

--------------------------------

### Initialize FastMCP Server with Implicit Scalekit Authentication in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/scalekit.mdx

Illustrates a simplified FastMCP server initialization where authentication is automatically configured from environment variables. This approach reduces boilerplate code in `server.py` when Scalekit credentials are provided externally.

```python
from fastmcp import FastMCP

# Authentication is automatically configured from environment
mcp = FastMCP(name="My Scalekit Protected Server")

@mcp.tool
def protected_action() -> str:
    """A tool that requires authentication."""
    return "Access granted via Scalekit!"
```

--------------------------------

### Run FastMCP Server with Explicit Entrypoint (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

Shows how to explicitly specify the FastMCP server instance to run using the `server.py:instance_name` syntax. This is useful when the server variable has a custom name or when multiple instances might exist in the same file.

```bash
fastmcp run server.py:custom_name
```

```python
from fastmcp import FastMCP

my_server = FastMCP("CustomServer")

@my_server.tool
def hello() -> str:
    return "Hello from custom server!"
```

```bash
fastmcp run server.py:my_server
```

--------------------------------

### Manually Trigger FastMCP Change Notifications (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/context.mdx

This code snippet demonstrates how to manually trigger list change notifications within FastMCP using context methods like `ctx.send_tool_list_changed()`. These methods are typically used internally by FastMCP's automatic notification system, but can be invoked directly in rare cases after custom component changes, such as adding or removing tools, resources, or prompts.

```python
@mcp.tool
async def custom_tool_management(ctx: Context) -> str:
    """Example of manual notification after custom tool changes."""
    # After making custom changes to tools
    await ctx.send_tool_list_changed()
    await ctx.send_resource_list_changed()
    await ctx.send_prompt_list_changed()
    return "Notifications sent"
```

--------------------------------

### Register Python function as resource or template using add_resource_fn

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

Converts a Python function into a resource or template resource based on URI parameters. Supports optional metadata including name, description, MIME type, and tags. Automatically detects if the URI contains parameters to determine template registration.

```python
add_resource_fn(self, fn: AnyFunction, uri: str, name: str | None = None, description: str | None = None, mime_type: str | None = None, tags: set[str] | None = None) -> None
```

--------------------------------

### Tool Management API

Source: https://github.com/jlowin/fastmcp/blob/main/src/fastmcp/contrib/component_manager/README.md

Endpoints to dynamically enable or disable specific tools within the FastMCP server at runtime.

```APIDOC
## POST /tools/{tool_name}/enable

### Description
Enables a specific tool by its name within the FastMCP server.

### Method
POST

### Endpoint
/tools/{tool_name}/enable

### Parameters
#### Path Parameters
- **tool_name** (string) - Required - The unique name of the tool to enable.

### Response
#### Success Response (200)
- **message** (string) - A confirmation message, e.g., "Enabled tool: {tool_name}".

#### Response Example
{
  "message": "Enabled tool: example_tool"
}

## POST /tools/{tool_name}/disable

### Description
Disables a specific tool by its name within the FastMCP server.

### Method
POST

### Endpoint
/tools/{tool_name}/disable

### Parameters
#### Path Parameters
- **tool_name** (string) - Required - The unique name of the tool to disable.

### Response
#### Success Response (200)
- **message** (string) - A confirmation message, e.g., "Disabled tool: {tool_name}".

#### Response Example
{
  "message": "Disabled tool: example_tool"
}
```

--------------------------------

### Asynchronously call a FastMCP server tool from a Python client

Source: https://github.com/jlowin/fastmcp/blob/main/docs/getting-started/quickstart.mdx

Connect to a running FastMCP HTTP server using `fastmcp.Client` and asynchronously invoke a registered tool like 'greet'. The client operates within an `async with` context and requires `asyncio.run` for execution.

```python
import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result)

asyncio.run(call_tool("Ford"))
```

--------------------------------

### Connect to FastMCP Servers with Client (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/README.md

This example illustrates the basic usage of the `fastmcp.Client` to connect to an MCP server. It demonstrates connecting via standard I/O (stdio) to a local script to list and call tools, and also shows how to establish a connection to an SSE endpoint.

```python
from fastmcp import Client

async def main():
    # Connect via stdio to a local script
    async with Client("my_server.py") as client:
        tools = await client.list_tools()
        print(f"Available tools: {tools}")
        result = await client.call_tool("add", {"a": 5, "b": 3})
        print(f"Result: {result.content[0].text}")

    # Connect via SSE
    async with Client("http://localhost:8000/sse") as client:
        # ... use the client
        pass
```

--------------------------------

### List Available Prompts via Context in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-context.mdx

This method retrieves a list of all available prompts configured on the `fastmcp` server. It returns a list of `MCPPrompt` objects, detailing the prompts that can be invoked.

```python
list_prompts(self) -> list[MCPPrompt]
```

--------------------------------

### Basic FastMCP Server Setup

Source: https://github.com/jlowin/fastmcp/blob/main/README.md

This Python code sets up a basic FastMCP server named 'Demo 🚀'. It defines a simple 'hello' tool that takes a name string and returns a greeting. The server is configured to run using the default STIDO transport when the script is executed directly.

```python
# server.py
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def hello(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()  # Default: uses STDIO transport
```

--------------------------------

### Accessing Server Context with get_context() in FastMCP (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/context.mdx

This example demonstrates how to access the FastMCP server context using `get_context()` within an asynchronous utility function and an `@mcp.tool`. The `get_context` function is server-only and must be called within the context of a server request; calling it outside will raise a `RuntimeError`.

```python
async def process_data(data: list[float]) -> dict:
    # Get the active context - only works when called within a request
    ctx = get_context()    
    await ctx.info(f"Processing {len(data)} data points")
    
@mcp.tool
async def analyze_dataset(dataset_name: str) -> dict:
    # Call utility function that uses context internally
    data = load_data(dataset_name)
    await process_data(data)
```

--------------------------------

### Run `fastmcp dev` with a specific Python version

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

Launch the `fastmcp dev` server using a designated Python interpreter version, for example, Python 3.11. This is useful for testing your server's compatibility across different Python environments.

```bash
fastmcp dev server.py --python 3.11
```

--------------------------------

### Secure Component Manager Endpoints with Auth Scopes

Source: https://github.com/jlowin/fastmcp/blob/main/src/fastmcp/contrib/component_manager/README.md

This Python example shows how to integrate authentication scopes with the Component Manager. It configures a FastMCP server with authentication and specifies a list of required scopes for accessing the component management endpoints, enhancing security.

```python
mcp = FastMCP(name="Component Manager", instructions="This is a test server with component manager.", auth=auth)
set_up_component_manager(server=mcp, required_scopes=["write", "read"])
```

--------------------------------

### Access Context in FastMCP Resource/Template Functions (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/context.mdx

Shows how to access the Context object within FastMCP resource and template functions. The context is injected as a typed parameter and can be used for request-aware operations like fetching user-specific data or logging. These functions must be async.

```python
from fastmcp import FastMCP, Context

mcp = FastMCP(name="Context Demo")

@mcp.resource("resource://user-data")
async def get_user_data(ctx: Context) -> dict:
    """Fetch personalized user data based on the request context."""
    # Context is available as the ctx parameter
    return {"user_id": "example"}

@mcp.resource("resource://users/{user_id}/profile")
async def get_user_profile(user_id: str, ctx: Context) -> dict:
    """Fetch user profile with context-aware logging."""
    # Context is available as the ctx parameter
    return {"id": user_id}

```

--------------------------------

### Wrap CPU-Bound Synchronous Tasks with `anyio` in FastMCP

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/tools.mdx

This snippet demonstrates how to wrap a synchronous, CPU-intensive function using `anyio.to_thread.run_sync` within an `async` FastMCP tool. This prevents the synchronous operation from blocking the event loop, maintaining server responsiveness for I/O-bound or long-running computations. `anyio` is internally used by FastMCP.

```python
import anyio
from fastmcp import FastMCP

mcp = FastMCP()

def cpu_intensive_task(data: str) -> str:
    # Some heavy computation that could block the event loop
    return processed_data

@mcp.tool
async def wrapped_cpu_task(data: str) -> str:
    """CPU-intensive task wrapped to prevent blocking."""
    return await anyio.to_thread.run_sync(cpu_intensive_task, data)
```

--------------------------------

### Install FastMCP Server with Dependencies from requirements.txt via CLI

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/claude-code.mdx

This command demonstrates how to provide all required Python dependencies for your FastMCP server from a `requirements.txt` file during installation. The `--with-requirements` flag automates the installation of packages listed in the specified file.

```bash
fastmcp install claude-code server.py --with-requirements requirements.txt
```

--------------------------------

### Handle MCP Session Context Availability in FastMCP Middleware (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

This Python middleware example demonstrates how to conditionally access the MCP session and request context. It checks if `context.fastmcp_context.request_context` is available to safely access session-specific attributes like `session_id` or `request_id`. When the MCP session is not yet established (e.g., during client initialization), it illustrates how to fall back to HTTP-specific helpers for transport-level request data.

```python
from fastmcp.server.middleware import Middleware, MiddlewareContext

class SessionAwareMiddleware(Middleware):
    async def on_request(self, context: MiddlewareContext, call_next):
        ctx = context.fastmcp_context

        if ctx.request_context:
            # MCP session available - can access session-specific attributes
            session_id = ctx.session_id
            request_id = ctx.request_id
        else:
            # MCP session not available yet - use HTTP helpers for request data (if using HTTP transport)
            from fastmcp.server.dependencies import get_http_headers
            headers = get_http_headers()
            # Access HTTP data for auth, logging, etc.

        return await call_next(context)
```

--------------------------------

### Get Prompt (MCP Protocol) in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-client.mdx

Sends a prompts/get request to retrieve a specific prompt by name with optional arguments. Returns the complete MCP protocol response including prompt messages and metadata. Requires an active client connection.

```python
get_prompt_mcp(self, name: str, arguments: dict[str, Any] | None = None) -> mcp.types.GetPromptResult
```

--------------------------------

### Configure FastMCP Logging Settings (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-utilities-logging.mdx

This Python function configures the global or a specific `logging.Logger` instance for the FastMCP project. It allows setting the logging `level` (e.g., 'INFO', 'DEBUG') and can enable `rich` tracebacks for enhanced output. Additional `rich_kwargs` can customize the `RichHandler`.

```python
configure_logging(level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] | int = 'INFO', logger: logging.Logger | None = None, enable_rich_tracebacks: bool | None = None, **rich_kwargs: Any) -> None
```

--------------------------------

### Install FastMCP Server with Specific Python Version and Project Directory

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/mcp-json-configuration.mdx

Specifies Python version and project directory for FastMCP server installation. The Python version ensures compatibility with specific language features, while the project directory sets the working directory for the server execution.

```bash
# Use specific Python version
fastmcp install mcp-json server.py --python 3.11

# Run within a project directory
fastmcp install mcp-json server.py --project /path/to/project
```

--------------------------------

### Initialize and Use FastMCP Client in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-client.mdx

This Python example demonstrates how to initialize a `Client` instance to connect to a FastMCP server running on `http://localhost:8080`. It showcases the asynchronous context manager (`async with client:`) for managing the client session, performing actions like listing available resources, and calling a tool with specific parameters.

```python
# Connect to FastMCP server
client = Client("http://localhost:8080")

async with client:
    # List available resources
    resources = await client.list_resources()

    # Call a tool
    result = await client.call_tool("my_tool", {"param": "value"})
```

--------------------------------

### Integrate MCP Server Logs with Python Logging

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/logging.mdx

This code demonstrates how to provide a custom `log_handler` function to the FastMCP client to integrate server log messages with Python's standard `logging` module. It shows how to configure basic logging, map MCP log levels to Python levels, and use a logger to output structured log data from the server, enhancing robustness and debugging capabilities.

```python
import logging
from fastmcp import Client
from fastmcp.client.logging import LogMessage

# In a real app, you might configure this in your main entry point
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Get a logger for the module where the client is used
logger = logging.getLogger(__name__)

# This mapping is useful for converting MCP level strings to Python's levels
LOGGING_LEVEL_MAP = logging.getLevelNamesMapping()

async def log_handler(message: LogMessage):
    """
    Handles incoming logs from the MCP server and forwards them
    to the standard Python logging system.
    """
    msg = message.data.get('msg')
    extra = message.data.get('extra')

    # Convert the MCP log level to a Python log level
    level = LOGGING_LEVEL_MAP.get(message.level.upper(), logging.INFO)

    # Log the message using the standard logging library
    logger.log(level, msg, extra=extra)


client = Client(
    "my_mcp_server.py",
    log_handler=log_handler,
)
```

--------------------------------

### POST /new_client

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-client.mdx

Creates a new FastMCP client instance with the same configuration as the original, but with a fresh, disconnected session state. Useful for managing independent client sessions.

```APIDOC
## POST /new_client

### Description
Create a new client instance with the same configuration but fresh session state. This creates a new client with the same transport, handlers, and configuration, but with no active session. Useful for creating independent sessions that don't share state with the original client.

### Method
POST

### Endpoint
/new_client

### Parameters

### Request Example
{}

### Response
#### Success Response (200)
- **client_instance** (object) - A new Client instance, configured but not yet connected.

#### Response Example
```json
{}
```
```

--------------------------------

### Implement RFC 6570 Query Parameters in FastMCP Python Resources

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/resources.mdx

Shows how to use form-style query parameters with {?param1,param2} syntax in FastMCP resources. Query parameters must be optional function parameters with default values, providing clean separation between required path data and optional configuration with automatic type coercion support.

```python
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")

# Basic query parameters
@mcp.resource("data://{id}{?format}")
def get_data(id: str, format: str = "json") -> str:
    """Retrieve data in specified format."""
    if format == "xml":
        return f"<data id='{id}' />"
    return f'{{"id": "{id}"}}'

# Multiple query parameters with type coercion
@mcp.resource("api://{endpoint}{?version,limit,offset}")
def call_api(endpoint: str, version: int = 1, limit: int = 10, offset: int = 0) -> dict:
    """Call API endpoint with pagination."""
    return {
        "endpoint": endpoint,
        "version": version,
        "limit": limit,
        "offset": offset,
        "results": fetch_results(endpoint, version, limit, offset)
    }
```

--------------------------------

### Import FastMCP Server Components with Prefix (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/composition.mdx

This Python code demonstrates how to use `FastMCP.import_server()` to statically combine components from a subserver (`weather_mcp`) into a main server (`main_mcp`). It shows how tools and resources defined in the subserver are incorporated into the main server, with an optional prefix to avoid naming conflicts. The example initializes two `FastMCP` instances, defines a tool and a resource in the subserver, and then imports the subserver into the main server, resulting in prefixed components.

```python
from fastmcp import FastMCP
import asyncio

# Define subservers
weather_mcp = FastMCP(name="WeatherService")

@weather_mcp.tool
def get_forecast(city: str) -> dict:
    """Get weather forecast."""
    return {"city": city, "forecast": "Sunny"}

@weather_mcp.resource("data://cities/supported")
def list_supported_cities() -> list[str]:
    """List cities with weather support."""
    return ["London", "Paris", "Tokyo"]

# Define main server
main_mcp = FastMCP(name="MainApp")

# Import subserver
async def setup():
    await main_mcp.import_server(weather_mcp, prefix="weather")

# Result: main_mcp now contains prefixed components:
# - Tool: "weather_get_forecast"
# - Resource: "data://weather/cities/supported" 

if __name__ == "__main__":
    asyncio.run(setup())
    main_mcp.run()
```

--------------------------------

### Install FastMCP Server with Individual Python Dependencies via CLI

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/claude-code.mdx

This command shows how to include specific Python packages as dependencies for your FastMCP server during installation. The `--with` flag can be used multiple times to specify several individual packages.

```bash
fastmcp install claude-code server.py --with pandas --with requests
```

--------------------------------

### List Resources (MCP Protocol Result) (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-client.mdx

Sends a 'resources/list' request to the server and returns the complete MCP protocol result. This includes the list of resources and any additional metadata. A 'RuntimeError' is raised if the client is not connected.

```python
list_resources_mcp(self) -> mcp.types.ListResourcesResult
```

--------------------------------

### Initialize Authenticated Client and FastMCP Proxy in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/claude-desktop.mdx

This Python snippet demonstrates how to create a client authenticated with a Bearer token for a given API endpoint, and then use that client to instantiate and run a FastMCP proxy. It requires the `Client` and `BearerAuth` classes from the respective libraries and an access token for authentication.

```python
client = Client(
    "https://api.example.com/mcp/sse",
    auth=BearerAuth(token="your-access-token")
)

# Create proxy using the authenticated client
proxy = FastMCP.as_proxy(client, name="Authenticated Proxy")

if __name__ == "__main__":
    proxy.run()
```

--------------------------------

### Access Context in FastMCP Prompt Function (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/context.mdx

Illustrates accessing the Context object within a FastMCP prompt function. The context is provided as a parameter typed 'Context' and can be utilized for incorporating contextual information into prompt generation. The function requires an async definition.

```python
from fastmcp import FastMCP, Context

mcp = FastMCP(name="Context Demo")

@mcp.prompt
async def data_analysis_request(dataset: str, ctx: Context) -> str:
    """Generate a request to analyze data with contextual information."""
    # Context is available as the ctx parameter
    return f"Please analyze the following dataset: {dataset}"

```

--------------------------------

### Configure FastMCP Server with GitHub OAuth

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/github.mdx

This Python code demonstrates how to set up a FastMCP server using the `GitHubProvider` to handle authentication. It requires your GitHub OAuth App's Client ID and Client Secret, and a base URL. A protected tool is included to show how to access authenticated user information.

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.github import GitHubProvider

# The GitHubProvider handles GitHub's token format and validation
auth_provider = GitHubProvider(
    client_id="Ov23liAbcDefGhiJkLmN",  # Your GitHub OAuth App Client ID
    client_secret="github_pat_...",     # Your GitHub OAuth App Client Secret
    base_url="http://localhost:8000",   # Must match your OAuth App configuration
    # redirect_path="/auth/callback"   # Default value, customize if needed
)

mcp = FastMCP(name="GitHub Secured App", auth=auth_provider)

# Add a protected tool to test authentication
@mcp.tool
async def get_user_info() -> dict:
    """Returns information about the authenticated GitHub user."""
    from fastmcp.server.dependencies import get_access_token
    
    token = get_access_token()
    # The GitHubProvider stores user data in token claims
    return {
        "github_user": token.claims.get("login"),
        "name": token.claims.get("name"),
        "email": token.claims.get("email")
    }
```

--------------------------------

### Configure FastMCP Server Transport Settings (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/server.mdx

Illustrates how to apply transport-specific configuration when running a FastMCP server using `mcp.run()` or `mcp.run_async()`. These settings control the network behavior, such as specifying the transport protocol (e.g., 'http'), binding host, custom port, and overriding the global log level for the specific run operation.

```python
# Configure transport when running
mcp.run(
    transport="http",
    host="0.0.0.0",           # Bind to all interfaces
    port=9000,                # Custom port
    log_level="DEBUG"         # Override global log level
)

# Or for async usage
await mcp.run_async(
    transport="http", 
    host="127.0.0.1",
    port=8080
)
```

--------------------------------

### Use In-Memory Transport for Testing FastMCP Servers in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/transports.mdx

Shows how to connect directly to a FastMCP server instance within the same Python process using in-memory transport. This eliminates subprocess management and network overhead, making it ideal for testing and development. The server shares the same memory space and environment variables as the client code.

```python
from fastmcp import FastMCP, Client
import os

mcp = FastMCP("TestServer")

@mcp.tool
def greet(name: str) -> str:
    prefix = os.environ.get("GREETING_PREFIX", "Hello")
    return f"{prefix}, {name}!"

client = Client(mcp)

async with client:
    result = await client.call_tool("greet", {"name": "World"})
```

--------------------------------

### OAuth Client Provider Methods for Browser-Based Authentication (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-auth-oauth.mdx

These Python methods are part of the `OAuth` client provider class, which facilitates browser-based OAuth authentication for FastMCP servers. They handle the authorization redirect, process the OAuth callback to extract codes, and manage the asynchronous authentication flow with automatic retry on stale credentials.

```python
redirect_handler(self, authorization_url: str) -> None
```

```python
callback_handler(self) -> tuple[str, str | None]
```

```python
async_auth_flow(self, request: httpx.Request) -> AsyncGenerator[httpx.Request, httpx.Response]
```

--------------------------------

### Create Protected FastMCP Tool with Google Authentication

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/google.mdx

Implement a FastMCP server with automatic Google authentication configured through environment variables. The tool decorator creates an authenticated endpoint that processes requests from users who have successfully authenticated via Google OAuth.

```python
from fastmcp import FastMCP

# Authentication is automatically configured from environment
mcp = FastMCP(name="Google Secured App")

@mcp.tool
async def protected_tool(query: str) -> str:
    """A tool that requires Google authentication to access."""
    # Your tool implementation here
    return f"Processing authenticated request: {query}"
```

--------------------------------

### Run FastMCP 1.x Server Asynchronously in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-cli-run.mdx

Executes a FastMCP 1.x server instance using asynchronous methods. Handles server startup with optional host, port, and transport protocol configuration for backward compatibility with version 1.x servers.

```python
async def run_v1_server_async(
    server: FastMCP1x,
    host: str | None = None,
    port: int | None = None,
    transport: TransportType | None = None
) -> None:
    """Run a FastMCP 1.x server using async methods.
    
    Args:
        server: FastMCP 1.x server instance
        host: Host to bind to
        port: Port to bind to
        transport: Transport protocol to use
    """
    pass
```

--------------------------------

### Create FastMCP Server with Tool Endpoint in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/chatgpt.mdx

Builds a basic FastMCP server with a dice rolling tool endpoint. The server runs on HTTP transport on port 8000 and demonstrates tool registration using the @mcp.tool decorator. This example provides a foundation for creating MCP servers compatible with ChatGPT integration.

```python
from fastmcp import FastMCP
import random

mcp = FastMCP("Demo Server")

@mcp.tool
def roll_dice(sides: int = 6) -> int:
    """Roll a dice with the specified number of sides."""
    return random.randint(1, sides)

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
```

--------------------------------

### Run FastMCP Client

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/oci.mdx

This bash command executes the FastMCP client script (`client.py`). The client is designed to interact with the running MCP server and automatically handles OCI OAuth authentication flows.

```bash
python3 client.py
```

--------------------------------

### Specify Python Version for FastMCP Server Installation

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/gemini-cli.mdx

This command ensures that the FastMCP server is installed and run with a specific Python version (e.g., 3.11) by using the `--python` flag, guaranteeing compatibility for server-specific Python features.

```bash
fastmcp install gemini-cli server.py --python 3.11
```

--------------------------------

### Register Tool with FastMCP Server using Decorator

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

This decorator registers a function as a tool on the FastMCP server. Tools can optionally request a Context object, providing access to MCP capabilities. It supports multiple calling patterns including direct decoration and specifying a custom name, as shown in the examples.

```python
tool(self, name_or_fn: AnyFunction) -> FunctionTool
```

```python
tool(self, name_or_fn: str | None = None) -> Callable[[AnyFunction], FunctionTool]
```

```python
tool(self, name_or_fn: str | AnyFunction | None = None) -> Callable[[AnyFunction], FunctionTool] | FunctionTool
```

```python
@server.tool
def my_tool(x: int) -> str:
    return str(x)
```

--------------------------------

### Install FastMCP Server with Dependencies from Requirements File

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/mcp-json-configuration.mdx

Installs a FastMCP server with dependencies specified in a requirements.txt file. The command generates an MCP JSON configuration that can be used by MCP clients. This approach is suitable for servers with multiple dependencies.

```bash
fastmcp install mcp-json server.py --with-requirements requirements.txt
```

--------------------------------

### Implement Simple Error Handling Middleware in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

This Python code defines a basic error handling middleware for FastMCP. It catches exceptions during request processing, logs them using a configured logger, tracks error counts per error type and method, and re-raises the exception.

```python
import logging
from fastmcp.server.middleware import Middleware, MiddlewareContext

class SimpleErrorHandlingMiddleware(Middleware):
    def __init__(self):
        self.logger = logging.getLogger("errors")
        self.error_counts = {}
    
    async def on_message(self, context: MiddlewareContext, call_next):
        try:
            return await call_next(context)
        except Exception as error:
            # Log the error and track statistics
            error_key = f"{type(error).__name__}:{context.method}"
            self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1
            
            self.logger.error(f"Error in {context.method}: {type(error).__name__}: {error}")
            raise
```

--------------------------------

### Run FastMCP Server in Async Context (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/running-server.mdx

This Python example illustrates using `mcp.run_async()` to start a FastMCP server within an existing asynchronous event loop. It's designed for applications already running in an `asyncio` context, preventing conflicts that would arise from `mcp.run()` trying to create a new event loop. The `transport` and `port` arguments configure the server's network interface.

```python
from fastmcp import FastMCP
import asyncio

mcp = FastMCP(name="MyServer")

@mcp.tool
def hello(name: str) -> str:
    return f"Hello, {name}!"

async def main():
    # Use run_async() in async contexts
    await mcp.run_async(transport="http", port=8000)

if __name__ == "__main__":
    asyncio.run(main())
```

--------------------------------

### Check for FastMCP uv Subprocess in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-utilities-cli.mdx

This Python function determines if the current execution environment is already within a FastMCP uv subprocess. It returns a boolean value indicating the subprocess status, useful for managing FastMCP's internal process execution.

```python
is_already_in_uv_subprocess() -> bool
```

--------------------------------

### Define Custom Route Mapping Logic with FastMCP

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openapi.mdx

This Python example demonstrates how to implement a `route_map_fn` callable to customize `FastMCP`'s component type assignment based on route properties like path, method, and tags. The function can override default assignments or exclude routes from processing, even for routes initially marked for exclusion.

```python
from fastmcp import FastMCP
from fastmcp.server.openapi import RouteMap, MCPType, HTTPRoute

def custom_route_mapper(route: HTTPRoute, mcp_type: MCPType) -> MCPType | None:
    """Advanced route type mapping."""
    # Convert all admin routes to tools regardless of HTTP method
    if "/admin/" in route.path:
        return MCPType.TOOL

    elif "internal" in route.tags:
        return MCPType.EXCLUDE
    
    # Convert user detail routes to templates even if they're POST
    elif route.path.startswith("/users/") and route.method == "POST":
        return MCPType.RESOURCE_TEMPLATE
    
    # Use defaults for all other routes
    return None

mcp = FastMCP.from_openapi(
    openapi_spec=spec,
    client=client,
    route_map_fn=custom_route_mapper,
)
```

--------------------------------

### Configure FastMCP Resources with Decorator Options in Python

Source: https://github.com/jlowin/fastmcp/blob/main/src/fastmcp/contrib/mcp_mixin/README.md

This snippet demonstrates how to define methods as FastMCP resources using the `@mcp_resource` decorator. It covers basic resource definition with a URI, disabling a resource, and adding custom `meta`data and a descriptive `title`. Resources provide structured data access endpoints that can be consumed by clients.

```python
@mcp_resource(uri="component://data")
def resource_method(self):
    return {"data": "some data"}
```

```python
# Disabled resource
@mcp_resource(uri="component://data", enabled=False)
def resource_method(self):
    return {"data": "some data"}
```

```python
# example resource w/meta and title
@mcp_resource(
    uri="component://config",
    title="Data resource Title",
    meta={"internal": True, "cache_ttl": 3600, "priority": "high"}
)
def config_resource_method(self):
    return {"config": "data"}
```

--------------------------------

### Accessing Server Resources via FastMCP Context (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/context.mdx

Illustrates how to list and read data from resources registered with your FastMCP server, allowing access to files, configuration, or dynamic content. The `ctx.list_resources()` method returns a list of available resources, and `ctx.read_resource()` retrieves their content.

```python
# List available resources
resources = await ctx.list_resources()

# Read a specific resource
content_list = await ctx.read_resource("resource://config")
content = content_list[0].content
```

--------------------------------

### POST /call_tools_bulk

Source: https://github.com/jlowin/fastmcp/blob/main/src/fastmcp/contrib/bulk_tool_caller/README.md

Calls multiple different tools registered on the MCP server in a single request, optimizing server interactions.

```APIDOC
## POST /call_tools_bulk

### Description
This endpoint allows you to call multiple different tools registered on the MCP server within a single HTTP request. It helps in optimizing communication by reducing the number of individual requests.

### Method
POST

### Endpoint
/call_tools_bulk

### Parameters
#### Request Body
- **tool_calls** (list of CallToolRequest) - Required - A list of objects, where each object specifies the `tool` name and `arguments` for an individual tool call.
- **continue_on_error** (boolean) - Optional - If `True`, execution of subsequent tool calls will continue even if a previous one resulted in an error. Defaults to `True`.

### Request Example
```json
{
  "tool_calls": [
    {
      "tool": "tool_A",
      "arguments": {
        "param1": "value1",
        "param2": 123
      }
    },
    {
      "tool": "tool_B",
      "arguments": {
        "data": "some_data_string"
      }
    }
  ],
  "continue_on_error": true
}
```

### Response
#### Success Response (200)
- **(list of CallToolRequestResult)** - A list of objects, each containing the result (`isError`, `content`) and the original `tool` name and `arguments` for each call.

#### Response Example
```json
[
  {
    "isError": false,
    "content": {
      "tool_A_result": "success"
    },
    "tool": "tool_A",
    "arguments": {
      "param1": "value1",
      "param2": 123
    }
  },
  {
    "isError": true,
    "content": {
      "error_message": "tool_B failed to process data"
    },
    "tool": "tool_B",
    "arguments": {
      "data": "some_data_string"
    }
  }
]
```
```

--------------------------------

### Install Dependencies and Run FastMCP Server

Source: https://github.com/jlowin/fastmcp/blob/main/examples/atproto_mcp/README.md

Execute these commands in your terminal to install the necessary Python dependencies using 'uv' and then start the FastMCP server for the AT Protocol.

```bash
# Install dependencies
uv pip install -e .

# Run the server
uv run atproto-mcp
```

--------------------------------

### list_tools_mcp

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-client.mdx

Request a list of available tools from the server and receive the complete MCP protocol result.

```APIDOC
## FUNCTION CALL list_tools_mcp

### Description
Send a tools/list request and return the complete MCP protocol result.

### Method
FUNCTION CALL

### Endpoint
list_tools_mcp

### Parameters
#### Request Body
(None)

### Request Example
```json
{}
```

### Response
#### Success Response (200)
- **result** (mcp.types.ListToolsResult) - The complete response object from the protocol, containing the list of tools and any additional metadata.

#### Response Example
```json
{
  "tools": [
    {
      "name": "search_web",
      "description": "Search the internet for information."
    },
    {
      "name": "calculate_math",
      "description": "Perform mathematical calculations."
    }
  ],
  "metadata": {
    "count": 2
  }
}
```
```

--------------------------------

### FastMCP Middleware: Check Resource and Prompt Tags/Status During Execution (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

This Python middleware illustrates how to perform similar metadata checks for FastMCP resources and prompts during their respective execution operations (`on_read_resource`, `on_get_prompt`). It fetches the resource or prompt object via `fastmcp_context` to inspect properties like `tags` (for resources) or `enabled` status (for prompts). `ResourceError` or `PromptError` can be raised for access control based on these properties.

```python
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.exceptions import ResourceError, PromptError

class ComponentAccessMiddleware(Middleware):
    async def on_read_resource(self, context: MiddlewareContext, call_next):
        if context.fastmcp_context:
            try:
                resource = await context.fastmcp_context.fastmcp.get_resource(context.message.uri)
                if "restricted" in resource.tags:
                    raise ResourceError("Access denied: restricted resource")
            except Exception:
                pass
        return await call_next(context)
    
    async def on_get_prompt(self, context: MiddlewareContext, call_next):
        if context.fastmcp_context:
            try:
                prompt = await context.fastmcp_context.fastmcp.get_prompt(context.message.name)
                if not prompt.enabled:
                    raise PromptError("Prompt is currently disabled")
            except Exception:
                pass
        return await call_next(context)
```

--------------------------------

### Integrate FastMCP with WorkOS AuthKit using AuthKitProvider

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/auth/authentication.mdx

This Python snippet demonstrates integrating `FastMCP` with WorkOS AuthKit via `AuthKitProvider`. It leverages Dynamic Client Registration (DCR) to automatically configure token validation and provide OAuth metadata, enabling seamless client authentication with an external identity provider.

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.workos import AuthKitProvider

auth = AuthKitProvider(
    authkit_domain="https://your-project.authkit.app",
    base_url="https://your-fastmcp-server.com"
)

mcp = FastMCP(name="Enterprise Server", auth=auth)
```

--------------------------------

### Implement Error Handling with ResourceError in FastMCP Resources - Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/resources.mdx

Demonstrates error handling patterns in FastMCP resources using both ResourceError and standard Python exceptions. ResourceError messages are always sent to clients regardless of masking settings, while standard exceptions can be masked. Includes examples for both simple and template-based resources with different error scenarios.

```python
from fastmcp import FastMCP
from fastmcp.exceptions import ResourceError

mcp = FastMCP(name="DataServer")

@mcp.resource("resource://safe-error")
def fail_with_details() -> str:
    """This resource provides detailed error information."""
    # ResourceError contents are always sent back to clients,
    # regardless of mask_error_details setting
    raise ResourceError("Unable to retrieve data: file not found")

@mcp.resource("resource://masked-error")
def fail_with_masked_details() -> str:
    """This resource masks internal error details when mask_error_details=True."""
    # This message would be masked if mask_error_details=True
    raise ValueError("Sensitive internal file path: /etc/secrets.conf")

@mcp.resource("data://{id}")
def get_data_by_id(id: str) -> dict:
    """Template resources also support the same error handling pattern."""
    if id == "secure":
        raise ValueError("Cannot access secure data")
    elif id == "missing":
        raise ResourceError("Data ID 'missing' not found in database")
    return {"id": id, "value": "data"}
```

--------------------------------

### Run FastMCP Tests with pytest and uv

Source: https://github.com/jlowin/fastmcp/blob/main/examples/testing_demo/README.md

Commands to install dependencies and run FastMCP tests using uv and pytest. Includes options for verbose output and running specific tests. These commands execute the test suite for MCP servers with tools, resources, and prompts.

```bash
# Install dependencies
uv sync

# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run a specific test
uv run pytest tests/test_server.py::test_add_tool
```

--------------------------------

### Running FastMCP Server with STIDO Transport

Source: https://github.com/jlowin/fastmcp/blob/main/README.md

This Python code explicitly runs a FastMCP server using the STIDO (Standard Input/Output) transport protocol. This is the default transport and is best suited for local tools and command-line scripts.

```python
mcp.run(transport="stdio")  # Default, so transport argument is optional
```

--------------------------------

### FastMCP Middleware: Check Tool Tags and Status During Execution (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

This Python middleware example demonstrates how to access and validate a FastMCP tool's metadata, such as `tags` and `enabled` status, during an `on_call_tool` execution operation. It uses `context.fastmcp_context` to retrieve the full tool object before execution, allowing for custom access control based on properties like a 'private' tag or disabled status. If checks fail, a `ToolError` is raised to prevent execution.

```python
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.exceptions import ToolError

class TagBasedMiddleware(Middleware):
    async def on_call_tool(self, context: MiddlewareContext, call_next):
        # Access the tool object to check its metadata
        if context.fastmcp_context:
            try:
                tool = await context.fastmcp_context.fastmcp.get_tool(context.message.name)
                
                # Check if this tool has a "private" tag
                if "private" in tool.tags:
                    raise ToolError("Access denied: private tool")
                    
                # Check if tool is enabled
                if not tool.enabled:
                    raise ToolError("Tool is currently disabled")
                    
            except Exception:
                # Tool not found or other error - let execution continue
                # and handle the error naturally
                pass
        
        return await call_next(context)
```

--------------------------------

### Import Changes for FastMCP OpenAPI Migration

Source: https://github.com/jlowin/fastmcp/blob/main/src/fastmcp/experimental/utilities/openapi/README.md

Illustrates the necessary import path changes when migrating from the legacy FastMCP OpenAPI implementation to the new one. This highlights the shift in module structure for the FastMCPOpenAPI class.

```python
# Old
from fastmcp.server.openapi import FastMCPOpenAPI

# New  
from fastmcp.server.openapi_new import FastMCPOpenAPI
```

--------------------------------

### POST /call_tool_bulk

Source: https://github.com/jlowin/fastmcp/blob/main/src/fastmcp/contrib/bulk_tool_caller/README.md

Calls a single tool registered on the MCP server multiple times with different arguments in one request, reducing communication overhead.

```APIDOC
## POST /call_tool_bulk

### Description
This endpoint allows you to call a single, specific tool registered on the MCP server multiple times, each with different sets of arguments, within a single HTTP request.

### Method
POST

### Endpoint
/call_tool_bulk

### Parameters
#### Request Body
- **tool** (string) - Required - The name of the tool to call repeatedly.
- **tool_arguments** (list of dict) - Required - A list of dictionaries, where each dictionary contains the arguments for an individual run of the specified tool.
- **continue_on_error** (boolean) - Optional - If `True`, execution of subsequent tool calls will continue even if a previous one resulted in an error. Defaults to `True`.

### Request Example
```json
{
  "tool": "process_item",
  "tool_arguments": [
    {
      "item_id": "ITEM001",
      "quantity": 10
    },
    {
      "item_id": "ITEM002",
      "quantity": 5,
      "urgent": true
    }
  ],
  "continue_on_error": false
}
```

### Response
#### Success Response (200)
- **(list of CallToolRequestResult)** - A list of objects, each containing the result (`isError`, `content`) and the original `tool` name and `arguments` for each call.

#### Response Example
```json
[
  {
    "isError": false,
    "content": {
      "processed_id": "ITEM001",
      "status": "completed"
    },
    "tool": "process_item",
    "arguments": {
      "item_id": "ITEM001",
      "quantity": 10
    }
  },
  {
    "isError": false,
    "content": {
      "processed_id": "ITEM002",
      "status": "completed_urgent"
    },
    "tool": "process_item",
    "arguments": {
      "item_id": "ITEM002",
      "quantity": 5,
      "urgent": true
    }
  }
]
```
```

--------------------------------

### Example FastMCP Server with JWT Authentication and Permit.io Middleware

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/permit.mdx

This comprehensive Python example demonstrates a FastMCP server configured with JWT-based authentication and integrated with Permit.io middleware. It includes a login tool to issue JWT tokens and a protected tool that leverages the middleware's JWT identity extraction for authenticated access.

```python
from fastmcp import FastMCP, Context
from permit_fastmcp.middleware.middleware import PermitMcpMiddleware
import jwt
import datetime
import os

# Configure JWT identity extraction
os.environ["PERMIT_MCP_IDENTITY_MODE"] = "jwt"
os.environ["PERMIT_MCP_IDENTITY_JWT_SECRET"] = "mysecretkey"

mcp = FastMCP("My MCP Server")

@mcp.tool
def login(username: str, password: str) -> str:
    """Login to get a JWT token"""
    if username == "admin" and password == "password":
        token = jwt.encode(
            {"sub": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            "mysecretkey",
            algorithm="HS256"
        )
        return f"Bearer {token}"
    raise Exception("Invalid credentials")

@mcp.tool
def greet_jwt(ctx: Context) -> str:
    """Greet a user by extracting their name from JWT"""
    # JWT extraction handled by middleware
    return "Hello, authenticated user!"

mcp.add_middleware(PermitMcpMiddleware(
    permit_pdp_url="http://localhost:7766",
    permit_api_key="your-permit-api-key"
))

if __name__ == "__main__":
    mcp.run(transport="http")
```

--------------------------------

### Restore Pre-2.8.0 FastMCP Semantic GET Mapping (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openapi.mdx

This code demonstrates how to use `RouteMap` objects in FastMCP to restore the pre-2.8.0 semantic mapping for GET requests. It maps GET requests with path parameters to `ResourceTemplate` and all other GET requests to `Resource` components, ensuring specific handling for different types of GET endpoints.

```python
from fastmcp import FastMCP
from fastmcp.server.openapi import RouteMap, MCPType

# Restore pre-2.8.0 semantic mapping
semantic_maps = [
    # GET requests with path parameters become ResourceTemplates
    RouteMap(methods=["GET"], pattern=r".*\{.*\}.*", mcp_type=MCPType.RESOURCE_TEMPLATE),
    # All other GET requests become Resources
    RouteMap(methods=["GET"], pattern=r".*", mcp_type=MCPType.RESOURCE),
]

mcp = FastMCP.from_openapi(
    openapi_spec=spec,
    client=client,
    route_maps=semantic_maps,
)
```

--------------------------------

### Complete FastMCP Authenticated Server with Dice Rolling Tool

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/anthropic.mdx

Full implementation of an authenticated FastMCP server with JWT verification, including key pair generation, token creation, and a dice rolling tool. The server runs on HTTP transport at port 8000 and prints the access token to console for demonstration purposes only. Includes a tool decorator for registering the dice rolling functionality.

```python
from fastmcp import FastMCP
from fastmcp.server.auth import JWTVerifier
from fastmcp.server.auth.providers.jwt import RSAKeyPair
import random

key_pair = RSAKeyPair.generate()
access_token = key_pair.create_token(audience="dice-server")

auth = JWTVerifier(
    public_key=key_pair.public_key,
    audience="dice-server",
)

mcp = FastMCP(name="Dice Roller", auth=auth)

@mcp.tool
def roll_dice(n_dice: int) -> list[int]:
    """Roll `n_dice` 6-sided dice and return the results."""
    return [random.randint(1, 6) for _ in range(n_dice)]

if __name__ == "__main__":
    print(f"\n---\n\n🔑 Dice Roller access token:\n\n{access_token}\n\n---\n")
    mcp.run(transport="http", port=8000)
```

--------------------------------

### Authenticate OpenAI Client with FastMCP Server (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openai.mdx

This code demonstrates how to authenticate an OpenAI client when calling a FastMCP server that requires a bearer token. The access token is passed within the `Authorization` header inside the `headers` property of the `mcp` tool definition.

```python
from openai import OpenAI

# Your server URL (replace with your actual URL)
url = 'https://your-server-url.com'

# Your access token (replace with your actual token)
access_token = 'your-access-token'

client = OpenAI()

resp = client.responses.create(
    model="gpt-4.1",
    tools=[
        {
            "type": "mcp",
            "server_label": "dice_server",
            "server_url": f"{url}/mcp/",
            "require_approval": "never",
            "headers": {
                "Authorization": f"Bearer {access_token}"
            }
        },
    ],
    input="Roll a few dice!",
)

print(resp.output_text)
```

--------------------------------

### Filter Prompts by Tags using Metadata

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/prompts.mdx

Filters a list of prompts to find those containing a specific tag, 'analysis', within their FastMCP metadata. This is useful for selecting prompts relevant to a particular task. It assumes prompts have a `_meta` field containing FastMCP tags.

```python
async with client:
    prompts = await client.list_prompts()
    
    # Filter prompts by tag
    analysis_prompts = [
        prompt for prompt in prompts 
        if hasattr(prompt, '_meta') and prompt._meta and
           prompt._meta.get('_fastmcp', {}) and
           'analysis' in prompt._meta.get('_fastmcp', {}).get('tags', [])
    ]
    
    print(f"Found {len(analysis_prompts)} analysis prompts")
```

--------------------------------

### Import RouteMap and MCPType from Experimental OpenAPI Parser (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openapi.mdx

Provides the correct import statement for `RouteMap` and `MCPType` when utilizing FastMCP's experimental OpenAPI parser. Although the API remains identical, this import path enables access to the new parser's improved performance and serverless compatibility features.

```python
from fastmcp.experimental.server.openapi import RouteMap, MCPType
```

--------------------------------

### Specify Entrypoint for FastMCP Server Installation

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/gemini-cli.mdx

These commands demonstrate how to explicitly specify the FastMCP server object within a Python file using the `file.py:object` notation during installation. This is useful when the server object is not named `mcp`, `server`, or `app`.

```bash
# These are equivalent if your server object is named 'mcp'
fastmcp install gemini-cli server.py
fastmcp install gemini-cli server.py:mcp

# Use explicit object name if your server has a different name
fastmcp install gemini-cli server.py:my_custom_server
```

--------------------------------

### FastMCP resource decorator usage examples with sync, async, and templated URIs

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

Demonstrates various patterns for registering resources including basic synchronous functions, asynchronous data fetching, parameterized URI templates for dynamic resources, and context-aware async functions with logging capabilities. All examples show different return types and integration patterns.

```python
@server.resource("resource://my-resource")
def get_data() -> str:
    return "Hello, world!"

@server.resource("resource://my-resource")
async get_data() -> str:
    data = await fetch_data()
    return f"Hello, world! {data}"

@server.resource("resource://{city}/weather")
def get_weather(city: str) -> str:
    return f"Weather for {city}"

@server.resource("resource://{city}/weather")
async def get_weather_with_context(city: str, ctx: Context) -> str:
    await ctx.info(f"Fetching weather for {city}")
    return f"Weather for {city}"

@server.resource("resource://{city}/weather")
async def get_weather(city: str) -> str:
    data = await fetch_weather(city)
    return f"Weather for {city}: {data}"
```

--------------------------------

### HTTP Endpoints for Enabling/Disabling Components

Source: https://github.com/jlowin/fastmcp/blob/main/src/fastmcp/contrib/component_manager/README.md

These HTTP endpoints allow for enabling or disabling tools, resources, and prompts within the FastMCP server. They accept POST requests to specific paths for each component type, including support for template URIs for resources.

```http
POST /tools/{tool_name}/enable
POST /tools/{tool_name}/disable
```

```http
POST /resources/{uri:path}/enable
POST /resources/{uri:path}/disable
```

```http
POST /resources/example://test/{id}/enable
POST /resources/example://test/{id}/disable
```

```http
POST /prompts/{prompt_name}/enable
POST /prompts/{prompt_name}/disable
```

--------------------------------

### Set up FastMCP Development Environment

Source: https://github.com/jlowin/fastmcp/blob/main/docs/development/contributing.mdx

This set of commands guides contributors through cloning the FastMCP repository, installing development dependencies using 'uv sync', and setting up pre-commit hooks with 'uv run prek install'. It ensures a consistent development environment for all contributors.

```bash
# Clone the repository
git clone https://github.com/jlowin/fastmcp.git
cd fastmcp

# Install all dependencies including dev tools
uv sync

# Install prek hooks
uv run prek install
```

--------------------------------

### Apply Custom Tags to FastMCP Components via RouteMap

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openapi.mdx

This Python example demonstrates how to attach custom tags to `FastMCP` components using the `mcp_tags` parameter within `RouteMap` objects. Tags are applied based on route matching rules (methods, patterns) and help categorize components for better organization and filtering.

```python
from fastmcp.server.openapi import RouteMap, MCPType

mcp = FastMCP.from_openapi(
    openapi_spec=spec,
    client=client,
    route_maps=[
        # Add custom tags to all POST endpoints
        RouteMap(
            methods=["POST"],
            pattern=r".*",
            mcp_type=MCPType.TOOL,
            mcp_tags={"write-operation", "api-mutation"}
        ),
        
        # Add different tags to detail view endpoints
        RouteMap(
            methods=["GET"],
            pattern=r".*\{.*\}.*",
            mcp_type=MCPType.RESOURCE_TEMPLATE,
            mcp_tags={"detail-view", "parameterized"}
        ),
        
        # Add tags to list endpoints
        RouteMap(
            methods=["GET"],
            pattern=r".*",
            mcp_type=MCPType.RESOURCE,
            mcp_tags={"list-data", "collection"}
        ),
    ],
)
```

--------------------------------

### Install FastMCP Server with Python Version and Project Directory

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/claude-desktop.mdx

Commands for controlling the Python environment during FastMCP server installation. The --python flag specifies the Python version to use, while --project flag sets the project directory for discovering pyproject.toml, uv.toml, and .python-version files. The project directory also determines where relative paths are resolved and which virtual environment is used.

```bash
fastmcp install claude-desktop server.py --python 3.11
```

```bash
fastmcp install claude-desktop server.py --project /path/to/my-project
```

--------------------------------

### Read Resource (MCP)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-client.mdx

Sends a resources/read request using the MCP protocol and returns the complete MCP protocol result, including resource contents and metadata.

```APIDOC
## GET /resources/read

### Description
Sends a resources/read request using the MCP protocol and returns the complete MCP protocol result, including resource contents and metadata.

### Method
GET

### Endpoint
/resources/read?uri={uri}

### Parameters
#### Query Parameters
- **uri** (string | AnyUrl) - Required - The URI of the resource to read.

### Request Example
None

### Response
#### Success Response (200)
- **ReadResourceResult** (mcp.types.ReadResourceResult) - The complete response object from the protocol, containing the resource contents and any additional metadata.

#### Response Example
```json
{
  "contents": [
    {
      "type": "text",
      "data": "string"
    }
  ],
  "metadata": {}
}
```

#### Error Handling
- `RuntimeError`: If called while the client is not connected.
```

--------------------------------

### Configure FastMCP Server with JWT Authentication Verifier

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/anthropic.mdx

Sets up a FastMCP server with JWT authentication using JWTVerifier. The verifier uses the public key from the RSA key pair to validate incoming tokens and checks the audience claim. This configuration ensures only authenticated requests with valid tokens can access the server.

```python
from fastmcp import FastMCP
from fastmcp.server.auth import JWTVerifier

auth = JWTVerifier(
    public_key=key_pair.public_key,
    audience="dice-server",
)

mcp = FastMCP(name="Dice Roller", auth=auth)
```

--------------------------------

### Initialize FastMCP Server with AuthKit Provider

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/authkit.mdx

Sets up a FastMCP server instance with WorkOS AuthKit authentication provider. The AuthKitProvider automatically discovers WorkOS endpoints and configures JWT token validation. Requires authkit_domain from your WorkOS dashboard and base_url for your server.

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.workos import AuthKitProvider

# The AuthKitProvider automatically discovers WorkOS endpoints
# and configures JWT token validation
auth_provider = AuthKitProvider(
    authkit_domain="https://your-project-12345.authkit.app",
    base_url="http://localhost:8000"  # Use your actual server URL
)

mcp = FastMCP(name="AuthKit Secured App", auth=auth_provider)
```

--------------------------------

### Implement Azure Authenticated FastMCP Tool in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/azure.mdx

This Python code demonstrates a FastMCP server (`server.py`) that leverages environment variables for automatic Azure AD authentication configuration. It initializes a `FastMCP` instance and defines an asynchronous tool (`protected_tool`) that requires successful Azure authentication to be accessed. The authentication details are abstracted, allowing the developer to focus on the tool's business logic.

```python
from fastmcp import FastMCP

# Authentication is automatically configured from environment
mcp = FastMCP(name="Azure Secured App")

@mcp.tool
async def protected_tool(query: str) -> str:
    """A tool that requires Azure authentication to access."""
    # Your tool implementation here
    return f"Processing authenticated request: {query}"
```

--------------------------------

### Implement Health Check Endpoint for FastMCP Server (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/http.mdx

This Python code snippet demonstrates how to add a custom health check endpoint to a FastMCP server using the `@mcp.custom_route` decorator. It returns a JSON response indicating the server's health status, which is essential for load balancers, monitoring systems, and deployment platforms to verify server operation.

```python
from starlette.responses import JSONResponse

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    return JSONResponse({"status": "healthy", "service": "mcp-server"})
```

--------------------------------

### Install FastMCP Server with Environment Variables

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/mcp-json-configuration.mdx

Configures environment variables for a FastMCP server installation. Supports both individual environment variable specification and loading from a .env file. Environment variables are included in the generated MCP JSON configuration.

```bash
# Individual environment variables
fastmcp install mcp-json server.py \
  --env API_KEY=your-secret-key \
  --env DEBUG=true

# Load from .env file
fastmcp install mcp-json server.py --env-file .env
```

--------------------------------

### Define a Tool with FastMCP Decorator in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/server.mdx

This example illustrates how to define a tool using the `@mcp.tool` decorator in Python. Tools are functions that clients can invoke to perform specific actions, such as multiplying two numbers.

```python
@mcp.tool
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers together."""
    return a * b
```

--------------------------------

### Configure FastMCP Tools with Various Decorator Options in Python

Source: https://github.com/jlowin/fastmcp/blob/main/src/fastmcp/contrib/mcp_mixin/README.md

This section illustrates different ways to define methods as FastMCP tools using the `@mcp_tool` decorator. Examples include disabling a tool, excluding specific arguments from client calls, adding rich `ToolAnnotations` for LLMs, and embedding custom `meta`data. These options provide fine-grained control over tool behavior, discoverability, and interaction.

```python
# example of disabled tool
@mcp_tool(name="my_tool", description="Does something cool.", enabled=False)
def disabled_tool_method(self):
    # This function can't be called by client because it's disabled
    return "You'll never get here!"
```

```python
# example of excluded parameter tool
@mcp_tool(
    name="my_tool", description="Does something cool.",
    enabled=False, exclude_args=['delete_everything'],
)
def excluded_param_tool_method(self, delete_everything=False):
    # MCP tool calls can't pass the "delete_everything" argument
    if delete_everything:
        return "Nothing to delete, I bet you're not a tool :)"
    return "You might be a tool if..."
```

```python
# example tool w/annotations
@mcp_tool(
    name="my_tool", description="Does something cool.",
    annotations=ToolAnnotations(
        title="Attn LLM, use this tool first!",
        readOnlyHint=False,
        destructiveHint=False,
        idempotentHint=False,
    )
)
def tool_method(self):
    return "Tool executed!"
```

```python
# example tool w/everything
@mcp_tool(
    name="my_tool", description="Does something cool.",
    enabled=True,
    exclude_args=['delete_all'],
    annotations=ToolAnnotations(
        title="Attn LLM, use this tool first!",
        readOnlyHint=False,
        destructiveHint=False,
        idempotentHint=False,
    )
)
def tool_method(self, delete_all=False):
    if delete_all:
        return "99 records deleted. I bet you're not a tool :)"
    return "Tool executed, but you might be a tool!"
```

```python
# example tool w/ meta
@mcp_tool(
    name="data_tool",
    description="Fetches user data from database",
    meta={"version": "2.0", "category": "database", "author": "dev-team"}
)
def data_tool_method(self, user_id: int):
    return f"Fetching data for user {user_id}"
```

--------------------------------

### Demonstrate Unified Post Tool Usage (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/examples/atproto_mcp/README.md

This Python code block showcases practical examples of using the FastMCP client to interact with the AT Protocol's unified 'post' tool. It covers simple posts, posts with images, replies, quotes, rich text with links and mentions, and demonstrates how to create multi-part threads.

```python
from fastmcp import Client
from atproto_mcp.server import atproto_mcp

async def demo():
    async with Client(atproto_mcp) as client:
        # Simple post
        await client.call_tool("post", {
            "text": "Hello from FastMCP!"
        })
        
        # Post with image
        await client.call_tool("post", {
            "text": "Beautiful sunset! 🌅",
            "images": ["https://example.com/sunset.jpg"],
            "image_alts": ["Sunset over the ocean"]
        })
        
        # Reply to a post
        await client.call_tool("post", {
            "text": "Great point!",
            "reply_to": "at://did:plc:xxx/app.bsky.feed.post/yyy"
        })
        
        # Quote post
        await client.call_tool("post", {
            "text": "This is important:",
            "quote": "at://did:plc:xxx/app.bsky.feed.post/yyy"
        })
        
        # Rich text with links and mentions
        await client.call_tool("post", {
            "text": "Check out FastMCP by @alternatebuild.dev",
            "links": [{"text": "FastMCP", "url": "https://github.com/jlowin/fastmcp"}],
            "mentions": [{"handle": "alternatebuild.dev", "display_text": "@alternatebuild.dev"}]
        })
        
        # Advanced: Quote with image
        await client.call_tool("post", {
            "text": "Adding visual context:",
            "quote": "at://did:plc:xxx/app.bsky.feed.post/yyy",
            "images": ["https://example.com/chart.png"]
        })
        
        # Advanced: Reply with rich text
        await client.call_tool("post", {
            "text": "I agree! See this article for more info",
            "reply_to": "at://did:plc:xxx/app.bsky.feed.post/yyy",
            "links": [{"text": "this article", "url": "https://example.com/article"}]
        })
        
        # Create a thread
        await client.call_tool("create_thread", {
            "posts": [
                {"text": "Starting a thread about Python 🧵"},
                {"text": "Python is great for rapid prototyping"},
                {"text": "And the ecosystem is amazing!", "images": ["https://example.com/python.jpg"]}
            ]
        })
```

--------------------------------

### Configure FastMCP for Production with Persistent Tokens (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/workos.mdx

This Python snippet introduces essential imports for configuring a FastMCP server for production deployments. It highlights the use of `jwt_signing_key` for token signing and `client_storage` with `RedisStore` and `FernetEncryptionWrapper` for persistent, encrypted token management across server restarts.

```python
import os
from fastmcp import FastMCP
from fastmcp.server.auth.providers.workos import WorkOSProvider
from key_value.aio.stores.redis import RedisStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper
from cryptography.fernet import Fernet
```

--------------------------------

### Reporting Operation Progress in FastMCP (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/context.mdx

Shows how to update clients on the progress of long-running operations using `ctx.report_progress()`, enabling progress indicators and a better user experience. This keeps users informed about the status of ongoing tasks.

```python
await ctx.report_progress(progress=50, total=100)  # 50% complete
```

--------------------------------

### Run or Connect to FastMCP Server with Python `run` Function

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-cli-cli.mdx

This function runs an MCP server or connects to a remote one, supporting various specification methods like module, import, URL, or config files. It allows passing server-specific arguments after `--` for flexible configuration.

```python
run(server_spec: str | None = None, *server_args: str) -> None
```

--------------------------------

### Configure Scalekit Authentication via Environment Variables for FastMCP

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/scalekit.mdx

Shows an example `.env` file for configuring FastMCP to automatically use `ScalekitProvider`. This setup allows the server to pull Scalekit configuration details from environment variables, simplifying the Python code.

```bash
# Use the Scalekit provider
FASTMCP_SERVER_AUTH=fastmcp.server.auth.providers.scalekit.ScalekitProvider

# Scalekit configuration
FASTMCP_SERVER_AUTH_SCALEKITPROVIDER_ENVIRONMENT_URL=https://your-env.scalekit.com
FASTMCP_SERVER_AUTH_SCALEKITPROVIDER_CLIENT_ID=skc_123
FASTMCP_SERVER_AUTH_SCALEKITPROVIDER_RESOURCE_ID=res_456
FASTMCP_SERVER_AUTH_SCALEKITPROVIDER_MCP_URL=https://your-server.com/mcp
```

--------------------------------

### Specify FastMCP issuer_url for discovery in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/http.mdx

This Python snippet shows how to define the `issuer_url` for FastMCP. This URL indicates where OAuth clients can find discovery metadata and must point to the root level of the server for RFC compliance, without any path prefix.

```python
issuer_url="http://localhost:8000" # Root level, no prefix
```

--------------------------------

### Define FastMCP Client with LLM Sampling Handler (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/sampling.mdx

This snippet demonstrates how to initialize a `fastmcp.Client` instance, providing an asynchronous `sampling_handler` function. This handler serves as the integration point for your Language Model (LLM) service, processing incoming `SamplingMessage`s and `SamplingParams` to generate a text response.

```python
from fastmcp import Client
from fastmcp.client.sampling import (
    SamplingMessage,
    SamplingParams,
    RequestContext,
)

async def sampling_handler(
    messages: list[SamplingMessage],
    params: SamplingParams,
    context: RequestContext
) -> str:
    # Your LLM integration logic here
    # Extract text from messages and generate a response
    return "Generated response based on the messages"

client = Client(
    "my_mcp_server.py",
    sampling_handler=sampling_handler,
)
```

--------------------------------

### Read File Resource with Wildcard Path and Query Parameters in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/resources.mdx

Defines a FastMCP resource handler that accepts a wildcard path parameter and optional query parameters for encoding and line limits. FastMCP automatically coerces query parameter string values to the correct types based on function type hints (str, int). This example demonstrates combining path wildcards with optional configuration parameters.

```python
@mcp.resource("files://{path*}{?encoding,lines}")
def read_file(path: str, encoding: str = "utf-8", lines: int = 100) -> str:
    """Read file with optional encoding and line limit."""
    return read_file_content(path, encoding, lines)
```

--------------------------------

### Python FastMCP: Masking Error Details

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/tools.mdx

Demonstrates how to mask internal error details when creating a FastMCP instance to enhance security. This prevents sensitive information from being exposed to the client LLM.

```python
from fastmcp import FastMCP

mcp = FastMCP(name="SecureServer", mask_error_details=True)
```

--------------------------------

### FastMCP OAuth Proxy Interaction Flow Diagram (Mermaid)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/auth/oauth-proxy.mdx

This Mermaid sequence diagram visualizes the complete OAuth flow managed by the FastMCP OAuth Proxy. It details the interactions between the MCP Client, User, FastMCP Proxy, and OAuth Provider across registration, authorization, callback, and token exchange phases, highlighting the dual-PKCE security mechanism and dynamic client registration. This diagram clarifies the transparent nature of the proxy to the MCP client.

```mermaid
sequenceDiagram
    participant Client as MCP Client<br/>(localhost:random)
    participant User as User
    participant Proxy as FastMCP OAuth Proxy<br/>(server:8000)
    participant Provider as OAuth Provider<br/>(GitHub, etc.)

    Note over Client, Proxy: Dynamic Registration (Local)
    Client->>Proxy: 1. POST /register<br/>redirect_uri: localhost:54321/callback
    Proxy-->>Client: 2. Returns fixed upstream credentials

    Note over Client, User: Authorization with User Consent
    Client->>Proxy: 3. GET /authorize<br/>redirect_uri=localhost:54321/callback<br/>code_challenge=CLIENT_CHALLENGE
    Note over Proxy: Store transaction with client PKCE<br/>Generate proxy PKCE pair
    Proxy->>User: 4. Show consent page<br/>(client details, redirect URI, scopes)
    User->>Proxy: 5. Approve/deny consent
    Proxy->>Provider: 6. Redirect to provider<br/>redirect_uri=server:8000/auth/callback<br/>code_challenge=PROXY_CHALLENGE

    Note over Provider, Proxy: Provider Callback
    Provider->>Proxy: 7. GET /auth/callback<br/>with authorization code
    Proxy->>Provider: 8. Exchange code for tokens<br/>code_verifier=PROXY_VERIFIER
    Provider-->>Proxy: 9. Access & refresh tokens

    Note over Proxy, Client: Client Callback Forwarding
    Proxy->>Client: 10. Redirect to localhost:54321/callback<br/>with new authorization code

    Note over Client, Proxy: Token Exchange
    Client->>Proxy: 11. POST /token with code<br/>code_verifier=CLIENT_VERIFIER
    Proxy-->>Client: 12. Returns stored provider tokens
```

--------------------------------

### Read Resource (MCP Protocol) in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-client.mdx

Sends a resources/read request to retrieve resource contents with complete MCP protocol metadata. Accepts URI as string or AnyUrl object and returns the full protocol response including contents and metadata. Requires an active client connection.

```python
read_resource_mcp(self, uri: AnyUrl | str) -> mcp.types.ReadResourceResult
```

--------------------------------

### Define Synchronous and Asynchronous FastMCP Prompts (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/prompts.mdx

This snippet illustrates how FastMCP seamlessly supports both standard ('def') and asynchronous ('async def') functions as prompts. Use 'async def' when your prompt function performs I/O-bound operations like network requests, database queries, or external service calls to ensure non-blocking execution.

```python
# Synchronous prompt
@mcp.prompt
def simple_question(question: str) -> str:
    """Generates a simple question to ask the LLM."""
    return f"Question: {question}"

# Asynchronous prompt
@mcp.prompt
async def data_based_prompt(data_id: str) -> str:
    """Generates a prompt based on data that needs to be fetched."""
    # In a real scenario, you might fetch data from a database or API
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.example.com/data/{data_id}") as response:
            data = await response.json()
            return f"Analyze this data: {data['content']}"
```

--------------------------------

### List Prompts (MCP)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-client.mdx

Sends a prompts/list request using the MCP protocol and returns the complete MCP protocol result, including prompts and metadata.

```APIDOC
## GET /prompts/list

### Description
Sends a prompts/list request using the MCP protocol and returns the complete MCP protocol result, including prompts and metadata.

### Method
GET

### Endpoint
/prompts/list

### Parameters
None

### Request Example
None

### Response
#### Success Response (200)
- **ListPromptsResult** (mcp.types.ListPromptsResult) - The complete response object from the protocol, containing the list of prompts and any additional metadata.

#### Response Example
```json
{
  "prompts": [
    {
      "name": "string",
      "description": "string"
    }
  ],
  "metadata": {}
}
```

#### Error Handling
- `RuntimeError`: If called while the client is not connected.
```

--------------------------------

### Configure Error Detail Masking in FastMCP Server - Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/resources.mdx

Creates a FastMCP server instance with error detail masking enabled for security. When mask_error_details is set to True, internal exception details are hidden from clients, while ResourceError messages remain visible. This protects sensitive information like file paths from being exposed to client LLMs.

```python
mcp = FastMCP(name="SecureServer", mask_error_details=True)
```

--------------------------------

### Start FastMCP Server using the run() Method (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/running-server.mdx

This snippet demonstrates the fundamental way to start a FastMCP server by calling the `run()` method on the FastMCP instance. It defines a simple tool and ensures the server starts only when the script is executed directly by placing the `run()` call within an `if __name__ == "__main__":` block, handling connection management automatically.

```python
from fastmcp import FastMCP

mcp = FastMCP(name="MyServer")

@mcp.tool
def hello(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
```

--------------------------------

### Import FastMCP Server with Optional Prefix - Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

Imports MCP objects (tools, resources, templates, prompts) from another FastMCP server with optional prefix support. This is a one-time operation where objects are immediately registered, and server-level configurations are not imported. The prefix is applied to tool names, resource URIs, template URIs, and prompt names using specific formatting rules.

```python
import_server(self, server: FastMCP[LifespanResultT], prefix: str | None = None, tool_separator: str | None = None, resource_separator: str | None = None, prompt_separator: str | None = None) -> None
```

--------------------------------

### Define FastMCP Tool Parameters with Pydantic Field and Annotated (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/tools.mdx

This example demonstrates using Pydantic's `Field` class with `Annotated` to add detailed metadata, validation constraints (e.g., `ge`, `le`), and descriptions to FastMCP tool parameters. These descriptions are exposed to Large Language Models (LLMs) for better understanding.

```python
from typing import Annotated
from pydantic import Field

@mcp.tool
def process_image(
    image_url: Annotated[str, Field(description="URL of the image to process")],
    resize: Annotated[bool, Field(description="Whether to resize the image")] = False,
    width: Annotated[int, Field(description="Target width in pixels", ge=1, le=2000)] = 800,
    format: Annotated[
        Literal["jpeg", "png", "webp"], 
        Field(description="Output image format")
    ] = "jpeg"
) -> dict:
    """Process an image with optional resizing."""
    # Implementation...
```

--------------------------------

### Send WARNING Log Message to fastmcp Client in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-context.mdx

Sends a log message with a `WARNING` level to the connected MCP client. This helper function allows for easy communication of non-critical issues or potential problems, with server-side logging also directed to `fastmcp.server.context.to_client`.

```python
warning(self, message: str, logger_name: str | None = None, extra: Mapping[str, Any] | None = None) -> None
```

--------------------------------

### Specify Python Version for FastMCP Server Installation via CLI

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/claude-code.mdx

This command demonstrates how to specify a particular Python version required by your FastMCP server using the `--python` flag during installation. This ensures compatibility and the correct environment for server execution.

```bash
fastmcp install claude-code server.py --python 3.11
```

--------------------------------

### Get FastMCP OAuth discovery routes in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/http.mdx

This Python snippet illustrates how to retrieve the well-known discovery routes from the FastMCP authentication provider. It's important to pass the `mcp_path` argument, matching the path used when creating the MCP app, to ensure correct metadata generation for protected resources.

```python
well_known_routes = auth.get_well_known_routes(mcp_path=MCP_PATH)
```

--------------------------------

### Install FastMCP Server with Individual Python Packages

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/gemini-cli.mdx

This command installs a FastMCP server and explicitly includes individual Python package dependencies like 'pandas' and 'requests' using the `--with` flag. The flag can be used multiple times for different packages.

```bash
fastmcp install gemini-cli server.py --with pandas --with requests
```

--------------------------------

### Load Environment Variables from `.env` File for FastMCP Server

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/gemini-cli.mdx

This command allows loading environment variables for the FastMCP server directly from a `.env` file using the `--env-file` flag during installation, simplifying the management of multiple or sensitive variables.

```bash
fastmcp install gemini-cli server.py --server-name "Weather Server" --env-file .env
```

--------------------------------

### Install FastMCP Server to a Specific Workspace in Cursor (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/cursor.mdx

These commands demonstrate how to install a FastMCP server into a project-specific workspace within Cursor using the `--workspace` flag. This creates a `.cursor/mcp.json` configuration file, allowing different projects to have unique server setups.

```bash
# Install to current directory's .cursor/ folder
fastmcp install cursor server.py --workspace .

# Install to specific workspace
fastmcp install cursor server.py --workspace /path/to/project
```

--------------------------------

### Create a Copy of a FastMCP Component in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-utilities-components.mdx

This method generates a duplicate instance of the FastMCP component. The copy created is a standalone version that can be modified independently.

```python
copy(self) -> Self
```

--------------------------------

### Create New Client Instance (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-client.mdx

Creates a new fastmcp client instance with the same configuration but a fresh session state. This is useful for establishing independent sessions that do not share state with the original client. The method returns a new Client instance with a disconnected state.

```python
new(self) -> Client[ClientTransportT]
```

--------------------------------

### Prepare FastMCP Project Environment with Python `prepare` Function

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-cli-cli.mdx

This function prepares a FastMCP project by creating a persistent `uv` environment, installing dependencies, and preparing the source code. It's useful for CI/CD, Docker builds, and production deployments to ensure fast startup times.

```python
prepare(config_path: Annotated[str | None, cyclopts.Parameter(help='Path to fastmcp.json configuration file')] = None, output_dir: Annotated[str | None, cyclopts.Parameter(help='Directory to create the persistent environment in')] = None, skip_source: Annotated[bool, cyclopts.Parameter(help='Skip source preparation (e.g., git clone)')] = False) -> None
```

--------------------------------

### Authenticate FastMCP Client with GitHub OAuth

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/github.mdx

This Python script demonstrates how a FastMCP client connects to an OAuth-protected server. It automatically handles the GitHub OAuth flow, opening a browser for user authorization on the first connection, then uses the retrieved token to call a protected tool.

```python
from fastmcp import Client
import asyncio

async def main():
    # The client will automatically handle GitHub OAuth
    async with Client("http://localhost:8000/mcp", auth="oauth") as client:
        # First-time connection will open GitHub login in your browser
        print("✓ Authenticated with GitHub!")
        
        # Test the protected tool
        result = await client.call_tool("get_user_info")
        print(f"GitHub user: {result['github_user']}")

if __name__ == "__main__":
    asyncio.run(main())
```

--------------------------------

### Configure FastMCP Server for Production Google OAuth with Persistent Storage in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/google.mdx

This Python code configures a `FastMCP` server for production environments using Google OAuth. It utilizes `GoogleProvider` along with `RedisStore` for persistent token storage and `FernetEncryptionWrapper` for encrypting sensitive OAuth tokens at rest. Essential parameters like `jwt_signing_key` and `client_storage` are configured using environment variables for security and resilience across server restarts. Dependencies include `fastmcp`, `key_value.aio.stores.redis`, `key_value.aio.wrappers.encryption`, and `cryptography.fernet`.

```python
import os
from fastmcp import FastMCP
from fastmcp.server.auth.providers.google import GoogleProvider
from key_value.aio.stores.redis import RedisStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper
from cryptography.fernet import Fernet

# Production setup with encrypted persistent token storage
auth_provider = GoogleProvider(
    client_id="123456789.apps.googleusercontent.com",
    client_secret="GOCSPX-abc123...",
    base_url="https://your-production-domain.com",
    required_scopes=["openid", "https://www.googleapis.com/auth/userinfo.email"],

    # Production token management
    jwt_signing_key=os.environ["JWT_SIGNING_KEY"],
    client_storage=FernetEncryptionWrapper(
        key_value=RedisStore(
            host=os.environ["REDIS_HOST"],
            port=int(os.environ["REDIS_PORT"])
        ),
        fernet=Fernet(os.environ["STORAGE_ENCRYPTION_KEY"])
    )
)

mcp = FastMCP(name="Production Google App", auth=auth_provider)
```

--------------------------------

### Set Environment Variables for FastMCP Server Installation

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/gemini-cli.mdx

This command demonstrates how to pass environment variables (e.g., API_KEY, DEBUG) directly to the FastMCP server during installation using the `--env` flag. This is crucial for configuring server behavior or credentials.

```bash
fastmcp install gemini-cli server.py --server-name "Weather Server" \
  --env API_KEY=your-api-key \
  --env DEBUG=true
```

--------------------------------

### Read Resource by URI in fastmcp Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-context.mdx

Reads a resource from the server using its URI. This function takes a URI (string or AnyUrl) as input and returns the content of the resource, which can be either text or bytes encapsulated in a list of `ReadResourceContents`. It's essential for accessing external data within the fastmcp environment.

```python
read_resource(self, uri: str | AnyUrl) -> list[ReadResourceContents]
```

--------------------------------

### Specify FastMCP Server Entrypoint during Installation via CLI

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/claude-code.mdx

These commands illustrate how to explicitly define the FastMCP server object during installation using the `file.py:object` notation. If the object name is not specified, the CLI defaults to looking for `mcp`, `server`, or `app`.

```bash
# These are equivalent if your server object is named 'mcp'
fastmcp install claude-code server.py
fastmcp install claude-code server.py:mcp

# Use explicit object name if your server has a different name
fastmcp install claude-code server.py:my_custom_server
```

--------------------------------

### Install FastMCP Server with Explicit Python Entrypoint (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

Shows how to explicitly define the server entrypoint within a Python file, for example, `server.py:my_server`. This is essential when the server instance is not named `mcp`, `server`, or `app`, ensuring `fastmcp` correctly identifies and runs your application.

```bash
fastmcp install claude-desktop server.py:my_server
```

--------------------------------

### Test FastMCP server with HTTP transport manually

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

The `fastmcp dev` command does not support HTTP testing. To test a server over Streamable HTTP or SSE, you must start your server manually with the appropriate transport. Then, open the MCP Inspector separately and connect to your running server.

```bash
fastmcp run server.py --transport http
```

```bash
python server.py  # Assuming your __main__ block sets Streamable HTTP transport
```

--------------------------------

### Interact with FastMCP Server Tools in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/client.mdx

Shows how to list available server-side tools and execute a specific tool with arguments. Tools are functions exposed by the server that the client can call.

```python
async with client:
    # List available tools
    tools = await client.list_tools()
    
    # Execute a tool
    result = await client.call_tool("multiply", {"a": 5, "b": 3})
    print(result.data)
```

--------------------------------

### Call FastMCP Server with Anthropic Messages API (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/anthropic.mdx

This Python code demonstrates how to call a FastMCP server using the Anthropic Messages API. It initializes an Anthropic client, then creates a message with a user prompt and specifies the MCP server URL. It's crucial to replace the placeholder URL and include the `anthropic-beta` header.

```python
import anthropic
from rich import print

# Your server URL (replace with your actual URL)
url = 'https://your-server-url.com'

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    messages=[{"role": "user", "content": "Roll a few dice!"}],
    mcp_servers=[
        {
            "type": "url",
            "url": f"{url}/mcp/",
            "name": "dice-server",
        }
    ],
    extra_headers={
        "anthropic-beta": "mcp-client-2025-04-04"
    }
)

print(response.content)
```

--------------------------------

### Install FastMCP Server in Claude Desktop (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-cli-install-claude_desktop.mdx

This Python function installs a FastMCP server into the Claude Desktop environment. It requires the path to the server file, an optional server object name, and a display name for the server within Claude's configuration. The function returns 'True' if the installation is successful, 'False' otherwise, and supports various optional parameters for customization like editable installs, additional packages, environment variables, and Python versions.

```python
install_claude_desktop(file: Path, server_object: str | None, name: str) -> bool
```

--------------------------------

### List All Prompts and Access Metadata

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/prompts.mdx

Retrieves all available prompt templates from an MCP server. It iterates through the prompts, printing their names, descriptions, arguments, and any FastMCP-specific tags found in the metadata. This function requires an active client connection.

```python
async with client:
    prompts = await client.list_prompts()
    # prompts -> list[mcp.types.Prompt]
    
    for prompt in prompts:
        print(f"Prompt: {prompt.name}")
        print(f"Description: {prompt.description}")
        if prompt.arguments:
            print(f"Arguments: {[arg.name for arg in prompt.arguments]}")
        # Access tags and other metadata
        if hasattr(prompt, '_meta') and prompt._meta:
            fastmcp_meta = prompt._meta.get('_fastmcp', {})
            print(f"Tags: {fastmcp_meta.get('tags', [])}")
```

--------------------------------

### Initialize FastMCP Starlette routing constants in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/http.mdx

This Python snippet demonstrates the initial setup for defining routing constants (`ROOT_URL`, `MOUNT_PREFIX`, `MCP_PATH`) when building a FastMCP application with Starlette. These constants are used to clearly establish the URL structure for an OAuth-protected server mounted under a prefix.

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.github import GitHubProvider
from starlette.applications import Starlette
from starlette.routing import Mount

# Define the routing structure
ROOT_URL = "http://localhost:8000"
MOUNT_PREFIX = "/api"
MCP_PATH = "/mcp"
```

--------------------------------

### Test Authenticated Tool Access in FastMCP with Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/development/tests.mdx

Demonstrates how to write a clear and concise test for an authenticated FastMCP tool. It sets up a FastMCP server with a bearer token provider, defines a protected tool, and then uses a client with a valid token to call the tool, asserting the successful result.

```python
async def test_authenticated_tool_requires_valid_token():
    """Test that authenticated users can access protected tools."""
    mcp = FastMCP("test-server")
    mcp.auth = BearerTokenProvider({"secret-token": "test-user"})
    
    @mcp.tool
    def protected_action() -> str:
        return "success"
    
    async with Client(mcp, auth=BearerAuth("secret-token")) as client:
        result = await client.call_tool("protected_action", {})
        assert result.content[0].text == "success"
```

--------------------------------

### Create a FastMCP Proxy Server with Session Isolation

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/proxy.mdx

This example demonstrates how to set up a FastMCP server to act as a proxy for a backend MCP server using `FastMCP.as_proxy()` and `ProxyClient`. This configuration ensures safe concurrent request handling and automatically forwards advanced MCP features by creating fresh isolated sessions for each client request.

```python
from fastmcp import FastMCP
from fastmcp.server.proxy import ProxyClient

# Create a proxy with full MCP feature support
proxy = FastMCP.as_proxy(
    ProxyClient("backend_server.py"),
    name="MyProxy"
)

# Run the proxy (e.g., via stdio for Claude Desktop)
if __name__ == "__main__":
    proxy.run()
```

--------------------------------

### Configure FastMCP Server Using JSON Configuration File

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/mcp-json-configuration.mdx

Defines a FastMCP server configuration using a fastmcp.json file with schema validation. The configuration specifies the source file, entrypoint, and environment dependencies. This is the recommended approach for complex server setups.

```json
{
  "$schema": "https://gofastmcp.com/public/schemas/fastmcp.json/v1.json",
  "source": {
    "path": "server.py",
    "entrypoint": "mcp"
  },
  "environment": {
    "dependencies": ["pandas", "matplotlib", "seaborn"]
  }
}
```

--------------------------------

### Create Complete HTML Page with FastMCP Styling (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-utilities-ui.mdx

This function constructs a complete HTML page with FastMCP's predefined styling. It accepts the main HTML content, a page title, optional additional CSS, and a Content Security Policy, returning the full HTML string. It is a foundational utility for rendering consistent and secure user interfaces.

```python
create_page(content: str, title: str = 'FastMCP', additional_styles: str = '', csp_policy: str = "default-src 'none'; style-src 'unsafe-inline'; img-src https: data:; base-uri 'none'") -> str
```

--------------------------------

### Register Multiple URI Templates for Single Function in FastMCP Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/resources.mdx

Shows how to register a single function with multiple URI patterns by manually applying multiple resource decorators. This enables the same function to be accessed through different URI schemes (e.g., by email or by name). Each template exposes different required parameters while others remain None, allowing flexible resource access patterns while maintaining a single implementation.

```python
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")

# Define a user lookup function that can be accessed by different identifiers
def lookup_user(name: str | None = None, email: str | None = None) -> dict:
    """Look up a user by either name or email."""
    if email:
        return find_user_by_email(email)  # pseudocode
    elif name:
        return find_user_by_name(name)  # pseudocode
    else:
        return {"error": "No lookup parameters provided"}

# Manually apply multiple decorators to the same function
mcp.resource("users://email/{email}")(lookup_user)
mcp.resource("users://name/{name}")(lookup_user)
```

--------------------------------

### Get HTTP Request Headers Safely in FastMCP Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/context.mdx

This snippet demonstrates using `get_http_headers()` in FastMCP to safely retrieve request headers. It returns an empty dictionary if no request context is available and by default excludes problematic headers like 'host'. To include all headers, set `include_all=True`.

```python
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers

mcp = FastMCP(name="Headers Demo")

@mcp.tool
async def safe_header_info() -> dict:
    """Safely get header information without raising errors."""
    # Get headers (returns empty dict if no request context)
    headers = get_http_headers()
    
    # Get authorization header
    auth_header = headers.get("authorization", "")
    is_bearer = auth_header.startswith("Bearer ")
    
    return {
        "user_agent": headers.get("user-agent", "Unknown"),
        "content_type": headers.get("content-type", "Unknown"),
        "has_auth": bool(auth_header),
        "auth_type": "Bearer" if is_bearer else "Other" if auth_header else "None",
        "headers_count": len(headers)
    }
```

--------------------------------

### Generate a unique name for fastmcp resources (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-client.mdx

The `generate_name` class method provides functionality to create a new name, optionally based on a provided string. It returns a string that can be used for naming resources within the fastmcp system.

```python
generate_name(cls, name: str | None = None) -> str
```

--------------------------------

### Recommended FastMCP Static Method Registration

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/decorating-methods.mdx

This pattern shows the preferred way to register static methods with FastMCP. The static method is defined first, and then explicitly registered with the FastMCP instance (e.g., `mcp.tool(MyClass.utility)`). This ensures proper method binding and avoids issues with decorator return values.

```python
from fastmcp import FastMCP

mcp = FastMCP()

class MyClass:
    @staticmethod
    def utility(x, y):
        return x + y

# This also works
mcp.tool(MyClass.utility)
```

--------------------------------

### Mount FastMCP routes in Starlette application in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/http.mdx

This Python snippet shows how to assemble a Starlette application by mounting FastMCP's discovery routes at the root level and its operational routes under a specified prefix. This ensures RFC compliance for discovery endpoints while allowing the main MCP application to operate within a sub-path.

```python
app = Starlette(
    routes=[
        *well_known_routes, # Discovery routes at root level
        Mount(MOUNT_PREFIX, app=mcp_app), # Operational routes under prefix
    ],
    lifespan=mcp_app.lifespan,
)
```

--------------------------------

### Register Custom HTTP Route with FastMCP Server

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

This decorator registers a custom HTTP route on the FastMCP server, allowing the creation of arbitrary endpoints for purposes like OAuth callbacks, health checks, or admin APIs. The handler function must be an asynchronous function that accepts a Starlette Request and returns a Response.

```python
custom_route(self, path: str, methods: list[str], name: str | None = None, include_in_schema: bool = True) -> Callable[[Callable[[Request], Awaitable[Response]]], Callable[[Request], Awaitable[Response]]]
```

--------------------------------

### Configure FastMCP Client with Persistent Disk Storage for OAuth Tokens in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/storage-backends.mdx

Configures a FastMCP OAuth client with disk-based token storage for persistence across client restarts. By default, tokens are stored in memory only. This configuration allows clients to reconnect without re-authenticating by persisting tokens to disk.

```python
from fastmcp.client.auth import OAuthClientProvider
from key_value.aio.stores.disk import DiskStore

# Store tokens on disk for persistence across restarts
token_storage = DiskStore(directory="~/.local/share/fastmcp/tokens")

oauth_provider = OAuthClientProvider(
    mcp_url="https://your-mcp-server.com/mcp/sse",
    token_storage=token_storage
)
```

--------------------------------

### Configure FastMCP with Custom Route Maps for GET Requests

Source: https://github.com/jlowin/fastmcp/blob/main/docs/tutorials/rest-api.mdx

This Python script demonstrates how to configure a FastMCP server to use custom route maps. It initializes an HTTP client for a target API and defines a simplified OpenAPI specification. The `FastMCP.from_openapi` method is then used with a list of `RouteMap` objects to specify that `GET` requests with path parameters should be converted to `MCPType.RESOURCE_TEMPLATE` and all other `GET` requests to `MCPType.RESOURCE`, altering the default `Tool` conversion.

```python
import httpx
from fastmcp import FastMCP
from fastmcp.server.openapi import RouteMap, MCPType


# Create an HTTP client for the target API
client = httpx.AsyncClient(base_url="https://jsonplaceholder.typicode.com")

# Define a simplified OpenAPI spec for JSONPlaceholder
openapi_spec = {
    "openapi": "3.0.0",
    "info": {"title": "JSONPlaceholder API", "version": "1.0"},
    "paths": {
        "/users": {
            "get": {
                "summary": "Get all users",
                "operationId": "get_users",
                "responses": {"200": {"description": "A list of users."}}
            }
        },
        "/users/{id}": {
            "get": {
                "summary": "Get a user by ID",
                "operationId": "get_user_by_id",
                "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
                "responses": {"200": {"description": "A single user."}}
            }
        }
    }
}

# Create the MCP server with custom route mapping
mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
    name="JSONPlaceholder MCP Server",
    route_maps=[
        # Map GET requests with path parameters (e.g., /users/{id}) to ResourceTemplate
        RouteMap(methods=["GET"], pattern=r".*\{.*\}.*", mcp_type=MCPType.RESOURCE_TEMPLATE),
        # Map all other GET requests to Resource
        RouteMap(methods=["GET"], mcp_type=MCPType.RESOURCE),
    ]
)

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
```

--------------------------------

### MCP Client Invoking Prompt with JSON String Arguments

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/prompts.mdx

Illustrates how an MCP client would call a FastMCP prompt, providing all arguments as JSON strings, as required by the MCP specification. FastMCP then handles the type conversion internally, allowing the Python function to receive native types.

```json
{
  "numbers": "[1, 2, 3, 4, 5]",
  "metadata": "{\"source\": \"api\", \"version\": \"1.0\"}",
  "threshold": "2.5"
}
```

--------------------------------

### Add Custom HTTP Routes to FastMCP Server in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/server.mdx

This snippet illustrates how to add custom web routes to a FastMCP server running with HTTP transport using the `@mcp.custom_route` decorator. This is useful for simple endpoints like health checks that need to be served alongside your MCP endpoint.

```python
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

mcp = FastMCP("MyServer")

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")

if __name__ == "__main__":
    mcp.run(transport="http")  # Health check at http://localhost:8000/health
```

--------------------------------

### Install FastMCP Server with fastmcp.json Configuration (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

Illustrates how to install a FastMCP server using a `fastmcp.json` configuration file. The command can automatically detect `fastmcp.json` in the current directory or accept a specific path to a configuration file. This method simplifies server setup by centralizing dependencies and settings.

```bash
fastmcp install claude-desktop
fastmcp install claude-desktop my-config.fastmcp.json
```

--------------------------------

### Handle messages with ErrorHandlingMiddleware in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-middleware-error_handling.mdx

This method of `ErrorHandlingMiddleware` intercepts incoming messages to provide consistent error handling and logging. It catches exceptions, logs them, and converts them into structured MCP error responses. It takes a `MiddlewareContext` and a `CallNext` function as input, returning an arbitrary type.

```python
on_message(self, context: MiddlewareContext, call_next: CallNext) -> Any
```

--------------------------------

### Create MCP Resource for System Status using FastMCP in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/tutorials/mcp.mdx

Shows how to expose read-only data as an MCP resource using the @mcp.resource decorator with a URI identifier. Resources function like GET requests, providing idempotent data retrieval without side effects. This example returns system operational status at the URI 'system://status'.

```python
from fastmcp import FastMCP

mcp = FastMCP()

# This function provides a resource at the URI "system://status"
@mcp.resource("system://status")
def get_system_status() -> dict:
    """Returns the current operational status of the service."""
    return {"status": "all systems normal"}
```

--------------------------------

### Convert MCPConfig to servers and transports in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-utilities-mcp_config.mdx

This utility function processes an `MCPConfig` object, iterating through its entries to generate a list of server and client transport tuples. It takes an `MCPConfig` object as input and returns a list of tuples, each containing a string identifier, a `FastMCP` instance, and a `ClientTransport` instance.

```python
mcp_config_to_servers_and_transports(config: MCPConfig) -> list[tuple[str, FastMCP[Any], ClientTransport]]
```

--------------------------------

### Manage Context State with FastMCP Middleware and Tools (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/context.mdx

This example demonstrates how FastMCP's `Context` object can be used to store and retrieve data during a single request. A middleware (`UserAuthMiddleware`) sets `user_id` and `permissions` in the context state, which are then accessed by a tool (`secure_operation`). Context state is isolated per request and ensures predictable data flow between middleware and handlers.

```python
from fastmcp.server.middleware import Middleware, MiddlewareContext

class UserAuthMiddleware(Middleware):
    async def on_call_tool(self, context: MiddlewareContext, call_next):

        # Middleware stores user info in context state
        context.fastmcp_context.set_state("user_id", "user_123")
        context.fastmcp_context.set_state("permissions", ["read", "write"])

        return await call_next(context)

@mcp.tool
async def secure_operation(data: str, ctx: Context) -> str:
    """Tool can access state set by middleware."""

    user_id = ctx.get_state("user_id")  # "user_123"
    permissions = ctx.get_state("permissions")  # ["read", "write"]
    
    if "write" not in permissions:
        return "Access denied"
    
    return f"Processing {data} for user {user_id}"
```

--------------------------------

### Access FastMCP Global Settings (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/server.mdx

Explains how to access and inspect FastMCP's global configuration settings, which can be defined via environment variables (prefixed with `FASTMCP_`) or a `.env` file. The example demonstrates printing the default values for common settings like `log_level`, `mask_error_details`, and `strict_input_validation`.

```python
import fastmcp

# Access global settings
print(fastmcp.settings.log_level)        # Default: "INFO"
print(fastmcp.settings.mask_error_details)  # Default: False
print(fastmcp.settings.resource_prefix_format)  # Default: "path"
print(fastmcp.settings.strict_input_validation)  # Default: False
print(fastmcp.settings.include_fastmcp_meta)   # Default: True
```

--------------------------------

### Load Environment Variables from .env file for FastMCP Server Installation via CLI

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/claude-code.mdx

This command demonstrates how to load environment variables for your FastMCP server from a `.env` file during installation. The `--env-file` flag simplifies managing multiple environment variables.

```bash
fastmcp install claude-code server.py --server-name "Weather Server" --env-file .env
```

--------------------------------

### Install FastMCP Server with Editable Local Packages via CLI

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/claude-code.mdx

This command illustrates how to install local Python packages in editable mode using the `--with-editable` flag during FastMCP server installation. This is useful for developing and testing local packages that your server depends on.

```bash
fastmcp install claude-code server.py --with-editable ./my-local-package
```

--------------------------------

### Initialize FastMCP Server with Environment-Configured Authentication in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/auth/authentication.mdx

Initialize a FastMCP server instance in Python, which automatically picks up authentication configurations from environment variables. This approach simplifies deployment by externalizing authentication setup, adhering to twelve-factor app principles.

```python
from fastmcp import FastMCP

# Authentication automatically configured from environment
mcp = FastMCP(name="My Server")
```

--------------------------------

### Configure FastMCP Tool for Creative Writing with Specific Model Preferences (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/sampling.mdx

This Python `fastmcp` tool demonstrates how to generate creative content by explicitly setting `model_preferences` to 'claude-3-sonnet' within `ctx.sample`. It uses a high `temperature` for creativity and includes server context, returning the generated text.

```python
@mcp.tool
async def creative_writing(topic: str, ctx: Context) -> str:
    """Generate creative content using a specific model."""
    response = await ctx.sample(
        messages=f"Write a creative short story about {topic}",
        model_preferences="claude-3-sonnet",  # Prefer a specific model
        include_context="thisServer",  # Use the server's context
        temperature=0.9,  # High creativity
        max_tokens=1000
    )
    
    return response.text
```

--------------------------------

### Set GitHub OAuth credentials as environment variables (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/examples/auth/github_oauth/README.md

Before running the FastMCP server, configure the GitHub OAuth Client ID and Client Secret as environment variables. These credentials allow the FastMCP server to interact with the GitHub OAuth service for user authentication.

```bash
export FASTMCP_SERVER_AUTH_GITHUB_CLIENT_ID="your-client-id"
export FASTMCP_SERVER_AUTH_GITHUB_CLIENT_SECRET="your-client-secret"
```

--------------------------------

### ToolInjectionMiddleware for FastMCP server

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-middleware-tool_injection.mdx

A middleware class for injecting tools into the FastMCP server context. It handles the `on_list_tools` and `on_call_tool` events to manage tool availability and execution.

```python
class ToolInjectionMiddleware:
    """A middleware for injecting tools into the context."""

    def on_list_tools(self, context: MiddlewareContext[mcp.types.ListToolsRequest], call_next: CallNext[mcp.types.ListToolsRequest, Sequence[Tool]]) -> Sequence[Tool]:
        """Inject tools into the response."""
        pass

    def on_call_tool(self, context: MiddlewareContext[mcp.types.CallToolRequestParams], call_next: CallNext[mcp.types.CallToolRequestParams, ToolResult]) -> ToolResult:
        """Intercept tool calls to injected tools."""
        pass
```

--------------------------------

### Create and Mount a FastMCP Proxy Server (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/composition.mdx

This Python code illustrates how to create a proxy for a remote FastMCP server using `FastMCP.as_proxy()` and subsequently mount it into another server. Mounting a server that was created as a proxy will always result in proxy mounting, ensuring full client lifecycle events.

```python
# Create a proxy for a remote server
remote_proxy = FastMCP.as_proxy(Client("http://example.com/mcp"))

# Mount the proxy (always uses proxy mounting)
main_server.mount(remote_proxy, prefix="remote")
```

--------------------------------

### Install FastMCP Server from .env File (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

Shows how to load environment variables for the FastMCP server from a `.env` file during installation using the `--env-file` option. This provides a convenient and organized way to manage multiple environment variables without cluttering the command line.

```bash
fastmcp install cursor server.py --env-file .env
```

--------------------------------

### Specify Project Directory for FastMCP Server Installation

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/gemini-cli.mdx

This command allows you to specify a project directory using the `--project` flag, ensuring that the FastMCP server runs within that project's context and utilizes its configuration files and virtual environment via `uv`.

```bash
fastmcp install gemini-cli server.py --project /path/to/my-project
```

--------------------------------

### Configure FastMCP Prompts with Decorator Options in Python

Source: https://github.com/jlowin/fastmcp/blob/main/src/fastmcp/contrib/mcp_mixin/README.md

This section illustrates how to define methods as FastMCP prompts using the `@mcp_prompt` decorator. It includes examples for a basic prompt, a disabled prompt, and a prompt with additional `title`, `description`, and `meta`data. Prompts are designed to generate conversational or instructional text based on input, often for AI models.

```python
@mcp_prompt(name="A prompt")
def prompt_method(self, name):
    return f"What's up {name}?"
```

```python
# disabled prompt
@mcp_prompt(name="A prompt", enabled=False)
def prompt_method(self, name):
    return f"What's up {name}?"
```

```python
# example prompt w/title and meta
@mcp_prompt(
    name="analysis_prompt",
    title="Data Analysis Prompt",
    description="Analyzes data patterns",
    meta={"complexity": "high", "domain": "analytics", "requires_context": True}
)
def analysis_prompt_method(self, dataset: str):
    return f"Analyze the patterns in {dataset}"
```

--------------------------------

### Implement Catch-All Route Exclusion in FastMCP (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openapi.mdx

This example shows how to implement a catch-all exclusion rule in FastMCP, preventing any routes not explicitly handled by preceding `RouteMap` entries from being processed. This effectively creates an allow-list, where only routes matching custom maps are included, and all others are excluded, overriding default routing behavior.

```python
from fastmcp import FastMCP
from fastmcp.server.openapi import RouteMap, MCPType

mcp = FastMCP.from_openapi(
    openapi_spec=spec,
    client=client,
    route_maps=[
        # custom mapping logic goes here
        # ... your specific route maps ...
        # exclude all remaining routes
        RouteMap(mcp_type=MCPType.EXCLUDE),
    ],
)
```

--------------------------------

### GET /server/app/streamable-http

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

Creates a Starlette application configured for Streamable HTTP transport.

```APIDOC
## GET /server/app/streamable-http

### Description
Create a Starlette app for the StreamableHTTP server.

### Method
GET

### Endpoint
/server/app/streamable-http

### Parameters
- **path** (str) - Optional - The path to the StreamableHTTP endpoint
- **middleware** (list[ASGIMiddleware]) - Optional - A list of middleware to apply to the app

### Response
#### Success Response (200)
- **app** (StarletteWithLifespan) - The configured Starlette application for Streamable HTTP.
```

--------------------------------

### Authenticate Remote MCP Connection with BearerAuth Helper in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/transports.mdx

Shows the convenience authentication helper for connecting to remote MCP servers. The BearerAuth helper simplifies adding Bearer token authentication to client connections, providing a cleaner alternative to manually setting Authorization headers.

```python
from fastmcp.client.auth import BearerAuth

client = Client(
    "https://api.example.com/mcp",
    auth=BearerAuth("your-token-here")
)
```

--------------------------------

### Create GitHub OAuth Provider for FastMCP in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/http.mdx

This Python snippet shows how to instantiate a `GitHubProvider` for FastMCP, configuring it with client credentials, `issuer_url` for discovery metadata at the root, and `base_url` for operational endpoints under a defined prefix. This setup is crucial for handling OAuth authentication correctly when the application is mounted under a path.

```python
auth = GitHubProvider(
    client_id="your-client-id",
    client_secret="your-client-secret",
    issuer_url=ROOT_URL, # Discovery metadata at root
    base_url=f"{ROOT_URL}{MOUNT_PREFIX}", # Operational endpoints under prefix
)
```

--------------------------------

### Report Percentage-Based Progress in FastMCP (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/progress.mdx

Illustrates how to report progress as a percentage (0-100) using `ctx.report_progress()`. This pattern is suitable for operations where a clear total can be defined, allowing clients to display accurate progress bars.

```python
@mcp.tool
async def download_file(url: str, ctx: Context) -> str:
    """Download a file with percentage progress."""
    total_size = 1000  # KB
    downloaded = 0
    
    while downloaded < total_size:
        # Download chunk
        chunk_size = min(50, total_size - downloaded)
        downloaded += chunk_size
        
        # Report percentage progress
        percentage = (downloaded / total_size) * 100
        await ctx.report_progress(progress=percentage, total=100)
        
        await asyncio.sleep(0.1)  # Simulate download time
    
    return f"Downloaded file from {url}"
```

--------------------------------

### Time MCP List Operations with DetailedTimingMiddleware in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-middleware-timing.mdx

Methods for timing various list operations in MCP servers including listing tools, resources, resource templates, and prompts. Each method follows the same pattern of accepting MiddlewareContext and CallNext parameters to measure operation performance.

```python
on_list_tools(self, context: MiddlewareContext, call_next: CallNext) -> Any
```

```python
on_list_resources(self, context: MiddlewareContext, call_next: CallNext) -> Any
```

```python
on_list_resource_templates(self, context: MiddlewareContext, call_next: CallNext) -> Any
```

```python
on_list_prompts(self, context: MiddlewareContext, call_next: CallNext) -> Any
```

--------------------------------

### Run a FastMCP Server with CLI (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/running-server.mdx

This command initiates a FastMCP server directly from the command line, automatically detecting a `FastMCP` instance within `server.py`. It provides a quick way to run servers without modifying source code, suitable for local execution and testing.

```bash
fastmcp run server.py
```

--------------------------------

### Pre-build FastMCP Project Environments via CLI

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/server-configuration.mdx

This Bash command shows how to use `fastmcp project prepare` to create a persistent `uv` project. This process pre-installs all necessary dependencies, streamlining subsequent server runs and ensuring a consistent and optimized environment for your FastMCP application.

```bash
fastmcp project prepare
```

--------------------------------

### Customize FastMCP Tool Output Serialization to YAML (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/server.mdx

This Python snippet illustrates how to customize the serialization of tool return values by providing a `tool_serializer` function during `FastMCP` server initialization. The example uses the `PyYAML` library to convert non-string tool outputs, such as dictionaries, into YAML format, offering fine-grained control over the response structure. The custom serializer is applied to all non-string return values from tools, bypassing it for pre-formatted strings.

```python
import yaml
from fastmcp import FastMCP

# Define a custom serializer that formats dictionaries as YAML
def yaml_serializer(data):
    return yaml.dump(data, sort_keys=False)

# Create a server with the custom serializer
mcp = FastMCP(name="MyServer", tool_serializer=yaml_serializer)

@mcp.tool
def get_config():
    """Returns configuration in YAML format."""
    return {"api_key": "abc123", "debug": True, "rate_limit": 100}
```

--------------------------------

### Manual Image Content Conversion with FastMCP

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/tools.mdx

This Python snippet demonstrates how to manually convert an image file into a structured image content block suitable for FastMCP, using the `Image` helper class and its `to_image_content()` method. It returns a dictionary containing the image content.

```python
return {"image": Image(path="chart.png").to_image_content()}
```

--------------------------------

### Add Python Dependencies to MCP Server Configuration with FastMCP

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/mcp-json-configuration.mdx

These `fastmcp` commands demonstrate how to include Python package dependencies in the generated MCP server configuration. You can specify single or multiple packages using the `--with` flag, and also include editable local packages with `--with-editable`.

```bash
# Single package
fastmcp install mcp-json server.py --with pandas

# Multiple packages  
fastmcp install mcp-json server.py --with pandas --with requests --with httpx

# Editable local package
fastmcp install mcp-json server.py --with-editable ./my-package
```

--------------------------------

### Send Completion Request and Get Full MCP Result (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-client.mdx

This Python method sends a completion request to the server, returning the full `mcp.types.CompleteResult` protocol object. It requires a reference (`ref`), arguments for the completion, and optional context arguments. A `RuntimeError` is raised if the client is not connected.

```python
complete_mcp(self, ref: mcp.types.ResourceTemplateReference | mcp.types.PromptReference, argument: dict[str, str], context_arguments: dict[str, Any] | None = None) -> mcp.types.CompleteResult
```

--------------------------------

### Testing FastMCP Network Transport In-Process with pytest and run_server_async

Source: https://github.com/jlowin/fastmcp/blob/main/docs/development/tests.mdx

Shows the preferred method for testing FastMCP network transports using `run_server_async` within the same process. This approach integrates with `pytest` fixtures, providing fast and deterministic tests with full debugger support for HTTP transport scenarios, automatically handling server lifecycle and cleanup.

```python
import pytest
from fastmcp import FastMCP, Client
from fastmcp.client.transports import StreamableHttpTransport
from fastmcp.utilities.tests import run_server_async

def create_test_server() -> FastMCP:
    """Create a test server instance."""
    server = FastMCP("TestServer")

    @server.tool
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    return server

@pytest.fixture
async def http_server() -> str:
    """Start server in-process for testing."""
    server = create_test_server()
    async with run_server_async(server) as url:
        yield url

async def test_http_transport(http_server: str):
    """Test actual HTTP transport behavior."""
    async with Client(
        transport=StreamableHttpTransport(http_server)
    ) as client:
        result = await client.ping()
        assert result is True

        greeting = await client.call_tool("greet", {"name": "World"})
        assert greeting.data == "Hello, World!"
```

--------------------------------

### Define Default OpenAPI Route Mapping in FastMCP (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openapi.mdx

Shows FastMCP's default `RouteMap` configuration, which converts all OpenAPI routes into MCP `TOOL` components. This provides a simple starting point for making all API functionality available to LLM clients that primarily support MCP tools.

```python
from fastmcp.server.openapi import RouteMap, MCPType

DEFAULT_ROUTE_MAPPINGS = [
    # All routes become tools
    RouteMap(mcp_type=MCPType.TOOL),
]
```

--------------------------------

### Logging Messages via FastMCP Context (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/context.mdx

Shows how to send various log levels (debug, info, warning, error) back to the MCP client for visibility into function execution. This allows developers to track the flow and status of their tools.

```python
await ctx.debug("Starting analysis")
await ctx.info(f"Processing {len(data)} items") 
await ctx.warning("Deprecated parameter used")
await ctx.error("Processing failed")
```

--------------------------------

### Deny FastMCP Tool Calls with Middleware in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

This Python middleware example demonstrates how to deny access to specific tools by raising a `ToolError` within the `on_call_tool` hook. It checks the tool name and prevents execution for restricted tools like 'delete' or 'admin_config', ensuring proper error propagation through the FastMCP error handling system.

```python
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.exceptions import ToolError

class AuthMiddleware(Middleware):
    async def on_call_tool(self, context: MiddlewareContext, call_next):
        tool_name = context.message.name
        
        # Deny access to restricted tools
        if tool_name.lower() in ["delete", "admin_config"]:
            raise ToolError("Access denied: tool requires admin privileges")
        
        # Allow other tools to proceed
        return await call_next(context)
```

--------------------------------

### Run `fastmcp dev` with editable packages and additional dependencies

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

Demonstrates how to run the `fastmcp dev` server, installing a local project in editable mode (`-e .`) and including additional packages like `pandas` and `matplotlib` for testing. The `--with` flag can be used multiple times for various packages.

```bash
fastmcp dev server.py -e . --with pandas --with matplotlib
```

--------------------------------

### call_tool_mcp

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-client.mdx

Send a tools/call request and retrieve the complete MCP protocol result, including error flags if applicable.

```APIDOC
## FUNCTION CALL call_tool_mcp

### Description
Send a tools/call request and return the complete MCP protocol result. This method returns the raw CallToolResult object, which includes an isError flag and other metadata. It does not raise an exception if the tool call results in an error.

### Method
FUNCTION CALL

### Endpoint
call_tool_mcp

### Parameters
#### Request Body
- **name** (str) - Required - The name of the tool to call.
- **arguments** (dict[str, Any]) - Required - Arguments to pass to the tool.
- **timeout** (datetime.timedelta | float | int | None) - Optional - The timeout for the tool call.
- **progress_handler** (ProgressHandler | None) - Optional - The progress handler to use for the tool call.

### Request Example
```json
{
  "name": "search_web",
  "arguments": {
    "query": "latest AI research"
  },
  "timeout": 30
}
```

### Response
#### Success Response (200)
- **result** (mcp.types.CallToolResult) - The complete response object from the protocol, containing the tool result and any additional metadata.

#### Response Example
```json
{
  "tool_name": "search_web",
  "output": {
    "results": [
      {
        "title": "Paper A",
        "url": "https://example.com/paperA"
      }
    ]
  },
  "isError": false,
  "metadata": {
    "duration": 1.5
  }
}
```
```

--------------------------------

### Define FastMCP Prompt with Optional Parameters

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/prompts.mdx

Demonstrates how to define a FastMCP prompt with both required and optional parameters using default values in Python. Parameters without default values are considered required, while those with defaults are optional, simplifying client interactions and providing flexibility.

```python
@mcp.prompt
def data_analysis_prompt(
    data_uri: str,                        # Required - no default value
    analysis_type: str = "summary",       # Optional - has default value
    include_charts: bool = False          # Optional - has default value
) -> str:
    """Creates a request to analyze data with specific parameters."""
    prompt = f"Please perform a '{analysis_type}' analysis on the data found at {data_uri}."
    if include_charts:
        prompt += " Include relevant charts and visualizations."
    return prompt
```

--------------------------------

### Set Environment Variables for FastMCP Server Installation via CLI

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/claude-code.mdx

This command illustrates how to pass environment variables directly to your FastMCP server during installation using the `--env` flag. This is crucial for providing API keys or other configuration settings required by your server.

```bash
fastmcp install claude-code server.py --server-name "Weather Server" \
  --env API_KEY=your-api-key \
  --env DEBUG=true
```

--------------------------------

### Create Middleware Wrapper in FastMCP Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-middleware-middleware.mdx

The `make_middleware_wrapper` function generates a callable that applies a single FastMCP middleware to a given context. This closure effectively bakes in the specific middleware and the subsequent `call_next` function, streamlining its integration into a middleware chain. It ensures that the wrapped function can be passed to other components expecting a `call_next` function.

```python
make_middleware_wrapper(middleware: Middleware, call_next: CallNext[T, R]) -> CallNext[T, R]
```

--------------------------------

### Mocking FastMCP Server External Dependencies with Python unittest.mock

Source: https://github.com/jlowin/fastmcp/blob/main/docs/development/tests.mdx

Demonstrates how to mock external asynchronous dependencies, like a database, for a FastMCP server using `unittest.mock.AsyncMock`. This allows for isolated unit testing of server tools without relying on actual external services, ensuring predictable test outcomes and simplifying test setup.

```python
from unittest.mock import AsyncMock

async def test_database_tool():
    server = FastMCP("DataServer")
    
    # Mock the database
    mock_db = AsyncMock()
    mock_db.fetch_users.return_value = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ]
    
    @server.tool
    async def list_users() -> list:
        return await mock_db.fetch_users()
    
    async with Client(server) as client:
        result = await client.call_tool("list_users", {})
        assert len(result.data) == 2
        assert result.data[0]["name"] == "Alice"
        mock_db.fetch_users.assert_called_once()
```

--------------------------------

### Configure CORS for Browser-Based FastMCP Clients (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/http.mdx

This Python code snippet configures `CORSMiddleware` for a FastMCP server to enable direct connections from browser-based clients, such as debugging tools or custom web apps. It specifies `allow_origins`, `allow_methods`, and crucial MCP-specific `allow_headers` (like `mcp-protocol-version`, `mcp-session-id`, `Authorization`) and `expose_headers` (`mcp-session-id`) for proper session management and secure communication.

```python
from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

mcp = FastMCP("MyServer")

# Configure CORS for browser-based clients
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins; use specific origins for security
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=[
            "mcp-protocol-version",
            "mcp-session-id",
            "Authorization",
            "Content-Type",
        ],
        expose_headers=["mcp-session-id"],
    )
]

app = mcp.http_app(middleware=middleware)
```

--------------------------------

### Save FastMCP Configuration to File and Use in Shell Scripts

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/mcp-json-configuration.mdx

Shows how to redirect FastMCP configuration output to a file and use it in shell scripts with jq for JSON processing. Useful for CI/CD pipelines and automation scripts that need to programmatically access configuration values.

```bash
# Save configuration to file
fastmcp install mcp-json server.py > mcp-config.json
```

```bash
#!/bin/bash
CONFIG=$(fastmcp install mcp-json server.py --name "CI Server")
echo "$CONFIG" | jq '."CI Server".command'
# Output: "uv"
```

--------------------------------

### Access FastMCP Server Instance from Context (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/context.mdx

This example shows how to retrieve the underlying FastMCP server instance using the `ctx.fastmcp` property. This allows direct interaction with server-level functionalities or access to server metadata, such as the server's name. This provides a way for tools to introspect or control parts of the server they are running on.

```python
@mcp.tool
async def my_tool(ctx: Context) -> None:
    # Access the FastMCP server instance
    server_name = ctx.fastmcp.name
    ...
```

--------------------------------

### Define Tool with Conditional Access using ABAC

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/permit.mdx

Define a FastMCP tool that incorporates Attribute-Based Access Control (ABAC) conditions based on its arguments. This example creates a `conditional_greet` tool that only allows access if the `number` argument is greater than 10, demonstrating granular policy enforcement.

```python
@mcp.tool
def conditional_greet(name: str, number: int) -> str:
    """Greet a user only if number > 10"""
    return f"Hello, {name}! Your number is {number}"
```

--------------------------------

### Create Auth0 Test Client

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/auth0.mdx

This Python code demonstrates how to create a test client that automatically handles Auth0 OAuth flows for authentication with a fastmcp server. It opens a browser for first-time logins and then makes an authenticated call to a tool. Dependencies include the 'fastmcp' and 'asyncio' libraries.

```python
from fastmcp import Client
import asyncio

async def main():
    # The client will automatically handle Auth0 OAuth flows
    async with Client("http://localhost:8000/mcp", auth="oauth") as client:
        # First-time connection will open Auth0 login in your browser
        print("✓ Authenticated with Auth0!")

        # Test the protected tool
        result = await client.call_tool("get_token_info")
        print(f"Auth0 audience: {result['audience']}")

if __name__ == "__main__":
    asyncio.run(main())
```

--------------------------------

### Configure FastMCP Server Mounting Modes (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/composition.mdx

This Python code demonstrates how to mount servers in FastMCP using both direct and proxy modes. It illustrates the default direct mounting behavior, explicit proxy mounting using the 'as_proxy=True' parameter, and mounting a server without a prefix for direct component access.

```python
# Direct mounting (default when no custom lifespan)
main_mcp.mount(api_server, prefix="api")

# Proxy mounting (preserves full client lifecycle)
main_mcp.mount(api_server, prefix="api", as_proxy=True)

# Mounting without a prefix (components accessible without prefixing)
main_mcp.mount(api_server)
```

--------------------------------

### Disable Specific FastMCP Feature Forwarding (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/proxy.mdx

This example shows how to selectively disable the forwarding of advanced MCP features by passing `None` to specific handler arguments in the `ProxyClient` constructor. This allows fine-grained control over which features are proxied.

```python
# Disable sampling but keep other features
backend = ProxyClient(
    "backend_server.py",
    sampling_handler=None,  # Disable LLM sampling forwarding
    log_handler=None        # Disable log forwarding
)
```

--------------------------------

### Run FastMCP Server with Legacy SSE Transport (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/running-server.mdx

This example illustrates how to start a FastMCP server using the legacy Server-Sent Events (SSE) transport. While still supported for backward compatibility, SSE has limitations compared to the newer Streamable HTTP transport, primarily offering only server-to-client streaming. It is not recommended for new projects.

```python
if __name__ == "__main__":
    # SSE transport - use HTTP instead for new projects
    mcp.run(transport="sse", host="127.0.0.1", port=8000)
```

--------------------------------

### Manage Multiple FastMCP Configuration Files (JSON, Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/server-configuration.mdx

This example demonstrates how to maintain separate FastMCP configuration files for different environments, such as `dev.fastmcp.json` for development and `prod.fastmcp.json` for production. It shows how to define environment-specific settings like log levels and dependencies, and then activate them using `fastmcp run` commands.

```json
{
  "$schema": "https://gofastmcp.com/public/schemas/fastmcp.json/v1.json",
  "source": {
    "path": "server.py",
    "entrypoint": "mcp"
  },
  "deployment": {
    "transport": "http",
    "log_level": "DEBUG"
  }
}
```

```json
{
  "$schema": "https://gofastmcp.com/public/schemas/fastmcp.json/v1.json",
  "source": {
    "path": "server.py",
    "entrypoint": "mcp"
  },
  "environment": {
    "requirements": "requirements/production.txt"
  },
  "deployment": {
    "transport": "http",
    "host": "0.0.0.0",
    "log_level": "WARNING"
  }
}
```

```bash
fastmcp run dev.fastmcp.json   # Development
fastmcp run prod.fastmcp.json  # Production
```

--------------------------------

### Implement FastMCP Client Elicitation Handler in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/elicitation.mdx

This Python code demonstrates how to define an asynchronous `elicitation_handler` for a FastMCP client. The handler receives a message, a Python dataclass `response_type` derived from the server's JSON schema, and contextual parameters. It prompts the user, constructs a structured response using the provided `response_type`, and returns the data, either directly or wrapped in an `ElicitResult` for explicit action control.

```python
from fastmcp import Client
from fastmcp.client.elicitation import ElicitResult

async def elicitation_handler(message: str, response_type: type, params, context):
    # Present the message to the user and collect input
    user_input = input(f"{message}: ")
    
    # Create response using the provided dataclass type
    # FastMCP converted the JSON schema to this Python type for you
    response_data = response_type(value=user_input)
    
    # You can return data directly - FastMCP will implicitly accept the elicitation
    return response_data
    
    # Or explicitly return an ElicitResult for more control
    # return ElicitResult(action="accept", content=response_data)

client = Client(
    "my_mcp_server.py",
    elicitation_handler=elicitation_handler,
)
```

--------------------------------

### Configure FastMCP with OAuth 2.0 Token Introspection in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-auth-providers-introspection.mdx

This example demonstrates how to set up FastMCP to use the `IntrospectionTokenVerifier` for OAuth 2.0 token validation. It initializes the verifier with an introspection URL, client credentials, and required scopes, then integrates it into a FastMCP application. This is suitable for validating opaque tokens from various OAuth providers.

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.introspection import IntrospectionTokenVerifier

# Verify opaque tokens via RFC 7662 introspection
verifier = IntrospectionTokenVerifier(
    introspection_url="https://auth.example.com/oauth/introspect",
    client_id="your-client-id",
    client_secret="your-client-secret",
    required_scopes=["read", "write"]
)

mcp = FastMCP("My Protected Server", auth=verifier)
```

--------------------------------

### Production FastMCP Server with Multiple Dependencies and Environment Variables

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/mcp-json-configuration.mdx

Configures a production-ready FastMCP server with multiple dependencies, custom name, and environment variables. The generated configuration includes all dependencies in the args array and environment variables in the env object. Suitable for production deployments.

```bash
fastmcp install mcp-json api_server.py \
  --name "Production API Server" \
  --with requests \
  --with python-dotenv \
  --env API_BASE_URL=https://api.example.com \
  --env TIMEOUT=30
```

```json
{
  "Production API Server": {
    "command": "uv",
    "args": [
      "run",
      "--with",
      "fastmcp",
      "--with",
      "python-dotenv", 
      "--with",
      "requests",
      "fastmcp",
      "run", 
      "/home/user/api_server.py"
    ],
    "env": {
      "API_BASE_URL": "https://api.example.com",
      "TIMEOUT": "30"
    }
  }
}
```

--------------------------------

### Incorrect FastMCP Decorator Usage on Instance Method (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/decorating-methods.mdx

This example demonstrates an incorrect way to apply a FastMCP decorator directly to an instance method. Doing so converts the method into a FastMCP Tool object, making it uncallable by Python code and also dysfunctional for LLMs due to issues with the `self` parameter.

```python
from fastmcp import FastMCP
mcp = FastMCP()

class MyClass:
    @mcp.tool
    def my_method(self, x: int) -> int:
        return x * 2

obj = MyClass()
obj.my_method(5)  # Fails - my_method is a Tool, not a function
```

--------------------------------

### Modify FastMCP Tool Behavior with Transform Function

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/tool-transformation.mdx

Shows how to completely replace a tool's logic using the transform_fn parameter. The transform function is an async function that replaces the parent tool's execution and determines the new tool's schema based on its arguments. Arguments from the transform function are added to the schema, with transform_args metadata taking precedence for shared argument names.

```python
async def my_custom_logic(user_input: str, max_length: int = 100) -> str:
    # Your custom logic here - this completely replaces the parent tool
    return f"Custom result for: {user_input[:max_length]}"

Tool.from_tool(transform_fn=my_custom_logic)
```

--------------------------------

### Default Lifespan Context Manager

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

Provides a default lifespan context manager for FastMCP server instances that performs no operations. This is used as a fallback when no custom lifespan management is required. Returns an empty dictionary as the lifespan result.

```python
def default_lifespan(server: FastMCP[LifespanResultT]) -> AsyncIterator[Any]
```

--------------------------------

### SlidingWindowRateLimitingMiddleware on_request handler

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-middleware-rate_limiting.mdx

Middleware handler that applies sliding window rate limiting to incoming requests. Provides more precise rate limiting by tracking individual request timestamps compared to token bucket approach, at the cost of higher memory usage.

```python
def on_request(self, context: MiddlewareContext, call_next: CallNext) -> Any:
    """
    Apply sliding window rate limiting to requests.
    
    Args:
        context: Middleware context containing request information
        call_next: Callback to continue request processing
    
    Returns:
        Response from the next middleware or handler
    
    Raises:
        RateLimitError: When rate limit is exceeded
    """
```

--------------------------------

### Advanced FastMCP Server Configuration with Python Version and Requirements

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/mcp-json-configuration.mdx

Demonstrates advanced FastMCP server configuration combining Python version specification, project directory, requirements file, and environment variables. The generated configuration includes all settings in the appropriate sections, suitable for complex machine learning or data science projects.

```bash
fastmcp install mcp-json ml_server.py \
  --name "ML Analysis Server" \
  --python 3.11 \
  --with-requirements requirements.txt \
  --project /home/user/ml-project \
  --env GPU_DEVICE=0
```

```json
{
  "ML Analysis Server": {
    "command": "uv",
    "args": [
      "run",
      "--python",
      "3.11",
      "--project",
      "/home/user/ml-project",
      "--with",
      "fastmcp",
      "--with-requirements",
      "requirements.txt",
      "fastmcp",
      "run",
      "/home/user/ml_server.py"
    ],
    "env": {
      "GPU_DEVICE": "0"
    }
  }
}
```

--------------------------------

### FastMCP Client Sample Code

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/oci.mdx

This asynchronous Python client sample demonstrates how to connect to the FastMCP server, automatically handle OCI OAuth authentication, and list available tools. The first connection will open an OCI login page in the user's browser for authorization and consent.

```python
from fastmcp import Client
import asyncio

async def main():
    # The client will automatically handle OCI OAuth flows
    async with Client("http://localhost:8000/mcp/", auth="oauth") as client:
        # First-time connection will open OCI login in your browser
        print("✓ Authenticated with OCI IAM")

        tools = await client.list_tools()
        print(f"🔧 Available tools ({len(tools)}):")
        for tool in tools:
            print(f"   - {tool.name}: {tool.description}")

if __name__ == "__main__":
    asyncio.run(main())
```

--------------------------------

### Install FastMCP Server with Explicit Server Object Selection

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/mcp-json-configuration.mdx

Specifies the server object to use from the Python file. FastMCP auto-detects common server object names (mcp, server, app), but explicit selection allows for custom object names. Uses file.py:object notation.

```bash
# Auto-detects server object (looks for 'mcp', 'server', or 'app')
fastmcp install mcp-json server.py

# Explicit server object
fastmcp install mcp-json server.py:my_custom_server
```

--------------------------------

### FastMCP Middleware: Filter Tools by Tag in Listing Operations (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

This Python middleware example shows how to modify the list of FastMCP tools returned during an `on_list_tools` operation. It calls `call_next` to get the initial list of component objects, then filters them based on their `tags` property, specifically removing tools marked as 'private'. The filtered list is then returned, affecting what MCP clients see.

```python
from fastmcp.server.middleware import Middleware, MiddlewareContext

class ListingFilterMiddleware(Middleware):
    async def on_list_tools(self, context: MiddlewareContext, call_next):
        result = await call_next(context)
        
        # Filter out tools with "private" tag
        filtered_tools = [
            tool for tool in result 
            if "private" not in tool.tags
        ]
        
        # Return modified list
        return filtered_tools
```

--------------------------------

### Run `fastmcp dev` with a server file

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

Execute the `fastmcp dev` command to launch your server script, `server.py`, for testing. This command runs the server through a `uv run` subprocess, enabling seamless integration with the MCP Inspector. Dependencies can be specified using flags, configuration files, or a `uv`-managed project.

```bash
fastmcp dev server.py
```

--------------------------------

### Define a Reusable FastMCP Prompt Template in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/server.mdx

This snippet illustrates how to define a reusable prompt template for guiding an LLM using the `@mcp.prompt` decorator. The function takes input data, formats it, and returns a string representing the prompt for analysis.

```python
@mcp.prompt
def analyze_data(data_points: list[float]) -> str:
    """Creates a prompt asking for analysis of numerical data."""
    formatted_data = ", ".join(str(point) for point in data_points)
    return f"Please analyze these data points: {formatted_data}"
```

--------------------------------

### Direct HTTP Server Deployment

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/http.mdx

Deploys a FastMCP server using the built-in HTTP transport. This method is simple and suitable for standalone deployments or development environments. It requires no external web server configuration.

```python
from fastmcp import FastMCP

mcp = FastMCP("My Server")

@mcp.tool
def process_data(input: str) -> str:
    """Process data on the server"""
    return f"Processed: {input}"

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
```

--------------------------------

### Manually Add a FastMCP Server to Claude Code

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/claude-code.mdx

This command shows how to manually add a FastMCP server to Claude Code using `claude mcp add`. This method provides fine-grained control over the server's launch configuration, allowing direct execution of `uv run` commands.

```bash
# Add a server with custom configuration
claude mcp add dice-roller -- uv run --with fastmcp fastmcp run server.py
```

--------------------------------

### Create Starlette App for Streamable HTTP Server in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

This function generates a Starlette application pre-configured for Streamable HTTP transport. It accepts an optional path for the server's endpoint and a list of ASGI middleware to enhance functionality. The returned StarletteWithLifespan instance is optimized for handling efficient streamable HTTP responses.

```python
streamable_http_app(self, path: str | None = None, middleware: list[ASGIMiddleware] | None = None) -> StarletteWithLifespan
```

--------------------------------

### Integrate FastMCP Generated Configuration into MCP Client

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/mcp-json-configuration.mdx

This JSON snippet demonstrates how to embed the configuration generated by `fastmcp install mcp-json` into a full MCP client configuration file. The generated server object is placed under the `mcpServers` root key, making it discoverable by the client.

```json
{
  "mcpServers": {
    "My Server": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp", 
        "fastmcp",
        "run",
        "/absolute/path/to/server.py"
      ]
    }
  }
}
```

--------------------------------

### Specify Project Directory for FastMCP Server Installation via CLI

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/claude-code.mdx

This command shows how to define a specific project context for your FastMCP server using the `--project` flag during installation. This directs `uv` to use the specified project's configuration files and virtual environment.

```bash
fastmcp install claude-code server.py --project /path/to/my-project
```

--------------------------------

### Set Up FastMCP with Static Token Verification for Development (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/auth/token-verification.mdx

This example shows how to configure FastMCP with `StaticTokenVerifier` to accept predefined development tokens and their associated claims. It eliminates the need for token generation infrastructure during development, allowing immediate testing with specified `client_id` and `scopes`. This method is not suitable for production.

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier

# Define development tokens and their associated claims
verifier = StaticTokenVerifier(
    tokens={
        "dev-alice-token": {
            "client_id": "alice@company.com",
            "scopes": ["read:data", "write:data", "admin:users"]
        },
        "dev-guest-token": {
            "client_id": "guest-user",
            "scopes": ["read:data"]
        }
    },
    required_scopes=["read:data"]
)

mcp = FastMCP(name="Development Server", auth=verifier)
```

--------------------------------

### Exclude Specific Routes in FastMCP (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openapi.mdx

This snippet demonstrates how to explicitly exclude routes from the FastMCP server's processing. It uses `RouteMap` to exclude all endpoints under `/admin/` and any routes tagged with "internal", preventing them from being exposed or processed by the server. This is useful for securing sensitive endpoints.

```python
from fastmcp import FastMCP
from fastmcp.server.openapi import RouteMap, MCPType

mcp = FastMCP.from_openapi(
    openapi_spec=spec,
    client=client,
    route_maps=[
        RouteMap(pattern=r"^/admin/.*", mcp_type=MCPType.EXCLUDE),
        RouteMap(tags={"internal"}, mcp_type=MCPType.EXCLUDE),
    ],
)
```

--------------------------------

### Define a FastMCP Dice Rolling Server in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/claude-code.mdx

This Python code defines a basic FastMCP server named 'Dice Roller'. It includes a tool function `roll_dice` that simulates rolling multiple 6-sided dice and returns the results, demonstrating how to expose custom functionality.

```python
import random
from fastmcp import FastMCP

mcp = FastMCP(name="Dice Roller")

@mcp.tool
def roll_dice(n_dice: int) -> list[int]:
    """Roll `n_dice` 6-sided dice and return the results."""
    return [random.randint(1, 6) for _ in range(n_dice)]

if __name__ == "__main__":
    mcp.run()
```

--------------------------------

### Install FastMCP Server with Specific Python Version (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

Illustrates specifying a particular Python version, such as `3.11`, for the FastMCP server during installation using the `--python` option. This ensures compatibility and consistency across different client environments, especially when dealing with specific Python feature requirements.

```bash
fastmcp install claude-desktop server.py --python 3.11
```

--------------------------------

### Generate RSA Key Pair and Access Token for FastMCP Server Authentication

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/anthropic.mdx

Creates an RSA key pair using FastMCP's RSAKeyPair utility and generates an access token for server authentication. This utility is intended for development and testing only, not production use. The token is signed with the private key and configured for a specific audience.

```python
from fastmcp.server.auth.providers.jwt import RSAKeyPair

key_pair = RSAKeyPair.generate()
access_token = key_pair.create_token(audience="dice-server")
```

--------------------------------

### Pass Complex Arguments for Automatic Serialization

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/prompts.mdx

Demonstrates FastMCP's automatic serialization of complex Python objects (like dataclasses and dictionaries) into JSON strings when passed as prompt arguments. The server can then deserialize these JSON strings back into their original types. This requires `pydantic_core` for serialization.

```python
from dataclasses import dataclass

@dataclass
class UserData:
    name: str
    age: int

async with client:
    # Complex arguments are automatically serialized
    result = await client.get_prompt("analyze_user", {
        "user": UserData(name="Alice", age=30),     # Automatically serialized to JSON
        "preferences": {"theme": "dark"},           # Dict serialized to JSON string
        "scores": [85, 92, 78],                     # List serialized to JSON string
        "simple_name": "Bob"                        # Strings passed through unchanged
    })
```

--------------------------------

### Define a FastMCP Server with a Dice Rolling Tool (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/anthropic.mdx

This Python code defines a FastMCP server named 'Dice Roller'. It includes a `roll_dice` tool that takes an integer `n_dice` and returns a list of random 6-sided dice rolls. The server is configured to run on HTTP transport on port 8000.

```python
import random
from fastmcp import FastMCP

mcp = FastMCP(name="Dice Roller")

@mcp.tool
def roll_dice(n_dice: int) -> list[int]:
    """Roll `n_dice` 6-sided dice and return the results."""
    return [random.randint(1, 6) for _ in range(n_dice)]

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
```

--------------------------------

### Authentication for OpenAPI-generated Servers

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openapi.mdx

Configure authentication for the underlying HTTP client (`httpx.AsyncClient`) used by FastMCP to interact with your API. This ensures that all requests made by the MCP server to your API are properly authenticated.

```APIDOC
## Authentication Configuration

### Description
To access protected APIs, configure authentication credentials directly on the `httpx.AsyncClient` instance provided to `FastMCP.from_openapi()`. This allows FastMCP to pass the necessary authentication details with every request it makes to your API.

### Parameters
#### `httpx.AsyncClient` Configuration
- **headers** (dict) - Required (for authentication) - A dictionary of HTTP headers to include with every request. Common headers include `Authorization` for bearer tokens or API keys.

### Request Example
```python
import httpx
from fastmcp import FastMCP

# Assume 'spec' is your loaded OpenAPI specification dictionary
spec = {}

# Bearer token authentication example
api_client = httpx.AsyncClient(
    base_url="https://api.example.com",
    headers={"Authorization": "Bearer YOUR_TOKEN"}
)

# Example with API key in a custom header
# api_client = httpx.AsyncClient(
#     base_url="https://api.example.com",
#     headers={"X-API-Key": "YOUR_API_KEY"}
# )

# Create MCP server with the authenticated client
# Also demonstrates setting a global timeout for API requests via from_openapi
mcp = FastMCP.from_openapi(
    openapi_spec=spec, 
    client=api_client,
    timeout=30.0  # 30 second timeout for all requests made by this client
)
```

### Response
No direct response for this configuration. The `mcp` instance will use the configured `api_client` for its operations.
```

--------------------------------

### Complete FastMCP Server Implementation with Tools and Resources in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/tutorials/create-mcp-server.mdx

Provides a complete, production-ready FastMCP server implementation. Includes server initialization, a computational tool for adding numbers, a static resource for configuration data, a dynamic resource template for personalized greetings, and the main execution block. This serves as a comprehensive reference for building MCP servers.

```python
from fastmcp import FastMCP

# 1. Create the server
mcp = FastMCP(name="My First MCP Server")

# 2. Add a tool
@mcp.tool
def add(a: int, b: int) -> int:
    """Adds two integer numbers together."""
    return a + b

# 3. Add a static resource
@mcp.resource("resource://config")
def get_config() -> dict:
    """Provides the application's configuration."""
    return {"version": "1.0", "author": "MyTeam"}

# 4. Add a resource template for dynamic content
@mcp.resource("greetings://{name}")
def personalized_greeting(name: str) -> str:
    """Generates a personalized greeting for the given name."""
    return f"Hello, {name}! Welcome to the MCP server."

# 5. Make the server runnable
if __name__ == "__main__":
    mcp.run()
```

--------------------------------

### Define Resource Templates with URI Parameters in FastMCP (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/resources.mdx

Shows how to create resource templates in FastMCP that allow dynamic resource generation based on URI parameters. By including `{parameter_name}` in the URI and corresponding arguments in the function signature, clients can request unique resources like `"weather://{city}/current"` with different parameter values, such as 'London' or 'Paris'.

```python
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")

# Template URI includes {city} placeholder
@mcp.resource("weather://{city}/current")
def get_weather(city: str) -> dict:
    """Provides weather information for a specific city."""
    # In a real implementation, this would call a weather API
    # Here we're using simplified logic for example purposes
    return {
        "city": city.capitalize(),
        "temperature": 22,
        "condition": "Sunny",
        "unit": "celsius"
    }
```

--------------------------------

### Handle FastMCP Request Context Availability in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/context.mdx

Demonstrates how to safely access the MCP request context (`ctx.request_context`), which can be `None` before an MCP session is established. It shows how to check for context availability and fall back to HTTP request data using `get_http_request()` when the MCP session is not present, allowing for graceful handling of both MCP-specific and HTTP-specific information.

```python
from fastmcp import FastMCP, Context
from fastmcp.server.dependencies import get_http_request

mcp = FastMCP(name="Session Aware Demo")

@mcp.tool
async def session_info(ctx: Context) -> dict:
    """Return session information when available."""

    # Check if MCP session is available
    if ctx.request_context:
        # MCP session available - can access MCP-specific attributes
        return {
            "session_id": ctx.session_id,
            "request_id": ctx.request_id,
            "has_meta": ctx.request_context.meta is not None
        }
    else:
        # MCP session not available - use HTTP helpers for request data (if using HTTP transport)
        request = get_http_request()
        return {
            "message": "MCP session not available",
            "user_agent": request.headers.get("user-agent", "Unknown")
        }
```

--------------------------------

### Image Class Methods - Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-utilities-types.mdx

Provides helper methods for the Image class to convert image data into MCP ImageContent or a data URI. These methods are essential for handling image outputs from FastMCP tools.

```python
to_image_content(self, mime_type: str | None = None, annotations: Annotations | None = None) -> mcp.types.ImageContent

to_data_uri(self, mime_type: str | None = None) -> str
```

--------------------------------

### Mount FastMCP Subserver with Live Linking

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/composition.mdx

Demonstrates mounting a dynamic subserver into a main FastMCP application with live linking. Changes made to the mounted subserver after mounting are immediately accessible through the main server. This example shows initial tools and tools added dynamically after mounting, all accessible via the main server with the specified prefix.

```python
import asyncio
from fastmcp import FastMCP, Client

# Define subserver
dynamic_mcp = FastMCP(name="DynamicService")

@dynamic_mcp.tool
def initial_tool():
    """Initial tool demonstration."""
    return "Initial Tool Exists"

# Mount subserver (synchronous operation)
main_mcp = FastMCP(name="MainAppLive")
main_mcp.mount(dynamic_mcp, prefix="dynamic")

# Add a tool AFTER mounting - it will be accessible through main_mcp
@dynamic_mcp.tool
def added_later():
    """Tool added after mounting."""
    return "Tool Added Dynamically!"

# Testing access to mounted tools
async def test_dynamic_mount():
    tools = await main_mcp.get_tools()
    print("Available tools:", list(tools.keys()))
    # Shows: ['dynamic_initial_tool', 'dynamic_added_later']
    
    async with Client(main_mcp) as client:
        result = await client.call_tool("dynamic_added_later")
        print("Result:", result.data)
        # Shows: "Tool Added Dynamically!"

if __name__ == "__main__":
    asyncio.run(test_dynamic_mount())
```

--------------------------------

### Deploy FastMCP Server with ngrok for Public Access

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/chatgpt.mdx

Demonstrates deployment of a FastMCP server for internet accessibility using ngrok tunneling. Terminal 1 runs the Python server locally, while Terminal 2 creates a public URL tunnel. This setup is essential for connecting local development servers to ChatGPT.

```bash
python server.py
```

```bash
ngrok http 8000
```

--------------------------------

### Create ProxyPrompt from MCP Prompt Schema (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-proxy.mdx

This class factory method constructs a `ProxyPrompt` instance, providing a local representation for a remote prompt. It accepts a `Client` for communication and a raw `mcp.types.Prompt` schema describing the remote prompt. The method returns a `ProxyPrompt` object.

```python
from_mcp_prompt(cls, client: Client, mcp_prompt: mcp.types.Prompt) -> ProxyPrompt
```

--------------------------------

### Configure FastMCP with Environment Variables

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/http.mdx

Securely manage sensitive information like API keys and authentication tokens by using environment variables instead of hardcoding them. This example demonstrates reading an MCP_AUTH_TOKEN for BearerTokenAuth.

```python
import os
from fastmcp import FastMCP
from fastmcp.server.auth import BearerTokenAuth

# Read configuration from environment
auth_token = os.environ.get("MCP_AUTH_TOKEN")
if auth_token:
    auth = BearerTokenAuth(token=auth_token)
    mcp = FastMCP("Production Server", auth=auth)
else:
    mcp = FastMCP("Production Server")

app = mcp.http_app()
```

--------------------------------

### Configure FastMCP Google OAuth Provider with Environment Variables

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/google.mdx

Set up Google OAuth authentication for FastMCP by configuring environment variables with provider class, OAuth credentials, and required scopes. These variables enable automatic authentication configuration without manual setup in application code.

```bash
# Use the Google provider
FASTMCP_SERVER_AUTH=fastmcp.server.auth.providers.google.GoogleProvider

# Google OAuth credentials
FASTMCP_SERVER_AUTH_GOOGLE_CLIENT_ID=123456789.apps.googleusercontent.com
FASTMCP_SERVER_AUTH_GOOGLE_CLIENT_SECRET=GOCSPX-abc123...
FASTMCP_SERVER_AUTH_GOOGLE_BASE_URL=https://your-server.com
FASTMCP_SERVER_AUTH_GOOGLE_REQUIRED_SCOPES=openid,https://www.googleapis.com/auth/userinfo.email
```

--------------------------------

### Define FastMCP Tool with Custom Metadata in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/tools.mdx

This Python code demonstrates how to use the @mcp.tool decorator to explicitly configure a FastMCP tool. It shows how to set a custom name, provide a detailed description, assign tags for categorization, and include arbitrary meta information for versioning or application-specific use, enhancing the tool's exposure and discoverability.

```python
@mcp.tool(
    name="find_products",           # Custom tool name for the LLM
    description="Search the product catalog with optional category filtering.", # Custom description
    tags={"catalog", "search"},      # Optional tags for organization/filtering
    meta={"version": "1.2", "author": "product-team"}  # Custom metadata
)
def search_products_implementation(query: str, category: str | None = None) -> list[dict]:
    """Internal function description (ignored if description is provided above)."""
    # Implementation...
    print(f"Searching for '{query}' in category '{category}'")
    return [{"id": 2, "name": "Another Product"}]
```

--------------------------------

### Define and Register Custom Middleware (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

This Python code defines a custom middleware class, `CustomHeaderMiddleware`, by extending FastMCP's `Middleware` base class. It overrides the `on_request` method to execute custom logic before and after processing a request, demonstrating how to print logs. The middleware is then registered with the FastMCP application instance `mcp`.

```python
from fastmcp.server.middleware import Middleware, MiddlewareContext

class CustomHeaderMiddleware(Middleware):
    async def on_request(self, context: MiddlewareContext, call_next):
        # Add custom logic here
        print(f"Processing {context.method}")
        
        result = await call_next(context)
        
        print(f"Completed {context.method}")
        return result

mcp.add_middleware(CustomHeaderMiddleware())
```

--------------------------------

### Test FastMCP Server with Client

Source: https://github.com/jlowin/fastmcp/blob/main/docs/tutorials/rest-api.mdx

This Python script connects to a running FastMCP server, lists the automatically generated tools, and then calls a specific tool (`get_user_by_id`) to fetch data. It demonstrates how to interact with the FastMCP server and verify its functionality, retrieving user data from the integrated JSONPlaceholder API.

```python
import asyncio
from fastmcp import Client

async def main():
    # Connect to the MCP server we just created
    async with Client("http://127.0.0.1:8000/mcp") as client:
        
        # List the tools that were automatically generated
        tools = await client.list_tools()
        print("Generated Tools:")
        for tool in tools:
            print(f"- {tool.name}")
            
        # Call one of the generated tools
        print("\n\nCalling tool 'get_user_by_id'...")
        user = await client.call_tool("get_user_by_id", {"id": 1})
        print(f"Result:\n{user.data}")

if __name__ == "__main__":
    asyncio.run(main())
```

--------------------------------

### Install FastMCP Server with Environment File in Cursor - Bash

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/cursor.mdx

Installs a FastMCP server in Cursor by loading environment variables from a .env file. This approach is useful for managing multiple environment variables or keeping sensitive data separate from command-line arguments. Requires a .env file in the working directory.

```bash
fastmcp install cursor server.py --server-name "Weather Server" --env-file .env
```

--------------------------------

### Serialize Array Parameters in FastMCP Requests

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openapi.mdx

FastMCP handles array parameters according to OpenAPI specifications. Query arrays are serialized based on the `explode` parameter (default `True`), while path arrays are always serialized as comma-separated values (OpenAPI 'simple' style). This ensures consistent array serialization for different parameter types.

```text
# Query array with explode=true (default)
# ?tags=red&tags=blue&tags=green

# Query array with explode=false  
# ?tags=red,blue,green

# Path array (always comma-separated)
# /items/red,blue,green
```

--------------------------------

### Request scalar elicitation responses in FastMCP (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/elicitation.mdx

FastMCP allows requesting simple scalar data types like strings, integers, or booleans for elicitation. It automatically wraps these into MCP-compatible object schemas for the client and unwraps the response, returning the scalar value in `result.data`, simplifying development for basic inputs.

```python
@mcp.tool
async def get_user_name(ctx: Context) -> str:
    """Get the user's name."""
    result = await ctx.elicit("What's your name?", response_type=str)
    
    if result.action == "accept":
        return f"Hello, {result.data}!"
    return "No name provided"
```

```python
@mcp.tool
async def pick_a_number(ctx: Context) -> str:
    """Pick a number."""
    result = await ctx.elicit("Pick a number!", response_type=int)
    
    if result.action == "accept":
        return f"You picked {result.data}"
    return "No number provided"
```

```python
@mcp.tool
async def pick_a_boolean(ctx: Context) -> str:
    """Pick a boolean."""
    result = await ctx.elicit("True or false?", response_type=bool)
    
    if result.action == "accept":
        return f"You picked {result.data}"
    return "No boolean provided"
```

--------------------------------

### Configure FastMCP Client with Default OAuth Settings (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/auth/oauth.mdx

This snippet demonstrates how to enable OAuth authentication for a FastMCP client using default settings. By passing the string "oauth" to the `auth` parameter, FastMCP automatically configures the client, suitable for basic scenarios requiring user interaction. It shows the basic setup to connect to an MCP server and perform an action like `ping()`.

```python
from fastmcp import Client

# Uses default OAuth settings
async with Client("https://fastmcp.cloud/mcp", auth="oauth") as client:
    await client.ping()
```

--------------------------------

### Configure FastMCP Server with Google OAuth Provider

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/google.mdx

This Python code initializes a FastMCP server, integrating Google OAuth for authentication. It uses the `GoogleProvider` to manage Google's specific token format and validation, requiring a client ID, client secret, base URL, and desired scopes. A protected tool is included to demonstrate how to retrieve authenticated user information from the token claims.

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.google import GoogleProvider

# The GoogleProvider handles Google's token format and validation
auth_provider = GoogleProvider(
    client_id="123456789.apps.googleusercontent.com",  # Your Google OAuth Client ID
    client_secret="GOCSPX-abc123...",                  # Your Google OAuth Client Secret
    base_url="http://localhost:8000",                  # Must match your OAuth configuration
    required_scopes=[                                  # Request user information
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
    ],
    # redirect_path="/auth/callback"                  # Default value, customize if needed
)

mcp = FastMCP(name="Google Secured App", auth=auth_provider)

# Add a protected tool to test authentication
@mcp.tool
async def get_user_info() -> dict:
    """Returns information about the authenticated Google user."""
    from fastmcp.server.dependencies import get_access_token
    
    token = get_access_token()
    # The GoogleProvider stores user data in token claims
    return {
        "google_id": token.claims.get("sub"),
        "email": token.claims.get("email"),
        "name": token.claims.get("name"),
        "picture": token.claims.get("picture"),
        "locale": token.claims.get("locale")
    }
```

--------------------------------

### Correctly Configure `base_url` and `mcp_path` for Authenticated FastMCP Mounting

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/http.mdx

This snippet illustrates the correct pattern for setting `base_url` and `mcp_path` when mounting an OAuth-protected FastMCP server under a path prefix. It ensures that the mount prefix is applied only once via `base_url` and not duplicated in `mcp_path`, preventing incorrect URL generation like `/api/api/mcp`.

```python
base_url = "http://localhost:8000/api"
mcp_path = "/mcp"
# Result: /api/mcp
```

--------------------------------

### Configure FastMCP with Introspection Token Verification (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/auth/token-verification.mdx

This snippet demonstrates how to configure FastMCP to use `IntrospectionTokenVerifier` for validating opaque tokens according to RFC 7662. It requires an introspection endpoint URL, client credentials, and defines required scopes. FastMCP will use HTTP Basic Auth to query the endpoint for token metadata.

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.introspection import IntrospectionTokenVerifier

# Configure introspection with your OAuth provider
verifier = IntrospectionTokenVerifier(
    introspection_url="https://auth.yourcompany.com/oauth/introspect",
    client_id="mcp-resource-server",
    client_secret="your-client-secret",
    required_scopes=["api:read", "api:write"]
)

mcp = FastMCP(name="Protected API", auth=verifier)
```

--------------------------------

### Retrieve FastMCP Server Context (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-dependencies.mdx

Retrieves the current FastMCP server context. This function provides access to the application's runtime context for dependency injection or state management.

```python
get_context() -> Context
```

--------------------------------

### Initialize a FastMCP Component Class with Basic Tool in Python

Source: https://github.com/jlowin/fastmcp/blob/main/src/fastmcp/contrib/mcp_mixin/README.md

This code snippet demonstrates the necessary imports and the basic class structure for creating a FastMCP component. By inheriting `MCPMixin`, the `MyComponent` class can use the provided decorators (`@mcp_tool`, `@mcp_resource`, `@mcp_prompt`) to register its methods. It includes a simple `mcp_tool` example to illustrate basic usage.

```python
from mcp.types import ToolAnnotations
from fastmcp import FastMCP
from fastmcp.contrib.mcp_mixin import MCPMixin, mcp_tool, mcp_resource, mcp_prompt

class MyComponent(MCPMixin):
    @mcp_tool(name="my_tool", description="Does something cool.")
    def tool_method(self):
        return "Tool executed!"
```

--------------------------------

### Inspect FastMCP v1.x Instance (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-utilities-inspect.mdx

This Python function extracts information from a FastMCP v1.x instance using a Client. It accepts a `FastMCP1x` object and returns a `FastMCPInfo` dataclass with the gathered details.

```python
inspect_fastmcp_v1(mcp: FastMCP1x) -> FastMCPInfo
```

--------------------------------

### Configure OIDC Proxy for FastMCP in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/auth/oidc-proxy.mdx

This snippet demonstrates how to set up an OIDC proxy using `fastmcp.server.auth.oidc_proxy.OIDCProxy` to integrate with an OIDC provider that doesn't support Dynamic Client Registration. It shows how to instantiate `OIDCProxy` with the provider's configuration URL, client credentials, and the FastMCP server's base URL, then integrates it into a `FastMCP` application. An optional `redirect_path` can also be configured.

```python
from fastmcp import FastMCP
from fastmcp.server.auth.oidc_proxy import OIDCProxy

# Create the OIDC proxy
auth = OIDCProxy(
    # Provider's configuration URL
    config_url="https://provider.com/.well-known/openid-configuration",

    # Your registered app credentials
    client_id="your-client-id",
    client_secret="your-client-secret",

    # Your FastMCP server's public URL
    base_url="https://your-server.com",

    # Optional: customize the callback path (default is "/auth/callback")
    # redirect_path="/custom/callback",
)

mcp = FastMCP(name="My Server", auth=auth)
```

--------------------------------

### Render Prompt from FastMCP Proxy Server (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-proxy.mdx

This method renders a specific prompt identified by its name, optionally accepting a dictionary of arguments. It prioritizes local or mounted prompts before falling back to proxy prompts if the prompt is not found locally. The method returns a `GetPromptResult`.

```python
render_prompt(self, name: str, arguments: dict[str, Any] | None = None) -> GetPromptResult
```

--------------------------------

### Testing FastMCP Network Transport in Subprocess with run_server_in_process

Source: https://github.com/jlowin/fastmcp/blob/main/docs/development/tests.mdx

Illustrates how to test FastMCP network transports in a separate subprocess using `run_server_in_process`. This method is suitable for scenarios requiring complete process isolation, such as STDIO transport testing, but is generally slower and harder to debug than in-process testing. It handles server lifecycle, port allocation, and cleanup automatically.

```python
import pytest
from fastmcp.utilities.tests import run_server_in_process
from fastmcp import FastMCP, Client
from fastmcp.client.transports import StreamableHttpTransport

def run_server(host: str, port: int) -> None:
    """Function to run in subprocess."""
    server = FastMCP("TestServer")
    
    @server.tool
    def greet(name: str) -> str:
        return f"Hello, {name}!"
    
    server.run(host=host, port=port)

@pytest.fixture
async def http_server():
    """Fixture that runs server in subprocess."""
    with run_server_in_process(run_server, transport="http") as url:
        yield f"{url}/mcp"

async def test_http_transport(http_server: str):
    """Test actual HTTP transport behavior."""
    async with Client(
        transport=StreamableHttpTransport(http_server)
    ) as client:
        result = await client.ping()
        assert result is True
```

--------------------------------

### Get FastMCP Access Token (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-dependencies.mdx

Retrieves the FastMCP access token from the current server context. This function returns the access token if an authenticated user is available, otherwise it returns `None`, indicating no active authentication.

```python
get_access_token() -> AccessToken | None
```

--------------------------------

### Implement FastMCP Middleware Base Class Hooks in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-middleware-middleware.mdx

The `Middleware` class serves as the abstract base for all FastMCP middleware, defining a set of dispatching hooks for various server events. Subclasses override methods like `on_message`, `on_request`, or `on_call_tool` to inject custom logic into the request processing flow. Each method receives a `MiddlewareContext` and a `call_next` function, allowing for flexible interception and modification of events.

```python
on_message(self, context: MiddlewareContext[Any], call_next: CallNext[Any, Any]) -> Any
```

```python
on_request(self, context: MiddlewareContext[mt.Request[Any, Any]], call_next: CallNext[mt.Request[Any, Any], Any]) -> Any
```

```python
on_notification(self, context: MiddlewareContext[mt.Notification[Any, Any]], call_next: CallNext[mt.Notification[Any, Any], Any]) -> Any
```

```python
on_initialize(self, context: MiddlewareContext[mt.InitializeRequest], call_next: CallNext[mt.InitializeRequest, None]) -> None
```

```python
on_call_tool(self, context: MiddlewareContext[mt.CallToolRequestParams], call_next: CallNext[mt.CallToolRequestParams, ToolResult]) -> ToolResult
```

```python
on_read_resource(self, context: MiddlewareContext[mt.ReadResourceRequestParams], call_next: CallNext[mt.ReadResourceRequestParams, Sequence[ReadResourceContents]]) -> Sequence[ReadResourceContents]
```

```python
on_get_prompt(self, context: MiddlewareContext[mt.GetPromptRequestParams], call_next: CallNext[mt.GetPromptRequestParams, mt.GetPromptResult]) -> mt.GetPromptResult
```

```python
on_list_tools(self, context: MiddlewareContext[mt.ListToolsRequest], call_next: CallNext[mt.ListToolsRequest, Sequence[Tool]]) -> Sequence[Tool]
```

--------------------------------

### Configure Redis Storage for FastMCP Caching Middleware

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

Illustrates how to configure the `ResponseCachingMiddleware` to use Redis as a distributed caching backend. This is ideal for distributed deployments and provides robust, scalable caching.

```python
from fastmcp.server.middleware.caching import ResponseCachingMiddleware
from key_value.aio.stores.redis import RedisStore

mcp.add_middleware(ResponseCachingMiddleware(
    cache_storage=RedisStore(host="redis.example.com", port=6379),
))
```

--------------------------------

### Install FastMCP Server in Claude Code (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-cli-install-claude_code.mdx

This function handles the installation of a FastMCP server into the Claude Code environment. It requires the path to the server file, an optional server object name, and a name for the server within Claude Code. The function returns a boolean indicating the success or failure of the installation process.

```python
install_claude_code(file: Path, server_object: str | None, name: str) -> bool
```

--------------------------------

### Toggle FastMCP Prompt State Programmatically (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/prompts.mdx

This example shows how to dynamically change the enabled or disabled state of a FastMCP prompt after it has been defined. The '.disable()' and '.enable()' methods on the prompt object allow for runtime control of its availability, triggering 'notifications/prompts/list_changed' for connected clients.

```python
@mcp.prompt
def seasonal_prompt(): return "Happy Holidays!"

# Disable and re-enable the prompt
seasonal_prompt.disable()
seasonal_prompt.enable()
```

--------------------------------

### Create FastMCP Proxy from Configuration Dictionary (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/proxy.mdx

This snippet demonstrates creating a FastMCP proxy directly from a configuration dictionary adhering to the MCPConfig schema. It's useful for quickly setting up proxies to remote servers, automatically creating a `ProxyClient` internally.

```python
from fastmcp import FastMCP

# Create a proxy directly from a config dictionary
config = {
    "mcpServers": {
        "default": {  # For single server configs, 'default' is commonly used
            "url": "https://example.com/mcp",
            "transport": "http"
        }
    }
}

# Create a proxy to the configured server (auto-creates ProxyClient)
proxy = FastMCP.as_proxy(config, name="Config-Based Proxy")

# Run the proxy with stdio transport for local access
if __name__ == "__main__":
    proxy.run()
```

--------------------------------

### Send INFO Log Message to fastmcp Client in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-context.mdx

Sends a log message with an `INFO` level to the connected MCP client. This helper function provides a convenient way to send informational messages, which are also logged server-side to `fastmcp.server.context.to_client` for general activity tracking.

```python
info(self, message: str, logger_name: str | None = None, extra: Mapping[str, Any] | None = None) -> None
```

--------------------------------

### Configure FastMCP Tool for Technical Analysis with Multiple Model Preferences (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/sampling.mdx

This `fastmcp` tool performs technical analysis, specifying a list of preferred models (`"claude-3-opus"`, `"gpt-4"`) for `ctx.sample`. It sets a low `temperature` for consistent, reasoning-focused output, returning the analysis as text.

```python
@mcp.tool
async def technical_analysis(data: str, ctx: Context) -> str:
    """Perform technical analysis with a reasoning-focused model."""
    response = await ctx.sample(
        messages=f"Analyze this technical data and provide insights: {data}",
        model_preferences=["claude-3-opus", "gpt-4"],  # Prefer reasoning models
        temperature=0.2,  # Low randomness for consistency
        max_tokens=800
    )
    
    return response.text
```

--------------------------------

### Define a Basic FastMCP Resource in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/server.mdx

This snippet demonstrates how to define a simple, read-only data source using the `@mcp.resource` decorator. The function returns a dictionary representing application configuration, exposed at the specified URI.

```python
@mcp.resource("data://config")
def get_config() -> dict:
    """Provides the application configuration."""
    return {"theme": "dark", "version": "1.0"}
```

--------------------------------

### Prepare Python Environment for fastmcp Server (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-utilities-mcp_server_config-v1-mcp_server_config.mdx

This method specifically handles the setup of the Python environment for the fastmcp server. It supports creating a persistent `uv` project in a specified `output_dir` for consistent environments, or it can populate `uv`'s cache for temporary use if no directory is provided. This function delegates the actual preparation to the environment's own `prepare()` method.

```python
prepare_environment(self, output_dir: Path | None = None) -> None
```

--------------------------------

### Retrieve Authenticated User Access Token in FastMCP Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/context.mdx

This FastMCP example shows how to use `get_access_token()` to obtain the authenticated user's access token. It returns an `AccessToken` object or `None` if the user is not authenticated. The token provides details such as `client_id`, `scopes`, and `claims` for authorization and user identification.

```python
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_access_token, AccessToken

mcp = FastMCP(name="Auth Token Demo")

@mcp.tool
async def get_user_info() -> dict:
    """Get information about the authenticated user."""
    # Get the access token (None if not authenticated)
    token: AccessToken | None = get_access_token()
    
    if token is None:
        return {"authenticated": False}
    
    return {
        "authenticated": True,
        "client_id": token.client_id,
        "scopes": token.scopes,
        "expires_at": token.expires_at,
        "token_claims": token.claims  # JWT claims or custom token data
    }
```

--------------------------------

### Get FastMCP Instance - MiddlewareServerSession (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-low_level.mdx

Retrieves the FastMCP instance associated with the MiddlewareServerSession. This method is part of the session management within the low-level server implementation.

```python
fastmcp(self) -> FastMCP
```

--------------------------------

### Manually Add a FastMCP Server with Environment Variables to Claude Code

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/claude-code.mdx

This command demonstrates how to include environment variables when manually adding a FastMCP server to Claude Code. The `-e` flag allows you to pass key-value pairs as environment variables directly to the server's execution context.

```bash
# Add with environment variables
claude mcp add weather-server -e API_KEY=secret -e DEBUG=true -- uv run --with fastmcp fastmcp run server.py
```

--------------------------------

### Accessing Hydrated Python Objects with FastMCP's .data

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/tools.mdx

Demonstrates how FastMCP's `.data` property provides fully hydrated Python objects, including complex types like `datetime` and `UUID`, going beyond standard JSON. It shows accessing structured output and comparing it with raw JSON and content blocks.

```python
from datetime import datetime
from uuid import UUID

async with client:
    result = await client.call_tool("get_weather", {"city": "London"})
    
    # FastMCP reconstructs complete Python objects from the server's output schema
    weather = result.data  # Server-defined WeatherReport object
    print(f"Temperature: {weather.temperature}°C at {weather.timestamp}")
    print(f"Station: {weather.station_id}")
    print(f"Humidity: {weather.humidity}%")
    
    # The timestamp is a real datetime object, not a string!
    assert isinstance(weather.timestamp, datetime)
    assert isinstance(weather.station_id, UUID)
    
    # Compare with raw structured JSON (standard MCP)
    print(f"Raw JSON: {result.structured_content}")
    # {"temperature": 20, "timestamp": "2024-01-15T14:30:00Z", "station_id": "123e4567-..."}
    
    # Traditional content blocks (standard MCP)  
    print(f"Text content: {result.content[0].text}")
```

--------------------------------

### Configure FastMCP Permit.io Middleware in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/permit.mdx

This Python code shows how to programmatically configure and add the Permit.io middleware to a FastMCP instance. It allows for direct setup of parameters such as the PDP URL, API key, audit logging, and methods to bypass authorization checks.

```python
from permit_fastmcp.middleware.middleware import PermitMcpMiddleware

middleware = PermitMcpMiddleware(
    permit_pdp_url="http://localhost:7766",
    permit_api_key="your-api-key",
    enable_audit_logging=True,
    bypass_methods=["initialize", "ping", "health/*"]
)

mcp.add_middleware(middleware)
```

--------------------------------

### Format Server Information with Specified Format (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-utilities-inspect.mdx

This Python function formats server information from a FastMCP instance based on a specified output format ("fastmcp" or "mcp"). It can optionally use pre-extracted `FastMCPInfo` or extract it if not provided, returning the data as JSON bytes.

```python
format_info(mcp: FastMCP[Any] | FastMCP1x, format: InspectFormat | Literal['fastmcp', 'mcp'], info: FastMCPInfo | None = None) -> bytes
```

--------------------------------

### Add Icon to a Resource

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/icons.mdx

Demonstrates how to assign an icon to a resource managed by FastMCP. The icon is specified using the `icons` argument in the `@mcp.resource` decorator.

```python
@mcp.resource(
    "config://settings",
    icons=[Icon(src="https://example.com/config-icon.png")]
)
def get_settings() -> dict:
    """Retrieve application settings."""
    return {"theme": "dark", "language": "en"}
```

--------------------------------

### List Prompts (MCP Protocol) in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-client.mdx

Sends a prompts/list request to retrieve available prompts with complete MCP protocol metadata. Returns the full protocol response object including prompts list and additional metadata. Requires an active client connection.

```python
list_prompts_mcp(self) -> mcp.types.ListPromptsResult
```

--------------------------------

### Add prompt to FastMCP server using add_prompt method

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

Registers a Prompt instance to the server for prompt management. This method accepts a pre-configured Prompt object and returns the same instance after registration, enabling prompt-based interactions.

```python
add_prompt(self, prompt: Prompt) -> Prompt
```

--------------------------------

### Implement Search and Fetch Tools for ChatGPT Deep Research Mode in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/chatgpt.mdx

Implements the required search and fetch tool pattern for ChatGPT Deep Research mode. The search tool must return a dictionary with an 'ids' array of string identifiers, while the fetch tool retrieves complete records by ID. These tools enable systematic information retrieval with proper citation support in Deep Research mode.

```python
@mcp.tool()
def search(query: str) -> dict:
    """
    Search for records matching the query.
    Must return {"ids": [list of string IDs]}
    """
    # Your search logic
    matching_ids = ["id1", "id2", "id3"]
    return {"ids": matching_ids}

@mcp.tool()
def fetch(id: str) -> dict:
    """
    Fetch a complete record by ID.
    Return the full record data for ChatGPT to analyze.
    """
    # Your fetch logic
    return {
        "id": id,
        "title": "Record Title",
        "content": "Full record content...",
        "metadata": {"author": "Jane Doe", "date": "2024"}
    }
```

--------------------------------

### Override MCP Server Name with FastMCP CLI

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/mcp-json-configuration.mdx

These `fastmcp` commands show how to control the server name in the generated MCP JSON configuration. The first command uses the default name derived from the server script, while the second explicitly overrides it using the `--name` flag.

```bash
# Use server's built-in name (from FastMCP constructor)
fastmcp install mcp-json server.py

# Override with custom name
fastmcp install mcp-json server.py --name "Custom Server Name"
```

--------------------------------

### Configure FastMCP with JWTVerifier for Token Validation

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/auth/authentication.mdx

This Python example configures a `FastMCP` server to use `JWTVerifier` for validating incoming JSON Web Tokens. It requires the JWKS URI, issuer, and audience to verify token signatures and claims, ensuring only tokens from trusted sources are accepted.

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import JWTVerifier

auth = JWTVerifier(
    jwks_uri="https://your-auth-system.com/.well-known/jwks.json",
    issuer="https://your-auth-system.com", 
    audience="your-mcp-server"
)

mcp = FastMCP(name="Protected Server", auth=auth)
```

--------------------------------

### Install FastMCP Server with Custom Name and Dependencies (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

Demonstrates installing a FastMCP server with a custom server name using the `--server-name` option and including additional Python packages via `--with`. This ensures the server is clearly identifiable within the client and that all required libraries are installed in its isolated environment.

```bash
fastmcp install claude-desktop server.py:my_server --server-name "My Analysis Server" --with pandas
```

--------------------------------

### Synchronizing Development Environment with uv

Source: https://github.com/jlowin/fastmcp/blob/main/README.md

This command uses 'uv', a Python package installer, to synchronize the project's dependencies. It installs all necessary packages, including development tools, based on the project's configuration, ensuring a consistent environment.

```bash
uv sync
```

--------------------------------

### Configure FastMCP Server with WorkOSProvider (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/workos.mdx

This Python code demonstrates how to set up a FastMCP server to use WorkOS Connect for authentication. It initializes a `WorkOSProvider` with client credentials, including client ID, secret, AuthKit domain, base URL, and required OAuth scopes, then defines and registers a protected tool.

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.workos import WorkOSProvider

# Configure WorkOS OAuth
auth = WorkOSProvider(
    client_id="client_YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    authkit_domain="https://your-app.authkit.app",
    base_url="http://localhost:8000",
    required_scopes=["openid", "profile", "email"]
)

mcp = FastMCP("WorkOS Protected Server", auth=auth)

@mcp.tool
def protected_tool(message: str) -> str:
    """This tool requires authentication."""
    return f"Authenticated user says: {message}"

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
```

--------------------------------

### Test FastMCP Server with Inline Snapshot Assertions

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/testing.mdx

Use the inline-snapshot library to assert complex data structures from MCP servers. This approach makes tests easy to read and update when data structures change. Run 'pytest --inline-snapshot=fix,create' to automatically populate snapshots with actual data.

```python
from inline_snapshot import snapshot

async def test_list_tools(main_mcp_client: Client[FastMCPTransport]):
    list_tools = await main_mcp_client.list_tools()

    assert list_tools == snapshot()
```

--------------------------------

### Define FastAPI Operation IDs for FastMCP Component Naming (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/fastapi.mdx

This snippet highlights the importance of explicitly defining `operation_id` for FastAPI routes when integrating with FastMCP. Meaningful operation IDs become the component names in the MCP server, crucial for clear LLM interactions. It contrasts a good example with an explicit ID against a less ideal auto-generated name.

```python
# Good - explicit operation_id
@app.get("/users/{user_id}", operation_id="get_user_by_id")
def get_user(user_id: int):
    return {"id": user_id}

# Less ideal - auto-generated name
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"id": user_id}
```

--------------------------------

### Configure Descope Provider Environment Variables

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/descope.mdx

These environment variables are essential for setting up the Descope authentication provider for your FastMCP server. They define the Descope project ID, the base URL of your FastMCP server, and the Descope API base URL. Ensure these sensitive variables are configured securely in your deployment environment.

```Shell
FASTMCP_SERVER_AUTH_DESCOPEPROVIDER_PROJECT_ID=P2abc...123
FASTMCP_SERVER_AUTH_DESCOPEPROVIDER_BASE_URL=https://your-server.com
FASTMCP_SERVER_AUTH_DESCOPEPROVIDER_DESCOPE_BASE_URL=https://api.descope.com
```

--------------------------------

### FastMCP Server with AWSCognitoProvider

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/aws-cognito.mdx

Initializes the FastMCP server using the AWSCognitoProvider for handling authentication. This provider automatically manages JWT token validation and user claim extraction from AWS Cognito.

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.aws import AWSCognitoProvider
from fastmcp.server.dependencies import get_access_token


```

--------------------------------

### Configure FastMCP with Asynchronous Debug Token Validation (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/auth/token-verification.mdx

This snippet demonstrates how to set up FastMCP with a `DebugTokenVerifier` for asynchronous token validation. It uses a custom `validate_token` function, which might check a cache like Redis, and allows for flexible token acceptance during development, testing, or prototyping. It's crucial to understand that `DebugTokenVerifier` bypasses standard security checks and should be used with caution in controlled environments only.

```python
async def validate_token(token: str) -> bool:
    # Check if token exists in Redis, database, etc.
    return await redis.exists(f"valid_tokens:{token}")

verifier = DebugTokenVerifier(
    validate=validate_token,
    client_id="api-client",
    scopes=["api:access"]
)

mcp = FastMCP(name="Custom API", auth=verifier)
```

--------------------------------

### Understand Client Authentication Error (Python Traceback)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openai.mdx

This snippet displays an `pythonAPIStatusError` traceback that occurs when an unauthenticated client attempts to interact with a protected FastMCP server. The error message indicates an 'Unauthorized' (401) status, signifying that authentication is required.

```python
pythonAPIStatusError: Error code: 424 - {
    "error": {
        "message": "Error retrieving tool list from MCP server: 'dice_server'. Http status code: 401 (Unauthorized)",
        "type": "external_connector_error",
        "param": "tools",
        "code": "http_error"
    }
}
```

--------------------------------

### Configure Advanced Caching Settings in FastMCP

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

Shows how to customize the `ResponseCachingMiddleware` by configuring individual settings for list tools, call tools, and resource reads. This includes setting custom TTLs, specifying included tools, or disabling caching for specific operations.

```python
from fastmcp.server.middleware.caching import ResponseCachingMiddleware, CallToolSettings, ListToolsSettings, ReadResourceSettings

mcp.add_middleware(ResponseCachingMiddleware(
    list_tools_settings=ListToolsSettings(
        ttl=30,
    ),
    call_tool_settings=CallToolSettings(
        included_tools=["tool1"],
    ),
    read_resource_settings=ReadResourceSettings(
        enabled=False
    )
))
```

--------------------------------

### Generate MCP JSON Configuration to Stdout using FastMCP CLI

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/mcp-json-configuration.mdx

This command demonstrates how to use `fastmcp install mcp-json` to generate an MCP server configuration. The output is printed to standard output, making it useful for piping or redirection into other processes or files. It configures a server based on `server.py`.

```bash
fastmcp install mcp-json server.py
```

--------------------------------

### Configure FastMCP Client for Remote Authenticated Server (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/gemini.mdx

This Python snippet demonstrates how to configure a `fastmcp.Client` to connect to a remote FastMCP server that requires authentication. It specifies the server's URL and uses `BearerAuth` with a provided token. This client configuration can then be seamlessly integrated with the Gemini SDK as shown in previous examples.

```python
from fastmcp import Client
from fastmcp.client.auth import BearerAuth

mcp_client = Client(
    "https://my-server.com/mcp/",
    auth=BearerAuth("<your-token>"),
)
```

--------------------------------

### Prepare fastmcp Server Environment and Source (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-utilities-mcp_server_config-v1-mcp_server_config.mdx

This method orchestrates the preparation of both the execution environment and the server source. It can create a persistent `uv` project if an `output_dir` is provided, or perform ephemeral caching otherwise. The `skip_source` parameter allows for bypassing source preparation when not needed.

```python
prepare(self, skip_source: bool = False, output_dir: Path | None = None) -> None
```

--------------------------------

### Parameterized Testing for FastMCP Tools with Multiple Inputs

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/testing.mdx

Use pytest's parametrize decorator to test FastMCP tools with multiple input combinations. This example tests an 'add' tool with various number pairs, verifying the result data type and expected output. The fixture provides the client instance for calling tools.

```python
import pytest
from my_project.main import mcp

from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport
@pytest.fixture
async def main_mcp_client():
    async with Client(mcp) as client:
        yield client


@pytest.mark.parametrize(
    "first_number, second_number, expected",
    [
        (1, 2, 3),
        (2, 3, 5),
        (3, 4, 7),
    ],
)
async def test_add(
    first_number: int,
    second_number: int,
    expected: int,
    main_mcp_client: Client[FastMCPTransport],
):
    result = await main_mcp_client.call_tool(
        name="add", arguments={"x": first_number, "y": second_number}
    )
    assert result.data is not None
    assert isinstance(result.data, int)
    assert result.data == expected
```

--------------------------------

### Implement Tag-Based Tool Allowlisting in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/transports.mdx

Shows how to use tags and include_tags to allowlist specific tools from an MCP server. Only tools marked with the forecast tag will be available to the client, effectively filtering out all other tools from the server.

```python
tool_transformations = {
    "weather_get_forecast": {
        "enabled": True,
        "tags": ["forecast"]
    }
}


config = {
    "mcpServers": {
        "weather": {
            "url": "https://weather.example.com/mcp",
            "transport": "http",
            "tools": tool_transformations,
            "include_tags": ["forecast"]
        }
    }
}
```

--------------------------------

### Load Environment Variables from .env file via fastmcp install (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/claude-desktop.mdx

This bash command shows how to install a server with `fastmcp` for Claude Desktop, loading environment variables from a `.env` file. This approach simplifies managing multiple environment variables by centralizing them in a file, rather than passing them individually.

```bash
fastmcp install claude-desktop server.py --server-name "Weather Server" --env-file .env
```

--------------------------------

### Add Icon to a Prompt

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/icons.mdx

Shows the method for assigning an icon to a prompt in FastMCP. The icon is specified using the `icons` parameter within the `@mcp.prompt` decorator.

```python
@mcp.prompt(
    icons=[Icon(src="https://example.com/prompt-icon.png")]
)
def analyze_code(code: str):
    """Create a prompt for code analysis."""
    return f"Please analyze this code:\n\n{code}"
```

--------------------------------

### Restrict FastMCP OAuth Proxy Redirect URIs to Localhost (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/auth/oauth-proxy.mdx

This Python code configures the FastMCP OAuth Proxy to accept redirect URIs exclusively from localhost. By defining `allowed_client_redirect_uris` with `http://localhost:*` and `http://127.0.0.1:*`, this setting is ideal for development environments, enhancing security by limiting client access.

```python
auth = OAuthProxy(
    # ... other parameters ...
    allowed_client_redirect_uris=[
        "http://localhost:*",
        "http://127.0.0.1:*"
    ]
)
```

--------------------------------

### Define Optional and Required Parameters in Python with FastMCP

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/tools.mdx

FastMCP leverages standard Python function parameter conventions to distinguish between required and optional arguments. Parameters without default values are mandatory, while those with default values (including `None` for optional types) are considered optional. This allows LLM clients to selectively provide inputs.

```python
@mcp.tool
def search_products(
    query: str,                   # Required - no default value
    max_results: int = 10,        # Optional - has default value
    sort_by: str = "relevance",   # Optional - has default value
    category: str | None = None   # Optional - can be None
) -> list[dict]:
    """Search the product catalog."""
    # Implementation...
```

--------------------------------

### Define FastMCP Middleware Context Class in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-middleware-middleware.mdx

The `MiddlewareContext` class provides a unified context object for all operations within the FastMCP middleware pipeline. It centralizes state relevant to the current request or event. The `copy` method allows for creating modified instances of the context, enabling immutable transformations and preventing unintended side effects across middleware components.

```python
copy(self, **kwargs: Any) -> MiddlewareContext[T]
```

--------------------------------

### Manually Control FastMCP Client Initialization in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/client.mdx

Illustrates how to disable automatic client initialization and manually call the `initialize()` method. This provides fine-grained control over the initialization process, allowing for custom error handling or deferred setup.

```python
from fastmcp import Client

# Disable automatic initialization
client = Client("my_mcp_server.py", auto_initialize=False)

async with client:
    # Connection established, but not initialized yet
    print(f"Connected: {client.is_connected()}")
    print(f"Initialized: {client.initialize_result is not None}")  # False

    # Initialize manually with custom timeout
    result = await client.initialize(timeout=10.0)
    print(f"Server: {result.serverInfo.name}")

    # Now ready for operations
    tools = await client.list_tools()
```

--------------------------------

### Direct FastMCP Prompt Invocation with Native Python Types

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/prompts.mdx

Shows how to call a FastMCP prompt directly within a Python application using native Python data types. This bypasses the string conversion layer, making it suitable for internal or programmatic invocations where type safety is already ensured.

```python
# This also works for direct calls
result = await prompt.render({
    "numbers": [1, 2, 3, 4, 5],
    "metadata": {"source": "api", "version": "1.0"}, 
    "threshold": 2.5
})
```

--------------------------------

### Accessing Raw MCP Protocol Objects with FastMCP in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/tools.mdx

Explains how to use `call_tool_mcp()` to get the raw `mcp.types.CallToolResult` object, providing complete control over the server response. It notes that this method does not perform automatic deserialization, requiring manual content processing.

```python
async with client:
    result = await client.call_tool_mcp("potentially_failing_tool", {"param": "value"})
    # result -> mcp.types.CallToolResult
    
    if result.isError:
        print(f"Tool failed: {result.content}")
    else:
        print(f"Tool succeeded: {result.content}")
        # Note: No automatic deserialization with call_tool_mcp()
```

--------------------------------

### Report Absolute Progress in FastMCP (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/progress.mdx

Shows how to report progress using absolute values, such as the number of items processed out of a total count. This is useful for tasks with a discrete number of steps or items.

```python
@mcp.tool
async def backup_database(ctx: Context) -> str:
    """Backup database tables with absolute progress."""
    tables = ["users", "orders", "products", "inventory", "logs"]
    
    for i, table in enumerate(tables):
        await ctx.info(f"Backing up table: {table}")
        
        # Report absolute progress
        await ctx.report_progress(progress=i + 1, total=len(tables))
        
        # Simulate backup time
        await asyncio.sleep(0.5)
    
    return "Database backup completed"
```

--------------------------------

### Tool Class Methods for Management and Creation

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-tools-tool.mdx

The `Tool` class serves as a base for all tools within FastMCP. It includes methods for enabling (`enable`) and disabling (`disable`) tools, converting them to MCP format (`to_mcp_tool`), and importantly, creating new tools from Python functions (`from_function`). It also defines an abstract `run` method that subclasses must implement.

```python
class Tool:
    # ... other attributes ...

    def enable(self) -> None:
        """Enable the tool."""
        # Implementation details

    def disable(self) -> None:
        """Disable the tool."""
        # Implementation details

    def to_mcp_tool(self, **overrides: Any) -> MCPTool:
        """Convert the FastMCP tool to an MCP tool."""
        # Implementation details

    @classmethod
    def from_function(cls, fn: Callable[..., Any], name: str | None = None, title: str | None = None, description: str | None = None, icons: list[Icon] | None = None, tags: set[str] | None = None, annotations: ToolAnnotations | None = None, exclude_args: list[str] | None = None, output_schema: dict[str, Any] | Literal[False] | NotSetT | None = NotSet, serializer: ToolResultSerializerType | None = None, meta: dict[str, Any] | None = None, enabled: bool | None = None) -> FunctionTool:
        """Create a Tool from a function."""
        # Implementation details

    def run(self, arguments: dict[str, Any]) -> ToolResult:
        """Run the tool with arguments."""
        # This method must be implemented by subclasses.
        # It can return a list of ContentBlocks or a tuple of (list of ContentBlocks, dict of structured output).
        raise NotImplementedError

    @classmethod
    def from_tool(cls, tool: Tool) -> TransformedTool:
        """Transform an existing tool."""
        # Implementation details
```

--------------------------------

### POST /progress

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-client.mdx

Sends a progress notification for an ongoing operation. Includes a progress token, current progress value, optional total, and a descriptive message.

```APIDOC
## POST /progress

### Description
Send a progress notification to the server for an ongoing operation. This allows the server to update clients about the status of a long-running task.

### Method
POST

### Endpoint
/progress

### Parameters
#### Request Body
- **progress_token** (string | number) - Required. A unique token identifying the specific progress update.
- **progress** (number) - Required. The current progress value (e.g., a percentage or a count).
- **total** (number | null) - Optional. The total value against which `progress` is measured, allowing for percentage calculation (e.g., 100 for percentage, or total items).
- **message** (string | null) - Optional. A human-readable message describing the current state of progress.

### Request Example
```json
{
  "progress_token": "import-job-789",
  "progress": 0.75,
  "total": 1.0,
  "message": "Processing 300 of 400 records."
}
```

### Response
#### Success Response (200)
- **message** (string) - A confirmation message indicating the progress notification was sent.

#### Response Example
```json
{
  "message": "Progress notification sent."
}
```
```

--------------------------------

### Create Basic MCP Server Instance in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/tutorials/create-mcp-server.mdx

Initialize a FastMCP server by creating an instance of the FastMCP class with a descriptive name. This serves as the container for all tools and resources.

```python
from fastmcp import FastMCP

# Create a server instance with a descriptive name
mcp = FastMCP(name="My First MCP Server")
```

--------------------------------

### List Resource Templates with Python Client

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/resources.mdx

This code shows how to fetch all available resource templates from an MCP server using the `client.list_resource_templates()` method. It then iterates over the templates, displaying their URI template, name, description, and `_fastmcp` tags if present.

```python
async with client:
    templates = await client.list_resource_templates()
    # templates -> list[mcp.types.ResourceTemplate]
    
    for template in templates:
        print(f"Template URI: {template.uriTemplate}")
        print(f"Name: {template.name}")
        print(f"Description: {template.description}")
        # Access tags and other metadata
        if hasattr(template, '_meta') and template._meta:
            fastmcp_meta = template._meta.get('_fastmcp', {})
            print(f"Tags: {fastmcp_meta.get('tags', [])}")
```

--------------------------------

### Configure Specific and Wildcard Redirect URIs for FastMCP OAuth Proxy (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/auth/oauth-proxy.mdx

This Python example illustrates how to specify a list of permitted redirect URIs for the FastMCP OAuth Proxy, including support for wildcard patterns. Using `allowed_client_redirect_uris` with specific URLs and wildcards like `https://*.mycompany.com/auth/*` enables granular control over client connections, crucial for production deployments and security.

```python
auth = OAuthProxy(
    # ... other parameters ...
    allowed_client_redirect_uris=[
        "http://localhost:*",
        "https://claude.ai/api/mcp/auth_callback",
        "https://*.mycompany.com/auth/*"  # Wildcard patterns supported
    ]
)
```

--------------------------------

### Test FastMCP Client with WorkOS Authentication (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/workos.mdx

This Python client code demonstrates how to connect to a WorkOS-protected FastMCP server. The `Client` instance, configured with `auth="oauth"`, automatically handles the WorkOS OAuth flow, including opening a browser for user login, and then successfully calls a protected tool.

```python
from fastmcp import Client
import asyncio

async def main():    
    # The client will automatically handle WorkOS OAuth
    async with Client("http://localhost:8000/mcp", auth="oauth") as client:
        # First-time connection will open WorkOS login in your browser
        print("✓ Authenticated with WorkOS!")
        
        # Test the protected tool
        result = await client.call_tool("protected_tool", {"message": "Hello!"})
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

--------------------------------

### Install FastMCP Server with Environment Variables in Cursor - Bash

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/cursor.mdx

Installs a FastMCP server in Cursor with explicitly defined environment variables. This is necessary because Cursor runs servers in an isolated environment with no access to shell environment variables. Variables like API keys and debug flags must be passed explicitly during installation.

```bash
fastmcp install cursor server.py --server-name "Weather Server" \
  --env API_KEY=your-api-key \
  --env DEBUG=true
```

--------------------------------

### Run FastMCP Server with Default STDIO Transport (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/running-server.mdx

This example shows how to run a FastMCP server utilizing the default STDIO (Standard Input/Output) transport. When `run()` is called without specific transport arguments, it defaults to STDIO, making it ideal for command-line tools, desktop applications, and local development where clients spawn server processes as needed.

```python
from fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.tool
def hello(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()  # Uses STDIO transport by default
```

--------------------------------

### Add Icon to a Tool

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/icons.mdx

Illustrates how to attach an icon to a specific tool defined within FastMCP. This is achieved by passing an Icon object to the `icons` parameter of the `@mcp.tool` decorator.

```python
from mcp.types import Icon

@mcp.tool(
    icons=[Icon(src="https://example.com/calculator-icon.png")]
)
def calculate_sum(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b
```

--------------------------------

### Configure FastMCPOpenAPI Server Instance

Source: https://github.com/jlowin/fastmcp/blob/main/src/fastmcp/experimental/server/openapi/README.md

Demonstrates how to initialize the FastMCPOpenAPI server with an OpenAPI specification and an HTTP client. Optional parameters like server name, route map, and caching can be configured. This setup is crucial for defining the API's behavior and enabling performance optimizations.

```python
server = FastMCPOpenAPI(
    openapi_spec=spec,           # Required: OpenAPI specification
    client=httpx_client,         # Required: HTTP client instance
    name="API Server",           # Optional: Server name
    route_map=custom_routes,     # Optional: Custom route mappings
    enable_caching=True,         # Optional: Enable response caching
)
```

--------------------------------

### Install FastMCP Server with Inline Environment Variables (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/cli.mdx

Explains how to pass environment variables directly to the FastMCP server during installation using the `--env` option. This is crucial for configuring server behavior, such as API keys or debug modes, within the isolated client environment, ensuring sensitive information is properly handled.

```bash
fastmcp install claude-code server.py --env API_KEY=secret --env DEBUG=true
fastmcp install cursor server.py --env API_KEY=secret --env DEBUG=true
```

--------------------------------

### Define FastMCP Prompt with PromptResult Return Type

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/prompts.mdx

Illustrates how to define a FastMCP prompt function that returns a `PromptResult`, which can be a list of `Message` or `str` objects. This enables the prompt to generate complex, multi-message conversational responses, providing more flexibility than a simple string return.

```python
from fastmcp.prompts.prompt import Message, PromptResult

@mcp.prompt
def roleplay_scenario(character: str, situation: str) -> PromptResult:
    """Sets up a roleplaying scenario with initial messages."""
    return [
        Message(f"Let's roleplay. You are {character}. The situation is: {situation}"),
        Message("Okay, I understand. I am ready. What happens next?", role="assistant")
    ]
```

--------------------------------

### Configure Production Server with Encrypted Token Storage

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/auth0.mdx

This Python code sets up a production fastmcp server with Auth0 authentication and persistent token management. It uses Redis for storage, wrapped in FernetEncryptionWrapper for encrypting tokens at rest. This requires environment variables for JWT signing key, Redis connection details, and encryption keys. Dependencies include 'fastmcp', 'key_value.aio.stores.redis', 'key_value.aio.wrappers.encryption', and 'cryptography.fernet'.

```python
import os
from fastmcp import FastMCP
from fastmcp.server.auth.providers.auth0 import Auth0Provider
from key_value.aio.stores.redis import RedisStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper
from cryptography.fernet import Fernet

# Production setup with encrypted persistent token storage
auth_provider = Auth0Provider(
    config_url="https://.../.well-known/openid-configuration",
    client_id="tv2ObNgaZAWWhhycr7Bz1LU2mxlnsmsB",
    client_secret="vPYqbjemq...",
    audience="https://...",
    base_url="https://your-production-domain.com",

    # Production token management
    jwt_signing_key=os.environ["JWT_SIGNING_KEY"],
    client_storage=FernetEncryptionWrapper(
        key_value=RedisStore(
            host=os.environ["REDIS_HOST"],
            port=int(os.environ["REDIS_PORT"])
        ),
        fernet=Fernet(os.environ["STORAGE_ENCRYPTION_KEY"])
    )
)

mcp = FastMCP(name="Production Auth0 App", auth=auth_provider)
```

--------------------------------

### Configure Python MCP Client with Global Progress Handler

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/progress.mdx

This code demonstrates how to initialize a fastmcp.Client with a custom asynchronous function acting as a global progress handler. The handler processes 'progress', 'total', and 'message' parameters to display operation status, such as percentage completion.

```python
from fastmcp import Client

async def my_progress_handler(
    progress: float, 
    total: float | None, 
    message: str | None
) -> None:
    if total is not None:
        percentage = (progress / total) * 100
        print(f"Progress: {percentage:.1f}% - {message or ''}")
    else:
        print(f"Progress: {progress} - {message or ''}")

client = Client(
    "my_mcp_server.py",
    progress_handler=my_progress_handler
)
```

--------------------------------

### Prepare FastMCP Environment and Run Server

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/server-configuration.mdx

This pattern demonstrates how to create a persistent FastMCP environment once and then reuse it to run the server. This separates the potentially slow environment setup from the faster server execution, which is ideal for deployment scenarios.

```bash
fastmcp project prepare fastmcp.json --output-dir ./env
```

```bash
fastmcp run fastmcp.json --project ./env
```

--------------------------------

### Create and Modify a Local Copy of a Mirrored FastMCP Tool (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/proxy.mdx

This Python example demonstrates how to interact with mirrored components from a FastMCP proxy server. It shows how to retrieve a mirrored tool, create a modifiable local copy, add it to your own server, and then disable the local copy, effectively overriding the remote component's behavior.

```python
# Create your own server
my_server = FastMCP("MyServer")

# Get a proxy server
proxy = FastMCP.as_proxy("backend_server.py")

# Get mirrored components from proxy
mirrored_tool = await proxy.get_tool("useful_tool")

# Create a local copy that you can modify
local_tool = mirrored_tool.copy()

# Add the local copy to your server
my_server.add_tool(local_tool)

# Now you can disable YOUR copy
local_tool.disable()
```

--------------------------------

### Pass Command-Line Arguments to FastMCP Server

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/server-configuration.mdx

This JSON example demonstrates how to specify command-line arguments for the FastMCP server. Arguments defined in the `args` field are passed after `--` to the server's internal argument parser, allowing for runtime customization such as pointing to a specific configuration file.

```json
"args": ["--config", "server-config.json"]
```

--------------------------------

### PUT /config/deployment

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/server-configuration.mdx

Configures the runtime behavior of the FastMCP server. This includes settings for transport protocols, network interfaces, logging levels, environment variables, and command-line arguments, which dictate how the server operates upon execution.

```APIDOC
## PUT /config/deployment

### Description
This endpoint allows you to define the runtime configuration for the FastMCP server. It encompasses various settings that control the server's operational characteristics from startup, including network parameters, environmental variables, and execution context.

### Method
PUT

### Endpoint
/config/deployment

### Parameters
#### Request Body
- **deployment** (object) - Optional - Runtime configuration for the server.
  - **transport** (string) - Optional - Default: `"stdio"` - Protocol for client communication.
    - `"stdio"`: Standard input/output for desktop clients
    - `"http"`: Network-accessible HTTP server
    - `"sse"`: Server-sent events
  - **host** (string) - Optional - Default: `"127.0.0.1"` - Network interface to bind (HTTP transport only).
    - `"127.0.0.1"`: Local connections only
    - `"0.0.0.0"`: All network interfaces
  - **port** (integer) - Optional - Default: `3000` - Port number for HTTP transport.
  - **path** (string) - Optional - Default: `"/mcp/"` - URL path for the MCP endpoint when using HTTP transport.
  - **log_level** (string) - Optional - Default: `"INFO"` - Server logging verbosity.
    - `"DEBUG"`: Detailed debugging information
    - `"INFO"`: General informational messages
    - `"WARNING"`: Warning messages
    - `"ERROR"`: Error messages only
    - `"CRITICAL"`: Critical errors only
  - **env** (object) - Optional - Environment variables to set when running the server. Supports `${VAR_NAME}` syntax for runtime interpolation.
  - **cwd** (string) - Optional - Working directory for the server process. Relative paths are resolved from the config file location.
  - **args** (list[string]) - Optional - Command-line arguments to pass to the server, passed after `--` to the server's argument parser.

### Request Example
```json
{
  "deployment": {
    "transport": "http",
    "host": "0.0.0.0",
    "port": 8080,
    "path": "/my-mcp-service/",
    "log_level": "DEBUG",
    "env": {
      "API_KEY": "your-secret-key",
      "DATABASE_URL": "postgres://${DB_USER}@${DB_HOST}/mydb"
    },
    "cwd": "./server_root",
    "args": ["--verbose", "--config", "server-config.json"]
  }
}
```

### Response
#### Success Response (200)
- **message** (string) - A confirmation message indicating that the deployment configuration has been successfully processed.

#### Response Example
```json
{
  "message": "Deployment configuration successfully processed."
}
```
```

--------------------------------

### Run fastmcp Server with Current Configuration (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-utilities-mcp_server_config-v1-mcp_server_config.mdx

This method loads the server based on the current configuration and initiates its execution. It accepts additional keyword arguments, allowing for dynamic overrides of configuration settings directly during runtime. This provides flexibility for customizing server behavior without modifying the base configuration.

```python
run_server(self, **kwargs: Any) -> None
```

--------------------------------

### Run Async HTTP/Streamable/SSE Server in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

This function starts the server using a specified HTTP transport type: standard HTTP, streamable HTTP, or Server-Sent Events (SSE). It supports configuring host, port, logging, endpoint paths, Uvicorn settings, middleware, JSON response, and stateless HTTP behavior. This method orchestrates the server's lifecycle based on provided or default parameters.

```python
run_http_async(self, show_banner: bool = True, transport: Literal['http', 'streamable-http', 'sse'] = 'http', host: str | None = None, port: int | None = None, log_level: str | None = None, path: str | None = None, uvicorn_config: dict[str, Any] | None = None, middleware: list[ASGIMiddleware] | None = None, json_response: bool | None = None, stateless_http: bool | None = None) -> None
```

--------------------------------

### Set Environment Variables via fastmcp install (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/claude-desktop.mdx

This bash command demonstrates how to install a server with `fastmcp` for Claude Desktop, explicitly passing environment variables like `API_KEY` and `DEBUG` directly during the installation process. This is necessary because Claude Desktop runs servers in an isolated environment with no access to your shell environment.

```bash
fastmcp install claude-desktop server.py --server-name "Weather Server" \
  --env API_KEY=your-api-key \
  --env DEBUG=true
```

--------------------------------

### Example JSON Response for Component Action

Source: https://github.com/jlowin/fastmcp/blob/main/src/fastmcp/contrib/component_manager/README.md

This is an example HTTP response indicating a successful operation, such as disabling a tool. The response includes a 200 OK status and a JSON body with a confirmation message.

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "message": "Disabled tool: example_tool"
}
```

--------------------------------

### PromptToolMiddleware for FastMCP server

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-middleware-tool_injection.mdx

A middleware designed to inject prompts as tools into the MCP server context. This allows prompts to be treated and invoked like other tools within the server.

```python
class PromptToolMiddleware:
    """A middleware for injecting prompts as tools into the context."""
    pass
```

--------------------------------

### Configure Disk Storage for FastMCP Caching Middleware

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

Provides an example of configuring the `ResponseCachingMiddleware` to use a disk-based storage backend. This ensures cache persistence across server restarts, which is suitable for production environments.

```python
from fastmcp.server.middleware.caching import ResponseCachingMiddleware
from key_value.aio.stores.disk import DiskStore

mcp.add_middleware(ResponseCachingMiddleware(
    cache_storage=DiskStore(directory="cache"),
))
```

--------------------------------

### Authenticate FastMCP Client with Azure OAuth

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/azure.mdx

Demonstrates how to create a FastMCP client that automatically handles Azure OAuth authentication. The client connects to the server at `http://localhost:8000/mcp` with `auth="oauth"`. The first connection will trigger a browser-based login flow, and subsequent connections will use cached tokens.

```python
from fastmcp import Client
import asyncio

async def main():
    # The client will automatically handle Azure OAuth
    async with Client("http://localhost:8000/mcp", auth="oauth") as client:
        # First-time connection will open Azure login in your browser
        print("✓ Authenticated with Azure!")
        
        # Test the protected tool
        result = await client.call_tool("get_user_info")
        print(f"Azure user: {result['email']}")
        print(f"Name: {result['name']}")

if __name__ == "__main__":
    asyncio.run(main())

```

--------------------------------

### FastMCP ToolResult for Complete Output Control (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/tools.mdx

Demonstrates the use of `ToolResult` for comprehensive control over a tool's response, enabling explicit management of traditional content, structured data, and execution metadata. It shows how to instantiate `ToolResult` with `content` (human-readable summary), `structured_content` (programmatic data), and `meta` (runtime metrics). This approach bypasses automatic wrapping or transformations by FastMCP.

```python
from fastmcp.tools.tool import ToolResult
from mcp.types import TextContent

@mcp.tool
def advanced_tool() -> ToolResult:
    """Tool with full control over output."""
    return ToolResult(
        content=[TextContent(type="text", text="Human-readable summary的发展")]
        structured_content={"data": "value", "count": 42},
        meta={"execution_time_ms": 145}
    )
```

--------------------------------

### Production Configuration for FastMCP with Persistent Token Management

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/azure.mdx

Configures a FastMCP server for production use with persistent token management. It involves setting `jwt_signing_key` for secure token signing and `client_storage` using a `RedisStore` with `FernetEncryptionWrapper` for encrypted storage of client tokens across server restarts. This ensures a more robust and secure deployment.

```python
import os
from fastmcp import FastMCP
from fastmcp.server.auth.providers.azure import AzureProvider
from key_value.aio.stores.redis import RedisStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper
from cryptography.fernet import Fernet

```

--------------------------------

### Access Current HTTP Request in FastMCP using Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/context.mdx

Demonstrates the recommended way to access the current HTTP request through the `get_http_request()` dependency function in FastMCP. This approach provides universal access to HTTP request data, such as headers, client IP, and URL path, within any part of a request's execution flow, including helper functions or middleware, not just directly within MCP tools.

```python
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_request
from starlette.requests import Request

mcp = FastMCP(name="HTTP Request Demo")

@mcp.tool
async def user_agent_info() -> dict:
    """Return information about the user agent."""
    # Get the HTTP request
    request: Request = get_http_request()
    
    # Access request data
    user_agent = request.headers.get("user-agent", "Unknown")
    client_ip = request.client.host if request.client else "Unknown"
    
    return {
        "user_agent": user_agent,
        "client_ip": client_ip,
        "path": request.url.path,
    }
```

--------------------------------

### Test Azure OAuth Integration with FastMCP Client

Source: https://github.com/jlowin/fastmcp/blob/main/examples/auth/azure_oauth/README.md

Executes the FastMCP client application to test Azure OAuth authentication flow. Connects to the running server and validates the OAuth callback mechanism. Used for verifying proper configuration of Azure App Registration and OAuth provider setup.

```bash
uv run python client.py
```

--------------------------------

### Install Eunomia MCP Package

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/eunomia-authorization.mdx

This command installs the necessary Python package `eunomia-mcp` using pip, which is required to integrate Eunomia authorization middleware with FastMCP servers.

```bash
pip install eunomia-mcp
```

--------------------------------

### Implement Basic LLM Sampling Handler for FastMCP Client (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/sampling.mdx

This example provides a basic implementation of a `sampling_handler` for the `fastmcp.Client`. It shows how to extract text content from `SamplingMessage` objects, utilize an optional `systemPrompt` from `SamplingParams`, and construct a placeholder response based on the conversation history. This structure serves as a starting point for integrating with any LLM service.

```python
from fastmcp import Client
from fastmcp.client.sampling import SamplingMessage, SamplingParams, RequestContext

async def basic_sampling_handler(
    messages: list[SamplingMessage],
    params: SamplingParams,
    context: RequestContext
) -> str:
    # Extract message content
    conversation = []
    for message in messages:
        content = message.content.text if hasattr(message.content, 'text') else str(message.content)
        conversation.append(f"{message.role}: {content}")

    # Use the system prompt if provided
    system_prompt = params.systemPrompt or "You are a helpful assistant."

    # Here you would integrate with your preferred LLM service
    # This is just a placeholder response
    return f"Response based on conversation: {' | '.join(conversation)}"

client = Client(
    "my_mcp_server.py",
    sampling_handler=basic_sampling_handler
)
```

--------------------------------

### Transform Client Method into Tool (FastMCP Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/tool-transformation.mdx

This FastMCP example demonstrates how to directly wrap an existing client method as a tool using `Tool.from_tool` and `ArgTransform`. This pattern eliminates boilerplate wrapper functions, treating the tool definition as an annotation layer over the client method.

```python
from fastmcp import FastMCP
from fastmcp.tools import Tool
from fastmcp.tools.tool_transform import ArgTransform

mcp = FastMCP("GitHub Tools")

# Wrap a client method directly as a tool
get_repo_tool = Tool.from_tool(
    tool=Tool.from_function(fn=github_client.get_repository),
    description="Get basic information about a GitHub repository.",
    transform_args={
        "owner": ArgTransform(description="The owner of the repository."),
        "repo": ArgTransform(description="The name of the repository."),
    }
)

mcp.add_tool(get_repo_tool)
```

--------------------------------

### Install FastMCP Server in Cursor IDE in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-cli-install-cursor.mdx

Installs FastMCP server in Cursor IDE with comprehensive configuration options. Supports global and workspace-specific installations with parameters for file path, server object, custom name, editable packages, environment variables, Python version, requirements files, and workspace directory. Returns boolean indicating success.

```python
def install_cursor(
    file: Path,
    server_object: str | None,
    name: str
) -> bool:
    """
    Install FastMCP server in Cursor.

    Args:
        file: Path to the server file
        server_object: Optional server object name (for :object suffix)
        name: Name for the server in Cursor
        with_editable: Optional list of directories to install in editable mode
        with_packages: Optional list of additional packages to install
        env_vars: Optional dictionary of environment variables
        python_version: Optional Python version to use
        with_requirements: Optional requirements file to install from
        project: Optional project directory to run within
        workspace: Optional workspace directory for project-specific installation

    Returns:
        True if installation was successful, False otherwise
    """
```

--------------------------------

### FunctionResource Class Methods in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-resources-resource.mdx

Details the methods of the `FunctionResource` class in Python, which allows for lazy loading of data. It includes a class method `from_function` to create instances and an overridden `read` method that executes the wrapped function to retrieve resource content. This is efficient for potentially expensive data operations.

```python
from_function(cls, fn: Callable[..., Any], uri: str | AnyUrl, name: str | None = None, title: str | None = None, description: str | None = None, icons: list[Icon] | None = None, mime_type: str | None = None, tags: set[str] | None = None, enabled: bool | None = None, annotations: Annotations | None = None, meta: dict[str, Any] | None = None) -> FunctionResource

read(self) -> str | bytes
```

--------------------------------

### Retrieve Cache Statistics from FastMCP Caching Middleware

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

Demonstrates how to access and retrieve operation statistics (hits, misses, etc.) from an instance of the `ResponseCachingMiddleware` after it has been added to the application, useful for monitoring cache performance.

```python
from fastmcp.server.middleware.caching import ResponseCachingMiddleware

middleware = ResponseCachingMiddleware()
mcp.add_middleware(middleware)

# Later, retrieve statistics
stats = middleware.statistics()
print(f"Total cache operations: {stats}")
```

--------------------------------

### Access OpenAPI Tags in FastMCP Client Metadata

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openapi.mdx

FastMCP automatically extracts OpenAPI tags from your specification and makes them available in the client's metadata under `_meta._fastmcp.tags`. This allows clients to filter and organize components based on their original OpenAPI categorization. The example shows an OpenAPI spec defining tags and a Python client accessing these tags.

```json
{
  "paths": {
    "/users": {
      "get": {
        "tags": ["users", "public"],
        "operationId": "list_users",
        "summary": "List all users"
      }
    }
  }
}
```

```python
async with client:
    tools = await client.list_tools()
    for tool in tools:
        if hasattr(tool, '_meta') and tool._meta:
            # OpenAPI tags are now available in _fastmcp namespace!
            fastmcp_meta = tool._meta.get('_fastmcp', {})
            openapi_tags = fastmcp_meta.get('tags', [])
            if 'users' in openapi_tags:
                print(f"Found user-related tool: {tool.name}")
```

--------------------------------

### ASGI Application Deployment

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/http.mdx

Creates a FastMCP ASGI application that can be served by any ASGI server (e.g., Uvicorn). This approach offers more flexibility for production deployments, allowing for advanced server configurations and integration with existing web applications.

```python
from fastmcp import FastMCP

mcp = FastMCP("My Server")

@mcp.tool
def process_data(input: str) -> str:
    """Process data on the server"""
    return f"Processed: {input}"

# Create ASGI application
app = mcp.http_app()
```

--------------------------------

### Configure FastMCP Server with Auth0Provider

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/auth0.mdx

This Python code snippet demonstrates how to initialize a FastMCP server to use Auth0 for authentication. It configures the Auth0Provider with Auth0 application credentials (config URL, client ID, client secret, audience, and base URL) and includes a protected tool to retrieve and display token information.

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.auth0 import Auth0Provider

# The Auth0Provider utilizes Auth0 OIDC configuration
auth_provider = Auth0Provider(
    config_url="https://.../.well-known/openid-configuration",  # Your Auth0 configuration URL
    client_id="tv2ObNgaZAWWhhycr7Bz1LU2mxlnsmsB",               # Your Auth0 application Client ID
    client_secret="vPYqbjemq...",                               # Your Auth0 application Client Secret
    audience="https://...",                                     # Your Auth0 API audience
    base_url="http://localhost:8000",                           # Must match your application configuration
    # redirect_path="/auth/callback"                            # Default value, customize if needed
)

mcp = FastMCP(name="Auth0 Secured App", auth=auth_provider)

# Add a protected tool to test authentication
@mcp.tool
async def get_token_info() -> dict:
    """Returns information about the Auth0 token."""
    from fastmcp.server.dependencies import get_access_token

    token = get_access_token()

    return {
        "issuer": token.claims.get("iss"),
        "audience": token.claims.get("aud"),
        "scope": token.claims.get("scope")
    }
```

--------------------------------

### Render a specific prompt in FastMCP server

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-middleware-tool_injection.mdx

Renders a specific prompt available on the MCP server, allowing for dynamic generation of responses based on provided arguments. It returns a `GetPromptResult` object containing the rendered prompt.

```python
def get_prompt(context: Context, name: Annotated[str, 'The name of the prompt to render.'], arguments: Annotated[dict[str, Any] | None, 'The arguments to pass to the prompt.'] = None) -> mcp.types.GetPromptResult:
    """Render a prompt available on the server."""
    pass
```

--------------------------------

### Server Composition with Parent and Child Middleware

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/middleware.mdx

This snippet illustrates server composition using FastMCP's `mount` functionality. It shows a parent server with its own middleware and a child server with its specific middleware. Parent middleware applies to all requests, including those routed to mounted servers, while child middleware only applies to requests handled by the child server.

```python
from fastmcp import FastMCP
from fastmcp.server.middleware.authentication import AuthenticationMiddleware
from fastmcp.server.middleware.logging import LoggingMiddleware
from fastmcp.server.tool import Tool

# Parent server with middleware
parent = FastMCP("Parent")
parent.add_middleware(AuthenticationMiddleware("token"))

# Child server with its own middleware  
child = FastMCP("Child")
child.add_middleware(LoggingMiddleware())

@child.tool
def child_tool() -> str:
    return "from child"

# Mount the child server
parent.mount(child, prefix="child")
```

--------------------------------

### Disable FastMCP Prompt During Creation (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/prompts.mdx

This snippet demonstrates how to disable a FastMCP prompt immediately upon its creation by setting the 'enabled' parameter to 'False' within the '@mcp.prompt' decorator. A disabled prompt will not appear in the list of available prompts and attempting to call it will result in an 'Unknown prompt' error.

```python
@mcp.prompt(enabled=False)
def experimental_prompt():
    """This prompt is not ready for use."""
    return "This is an experimental prompt."
```

--------------------------------

### Python FastMCP: Example Tool for Notifications

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/tools.mdx

A simple example of a tool definition in FastMCP. This snippet is used to illustrate the automatic `notifications/tools/list_changed` notifications sent when tools are modified.

```python
# Assuming mcp is an instance of FastMCP
# mcp = FastMCP()

@mcp.tool
def example_tool() -> str:
    return "Hello!"
```

--------------------------------

### Create a FunctionPrompt from Callable in FastMCP Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-prompts-prompt.mdx

This class method creates a FunctionPrompt instance from a Python callable. The callable can return a string, Message object, dictionary, or a sequence of these, which are converted into prompt messages. It supports specifying metadata like name, title, description, icons, tags, enabled status, and additional custom metadata.

```python
from_function(cls, fn: Callable[..., PromptResult | Awaitable[PromptResult]], name: str | None = None, title: str | None = None, description: str | None = None, icons: list[Icon] | None = None, tags: set[str] | None = None, enabled: bool | None = None, meta: dict[str, Any] | None = None) -> FunctionPrompt
```

--------------------------------

### Connect FastMCP Client and Create Proxy (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/proxy.mdx

This snippet demonstrates how to connect a client to a FastMCP backend server and create a proxy that reuses the connected session for all requests. It includes a warning about potential context mixing in concurrent scenarios if not explicitly synchronized.

```python
async with Client("backend_server.py") as connected_client:
    # This proxy will reuse the connected session for all requests
    proxy = FastMCP.as_proxy(connected_client)
    
    # ⚠️ Warning: All requests share the same backend session
    # This may cause context mixing in concurrent scenarios
```

--------------------------------

### Exclude Arguments from FastMCP Tool Schema (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/tools.mdx

Learn how to exclude specific arguments from a FastMCP tool's schema, preventing them from being exposed to LLMs or clients. This is useful for arguments injected at runtime (e.g., `user_id`, credentials). Only arguments with default values can be excluded; attempting to exclude a required argument will raise an error.

```python
@mcp.tool(
    name="get_user_details",
    exclude_args=["user_id"]
)
def get_user_details(user_id: str = None) -> str:
    # user_id will be injected by the server, not provided by the LLM
    ...
```

--------------------------------

### Extract Tenant and User Data from Access Token Claims in FastMCP Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/context.mdx

This code illustrates how to access the `claims` field within a FastMCP `AccessToken` to extract specific data. It demonstrates retrieving a custom `tenant_id` and the standard `sub` (subject) claim for user identification. This is crucial for implementing multi-tenancy and fine-grained authorization logic based on token contents.

```python
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_access_token

mcp = FastMCP(name="Multi-tenant Demo")

@mcp.tool
async def get_tenant_data(resource_id: str) -> dict:
    """Get tenant-specific data using token claims."""
    token: AccessToken | None = get_access_token()
    
    # Extract tenant ID from token claims
    tenant_id = token.claims.get("tenant_id") if token else None
    
    # Extract user ID from standard JWT subject claim
    user_id = token.claims.get("sub") if token else None
    
    # Use tenant and user info to authorize and filter data
    if not tenant_id:
        raise ValueError("No tenant information in token")
    
    return {
        "resource_id": resource_id,
        "tenant_id": tenant_id,
        "user_id": user_id,
        "data": f"Tenant-specific data for {tenant_id}",
    }
```

--------------------------------

### Configure FastMCP Proxy for Fresh Sessions per Request

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/proxy.mdx

This code snippet illustrates the recommended way to configure a FastMCP proxy to ensure each incoming request gets its own isolated backend session. By passing a disconnected `ProxyClient`, it prevents context mixing between concurrent client requests, enhancing reliability and concurrency for the backend server.

```python
from fastmcp.server.proxy import ProxyClient

# Each request creates a fresh backend session (recommended)
proxy = FastMCP.as_proxy(ProxyClient("backend_server.py"))

# Multiple clients can use this proxy simultaneously without interference:
# - Client A calls a tool -> gets isolated backend session
# - Client B calls a tool -> gets different isolated backend session  
# - No context mixing between requests
```

--------------------------------

### Implement retry logic with RetryMiddleware in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-middleware-error_handling.mdx

This method of `RetryMiddleware` applies automatic retry logic to requests that encounter transient failures. It uses an exponential backoff strategy to prevent overwhelming the server or external dependencies during retries. It takes a `MiddlewareContext` and a `CallNext` function as input, returning an arbitrary type.

```python
on_request(self, context: MiddlewareContext, call_next: CallNext) -> Any
```

--------------------------------

### Constrain elicitation responses with options in FastMCP (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/elicitation.mdx

FastMCP allows constraining user responses to a specific set of values, which is automatically adapted for MCP spec compliance. This can be achieved by passing a list of strings, using a `typing.Literal` type, or defining a Python `Enum` as the `response_type` parameter.

```python
@mcp.tool
async def set_priority(ctx: Context) -> str:
    """Set task priority level."""
    result = await ctx.elicit(
        "What priority level?", 
        response_type=["low", "medium", "high"],
    )
    
    if result.action == "accept":
        return f"Priority set to: {result.data}"
```

```python
from typing import Literal

@mcp.tool
async def set_priority(ctx: Context) -> str:
    """Set task priority level."""
    result = await ctx.elicit(
        "What priority level?", 
        response_type=Literal["low", "medium", "high"]
    )
    
    if result.action == "accept":
        return f"Priority set to: {result.data}"
    return "No priority set"
```

```python
from enum import Enum

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"   

@mcp.tool
async def set_priority(ctx: Context) -> str:
    """Set task priority level."""
    result = await ctx.elicit("What priority level?", response_type=Priority)
    
    if result.action == "accept":
        return f"Priority set to: {result.data.value}"
    return "No priority set"
```

--------------------------------

### GET /ping

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-client.mdx

Sends a ping request to the server to verify connectivity and responsiveness. Returns a boolean indicating success.

```APIDOC
## GET /ping

### Description
Send a ping request to the server to check connectivity and responsiveness.

### Method
GET

### Endpoint
/ping

### Parameters

### Request Example
{}

### Response
#### Success Response (200)
- **success** (boolean) - True if the ping was successful and the server responded, False otherwise.

#### Response Example
```json
{
  "success": true
}
```
```

--------------------------------

### Trigger Resource List Change Notifications in FastMCP (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/resources.mdx

Demonstrates how FastMCP automatically sends `notifications/resources/list_changed` to connected clients when resources are added, enabled, or disabled. These operations must occur within an active MCP request context to trigger notifications, allowing clients to stay updated without polling.

```python
@mcp.resource("data://example")
def example_resource() -> str:
    return "Hello!"

# These operations trigger notifications:
mcp.add_resource(example_resource)  # Sends resources/list_changed notification
example_resource.disable()          # Sends resources/list_changed notification  
example_resource.enable()           # Sends resources/list_changed notification
```

--------------------------------

### Customize FastMCP Component Names from OpenAPI operationId

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openapi.mdx

This Python snippet illustrates how to use the `mcp_names` dictionary with `FastMCP.from_openapi` to explicitly map OpenAPI `operationId`s to desired custom component names. This provides more control over automatically generated names, which are slugified and truncated by default, ensuring unique and compliant identifiers.

```python
mcp = FastMCP.from_openapi(
    openapi_spec=spec,
    client=client,
    mcp_names={
        "list_users__with_pagination": "user_list",
        "create_user__admin_required": "create_user", 
        "get_user_details__admin_required": "user_detail",
    }
)
```

--------------------------------

### Initialize FastMCP Server with Descope Authentication in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/descope.mdx

This Python code sets up a FastMCP server with integrated Descope authentication using the `DescopeProvider`. It automatically discovers Descope endpoints and configures JWT token validation, requiring the Descope project ID, the server's public URL, and the Descope API base URL as inputs. This ensures all incoming client requests are authenticated by Descope.

```python
from fastmcp import FastMCP
from fastmcp.server.auth.providers.descope import DescopeProvider

# The DescopeProvider automatically discovers Descope endpoints
# and configures JWT token validation
auth_provider = DescopeProvider(
    project_id=DESCOPE_PROJECT_ID,        # Your Descope Project ID
    base_url=SERVER_URL,                  # Your server's public URL
    descope_base_url=DESCOPE_BASE_URL    # Descope API base URL
)

# Create FastMCP server with auth
mcp = FastMCP(name="My Descope Protected Server", auth=auth_provider)
```

--------------------------------

### Client Initialization with File Path (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/transports.mdx

Demonstrates a simplified way to initialize the FastMCP client using just the server's file path. The client attempts to infer the STDIO transport automatically. However, this method offers limited configuration options compared to explicit transport instantiation.

```python
from fastmcp import Client

client = Client("my_server.py")  # Limited - no configuration options
```

--------------------------------

### Create Server-Sent Events Application in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-http.mdx

This Python function generates an instance of an SSE server application, designed to work with a `FastMCP` server. It allows specification of message and SSE connection paths, along with optional authentication, debug settings, custom routes, and middleware. The result is a `StarletteWithLifespan` application tailored for Server-Sent Events.

```python
create_sse_app(server: FastMCP[LifespanResultT], message_path: str, sse_path: str, auth: AuthProvider | None = None, debug: bool = False, routes: list[BaseRoute] | None = None, middleware: list[Middleware] | None = None) -> StarletteWithLifespan
```

--------------------------------

### Create a Model Copy of a Component in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-utilities-components.mdx

This method creates a copy of the FastMCP component. It can be used to update specific fields, perform a deep copy of the component, or assign a new key to the copied instance.

```python
model_copy(self) -> Self
```

--------------------------------

### POST /close

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-client.mdx

Closes the FastMCP client connection, terminating communication with the server. This action does not return any specific data.

```APIDOC
## POST /close

### Description
Close the client connection.

### Method
POST

### Endpoint
/close

### Parameters

### Request Example
{}

### Response
#### Success Response (200)
- **message** (string) - A confirmation message that the client connection has been closed.

#### Response Example
```json
{
  "message": "Client closed successfully."
}
```
```

--------------------------------

### Run Async SSE Server in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

This function asynchronously initiates a server configured to use Server-Sent Events (SSE) transport. It allows customization of the host, port, log level, endpoint path, and additional Uvicorn server settings. The primary goal is to establish and manage an SSE connection for event-driven communication.

```python
run_sse_async(self, host: str | None = None, port: int | None = None, log_level: str | None = None, path: str | None = None, uvicorn_config: dict[str, Any] | None = None) -> None
```

--------------------------------

### Python FastMCP: Custom Tool Error Handling

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/tools.mdx

Shows how to use `ToolError` for explicit control over error information sent to clients, even when `mask_error_details` is enabled. Includes type checking and division by zero scenarios.

```python
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

# Assuming mcp is an instance of FastMCP
# mcp = FastMCP(name="SecureServer", mask_error_details=True)

@mcp.tool
def divide(a: float, b: float) -> float:
    """Divide a by b."""

    if b == 0:
        # Error messages from ToolError are always sent to clients,
        # regardless of mask_error_details setting
        raise ToolError("Division by zero is not allowed.")
    
    # If mask_error_details=True, this message would be masked
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers.")
        
    return a / b
```

--------------------------------

### Define `on_list_resource_templates` Python Middleware Hook

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-middleware-middleware.mdx

This Python function signature defines a middleware hook for intercepting requests to list resource templates. It takes a `MiddlewareContext` containing the `ListResourceTemplatesRequest` and a `call_next` function to proceed, returning a sequence of `ResourceTemplate` objects.

```python
on_list_resource_templates(self, context: MiddlewareContext[mt.ListResourceTemplatesRequest], call_next: CallNext[mt.ListResourceTemplatesRequest, Sequence[ResourceTemplate]]) -> Sequence[ResourceTemplate]
```

--------------------------------

### Anthropic Claude Client with MCP Server Authentication Token

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/anthropic.mdx

Demonstrates configuring an Anthropic Claude client to authenticate with an MCP server using an authorization token. The client passes the token in the mcp_servers configuration to access protected endpoints. Shows proper error handling and the authorization_token parameter usage for authenticated MCP connections.

```python
import anthropic
from rich import print

# Your server URL (replace with your actual URL)
url = 'https://your-server-url.com'

# Your access token (replace with your actual token)
access_token = 'your-access-token'

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    messages=[{"role": "user", "content": "Roll a few dice!"}],
    mcp_servers=[
        {
            "type": "url",
            "url": f"{url}/mcp/",
            "name": "dice-server",
            "authorization_token": access_token
        }
    ],
    extra_headers={
        "anthropic-beta": "mcp-client-2025-04-04"
    }
)

print(response.content)
```

--------------------------------

### Match URI Against Template and Extract Parameters

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-resources-template.mdx

Matches a given URI against a RFC 6570 URI template and extracts both path and query parameters. It returns a dictionary of extracted parameters if a match is found, otherwise returns None. Supports path parameters like {var} and {var*}, and query parameters like {?var1,var2}.

```python
from typing import Dict, Any, Optional

def match_uri_template(uri: str, uri_template: str) -> Optional[Dict[str, Any]]:
    # Implementation details omitted for brevity
    pass
```

--------------------------------

### Define a Static FastMCP Resource

Source: https://github.com/jlowin/fastmcp/blob/main/README.md

This Python snippet illustrates how to create a static 'resource' using the `@mcp.resource` decorator. Resources expose read-only data to LLMs, similar to GET endpoints. This example defines a resource that always returns a fixed version string.

```python
@mcp.resource("config://version")
def get_version(): 
    return "2.0.1"
```

--------------------------------

### Create CLI-based FastMCP Server with Tool Registration in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/running-server.mdx

Demonstrates creating a FastMCP server instance that can be automatically discovered and run by the CLI. The server is named 'MyServer' and includes a tool decorator for processing string data. No explicit main block is required as the CLI automatically finds variables named 'mcp', 'server', or 'app'.

```python
from fastmcp import FastMCP

mcp = FastMCP("MyServer")  # CLI looks for 'mcp', 'server', or 'app'

@mcp.tool
def process(data: str) -> str:
    return f"Processed: {data}"

# No if __name__ block needed - CLI will find and run 'mcp'
```

--------------------------------

### Manually Add FastMCP Server to Gemini CLI

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/gemini-cli.mdx

These commands provide a way to manually add a FastMCP server to Gemini CLI using `gemini mcp add`, offering more granular control over the server's launch configuration. The first example shows a basic setup, while the second demonstrates adding environment variables.

```bash
# Add a server with custom configuration
gemini mcp add dice-roller uv -- run --with fastmcp fastmcp run server.py
```

```bash
# Add with environment variables
gemini mcp add weather-server -e API_KEY=secret -e DEBUG=true uv -- run --with fastmcp fastmcp run server.py
```

--------------------------------

### Import FastMCP Subserver Without Prefix

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/composition.mdx

Demonstrates importing a weather subserver into a main FastMCP application without a prefix, preserving original component names. The subserver contains a tool for weather forecasts and a resource listing supported cities. This is a one-time copy operation, so subsequent changes to the subserver are not reflected in the main server.

```python
from fastmcp import FastMCP
import asyncio

# Define subservers
weather_mcp = FastMCP(name="WeatherService")

@weather_mcp.tool
def get_forecast(city: str) -> dict:
    """Get weather forecast."""
    return {"city": city, "forecast": "Sunny"}

@weather_mcp.resource("data://cities/supported")
def list_supported_cities() -> list[str]:
    """List cities with weather support."""
    return ["London", "Paris", "Tokyo"]

# Define main server
main_mcp = FastMCP(name="MainApp")

# Import subserver
async def setup():
    # Import without prefix - components keep original names
    await main_mcp.import_server(weather_mcp)

# Result: main_mcp now contains:
# - Tool: "get_forecast" (original name preserved)
# - Resource: "data://cities/supported" (original URI preserved)

if __name__ == "__main__":
    asyncio.run(setup())
    main_mcp.run()
```

--------------------------------

### Example FastMCP `uv` Environment Configuration

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/server-configuration.mdx

This comprehensive JSON example demonstrates a full FastMCP environment configuration utilizing `uv`. It specifies a minimum Python version, lists core dependencies like 'pandas' and 'numpy', and includes the current project in editable mode, ensuring an isolated and reproducible server runtime setup.

```json
"environment": {
  "type": "uv",
  "python": ">=3.10",
  "dependencies": ["pandas", "numpy"],
  "editable": ["."]
}
```

--------------------------------

### Utilize FastMCP's Default Server Log Handling

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/logging.mdx

This snippet demonstrates how FastMCP automatically handles server log messages if no custom `log_handler` is explicitly provided during client initialization. FastMCP's default behavior routes incoming server logs to appropriate Python logging levels, making it simple to get basic log visibility without custom configuration.

```python
client = Client("my_mcp_server.py")

async with client:
    # Server logs are forwarded at their proper severity (DEBUG/INFO/WARNING/ERROR/CRITICAL)
    await client.call_tool("some_tool")
```

--------------------------------

### Add Meta Information to FastMCP Tools for Categorization and Routing

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/tool-transformation.mdx

Demonstrates how to add custom meta information to FastMCP tools using the Tool.from_tool() method. Meta information includes properties like category, priority, and authentication requirements that don't affect functionality but help with tool organization and client-side routing. The meta parameter accepts a dictionary of custom key-value pairs.

```python
from fastmcp import FastMCP
from fastmcp.tools import Tool

mcp = FastMCP()

@mcp.tool
def analyze_data(data: str) -> dict:
    """Analyzes the provided data."""
    return {"result": f"Analysis of {data}"}

# Add custom meta information
enhanced_tool = Tool.from_tool(
    analyze_data,
    name="enhanced_analyzer",
    meta={
        "category": "analytics",
        "priority": "high",
        "requires_auth": True
    }
)

mcp.add_tool(enhanced_tool)
```

--------------------------------

### GET /server/app/http

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-server.mdx

Creates a Starlette application using the specified HTTP transport, supporting streamable HTTP and SSE.

```APIDOC
## GET /server/app/http

### Description
Create a Starlette app using the specified HTTP transport.

### Method
GET

### Endpoint
/server/app/http

### Parameters
- **path** (str) - Optional - The path for the HTTP endpoint
- **middleware** (list[ASGIMiddleware]) - Optional - A list of middleware to apply to the app
- **json_response** (bool) - Optional - Whether to use JSON response format
- **stateless_http** (bool) - Optional - Whether to use stateless HTTP
- **transport** (Literal['http', 'streamable-http', 'sse']) - Optional - Transport protocol to use - either "streamable-http" (default) or "sse"

### Response
#### Success Response (200)
- **app** (StarletteWithLifespan) - A Starlette application configured with the specified transport.
```

--------------------------------

### Disable PKCE Forwarding in FastMCP OAuth Proxy (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/auth/oauth-proxy.mdx

This Python snippet demonstrates how to disable PKCE (Proof Key for Code Exchange) forwarding for the FastMCP OAuth Proxy by setting `forward_pkce=False`. This configuration is typically used when integrating with legacy upstream OAuth providers that do not support PKCE. The default behavior is to forward PKCE parameters.

```python
auth = OAuthProxy(
    ...,
    forward_pkce=False  # Default is True
)
```

--------------------------------

### Implement Multi-Turn Analysis with FastMCP Structured Messages (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/sampling.mdx

This Python `fastmcp` tool demonstrates multi-turn conversation using `SamplingMessage` objects within `ctx.sample`. It sets up an initial user query, an assistant response, and a follow-up user query, guided by a system prompt to act as a data analyst.

```python
from fastmcp.client.sampling import SamplingMessage

@mcp.tool
async def multi_turn_analysis(user_query: str, context_data: str, ctx: Context) -> str:
    """Perform analysis using multi-turn conversation structure."""
    messages = [
        SamplingMessage(role="user", content=f"I have this data: {context_data}"),
        SamplingMessage(role="assistant", content="I can see your data. What would you like me to analyze?"),
        SamplingMessage(role="user", content=user_query)
    ]
    
    response = await ctx.sample(
        messages=messages,
        system_prompt="You are a data analyst. Provide detailed insights based on the conversation context.",
        temperature=0.3
    )
    
    return response.text
```

--------------------------------

### Get a Setting in FastMCP (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-settings.mdx

This method retrieves a setting from the FastMCP settings configuration. If the setting's attribute name contains `__`, it is treated as a nested setting. It takes the attribute name (`attr`) as a string and returns the setting's value.

```python
get_setting(self, attr: str) -> Any
```

--------------------------------

### Send ERROR Log Message to fastmcp Client in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-context.mdx

Sends a log message with an `ERROR` level to the connected MCP client. This helper function is used to report significant issues or failures, ensuring that critical errors are communicated to both the client and the server's internal logs via `fastmcp.server.context.to_client`.

```python
error(self, message: str, logger_name: str | None = None, extra: Mapping[str, Any] | None = None) -> None
```

--------------------------------

### Load and Merge FastMCP Server Configuration in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-utilities-cli.mdx

This Python function loads server configuration based on a provided specification and applies command-line interface overrides. It consolidates configuration parsing logic used across various FastMCP commands, ensuring consistent behavior. The function returns a tuple containing the `MCPServerConfig` object and the resolved server specification string.

```python
load_and_merge_config(server_spec: str | None, **cli_overrides) -> tuple[MCPServerConfig, str]
```

--------------------------------

### Define MCP Resource with Metadata using @resource Decorator in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/resources.mdx

Creates an MCP resource endpoint with comprehensive metadata including URI, name, description, MIME type, tags, and custom meta information. The decorator wraps a function that returns application status as a JSON dictionary. FastMCP automatically handles serialization and content type conversion based on the return value type.

```python
@mcp.resource(
    uri="data://app-status",      # Explicit URI (required)
    name="ApplicationStatus",     # Custom name
    description="Provides the current status of the application.", # Custom description
    mime_type="application/json", # Explicit MIME type
    tags={"monitoring", "status"}, # Categorization tags
    meta={"version": "2.1", "team": "infrastructure"}  # Custom metadata
)
def get_application_status() -> dict:
    """Internal function description (ignored if description is provided above)."""
    return {"status": "ok", "uptime": 12345, "version": mcp.settings.version} # Example usage
```

--------------------------------

### Example .env File for FastMCP GitHub Authentication Configuration (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/github.mdx

This Bash snippet provides an example of a `.env` file, illustrating how to define environment variables for configuring `FastMCP`'s GitHub authentication provider and its specific parameters. This method centralizes configuration, enhances security by avoiding hardcoded credentials, and allows for automatic provider selection.

```bash
# Use the GitHub provider
FASTMCP_SERVER_AUTH=fastmcp.server.auth.providers.github.GitHubProvider

# GitHub OAuth credentials
FASTMCP_SERVER_AUTH_GITHUB_CLIENT_ID=Ov23liAbcDefGhiJkLmN
FASTMCP_SERVER_AUTH_GITHUB_CLIENT_SECRET=github_pat_...
FASTMCP_SERVER_AUTH_GITHUB_BASE_URL=https://your-server.com
FASTMCP_SERVER_AUTH_GITHUB_REQUIRED_SCOPES=user,repo
```

--------------------------------

### Validate JWT Access Token with Upstream Provider in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-auth-oauth_proxy.mdx

Implements token swap pattern to validate FastMCP JWT tokens. Verifies JWT signature, retrieves mapped upstream token, decrypts it, validates with upstream provider (GitHub API, JWT validation), and returns validation result. FastMCP JWT acts as a reference token with authorization data from upstream.

```python
def load_access_token(self, token: str) -> AccessToken | None:
    """Validate FastMCP JWT by swapping for upstream token.
    
    This implements the token swap pattern:
    1. Verify FastMCP JWT signature (proves it's our token)
    2. Look up upstream token via JTI mapping
    3. Decrypt upstream token
    4. Validate upstream token with provider (GitHub API, JWT validation, etc.)
    5. Return upstream validation result
    
    The FastMCP JWT is a reference token - all authorization data comes
    from validating the upstream token via the TokenVerifier.
    """
```

--------------------------------

### Initialize FastMCP Client with Multi-Server Configuration in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-transports.mdx

This Python example demonstrates how to create a `fastmcp.Client` instance using an `MCPConfig` that defines multiple distinct MCP servers. It illustrates accessing server-specific tools (e.g., `weather_get_forecast`) and resources (e.g., `weather://weather/icons/sunny`) by prefixing them with the server's name, providing a consolidated client interface.

```python
from fastmcp import Client
from fastmcp.utilities.mcp_config import MCPConfig

# Create a config with multiple servers
config = {
    "mcpServers": {
        "weather": {
            "url": "https://weather-api.example.com/mcp",
            "transport": "http"
        },
        "calendar": {
            "url": "https://calendar-api.example.com/mcp",
            "transport": "http"
        }
    }
}

# Create a client with the config
client = Client(config)

async with client:
    # Access tools with prefixes
    weather = await client.call_tool("weather_get_forecast", {"city": "London"})
    events = await client.call_tool("calendar_list_events", {"date": "2023-06-01"})

    # Access resources with prefixed URIs
    icons = await client.read_resource("weather://weather/icons/sunny")
```

--------------------------------

### Set Up FastMCP for Production Deployment (JSON)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/server-configuration.mdx

This JSON configuration details a production-ready FastMCP setup, specifying the server source, a Python 3.11 environment with dependencies from `requirements/production.txt`, and HTTP deployment on host `0.0.0.0`. It includes a custom port, path, INFO logging, and production-specific environment variables for API base URL and database connection.

```json
{
  "$schema": "https://gofastmcp.com/public/schemas/fastmcp.json/v1.json",
  "source": {
    "path": "app/main.py",
    "entrypoint": "mcp_server"
  },
  "environment": {
    "python": "3.11",
    "requirements": "requirements/production.txt",
    "project": "."
  },
  "deployment": {
    "transport": "http",
    "host": "0.0.0.0",
    "port": 3000,
    "path": "/api/mcp/",
    "log_level": "INFO",
    "env": {
      "ENV": "production",
      "API_BASE_URL": "https://api.example.com",
      "DATABASE_URL": "postgresql://user:pass@db.example.com/prod"
    },
    "cwd": "/app",
    "args": ["--workers", "4"]
  }
}
```

--------------------------------

### Install Anthropic Python SDK (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/anthropic.mdx

This command installs the `anthropic` Python SDK, which is required to interact with the Anthropic Messages API. This SDK is not included with FastMCP.

```bash
pip install anthropic
```

--------------------------------

### Dynamically Removing a Tool from a FastMCP Server (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/tools.mdx

This example demonstrates how to remove a registered tool from a FastMCP server using the `remove_tool` method. After defining and registering a tool, calling `mcp.remove_tool("tool_name")` dynamically unregisters it, allowing for flexible management of server capabilities.

```python
from fastmcp import FastMCP

mcp = FastMCP(name="DynamicToolServer")

@mcp.tool
def calculate_sum(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

mcp.remove_tool("calculate_sum")
```

--------------------------------

### Configure FastMCP Server with OpenAI Sampling Fallback Handler (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/sampling.mdx

This example initializes a `FastMCP` server with an `OpenAISamplingHandler` configured in `"fallback"` mode. The server attempts to use the client's LLM for `ctx.sample` requests, falling back to the OpenAI handler only if the client does not support sampling.

```python
import asyncio
import os

from mcp.types import ContentBlock
from openai import OpenAI

from fastmcp import FastMCP
from fastmcp.experimental.sampling.handlers.openai import OpenAISamplingHandler
from fastmcp.server.context import Context


async def async_main():
    server = FastMCP(
        name="OpenAI Sampling Fallback Example",
        sampling_handler=OpenAISamplingHandler(
            default_model="gpt-4o-mini",
            client=OpenAI(
                api_key=os.getenv("API_KEY"),
                base_url=os.getenv("BASE_URL"),
            ),
        ),
        sampling_handler_behavior="fallback",  # Default - only use when client doesn't support sampling
    )

    @server.tool
    async def test_sample_fallback(ctx: Context) -> ContentBlock:
        # Will use client's LLM if available, otherwise falls back to the handler
        return await ctx.sample(
            messages=["hello world!"],
        )

    await server.run_http_async()


if __name__ == "__main__":
    asyncio.run(async_main())
```

--------------------------------

### Configure In-Memory Client Storage for Testing

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/auth/oauth-proxy.mdx

Sets up OAuthProxy to use `MemoryStore` for client storage. This is suitable for testing as it's fast but clients are lost upon restart. No external dependencies are needed beyond the core library.

```python
from fastmcp.server.auth.stores.memory import MemoryStore

auth = OAuthProxy(..., client_storage=MemoryStore())
```

--------------------------------

### ResourceToolMiddleware for FastMCP server

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-middleware-tool_injection.mdx

A middleware specifically for injecting resources as tools into the MCP server context. This enables direct interaction with server resources through the established tool invocation mechanism.

```python
class ResourceToolMiddleware:
    """A middleware for injecting resources as tools into the context."""
    pass
```

--------------------------------

### Add Icon to a Resource Template

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/icons.mdx

Explains how to add an icon to a resource template in FastMCP. This allows for visual identification of resource templates, configured via the `icons` parameter in the `@mcp.resource` decorator.

```python
@mcp.resource(
    "user://{user_id}/profile",
    icons=[Icon(src="https://example.com/user-icon.png")]
)
def get_user_profile(user_id: str) -> dict:
    """Get a user's profile."""
    return {"id": user_id, "name": f"User {user_id}"}
```

--------------------------------

### Run FastMCP Server with __main__ Block in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/tutorials/create-mcp-server.mdx

Demonstrates how to make a FastMCP server executable by adding a __main__ block that calls mcp.run(). This enables the server to start using the default STDIO transport for communication with clients like Claude Desktop. The example includes a complete server with tools and resources.

```python
from fastmcp import FastMCP

mcp = FastMCP(name="My First MCP Server")

@mcp.tool
def add(a: int, b: int) -> int:
    """Adds two integer numbers together."""
    return a + b

@mcp.resource("resource://config")
def get_config() -> dict:
    """Provides the application's configuration."""
    return {"version": "1.0", "author": "MyTeam"}

@mcp.resource("greetings://{name}")
def personalized_greeting(name: str) -> str:
    """Generates a personalized greeting for the given name."""
    return f"Hello, {name}! Welcome to the MCP server."

if __name__ == "__main__":
    mcp.run()
```

--------------------------------

### Run FastMCP Server from Configuration File (Bash)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/server-configuration.mdx

This bash command demonstrates how to execute a FastMCP server using its declarative configuration file. It shows how to explicitly specify the configuration file or rely on the default `fastmcp.json` in the current directory, simplifying server startup.

```bash
# Run the server using the configuration
fastmcp run fastmcp.json

# Or if fastmcp.json exists in the current directory
fastmcp run
```

--------------------------------

### Get MCP Session ID in fastmcp Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-context.mdx

Retrieves the MCP session ID, which remains consistent across all transports for a given client session. This ID is crucial for storing and sharing session-specific data, such as with Redis, across different tool calls or server interactions within the same client session.

```python
session_id(self) -> str
```

--------------------------------

### Build Regex for URI Template Matching

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-resources-template.mdx

Builds a regular expression pattern from a URI template string to match against actual URIs. It supports simple path variables ({var}), wildcard path variables ({var*}), and query parameters ({?var1,var2}), though query parameters are ignored in the path matching.

```python
import re

def build_regex(template: str) -> re.Pattern:
    # Implementation details omitted for brevity
    pass
```

--------------------------------

### Install FastMCP Server to Cursor Workspace Configuration in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-cli-install-cursor.mdx

Installs FastMCP server to workspace-specific Cursor configuration. Accepts file path, optional server object name, server name, and workspace path along with optional parameters for editable directories, packages, environment variables, Python version, and requirements. Returns boolean indicating installation success.

```python
def install_cursor_workspace(
    file: Path,
    server_object: str | None,
    name: str,
    workspace_path: Path
) -> bool:
    """
    Install FastMCP server to workspace-specific Cursor configuration.

    Args:
        file: Path to the server file
        server_object: Optional server object name (for :object suffix)
        name: Name for the server in Cursor
        workspace_path: Path to the workspace directory
        with_editable: Optional list of directories to install in editable mode
        with_packages: Optional list of additional packages to install
        env_vars: Optional dictionary of environment variables
        python_version: Optional Python version to use
        with_requirements: Optional requirements file to install from
        project: Optional project directory to run within

    Returns:
        True if installation was successful, False otherwise
    """
```

--------------------------------

### Create and Use `asyncer` Decorator for Background Async Tasks in FastMCP

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/tools.mdx

This example provides a recipe to create a decorator using the `asyncer` library, which converts a synchronous function into an awaitable background task. It then shows how to apply this decorator to a FastMCP tool, enabling potentially blocking synchronous operations to run asynchronously without impacting the event loop. The `asyncer` library is not included in FastMCP by default.

```python
import asyncer
import functools
from typing import Callable, ParamSpec, TypeVar, Awaitable

_P = ParamSpec("_P")
_R = TypeVar("_R")

def make_async_background(fn: Callable[_P, _R]) -> Callable[_P, Awaitable[_R]]:
    @functools.wraps(fn)
    async def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        return await asyncer.asyncify(fn)(*args, **kwargs)

    return wrapper
```

```python
from fastmcp import FastMCP

mcp = FastMCP()

@mcp.tool()
@make_async_background
def my_tool() -> None:
    time.sleep(5)
```

--------------------------------

### PUT /client/elicitation_callback

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-client.mdx

Sets the callback function for handling elicitation requests from the MCP server. This enables the client to respond to requests for additional information or user input.

```APIDOC
## PUT /client/elicitation_callback

### Description
Sets the callback function for handling elicitation requests from the MCP server. This enables the client to respond to requests for additional information or user input.

### Method
PUT

### Endpoint
/client/elicitation_callback

### Parameters
#### Path Parameters
- No path parameters.

#### Query Parameters
- No query parameters.

#### Request Body
- **elicitation_callback** (ElicitationHandler) - Required - The handler function to be invoked for elicitation requests.

### Request Example
{
  "elicitation_callback": "my_elicitation_function_reference"
}

### Response
#### Success Response (200)
- No response body. Indicates successful update.

#### Response Example
{}
```

--------------------------------

### Execute OpenAPI Tool with HTTP Request - Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-server-openapi.mdx

The run method executes an HTTP request based on the route configuration for an OpenAPI endpoint. It accepts a dictionary of arguments and returns a ToolResult containing the response data.

```python
run(self, arguments: dict[str, Any]) -> ToolResult
```

--------------------------------

### Add FastMCP Server with Custom Python Version or Project Directory using Gemini CLI

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/gemini-cli.mdx

These commands demonstrate how to register a FastMCP server with Gemini CLI while specifying advanced configurations. The first command sets a specific Python version (3.11) for the server's environment, and the second command defines a custom project directory where the server should operate.

```bash
gemini mcp add ml-server uv -- run --python 3.11 --with fastmcp fastmcp run server.py
```

```bash
gemini mcp add project-server uv -- run --project /path/to/project --with fastmcp fastmcp run server.py
```

--------------------------------

### Generate Multi-Turn Conversation Templates with Prompts in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/prompts.mdx

Shows how to use prompts to generate conversation templates with multiple messages. The prompt creates a multi-turn conversation flow based on input parameters, returning an array of messages with different roles that can be iterated through to display the conversation structure.

```python
async with client:
    result = await client.get_prompt("interview_template", {
        "candidate_name": "Alice",
        "position": "Senior Developer"
    })
    
    # Multiple messages for a conversation flow
    for message in result.messages:
        print(f"{message.role}: {message.content}")
```

--------------------------------

### Define Reusable Argument Patterns in fastmcp

Source: https://github.com/jlowin/fastmcp/blob/main/docs/patterns/tool-transformation.mdx

This example shows how to define reusable `ArgTransform` objects for common arguments like 'owner', 'repo', and 'limit'. This pattern promotes consistency and scalability when creating multiple tools from client methods, reducing code duplication and simplifying maintenance.

```python
from fastmcp import FastMCP
from fastmcp.tools import Tool
from fastmcp.tools.tool_transform import ArgTransform

mcp = FastMCP("GitHub Tools")

# Define reusable argument patterns
OWNER_ARG = ArgTransform(description="The repository owner.")
REPO_ARG = ArgTransform(description="The repository name.")
LIMIT_ARG = ArgTransform(description="Maximum number of items to return.")
HIDE_ERROR = ArgTransform(hide=True, default=True)

def create_github_tools(client):
    """Create tools from GitHub client methods with shared argument patterns."""

    owner_repo_args = {
        "owner": OWNER_ARG,
        "repo": REPO_ARG,
    }

    error_args = {
        "error_on_not_found": HIDE_ERROR,
    }

    return [
        Tool.from_tool(
            tool=Tool.from_function(fn=client.get_repository),
            description="Get basic information about a GitHub repository.",
            transform_args={**owner_repo_args, **error_args}
        ),
        Tool.from_tool(
            tool=Tool.from_function(fn=client.get_issue),
            description="Get a specific issue from a repository.",
            transform_args={
                **owner_repo_args,
                "issue_number": ArgTransform(description="The issue number."),
                "limit_comments": LIMIT_ARG,
                **error_args,
            }
        ),
        Tool.from_tool(
            tool=Tool.from_function(fn=client.get_pull_request),
            description="Get a specific pull request from a repository.",
            transform_args={
                **owner_repo_args,
                "pull_request_number": ArgTransform(description="The PR number."),
                "limit_comments": LIMIT_ARG,
                **error_args,
            }
        ),
    ]

# Add all tools to the server
for tool in create_github_tools(github_client):
    mcp.add_tool(tool)
```

--------------------------------

### Log FastMCP Server Banner in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-utilities-cli.mdx

This Python function generates and logs a formatted banner that includes server information and a logo. It takes the `FastMCP` server instance and the transport protocol as inputs. The function is designed to provide clear startup information for different server transport types (stdio, http, sse, streamable-http).

```python
log_server_banner(server: FastMCP[Any], transport: Literal['stdio', 'http', 'sse', 'streamable-http']) -> None
```

--------------------------------

### Set a Setting in FastMCP (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-settings.mdx

This method sets a specific setting within the FastMCP settings configuration. Similar to `get_setting`, if the attribute name contains `__`, it is interpreted as a nested setting. It accepts the attribute name (`attr`) and the `value` to be set.

```python
set_setting(self, attr: str, value: Any) -> None
```

--------------------------------

### Customizing OpenAPI Route Mapping

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openapi.mdx

Learn how to customize FastMCP's default behavior for mapping OpenAPI routes to MCP component types. This advanced configuration allows you to define specific rules for how API endpoints are exposed (e.g., as Tools, Resources, or excluded entirely).

```APIDOC
## Customizing OpenAPI Route Mapping

### Description
FastMCP uses an ordered list of `RouteMap` objects to determine how OpenAPI routes are converted into MCP components. By default, all routes become Tools. This section explains how to define custom mapping rules to control component types, exclude routes, or add custom MCP tags.

### Method/Function
`RouteMap` object instantiation and usage. Custom `RouteMap` lists can be passed to `FastMCP.from_openapi()` via a `route_maps` argument (not explicitly shown in the original text, but implied for custom behavior).

### Parameters
#### `RouteMap` Fields
- **methods** (list[str] or "*") - Optional - HTTP methods to match (e.g., `["GET", "POST"]`). Use `"*"` to match all methods. Defaults to `"*"` if not specified.
- **pattern** (str) - Optional - A regular expression string to match against the OpenAPI route path. Use `r".*"` to match all paths. Defaults to `r".*"` if not specified.
- **tags** (set[str]) - Optional - A set of OpenAPI tags. All specified tags must be present on the route for a match. An empty set `{}` means no tag filtering. Defaults to `{}`.
- **mcp_type** (MCPType) - Required - The desired MCP component type for matching routes. Valid values are `TOOL`, `RESOURCE`, `RESOURCE_TEMPLATE`, or `EXCLUDE`.
- **mcp_tags** (set[str]) - Optional - A set of custom tags to apply to the generated MCP components.

### Request Example
```python
from fastmcp.server.openapi import RouteMap, MCPType
# For experimental parser (FastMCP 2.11+):
# from fastmcp.experimental.server.openapi import RouteMap, MCPType

# Default mapping (all routes become tools) as defined by FastMCP:
DEFAULT_ROUTE_MAPPINGS = [
    RouteMap(mcp_type=MCPType.TOOL),
]

# Example of custom route mapping configuration:
# 1. Exclude all routes under /admin
# 2. Make all GET requests to /users/* into Resources with a 'user_data' tag
# 3. All other routes become Tools (this acts as a fallback default)
custom_route_maps = [
    RouteMap(pattern=r"^/admin/.*", mcp_type=MCPType.EXCLUDE),
    RouteMap(methods=["GET"], pattern=r"^/users/.*", mcp_type=MCPType.RESOURCE, mcp_tags={"user_data"}),
    RouteMap(mcp_type=MCPType.TOOL) # Catches any routes not matched by previous rules
]

# To use these custom_route_maps, you would pass them to FastMCP.from_openapi:
# mcp = FastMCP.from_openapi(openapi_spec=your_spec, client=your_client, route_maps=custom_route_maps)
```

### Response
No direct response. The `FastMCP` server will be built according to the provided `RouteMap` configurations, influencing how its components are exposed.
```

--------------------------------

### Declare FastMCP dependencies in fastmcp.json

Source: https://github.com/jlowin/fastmcp/blob/main/examples/fastmcp_config_demo/README.md

This JSON configuration snippet demonstrates the recommended way to declare server dependencies within the `fastmcp.json` file. Dependencies are specified under the `environment` section, ensuring they are installed in an isolated environment before the server starts.

```json
{
  "environment": {
    "dependencies": ["pyautogui", "Pillow"]
  }
}
```

--------------------------------

### Instantiate STDIO Transport with Command and Arguments (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/transports.mdx

Shows the basic usage of the STDIO transport by creating a `StdioTransport` instance. It specifies the command to run the server and its arguments, allowing the FastMCP client to establish communication through standard input/output pipes.

```python
from fastmcp.client.transports import StdioTransport

transport = StdioTransport(
    command="python",
    args=["my_server.py"]
)
client = Client(transport)
```

--------------------------------

### Define Advanced Custom Route Maps in FastMCP (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openapi.mdx

This example illustrates how to define complex custom routing rules using `RouteMap` objects in FastMCP. It configures GET endpoints under `/analytics/` as `TOOL`s, excludes all admin endpoints (`/admin/`), and excludes routes tagged "internal" from the server's routing logic, allowing for granular control over how different API paths are processed.

```python
from fastmcp import FastMCP
from fastmcp.server.openapi import RouteMap, MCPType

mcp = FastMCP.from_openapi(
    openapi_spec=spec,
    client=client,
    route_maps=[
        # Analytics `GET` endpoints are tools
        RouteMap(
            methods=["GET"], 
            pattern=r"^/analytics/.*", 
            mcp_type=MCPType.TOOL,
        ),

        # Exclude all admin endpoints
        RouteMap(
            pattern=r"^/admin/.*", 
            mcp_type=MCPType.EXCLUDE,
        ),

        # Exclude all routes tagged "internal"
        RouteMap(
            tags={"internal"},
            mcp_type=MCPType.EXCLUDE,
        ),
    ],
)
```

--------------------------------

### Run FastMCP API Server

Source: https://github.com/jlowin/fastmcp/blob/main/docs/tutorials/rest-api.mdx

This command executes the Python script to start the FastMCP server. It initiates the server, making the OpenAPI-defined REST API endpoints available as MCP tools for client connections.

```bash
python api_server.py
```

--------------------------------

### Generate FastMCP SDK Documentation

Source: https://github.com/jlowin/fastmcp/blob/main/docs/development/contributing.mdx

Triggers the proactive generation of SDK documentation from source code docstrings and type annotations. While typically updated automatically by GitHub Actions, this command allows manual regeneration for immediate review or specific development needs.

```bash
just api-ref-all
```

--------------------------------

### Run MCP Server with Flexible Configuration in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-cli-run.mdx

Main command function to start an MCP server or connect to a remote instance. Supports multiple server specification formats (Python files, object specs, config files, URLs), configurable transport protocols, network binding options, logging levels, and execution modes (direct import or subprocess). Returns None and executes the server until termination.

```python
def run_command(
    server_spec: str,
    transport: TransportType | None = None,
    host: str | None = None,
    port: int | None = None,
    path: str | None = None,
    log_level: LogLevelType | None = None,
    server_args: list[str] | None = None,
    show_banner: bool = True,
    use_direct_import: bool = False,
    skip_source: bool = False
) -> None:
    """Run a MCP server or connect to a remote one.
    
    Args:
        server_spec: Python file, object specification (file:obj), config file, or URL
        transport: Transport protocol to use
        host: Host to bind to when using http transport
        port: Port to bind to when using http transport
        path: Path to bind to when using http transport
        log_level: Log level
        server_args: Additional arguments to pass to the server
        show_banner: Whether to show the server banner
        use_direct_import: Whether to use direct import instead of subprocess
        skip_source: Whether to skip source preparation step
    """
    pass
```

--------------------------------

### Check MCP Endpoint Authentication Requirement (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-auth-oauth.mdx

This Python function sends a test request to an MCP endpoint to determine if authentication is necessary. It takes the MCP URL and optional `httpx` keyword arguments, returning `True` if authentication appears required or `False` otherwise.

```python
check_if_auth_required(mcp_url: str, httpx_kwargs: dict[str, Any] | None = None) -> bool
```

--------------------------------

### Instantiate FastMCPProxy with a Client Factory (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/servers/proxy.mdx

This Python code illustrates the direct instantiation of the FastMCPProxy class, which is used internally by FastMCP.as_proxy(). It shows how to provide a client_factory callable that returns a ProxyClient instance, allowing for explicit control over session creation.

```python
from fastmcp.server.proxy import FastMCPProxy, ProxyClient

# Provide a client factory for explicit session control
def create_client():
    return ProxyClient("backend_server.py")

proxy = FastMCPProxy(client_factory=create_client)
```

--------------------------------

### Configure FastMCP GitHub Provider with Persistent Encrypted Token Storage (Python)

Source: https://github.com/jlowin/fastmcp/blob/main/docs/integrations/github.mdx

This Python snippet demonstrates how to set up `FastMCP` with `GitHubProvider` for production. It includes `jwt_signing_key` for securing JSON Web Tokens and configures `client_storage` using `RedisStore` wrapped in `FernetEncryptionWrapper` to ensure OAuth tokens are encrypted at rest and persist across server restarts. Environment variables are used to securely inject keys and host details.

```python
import os
from fastmcp import FastMCP
from fastmcp.server.auth.providers.github import GitHubProvider
from key_value.aio.stores.redis import RedisStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper
from cryptography.fernet import Fernet

# Production setup with encrypted persistent token storage
auth_provider = GitHubProvider(
    client_id="Ov23liAbcDefGhiJkLmN",
    client_secret="github_pat_...",
    base_url="https://your-production-domain.com",

    # Production token management
    jwt_signing_key=os.environ["JWT_SIGNING_KEY"],
    client_storage=FernetEncryptionWrapper(
        key_value=RedisStore(
            host=os.environ["REDIS_HOST"],
            port=int(os.environ["REDIS_PORT"])
        ),
        fernet=Fernet(os.environ["STORAGE_ENCRYPTION_KEY"])
    )
)

mcp = FastMCP(name="Production GitHub App", auth=auth_provider)
```

--------------------------------

### Infer MCP Client Transport Type in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/python-sdk/fastmcp-client-transports.mdx

The `infer_transport` function automatically determines the correct `ClientTransport` subclass based on the provided argument. It supports various input types including `ClientTransport` instances, `FastMCP` or `FastMCP1Server` objects for in-memory transports, file paths (`.py` or `.js`) for stdio transports, URLs for HTTP/SSE, and `MCPConfig` dictionaries for multi-server setups. For HTTP URLs, `StreamableHttpTransport` is used by default unless the URL ends in `/sse`, in which case `SSETransport` is created. MCPConfig allows consolidating access to multiple servers via a single client interface, optionally prefixing server names.

```python
infer_transport(transport: ClientTransport | FastMCP | FastMCP1Server | AnyUrl | Path | MCPConfig | dict[str, Any] | str) -> ClientTransport
```

```python
# Connect to a local Python script
transport = infer_transport("my_script.py")
```

```python
# Connect to a remote server via HTTP
transport = infer_transport("http://example.com/mcp")
```

```python
# Connect to multiple servers using MCPConfig
config = {
    "mcpServers": {
        "weather": {"url": "http://weather.example.com/mcp"},
        "calendar": {"url": "http://calendar.example.com/mcp"}
    }
}
transport = infer_transport(config)
```

--------------------------------

### Configure STDIO Transport Session Persistence in Python

Source: https://github.com/jlowin/fastmcp/blob/main/docs/clients/transports.mdx

Demonstrates how to control session persistence in STDIO transports. By default, keep_alive=True maintains the subprocess across multiple client connections for improved performance. Setting keep_alive=False provides complete isolation between connections, useful for test suites or when server state could cause issues.

```python
from fastmcp.client.transports import StdioTransport

transport = StdioTransport(
    command="python",
    args=["server.py"]
)
client = Client(transport)

async def efficient_multiple_operations():
    async with client:
        await client.ping()
    
    async with client:  # Reuses the same subprocess
        await client.call_tool("process_data", {"file": "data.csv"})
```

--------------------------------

### Run FastMCP Skipping Environment Creation

Source: https://github.com/jlowin/fastmcp/blob/main/docs/deployment/server-configuration.mdx

Use the `--skip-env` flag to prevent FastMCP from creating a new isolated Python environment when a suitable one already exists. This is useful when running in a pre-configured virtual environment, Docker container, CI/CD pipeline, or an existing uv-managed environment.

```bash
fastmcp run fastmcp.json --skip-env
```
