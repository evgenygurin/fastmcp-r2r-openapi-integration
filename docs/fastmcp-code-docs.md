### Extending FastMCP with Contrib Modules

Source: https://gofastmcp.com/llms

Explore community-contributed modules that extend the functionality of FastMCP. These modules offer custom features and integrations developed by the FastMCP community.

```markdown
- [Contrib Modules](https://gofastmcp.com/patterns/contrib.md): Community-contributed modules extending FastMCP
```

--------------------------------

### FastMCP Client - Messages

Source: https://gofastmcp.com/llms

Handling and sending messages using the FastMCP client.

```APIDOC
## FastMCP Client - Messages

### Description
APIs for sending and receiving messages through the FastMCP client SDK.

### Method
POST

### Endpoint
/python-sdk/fastmcp-client-messages

### Parameters
#### Request Body
- **message_content** (string) - Required - The content of the message.
- **recipient** (string) - Optional - The recipient of the message.

### Request Example
{
  "message_content": "Hello from FastMCP client!",
  "recipient": "user123"
}

### Response
#### Success Response (200)
- **status** (string) - The status of the message operation (e.g., 'sent', 'delivered').

#### Response Example
{
  "status": "sent"
}
```

--------------------------------

### Import FastMCP in Python

Source: https://gofastmcp.com/changelog

Demonstrates how to import the FastMCP class from the mcp.server.fastmcp module in Python. This is the primary way to start using FastMCP in your application.

```python
from mcp.server.fastmcp import FastMCP
```

--------------------------------

### FastMCP Client Module Initialization

Source: https://gofastmcp.com/llms

Initializes the core FastMCP client module. This sets up the fundamental components required for interacting with FastMCP services as a client.

```python
from fastmcp.client import (
    auth,
    client,
    elicitation,
    logging,
    messages,
    oauth_callback,
    progress,
    roots,
    sampling,
    transports
)

__all__ = [
    "auth",
    "client",
    "elicitation",
    "logging",
    "messages",
    "oauth_callback",
    "progress",
    "roots",
    "sampling",
    "transports"
]
```

--------------------------------

### FastMCP Client Authentication - Bearer Token

Source: https://gofastmcp.com/llms

Authenticate FastMCP client requests using Bearer tokens.

```APIDOC
## FastMCP Client Authentication - Bearer Token

### Description
This endpoint facilitates authentication for FastMCP clients using Bearer tokens.

### Method
POST

### Endpoint
/python-sdk/fastmcp-client-auth-bearer

### Parameters
#### Request Body
- **token** (string) - Required - The Bearer token for authentication.

### Request Example
{
  "token": "your_bearer_token_here"
}

### Response
#### Success Response (200)
- **authenticated** (boolean) - True if authentication is successful, False otherwise.

#### Response Example
{
  "authenticated": true
}
```

--------------------------------

### Enable Strict Input Validation in FastMCP

Source: https://gofastmcp.com/servers/tools

Shows how to enable strict input validation for a FastMCP server. By setting `strict_input_validation=True` during FastMCP instantiation, the server will reject inputs that do not strictly match the type annotations, enhancing data integrity.

```python
# Enable strict validation for this server
mcp = FastMCP("StrictServer", strict_input_validation=True)

@mcp.tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

# With strict_input_validation=True, sending {"a": "10", "b": "20"} will fail

```

--------------------------------

### OpenAI API Connection for FastMCP

Source: https://gofastmcp.com/llms

Connect your FastMCP servers to the OpenAI API for advanced natural language processing capabilities. This enables features like AI-powered content generation and analysis within your FastMCP applications.

```markdown
- [OpenAI API 🤝 FastMCP](https://gofastmcp.com/integrations/openai.md): Connect FastMCP servers to the OpenAI API
```

--------------------------------

### Define FastMCP Tool with Type Annotations

Source: https://gofastmcp.com/servers/tools

Demonstrates how to define a FastMCP tool using standard Python type annotations for its arguments and return type. This allows FastMCP to correctly determine argument types, improving compatibility with LLM clients.

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

### FastMCP Client - Sampling

Source: https://gofastmcp.com/llms

APIs for performing sampling operations using the FastMCP client.

```APIDOC
## FastMCP Client - Sampling

### Description
Provides capabilities for data sampling using the FastMCP client SDK.

### Method
POST

### Endpoint
/python-sdk/fastmcp-client-sampling

### Parameters
#### Request Body
- **data_source** (string) - Required - The source of the data to sample from.
- **sample_size** (integer) - Required - The number of samples to collect.

### Request Example
{
  "data_source": "/path/to/data.csv",
  "sample_size": 100
}

### Response
#### Success Response (200)
- **samples** (array) - A list of collected samples.

#### Response Example
{
  "samples": [
    {"id": 1, "value": "A"},
    {"id": 2, "value": "B"}
  ]
}
```

--------------------------------

### FastMCP Client - Progress Tracking

Source: https://gofastmcp.com/llms

APIs for tracking progress of operations within the FastMCP client.

```APIDOC
## FastMCP Client - Progress Tracking

### Description
Provides endpoints for monitoring the progress of long-running operations managed by the FastMCP client SDK.

### Method
GET

### Endpoint
/python-sdk/fastmcp-client-progress/{operation_id}

### Parameters
#### Path Parameters
- **operation_id** (string) - Required - The unique identifier of the operation.

### Request Example
`/python-sdk/fastmcp-client-progress/op-12345`

### Response
#### Success Response (200)
- **progress_percentage** (number) - The percentage of completion for the operation.
- **status** (string) - The current status of the operation (e.g., 'running', 'completed', 'failed').

#### Response Example
{
  "progress_percentage": 75,
  "status": "running"
}
```

--------------------------------

### FastMCP Server Module Initialization

Source: https://gofastmcp.com/llms

Initializes the core FastMCP server module. This sets up the foundational components for running a FastMCP server.

```python
from fastmcp.server import (
    auth,
    middleware
)

__all__ = [
    "auth",
    "middleware"
]
```

--------------------------------

### FastMCP Client - Elicitation

Source: https://gofastmcp.com/llms

Functions related to elicitation for the FastMCP client.

```APIDOC
## FastMCP Client - Elicitation

### Description
Provides functionalities for elicitation processes within the FastMCP client SDK.

### Method
Various (e.g., GET, POST)

### Endpoint
/python-sdk/fastmcp-client-elicitation

### Parameters
Depends on the specific elicitation function.

### Request Example
Refer to SDK documentation for specific function calls.

### Response
Depends on the elicitation function's output.
```

--------------------------------

### FastMCP Client - Transports

Source: https://gofastmcp.com/llms

Configuration and management of transport layers for the FastMCP client.

```APIDOC
## FastMCP Client - Transports

### Description
Details on configuring and managing different transport protocols used by the FastMCP client SDK.

### Method
N/A (Configuration)

### Endpoint
/python-sdk/fastmcp-client-transports

### Parameters
Transport type (e.g., HTTP, WebSockets), connection details.

### Request Example
Refer to SDK documentation for transport configuration.

### Response
N/A
```

--------------------------------

### FastMCP Client - OAuth Callback

Source: https://gofastmcp.com/llms

Handles the callback from OAuth providers for the FastMCP client.

```APIDOC
## FastMCP Client - OAuth Callback

### Description
This endpoint is responsible for receiving and processing callbacks from OAuth providers during the authentication process.

### Method
GET

### Endpoint
/python-sdk/fastmcp-client-oauth_callback

### Parameters
Query parameters provided by the OAuth provider (e.g., `code`, `state`).

### Request Example
`/python-sdk/fastmcp-client-oauth_callback?code=authorization_code_xyz&state=some_state`

### Response
#### Success Response (200)
- **redirect_url** (string) - The URL to redirect the user to after successful authentication.

#### Response Example
{
  "redirect_url": "/dashboard"
}
```

--------------------------------

### FastMCP Prompts - Prompt Manager

Source: https://gofastmcp.com/llms

Utilities for managing prompts using the PromptManager in FastMCP.

```APIDOC
## FastMCP Prompts - Prompt Manager

### Description
This module provides the PromptManager class for organizing, loading, and utilizing prompts within FastMCP applications.

### Method
Various (e.g., CREATE, LOAD, RENDER)

### Endpoint
/python-sdk/fastmcp-prompts-prompt_manager.md

### Parameters
Depends on the PromptManager methods used.

### Request Example
```python
from fastmcp.prompts import PromptManager

pm = PromptManager()
pm.load_prompts('path/to/prompts')
rendered_prompt = pm.render_prompt('greeting', name='World')
```

### Response
Depends on the PromptManager method called.
```

--------------------------------

### Testing your FastMCP Server

Source: https://gofastmcp.com/llms

Learn the best practices and methods for testing your FastMCP server applications.

```APIDOC
## Testing your FastMCP Server

### Description
This documentation provides instructions and examples on how to effectively test your FastMCP server applications.

### Method
N/A (Guide)

### Endpoint
/patterns/testing

### Parameters
None

### Request Example
Refer to the guide for specific testing code examples.

### Response
N/A
```

--------------------------------

### FastMCP Client - Logging

Source: https://gofastmcp.com/llms

Configuration and usage of logging for the FastMCP client.

```APIDOC
## FastMCP Client - Logging

### Description
Details on how to configure and utilize the logging facilities for the FastMCP client SDK.

### Method
N/A (Configuration)

### Endpoint
/python-sdk/fastmcp-client-logging

### Parameters
Logging level, format, output destination.

### Request Example
```python
import fastmcp

fastmcp.configure_logging(level='INFO')
```

### Response
N/A
```

--------------------------------

### Google OAuth Integration for FastMCP

Source: https://gofastmcp.com/llms

Secure your FastMCP server using Google OAuth for authentication. This integration allows users to log in and authorize access to your FastMCP services through their Google accounts.

```markdown
- [Google OAuth 🤝 FastMCP](https://gofastmcp.com/integrations/google.md): Secure your FastMCP server with Google OAuth
```

--------------------------------

### Configure FastMCP to Mask Error Details in Python

Source: https://gofastmcp.com/servers/tools

Explains how to initialize FastMCP with `mask_error_details=True` to prevent sensitive internal error information from being exposed to clients. This enhances security by providing generic error messages for standard exceptions.

```python
mcp = FastMCP(name="SecureServer", mask_error_details=True)
```

--------------------------------

### OpenAI API Integration

Source: https://gofastmcp.com/llms

Connect your FastMCP servers to the OpenAI API for advanced AI capabilities.

```APIDOC
## OpenAI API Integration

### Description
Integrate your FastMCP servers with the OpenAI API to leverage powerful AI models.

### Method
POST

### Endpoint
/integrations/openai

### Parameters
#### Request Body
- **api_key** (string) - Required - Your OpenAI API key.
- **prompt** (string) - Required - The prompt to send to the OpenAI API.

### Request Example
{
  "api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "prompt": "What is the weather today?"
}

### Response
#### Success Response (200)
- **completion** (string) - The response from the OpenAI API.

#### Response Example
{
  "completion": "The weather today is sunny."
}
```

--------------------------------

### fastmcp-server-auth-providers: In-Memory Authentication

Source: https://gofastmcp.com/llms

Provides an in-memory authentication provider for the fastmcp server. This is suitable for development or simple use cases where authentication data is stored in memory. It offers a quick way to manage users and permissions without external databases.

```python
from fastmcp.server.auth_providers.in_memory import InMemoryAuthProvider

# Example usage:
auth_provider = InMemoryAuthProvider(users={'user1': 'pass1'})

```

--------------------------------

### FastMCP Server Authentication - Auth Middleware

Source: https://gofastmcp.com/llms

Middleware for handling authentication in FastMCP servers.

```APIDOC
## FastMCP Server Authentication - Auth Middleware

### Description
This middleware component assists in authenticating incoming requests to your FastMCP server.

### Method
N/A (Middleware)

### Endpoint
/python-sdk/fastmcp-server-auth-middleware.md

### Parameters
Authentication configuration, token validation settings.

### Request Example
Integrate into your FastMCP server setup.

### Response
Handles request authentication, allowing or denying access based on credentials.
```

--------------------------------

### FastMCP Client Authentication - OAuth

Source: https://gofastmcp.com/llms

Handles OAuth authentication flows for FastMCP clients.

```APIDOC
## FastMCP Client Authentication - OAuth

### Description
This section covers the implementation of OAuth authentication for FastMCP clients.

### Method
GET/POST

### Endpoint
/python-sdk/fastmcp-client-auth-oauth

### Parameters
Depends on the OAuth flow (e.g., authorization code, client credentials).

### Request Example
Refer to OAuth 2.0 standard flows.

### Response
#### Success Response (200)
- **access_token** (string) - The OAuth access token.
- **refresh_token** (string) - The OAuth refresh token.

#### Response Example
{
  "access_token": "oauth_access_token_xxxx",
  "refresh_token": "oauth_refresh_token_yyyy"
}
```

--------------------------------

### fastmcp-server: Proxy Utilities

Source: https://gofastmcp.com/llms

Provides utilities for implementing proxy functionality within the fastmcp server. A proxy server forwards requests to other servers. This module likely assists in setting up reverse proxies or forwarding requests.

```python
from fastmcp.server.proxy import Proxy

# Example usage:
proxy = Proxy(target_url="http://backend.service.com")
# You would integrate this proxy into your request handling logic.

```

--------------------------------

### Contrib Modules

Source: https://gofastmcp.com/llms

Explore community-contributed modules that extend the functionality of FastMCP.

```APIDOC
## Contrib Modules

### Description
Information about community-developed modules that can be integrated with FastMCP to add new features or capabilities.

### Method
N/A

### Endpoint
/patterns/contrib

### Parameters
None

### Request Example
None

### Response
N/A

#### Note
This section links to external documentation for community modules.
```

--------------------------------

### fastmcp-server: HTTP Utilities

Source: https://gofastmcp.com/llms

Provides utilities for handling HTTP requests and responses within the fastmcp server. This module likely includes functions for making HTTP calls, parsing responses, and managing HTTP-related operations. It simplifies network communication.

```python
from fastmcp.server.http import make_request

# Example usage:
response = make_request("GET", "https://api.example.com/data")
print(response.json())

```

--------------------------------

### FastMCP Client Progress Tracking

Source: https://gofastmcp.com/llms

Enables tracking of progress for long-running operations within the FastMCP client. This module allows users to monitor the status of tasks.

```python
from fastmcp.client.client import FastMCPClient

class ProgressClient(FastMCPClient):
    def get_progress(self, task_id: str):
        return self.request("GET", f"/progress/{task_id}")
```

--------------------------------

### FastMCP Exceptions

Source: https://gofastmcp.com/llms

Custom exception classes used within the FastMCP library.

```APIDOC
## FastMCP Exceptions

### Description
Documentation for the custom exception classes provided by the FastMCP library to handle specific error conditions.

### Method
N/A (Library Reference)

### Endpoint
/python-sdk/fastmcp-exceptions.md

### Parameters
N/A

### Request Example
Refer to Python exception handling examples.

### Response
N/A

#### Note
This section lists and describes available exception types.
```

--------------------------------

### FastMCP Client Messages Module

Source: https://gofastmcp.com/llms

Manages message handling and communication for the FastMCP client. This module could be used for sending or receiving messages between client and server.

```python
from fastmcp.client.client import FastMCPClient

class MessageClient(FastMCPClient):
    def send_message(self, recipient: str, content: str):
        return self.request("POST", "/messages", json={"to": recipient, "content": content})
```

--------------------------------

### FastMCP CLI Run Command

Source: https://gofastmcp.com/llms

The primary command for running FastMCP services or tasks via the CLI. This orchestrates the execution of various FastMCP operations.

```python
import click

@click.command()
def run():
    """Run a FastMCP service or task."""
    click.echo('Running FastMCP service...')
```

--------------------------------

### FastMCP Resources - Resource Manager

Source: https://gofastmcp.com/llms

Utilities for managing resources using the ResourceManager in FastMCP.

```APIDOC
## FastMCP Resources - Resource Manager

### Description
Provides the ResourceManager class for handling and managing various types of resources within the FastMCP framework.

### Method
Various (e.g., REGISTER, GET, DELETE)

### Endpoint
/python-sdk/fastmcp-resources-resource_manager.md

### Parameters
Depends on the ResourceManager methods used.

### Request Example
```python
from fastmcp.resources import ResourceManager

rm = ResourceManager()
rm.register_resource('my_resource', data={'key': 'value'})
resource_data = rm.get_resource('my_resource')
```

### Response
Depends on the ResourceManager method called.
```

--------------------------------

### Scalekit Integration

Source: https://gofastmcp.com/llms

Secure your FastMCP server using Scalekit for robust security measures.

```APIDOC
## Scalekit Integration

### Description
Integrate Scalekit with your FastMCP server to implement advanced security features.

### Method
GET

### Endpoint
/integrations/scalekit

### Parameters
None

### Request Example
None

### Response
#### Success Response (200)
- **message** (string) - A confirmation message for Scalekit integration.

#### Response Example
{
  "message": "Scalekit integration configured successfully."
}
```

--------------------------------

### FastMCP MCP Configuration

Source: https://gofastmcp.com/llms

Utilities for managing MCP configurations.

```APIDOC
## FastMCP MCP Configuration

### Description
Provides functions and utilities for working with MCP configuration files within the FastMCP ecosystem.

### Method
Various (e.g., READ, WRITE)

### Endpoint
/python-sdk/fastmcp-mcp_config.md

### Parameters
Depends on the specific configuration operation.

### Request Example
Refer to the documentation for configuration management functions.

### Response
Depends on the operation performed.
```

--------------------------------

### FastMCP Client Sampling Module

Source: https://gofastmcp.com/llms

Provides functionality for sampling data or events within the FastMCP client. This is useful for analytics or data collection purposes.

```python
from fastmcp.client.client import FastMCPClient

class SamplingClient(FastMCPClient):
    def sample_data(self, endpoint: str, sample_rate: float):
        return self.request("POST", f"/sampling/{endpoint}", json={"rate": sample_rate})
```

--------------------------------

### fastmcp-utilities: Logging Utilities

Source: https://gofastmcp.com/llms

Provides enhanced logging capabilities for fastmcp applications. This module likely offers pre-configured loggers, handlers, and formatters to streamline the logging process. It ensures consistent and informative logging across the application.

```python
from fastmcp.utilities.logging import get_logger

# Example usage:
logger = get_logger(__name__)
logger.info("Processing data...")

```

--------------------------------

### FastMCP Tool with Primitive Return Type Wrapping

Source: https://gofastmcp.com/servers/tools

Demonstrates a FastMCP tool 'calculate_sum' that returns a primitive integer. FastMCP automatically wraps the integer result under a 'result' key to ensure structured output, generating a schema that reflects this wrapping.

```python
@mcp.tool
def calculate_sum(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b
```

```json
{
  "type": "object",
  "properties": {
    "result": {"type": "integer"}
  },
  "x-fastmcp-wrap-result": true
}
```

```json
{
  "result": 8
}
```

--------------------------------

### FastMCP Client - Roots

Source: https://gofastmcp.com/llms

Utilities for managing root elements or configurations within the FastMCP client.

```APIDOC
## FastMCP Client - Roots

### Description
Functions related to managing root configurations or resources within the FastMCP client SDK.

### Method
Various (e.g., GET, POST)

### Endpoint
/python-sdk/fastmcp-client-roots

### Parameters
Depends on the specific root management operation.

### Request Example
Refer to SDK documentation for root management functions.

### Response
Depends on the operation performed.
```

--------------------------------

### fastmcp-utilities: HTTP Utilities

Source: https://gofastmcp.com/llms

Offers utility functions for performing HTTP operations. This module likely provides helpers for making requests, handling responses, and managing HTTP clients. It simplifies network communication for various utility tasks.

```python
from fastmcp.utilities.http import fetch_url

# Example usage:
content = fetch_url("https://example.com")
print(content[:100])

```

--------------------------------

### fastmcp-server: Context Management

Source: https://gofastmcp.com/llms

Manages context within the fastmcp server. Request context often holds information relevant to a specific request, such as user data, request IDs, or other state. This module provides utilities for handling such context.

```python
from fastmcp.server.context import RequestContext

# Example usage:
context = RequestContext()
context.set("user_id", 123)
print(context.get("user_id"))

```

--------------------------------

### Permit.io Authorization Integration for FastMCP

Source: https://gofastmcp.com/llms

Add fine-grained authorization to your FastMCP servers using Permit.io. This integration provides robust access control policies to manage user permissions effectively.

```markdown
- [Permit.io Authorization 🤝 FastMCP](https://gofastmcp.com/integrations/permit.md): Add fine-grained authorization to your FastMCP servers with Permit.io
```

--------------------------------

### FastMCP CLI Usage

Source: https://gofastmcp.com/llms

Learn how to effectively use the FastMCP command-line interface for managing your servers.

```APIDOC
## FastMCP CLI Usage

### Description
Documentation on how to utilize the FastMCP command-line interface for various server management tasks.

### Method
N/A (CLI Command)

### Endpoint
N/A

### Parameters
Refer to specific CLI commands for details.

### Request Example
```bash
fastmcp --help
```

### Response
N/A
```

--------------------------------

### FastMCP MCP Configuration Module

Source: https://gofastmcp.com/llms

Provides utilities for managing MCP configuration settings. This module likely handles loading, parsing, and validating MCP configuration files.

```python
import yaml

def load_mcp_config(filepath: str) -> dict:
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

def validate_mcp_config(config: dict):
    # Add validation logic here
    pass
```

--------------------------------

### Using Decorators with FastMCP Methods

Source: https://gofastmcp.com/llms

Understand how to properly use instance methods, class methods, and static methods with FastMCP decorators. This guide ensures correct implementation of method types within the FastMCP framework.

```markdown
- [Decorating Methods](https://gofastmcp.com/patterns/decorating-methods.md): Properly use instance methods, class methods, and static methods with FastMCP decorators.
```

--------------------------------

### FastMCP Server Authentication Handler

Source: https://gofastmcp.com/llms

Provides the core authentication logic for the FastMCP server. This module handles user verification and session management.

```python
from fastapi import Request, HTTPException

def authenticate_request(request: Request):
    # Implement authentication logic here (e.g., check headers, tokens)
    if "Authorization" not in request.headers:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    # Further validation...
    return True
```

--------------------------------

### fastmcp-server: Low-Level Utilities

Source: https://gofastmcp.com/llms

Offers low-level utility functions for the fastmcp server. These might include core functionalities or helpers that are not specific to a higher-level abstraction. They provide foundational capabilities for the server's operation.

```python
# Example of a potential low-level utility (implementation specific)
def perform_operation(data):
    # ... low-level processing ...
    return processed_data

```

--------------------------------

### FastMCP Command-Line Interface Usage

Source: https://gofastmcp.com/llms

Learn how to effectively use the FastMCP command-line interface (CLI). This documentation covers common commands and workflows for managing FastMCP services from the terminal.

```markdown
- [FastMCP CLI](https://gofastmcp.com/patterns/cli.md): Learn how to use the FastMCP command-line interface
```

--------------------------------

### fastmcp-server-middleware: Timing

Source: https://gofastmcp.com/llms

Adds timing middleware to the fastmcp server. This middleware measures the execution time of requests, providing insights into performance bottlenecks. It helps in optimizing the server's response times.

```python
from fastmcp.server.middleware.timing import TimingMiddleware

# Example usage:
# Assuming 'app' is your ASGI application
# app = TimingMiddleware(app)

```

--------------------------------

### Tool Transformation in FastMCP

Source: https://gofastmcp.com/llms

Create enhanced tool variants with modified schemas, argument mappings, and custom behavior.

```APIDOC
## Tool Transformation in FastMCP

### Description
Understand how to transform existing tools within FastMCP by altering their schemas, argument mappings, and defining custom behaviors.

### Method
N/A (Conceptual/Code Example)

### Endpoint
/patterns/tool-transformation

### Parameters
N/A

### Request Example
Refer to the documentation for code examples on tool transformation.

### Response
N/A
```

--------------------------------

### FastMCP Client Authentication Module Initialization

Source: https://gofastmcp.com/llms

Initializes the authentication submodule for the FastMCP client. This sets up various authentication methods and handlers.

```python
from fastmcp.client.auth import (
    bearer,
    oauth
)

__all__ = [
    "bearer",
    "oauth"
]
```

--------------------------------

### FastMCP Server Authentication - OIDC Proxy

Source: https://gofastmcp.com/llms

Proxy for handling OpenID Connect (OIDC) authentication flows on the FastMCP server side.

```APIDOC
## FastMCP Server Authentication - OIDC Proxy

### Description
Acts as a proxy for managing OpenID Connect (OIDC) authentication, enabling identity verification for FastMCP servers.

### Method
GET/POST

### Endpoint
/python-sdk/fastmcp-server-auth-oidc_proxy

### Parameters
Depends on the OIDC provider and flow.

### Request Example
Refer to OIDC provider documentation for integration.

### Response
Manages OIDC authentication flows, including token validation and user info retrieval.
```

--------------------------------

### FastMCP Prompts Module Initialization

Source: https://gofastmcp.com/llms

Initializes the prompts submodule for FastMCP. This sets up the necessary components for managing and generating prompts.

```python
from fastmcp.prompts import (
    prompt,
    prompt_manager
)

__all__ = [
    "prompt",
    "prompt_manager"
]
```

--------------------------------

### FastMCP Server Authentication - OAuth Proxy

Source: https://gofastmcp.com/llms

Proxy for handling OAuth authentication flows on the FastMCP server side.

```APIDOC
## FastMCP Server Authentication - OAuth Proxy

### Description
This component acts as a proxy to manage OAuth authentication processes for your FastMCP server.

### Method
GET/POST

### Endpoint
/python-sdk/fastmcp-server-auth-oauth_proxy

### Parameters
Depends on the OAuth provider and flow being proxied.

### Request Example
Refer to OAuth provider documentation for integration details.

### Response
Handles redirects and token exchanges required for OAuth authentication.
```

--------------------------------

### FastMCP Client Transports Module

Source: https://gofastmcp.com/llms

Manages different communication transports for the FastMCP client. This module could support various protocols like HTTP, WebSockets, etc.

```python
from fastmcp.client.client import FastMCPClient

class TransportClient(FastMCPClient):
    def send_via_transport(self, transport_type: str, data: dict):
        return self.request("POST", f"/transports/{transport_type}", json=data)
```

--------------------------------

### fastmcp-utilities: Component Utilities

Source: https://gofastmcp.com/llms

Provides utilities for managing and interacting with different components within the fastmcp ecosystem. This module helps in organizing and utilizing various parts of the application effectively. It promotes modularity and reusability.

```python
from fastmcp.utilities.components import register_component

# Example usage:
# register_component('database', MyDatabaseClass())

```

--------------------------------

### Scalekit Security for FastMCP Servers

Source: https://gofastmcp.com/llms

Secure your FastMCP server using Scalekit. This integration enhances the security posture of your server, protecting it against unauthorized access and potential threats.

```markdown
- [Scalekit 🤝 FastMCP](https://gofastmcp.com/integrations/scalekit.md): Secure your FastMCP server with Scalekit
```

--------------------------------

### FastMCP Client Authentication Bearer

Source: https://gofastmcp.com/llms

Handles Bearer token authentication for the FastMCP client. This allows clients to authenticate requests using Bearer tokens.

```python
from fastmcp.client.auth.auth import BaseAuth

class BearerAuth(BaseAuth):
    def __init__(self, token: str):
        self.token = token

    def get_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"}
```

--------------------------------

### Decorating Methods in FastMCP

Source: https://gofastmcp.com/llms

Properly use instance methods, class methods, and static methods with FastMCP decorators.

```APIDOC
## Decorating Methods in FastMCP

### Description
Guidance on applying FastMCP decorators to instance methods, class methods, and static methods for enhanced behavior.

### Method
N/A (Code Example)

### Endpoint
N/A

### Parameters
N/A

### Request Example
```python
from fastmcp import decorator

class MyClass:
    @decorator.instance_method
    def my_instance_method(self):
        pass

    @decorator.class_method
    def my_class_method(cls):
        pass

    @decorator.static_method
    def my_static_method():
        pass
```

### Response
N/A
```

--------------------------------

### FastMCP Server Auth Providers - Auth0

Source: https://gofastmcp.com/llms

Integration details for using Auth0 as an authentication provider for FastMCP servers.

```APIDOC
## FastMCP Server Auth Providers - Auth0

### Description
Instructions and configuration for integrating Auth0 as an identity provider with your FastMCP server.

### Method
N/A (Configuration)

### Endpoint
/python-sdk/fastmcp-server-auth-providers-auth0.md

### Parameters
Auth0 domain, client ID, client secret.

### Request Example
Refer to Auth0 documentation for setup.

### Response
Enables authentication via Auth0 for FastMCP server access.
```

--------------------------------

### FastMCP Client Core Functionality

Source: https://gofastmcp.com/llms

Provides the core client logic for interacting with FastMCP services. This class likely handles making requests and processing responses.

```python
import httpx
from fastmcp.client.auth.auth import BaseAuth

class FastMCPClient:
    def __init__(self, base_url: str, auth: BaseAuth = None):
        self.base_url = base_url
        self.auth = auth
        self.client = httpx.Client(
            base_url=self.base_url,
            headers=self.auth.get_headers() if self.auth else {}
        )

    def request(self, method: str, endpoint: str, **kwargs):
        response = self.client.request(method, endpoint, **kwargs)
        response.raise_for_status()
        return response.json()
```

--------------------------------

### FastMCP Server Authentication Middleware

Source: https://gofastmcp.com/llms

Provides middleware for automatically handling authentication on incoming requests. This integrates authentication logic into the request processing pipeline.

```python
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Example: Call authentication logic before proceeding
        if "/protected" in str(request.url):
            if not authenticate_request(request): # Assuming authenticate_request is defined
                return Response("Unauthorized", status_code=401)
        response = await call_next(request)
        return response
```

--------------------------------

### Create Advanced Tool with Full Output Control in Python

Source: https://gofastmcp.com/servers/tools

Demonstrates how to create a tool with complete control over its output using ToolResult. This includes traditional content, structured data, and execution metadata. Requires FastMCP and MCP types.

```python
from fastmcp.tools.tool import ToolResult
from mcp.types import TextContent

@mcp.tool
def advanced_tool() -> ToolResult:
    """Tool with full control over output."""
    return ToolResult(
        content=[TextContent(type="text", text="Human-readable summary")],
        structured_content={"data": "value", "count": 42},
        meta={"execution_time_ms": 145}
    )
```

--------------------------------

### FastMCP Resources Module Initialization

Source: https://gofastmcp.com/llms

Initializes the resources submodule for FastMCP. This sets up the components for managing and accessing various resources.

```python
from fastmcp.resources import (
    resource,
    resource_manager,
    template,
    types
)

__all__ = [
    "resource",
    "resource_manager",
    "template",
    "types"
]
```

--------------------------------

### MCP Annotations for Tool Metadata

Source: https://gofastmcp.com/servers/tools

Add specialized metadata to tools using annotations. These annotations provide client applications with user-friendly titles, hints about data modification, safety profiles, and external system interactions without consuming LLM token context.

```APIDOC
## MCP Annotations

FastMCP allows you to add specialized metadata to your tools through annotations. These annotations communicate how tools behave to client applications without consuming token context in LLM prompts.

Annotations serve several purposes in client applications:

* Adding user-friendly titles for display purposes
* Indicating whether tools modify data or systems
* Describing the safety profile of tools (destructive vs. non-destructive)
* Signaling if tools interact with external systems

You can add annotations to a tool using the `annotations` parameter in the `@mcp.tool` decorator:

### Example: Adding annotations to a tool

```python
@mcp.tool(
    annotations={
        "title": "Calculate Sum",
        "readOnlyHint": True,
        "openWorldHint": False
    }
)
def calculate_sum(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b
```

FastMCP supports these standard annotations:

| Annotation        | Type    | Default | Purpose                                                                     |
| :---------------- | :------ | :------ | :-------------------------------------------------------------------------- |
| `title`           | string  | -       | Display name for user interfaces                                            |
| `readOnlyHint`    | boolean | false   | Indicates if the tool only reads without making changes                     |
| `destructiveHint` | boolean | true    | For non-readonly tools, signals if changes are destructive                  |
| `idempotentHint`  | boolean | false   | Indicates if repeated identical calls have the same effect as a single call |
| `openWorldHint`   | boolean | true    | Specifies if the tool interacts with external systems                       |

Remember that annotations help make better user experiences but should be treated as advisory hints. They help client applications present appropriate UI elements and safety controls, but won't enforce security boundaries on their own. Always focus on making your annotations accurately represent what your tool actually does.
```

--------------------------------

### FastMCP Server Authentication Module Initialization

Source: https://gofastmcp.com/llms

Initializes the authentication submodule for the FastMCP server. This configures various authentication providers and mechanisms.

```python
from fastmcp.server.auth import (
    auth,
    jwt_issuer,
    middleware,
    oauth_proxy,
    oidc_proxy,
    providers
)

__all__ = [
    "auth",
    "jwt_issuer",
    "middleware",
    "oauth_proxy",
    "oidc_proxy",
    "providers"
]
```

--------------------------------

### FastMCP Client Elicitation Module

Source: https://gofastmcp.com/llms

Handles elicitation processes within the FastMCP client. This module likely manages interactions related to gathering information or user input.

```python
from fastmcp.client.client import FastMCPClient

class ElicitationClient(FastMCPClient):
    def get_prompt(self, session_id: str):
        return self.request("GET", f"/elicitation/{session_id}/prompt")
```

--------------------------------

### fastmcp-server-auth-providers: ScaleKit Authentication

Source: https://gofastmcp.com/llms

Integrates ScaleKit for authentication purposes within the fastmcp server. ScaleKit is likely a service for managing access and permissions. This module facilitates connecting fastmcp with ScaleKit's authentication features.

```python
from fastmcp.server.auth_providers.scalekit import ScaleKitAuthProvider

# Example usage:
auth_provider = ScaleKitAuthProvider(api_key="your_api_key")

```

--------------------------------

### FastMCP Server Authentication - JWT Issuer

Source: https://gofastmcp.com/llms

Functionality for issuing JSON Web Tokens (JWT) for FastMCP server authentication.

```APIDOC
## FastMCP Server Authentication - JWT Issuer

### Description
Provides tools for generating and signing JSON Web Tokens (JWT) to be used for authentication in FastMCP servers.

### Method
POST

### Endpoint
/python-sdk/fastmcp-server-auth-jwt_issuer

### Parameters
#### Request Body
- **user_id** (string) - Required - The identifier of the user.
- **claims** (object) - Optional - Additional claims to include in the JWT.

### Request Example
{
  "user_id": "user-123",
  "claims": {
    "role": "admin"
  }
}

### Response
#### Success Response (200)
- **token** (string) - The generated JWT.

#### Response Example
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

--------------------------------

### OpenAPI Specification to MCP Server Generation

Source: https://gofastmcp.com/llms

Generate FastMCP servers directly from any OpenAPI specification. This streamlines the development process by automating server creation based on existing API definitions.

```markdown
- [OpenAPI 🤝 FastMCP](https://gofastmcp.com/integrations/openapi.md): Generate MCP servers from any OpenAPI specification
```

--------------------------------

### fastmcp-server-middleware: Error Handling

Source: https://gofastmcp.com/llms

Provides error handling middleware for the fastmcp server. This middleware intercepts exceptions and errors, providing consistent error responses to clients. It enhances the robustness and user experience of the application.

```python
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware

# Example usage:
# Assuming 'app' is your ASGI application
# app = ErrorHandlingMiddleware(app)

```

--------------------------------

### Permit.io Authorization Integration

Source: https://gofastmcp.com/llms

Add fine-grained authorization to your FastMCP servers with Permit.io.

```APIDOC
## Permit.io Authorization Integration

### Description
Enhance your FastMCP servers with fine-grained authorization policies managed by Permit.io.

### Method
POST

### Endpoint
/integrations/permit

### Parameters
#### Request Body
- **permit_api_key** (string) - Required - Your Permit.io API key.
- **resource_type** (string) - Required - The type of resource to protect.
- **action** (string) - Required - The action to authorize.

### Request Example
{
  "permit_api_key": "permit_key_xxxxxxxxxxxxxx",
  "resource_type": "document",
  "action": "read"
}

### Response
#### Success Response (200)
- **authorization_status** (boolean) - Indicates if the action is authorized.

#### Response Example
{
  "authorization_status": true
}
```

--------------------------------

### FastMCP Exceptions Module

Source: https://gofastmcp.com/llms

Defines custom exception classes for the FastMCP library. These exceptions help in handling errors gracefully and provide specific error information.

```python
class FastMCPError(Exception):
    """Base exception for FastMCP errors."""
    pass

class AuthenticationError(FastMCPError):
    """Raised for authentication failures."""
    pass

class APIError(FastMCPError):
    """Raised for API-related errors."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")
```

--------------------------------

### FastMCP Server Auth Providers - AWS Cognito

Source: https://gofastmcp.com/llms

Integration details for using AWS Cognito as an authentication provider for FastMCP servers.

```APIDOC
## FastMCP Server Auth Providers - AWS Cognito

### Description
Guidance on configuring AWS Cognito as an authentication provider for securing your FastMCP server.

### Method
N/A (Configuration)

### Endpoint
/python-sdk/fastmcp-server-auth-providers-aws.md

### Parameters
AWS Cognito User Pool ID, App Client ID, Region.

### Request Example
Refer to AWS Cognito documentation for setup.

### Response
Allows authentication through AWS Cognito for FastMCP server resources.
```

--------------------------------

### Google OAuth Integration

Source: https://gofastmcp.com/llms

Secure your FastMCP server with Google OAuth for enhanced authentication and authorization.

```APIDOC
## Google OAuth Integration

### Description
This integration allows you to secure your FastMCP server using Google OAuth.

### Method
GET

### Endpoint
/integrations/google

### Parameters
None

### Request Example
None

### Response
#### Success Response (200)
- **message** (string) - A success message indicating the integration is set up.

#### Response Example
{
  "message": "Google OAuth integration successful"
}
```

--------------------------------

### Return Media Content Blocks with Helper Classes

Source: https://gofastmcp.com/servers/tools

Illustrates using helper classes (`Image`, `Audio`, `File`) provided by FastMCP to return media content. These classes are automatically converted into appropriate MCP content blocks when returned directly or within a list. For nested structures, manual conversion might be necessary.

```python
from fastmcp.utilities.types import Image, Audio, File

@mcp.tool
def get_chart() -> Image:
    """Generate a chart image."""
    return Image(path="chart.png")

@mcp.tool
def get_multiple_charts() -> list[Image]:
    """Return multiple charts."""
    return [Image(path="chart1.png"), Image(path="chart2.png")]

```

--------------------------------

### fastmcp-server-middleware: Rate Limiting

Source: https://gofastmcp.com/llms

Implements rate limiting middleware for the fastmcp server. Rate limiting controls the number of requests a client can make within a certain time period, protecting the server from abuse and overload. This middleware enforces usage policies.

```python
from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware

# Example usage:
# Assuming 'app' is your ASGI application
# app = RateLimitingMiddleware(app, max_requests=100, period=60)

```

--------------------------------

### FastMCP Tool with Dataclass Output Schema

Source: https://gofastmcp.com/servers/tools

Defines a FastMCP tool 'get_user_profile' that returns a 'Person' dataclass. FastMCP automatically generates a JSON schema from the 'Person' dataclass, which describes the expected output structure. The tool's execution results in structured content matching this schema.

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

### fastmcp-utilities: MCP Configuration Utilities

Source: https://gofastmcp.com/llms

Contains utilities for managing MCP-specific configurations. This module helps in loading, accessing, and validating configuration parameters required for MCP services. It ensures that the application is correctly configured.

```python
from fastmcp.utilities.mcp_config import load_mcp_config

# Example usage:
config = load_mcp_config("path/to/config.yaml")
print(config.get('api_key'))

```

--------------------------------

### FastMCP Tool with Manual Output Schema Control

Source: https://gofastmcp.com/servers/tools

Illustrates how to manually define an output schema for a FastMCP tool using the 'output_schema' argument. This allows for custom structuring of the tool's output, deviating from automatically generated schemas.

```python
@mcp.tool(output_schema={
    "type": "object", 
    "properties": {
        "data": {"type": "string"},
        "metadata": {"type": "object"}
    }
})
def custom_schema_tool() -> dict:
    """Tool with custom output schema."""
    return {"data": "Hello", "metadata": {"version": "1.0"}}
```

--------------------------------

### FastMCP Client Logging Module

Source: https://gofastmcp.com/llms

Provides functionality for logging client-side events and operations. This helps in debugging and monitoring client interactions with FastMCP services.

```python
import logging

logger = logging.getLogger(__name__)

def log_event(message: str):
    logger.info(message)
```

--------------------------------

### fastmcp-server-middleware: Caching

Source: https://gofastmcp.com/llms

Implements caching middleware for the fastmcp server. Caching helps improve performance by storing frequently accessed data and serving it quickly. This middleware can cache responses or specific data points.

```python
from fastmcp.server.middleware.caching import CachingMiddleware

# Example usage:
# Assuming 'app' is your ASGI application
# app = CachingMiddleware(app, cache_duration=300) 

```

--------------------------------

### FastMCP Resource Manager

Source: https://gofastmcp.com/llms

Manages a collection of resources and provides methods for accessing, adding, and deleting them. This class facilitates resource management within FastMCP.

```python
from fastmcp.resources.resource import Resource

class ResourceManager:
    def __init__(self):
        self.resources = {}

    def add_resource(self, resource: Resource):
        self.resources[resource.name] = resource

    def get_resource(self, name: str) -> Resource:
        if name in self.resources:
            return self.resources[name]
        raise ValueError(f"Resource '{name}' not found.")
```

--------------------------------

### FastMCP Resource Types

Source: https://gofastmcp.com/llms

Defines specific types or categories for resources. This module helps in organizing and classifying different kinds of resources used in FastMCP.

```python
from enum import Enum

class ResourceType(Enum):
    DATA = "data"
    MODEL = "model"
    CONFIG = "config"
```

--------------------------------

### FastMCP Client Authentication OAuth

Source: https://gofastmcp.com/llms

Manages OAuth 2.0 authentication flows for the FastMCP client. This enables clients to obtain access tokens via OAuth.

```python
from fastmcp.client.auth.auth import BaseAuth

class OAuthAuth(BaseAuth):
    def __init__(self, client_id: str, client_secret: str, token_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.token = None

    def get_token(self):
        # Logic to obtain token from token_url
        pass

    def get_headers(self) -> dict:
        if not self.token:
            self.get_token()
        return {"Authorization": f"Bearer {self.token}"}
```

--------------------------------

### fastmcp-server-auth-providers: Supabase Authentication

Source: https://gofastmcp.com/llms

Enables authentication using Supabase for the fastmcp server. Supabase provides backend-as-a-service features, including authentication. This provider integrates fastmcp with Supabase's authentication system.

```python
from fastmcp.server.auth_providers.supabase import SupabaseAuthProvider

# Example usage:
auth_provider = SupabaseAuthProvider(url="https://your_project.supabase.co", key="your_anon_key")

```

--------------------------------

### FastMCP Resource Object

Source: https://gofastmcp.com/llms

Represents a generic resource within the FastMCP framework. This class serves as a base for different types of resources.

```python
class Resource:
    def __init__(self, name: str, data: dict):
        self.name = name
        self.data = data

    def get_data(self) -> dict:
        return self.data
```

--------------------------------

### FastMCP Server Auth Providers - Azure AD

Source: https://gofastmcp.com/llms

Integration details for using Azure Active Directory as an authentication provider for FastMCP servers.

```APIDOC
## FastMCP Server Auth Providers - Azure AD

### Description
Instructions for integrating Azure Active Directory (Azure AD) as an authentication provider for your FastMCP server.

### Method
N/A (Configuration)

### Endpoint
/python-sdk/fastmcp-server-auth-providers-azure.md

### Parameters
Azure AD Tenant ID, Client ID, Client Secret.

### Request Example
Refer to Azure AD documentation for configuration.

### Response
Enables authentication using Azure AD for accessing FastMCP server services.
```

--------------------------------

### Wrap Sync CPU-Intensive Tasks with AnyIO

Source: https://gofastmcp.com/servers/tools

Demonstrates how to wrap a synchronous, CPU-intensive function into an asynchronous tool using `anyio.to_thread.run_sync`. This prevents blocking the event loop in FastMCP. It takes string data as input and returns processed string data.

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

### OpenAPI to MCP Server Generation

Source: https://gofastmcp.com/llms

Generate MCP servers from any OpenAPI specification.

```APIDOC
## OpenAPI to MCP Server Generation

### Description
This feature allows you to automatically generate MCP servers based on an existing OpenAPI specification.

### Method
POST

### Endpoint
/integrations/openapi

### Parameters
#### Request Body
- **openapi_spec** (object) - Required - The OpenAPI specification in JSON or YAML format.

### Request Example
```yaml
openapi: 3.0.0
info:
  title: Sample API
  version: 1.0.0
paths:
  /items:
    get:
      summary: Get a list of items
      responses:
        '200':
          description: A list of items
```

### Response
#### Success Response (200)
- **server_definition** (object) - The generated MCP server definition.

#### Response Example
{
  "server_definition": {
    "routes": [
      {
        "path": "/items",
        "method": "GET"
      }
    ]
  }
}
```

--------------------------------

### Configure Duplicate Tool Registration Behavior in Python

Source: https://gofastmcp.com/servers/tools

Shows how to configure the behavior of the FastMCP server when duplicate tool names are registered using the `on_duplicate_tools` argument during `FastMCP` instantiation in Python. Options include 'error', 'warn', 'replace', and 'ignore'.

```python
from fastmcp import FastMCP

mcp = FastMCP(
    name="StrictServer",
    # Configure behavior for duplicate tool names
    on_duplicate_tools="error"
)

@mcp.tool
def my_tool(): return "Version 1"

# This will now raise a ValueError because 'my_tool' already exists
# and on_duplicate_tools is set to "error".
# @mcp.tool
# def my_tool(): return "Version 2"
```

--------------------------------

### fastmcp-utilities: Authentication Helpers

Source: https://gofastmcp.com/llms

Provides utility functions related to authentication and authorization. This module likely contains helpers for managing user sessions, permissions, or interacting with authentication providers. It supports security-related operations.

```python
from fastmcp.utilities.auth import verify_password

# Example usage:
if verify_password(plain_password, hashed_password):
    print("Password matches!")

```

--------------------------------

### FastMCP Client Roots Module

Source: https://gofastmcp.com/llms

Handles root-level operations or configurations for the FastMCP client. This might involve managing server connections or global settings.

```python
from fastmcp.client.client import FastMCPClient

class RootsClient(FastMCPClient):
    def get_server_info(self):
        return self.request("GET", "/")
```

--------------------------------

### FastMCP CLI Module Initialization

Source: https://gofastmcp.com/llms

Provides the initialization logic for the FastMCP CLI module. This typically sets up the command-line interface environment.

```python
from fastmcp.cli import cli

__all__ = [
    "cli"
]
```

--------------------------------

### fastmcp-server-auth-providers: Bearer Authentication

Source: https://gofastmcp.com/llms

Implements bearer token authentication for the fastmcp server. It likely validates incoming requests using a bearer token, ensuring secure access to resources. This module is essential for securing APIs and services.

```python
from fastmcp.server.auth_providers.bearer import BearerAuthProvider

# Example usage:
auth_provider = BearerAuthProvider(token_secret="your_secret_key")

```

--------------------------------

### fastmcp-tools: Initialization

Source: https://gofastmcp.com/llms

Handles the initialization of the tools module in fastmcp. This likely sets up the environment or registry for various tools that can be used within the fastmcp ecosystem. It ensures tools are ready for use.

```python
# __init__.py for fastmcp.tools
# May contain imports or setup for the tools package.

```

--------------------------------

### Handle Optional Arguments in FastMCP Tools

Source: https://gofastmcp.com/servers/tools

Illustrates how to define optional arguments in FastMCP tools using Python's default value conventions. Arguments with default values are considered optional and will use their defaults if not provided by the LLM.

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

### Dynamically Remove Tools from FastMCP Server in Python

Source: https://gofastmcp.com/servers/tools

Illustrates how to remove a tool from a running FastMCP server dynamically using the `remove_tool` method in Python. This allows for modifying the available tools after the server has been initialized.

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

### FastMCP Prompt Object

Source: https://gofastmcp.com/llms

Defines the structure and behavior of a prompt within FastMCP. This class represents a single prompt used for interacting with AI models.

```python
class Prompt:
    def __init__(self, template: str, input_variables: list = None):
        self.template = template
        self.input_variables = input_variables or []

    def format(self, **kwargs) -> str:
        # Format the prompt template with provided variables
        return self.template.format(**kwargs)
```

--------------------------------

### Add Annotations to Tools

Source: https://gofastmcp.com/servers/tools

Illustrates how to add metadata annotations to FastMCP tools using the 'annotations' parameter in the @mcp.tool decorator. These annotations provide hints for client applications regarding the tool's title, read-only status, and interaction with external systems.

```python
@mcp.tool(
    annotations={
        "title": "Calculate Sum",
        "readOnlyHint": True,
        "openWorldHint": False
    }
)
def calculate_sum(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b
```

--------------------------------

### FastMCP Server OAuth Proxy

Source: https://gofastmcp.com/llms

Acts as a proxy for handling OAuth authentication flows on the server side. This module facilitates integration with external OAuth providers.

```python
from fastapi import Request, Depends, HTTPException
from authlib.integrations.starlette_client import OAuth

# Assume OAuth setup is done elsewhere
oauth = OAuth()

async def get_oauth_client():
    # Configure and return OAuth client instance
    pass

async def oauth_login(request: Request, oauth_client = Depends(get_oauth_client)):
    redirect_uri = request.url_for('oauth_callback') # Needs a callback endpoint
    return await oauth_client.google.authorize_redirect(request, redirect_uri)
```

--------------------------------

### fastmcp-tools: Tool Transformation

Source: https://gofastmcp.com/llms

Provides utilities for transforming or adapting tools within the fastmcp framework. This could involve modifying tool inputs/outputs or creating wrappers for compatibility. It enhances the flexibility of using different tools together.

```python
from fastmcp.tools.tool_transform import adapt_tool_signature

# Example usage:
def process_tool_output(output):
    # ... transform output ...
    return transformed_output

```

--------------------------------

### fastmcp-server: OpenAPI Specification

Source: https://gofastmcp.com/llms

Generates or utilizes OpenAPI specifications for the fastmcp server. OpenAPI (formerly Swagger) is a standard for describing RESTful APIs. This module helps in documenting and exposing the API structure.

```python
from fastmcp.server.openapi import generate_openapi_spec

# Example usage:
spec = generate_openapi_spec(app)
print(spec)

```

--------------------------------

### WorkOS Authentication for FastMCP Servers

Source: https://gofastmcp.com/llms

Authenticate FastMCP servers with WorkOS Connect. This integration simplifies user authentication by leveraging WorkOS's identity management solutions.

```markdown
- [WorkOS 🤝 FastMCP](https://gofastmcp.com/integrations/workos.md): Authenticate FastMCP servers with WorkOS Connect
```

--------------------------------

### FastMCP CLI Core Functionality

Source: https://gofastmcp.com/llms

Contains the core command-line interface commands and logic for FastMCP. This module handles user interactions and command execution via the terminal.

```python
import click

@click.group()
def cli():
    """FastMCP CLI tools."""
    pass

# Add commands here...
```

--------------------------------

### FastMCP Client OAuth Callback Handler

Source: https://gofastmcp.com/llms

Handles the callback process after an OAuth authentication flow. This endpoint receives authorization codes or tokens from the OAuth provider.

```python
from fastmcp.client.client import FastMCPClient

class OAuthCallbackClient(FastMCPClient):
    def handle_callback(self, code: str):
        # Exchange code for token
        return self.request("POST", "/oauth/callback", json={"code": code})
```

--------------------------------

### FastMCP CLI Install Module Initialization

Source: https://gofastmcp.com/llms

Initialization for the install submodule within the FastMCP CLI. This likely handles package installation or setup routines.

```python
from fastmcp.cli.install import (
    claude_code,
    claude_desktop,
    cursor,
    gemini_cli,
    mcp_json,
    shared
)

__all__ = [
    "claude_code",
    "claude_desktop",
    "cursor",
    "gemini_cli",
    "mcp_json",
    "shared"
]
```

--------------------------------

### fastmcp-settings: Configuration Management

Source: https://gofastmcp.com/llms

Manages application settings and configuration for fastmcp. This module allows for flexible configuration loading from various sources like environment variables or files. It ensures that the application can be easily configured for different environments.

```python
from fastmcp.settings import Settings

# Example usage:
settings = Settings()
print(settings.database_url)

```

--------------------------------

### fastmcp-server: Redirect Validation

Source: https://gofastmcp.com/llms

Handles validation of redirect URIs for the fastmcp server. This is crucial for security to ensure that users are redirected to trusted locations after authentication or other actions. It prevents open redirect vulnerabilities.

```python
from fastmcp.server.redirect_validation import validate_redirect_uri

# Example usage:
valid = validate_redirect_uri("https://trusted.domain.com/callback", trusted_domains=["trusted.domain.com"])

```

--------------------------------

### Server Configuration and Deployment

Source: https://gofastmcp.com/llms

This section focuses on server configuration, OpenAPI integration, proxying, and the main server setup.

```APIDOC
## Server Configuration and Deployment

This section covers aspects related to server configuration and deployment.

### OpenAPI Integration
Documentation for integrating OpenAPI specifications.

### Proxy
Information on proxy configurations and usage.

### Server Configuration
Details on general server settings and configuration options.

### Server Setup
Guides for setting up and running the GoFastMCP server.
```

--------------------------------

### Testing FastMCP Servers

Source: https://gofastmcp.com/llms

Learn the recommended practices and strategies for testing your FastMCP server. This documentation provides guidance on setting up test environments and writing effective tests.

```markdown
- [Testing your FastMCP Server](https://gofastmcp.com/patterns/testing.md): How to test your FastMCP server.
```

--------------------------------

### Using Decorator for Blocking Sync Tool in FastMCP

Source: https://gofastmcp.com/servers/tools

Illustrates how to use the `make_async_background` decorator (from the previous snippet) with a FastMCP tool. This example shows a synchronous tool `my_tool` that performs a blocking operation (`time.sleep(5)`), which is made non-blocking by the decorator. The tool is registered with FastMCP.

```python
from fastmcp import FastMCP

mcp = FastMCP()

@mcp.tool()
@make_async_background
def my_tool() -> None:
    time.sleep(5)
```

--------------------------------

### Python Tool Returning Dictionary to Structured Content

Source: https://gofastmcp.com/servers/tools

Demonstrates how a Python tool returning a dictionary automatically generates structured JSON content. FastMCP serializes the dictionary directly into the 'structuredContent' field of the MCP result, making it easily deserializable by clients.

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

### FastMCP Tool Transformation Patterns

Source: https://gofastmcp.com/llms

Discover how to create enhanced tool variants with modified schemas, argument mappings, and custom behavior. This pattern allows for flexible and powerful tool customization within FastMCP.

```markdown
- [Tool Transformation](https://gofastmcp.com/patterns/tool-transformation.md): Create enhanced tool variants with modified schemas, argument mappings, and custom behavior.
```

--------------------------------

### Server Core Functionality

Source: https://gofastmcp.com/llms

This section covers core server functionalities including redirection validation, context management, dependency injection, elicitation, HTTP handling, low-level server operations, and middleware.

```APIDOC
## Server Core Functionality

This section details fundamental aspects of the GoFastMCP server.

### Redirect Validation
Documentation for validating redirects within the server.

### Context Management
Information on managing server context.

### Dependency Injection
Details on how dependency injection is handled.

### Elicitation
Covers the elicitation process within the server.

### HTTP Handling
Documentation for the HTTP request and response handling.

### Low-Level Server Operations
Information on low-level server operations and configurations.

### Middleware
Details various middleware components and their usage.

#### Caching Middleware
Documentation for the caching middleware.

#### Error Handling Middleware
Explains the error handling middleware.

#### Logging Middleware
Information on the logging middleware.

#### Rate Limiting Middleware
Guides for the rate limiting middleware.

#### Timing Middleware
Details on the timing middleware.

#### Tool Injection Middleware
Covers the tool injection middleware.
```

--------------------------------

### fastmcp-tools: Tool Definition

Source: https://gofastmcp.com/llms

Defines the base structure and interface for tools within the fastmcp framework. A 'tool' can represent a specific function, utility, or microservice that can be invoked. This module provides the blueprint for creating custom tools.

```python
from fastmcp.tools.tool import Tool

# Example usage:
class MyCustomTool(Tool):
    def execute(self, **kwargs):
        # ... tool logic ...
        return "result"

```

--------------------------------

### WorkOS Integration

Source: https://gofastmcp.com/llms

Authenticate your FastMCP servers with WorkOS Connect for seamless identity management.

```APIDOC
## WorkOS Integration

### Description
Use WorkOS Connect to authenticate your FastMCP servers, simplifying user authentication.

### Method
GET

### Endpoint
/integrations/workos

### Parameters
None

### Request Example
None

### Response
#### Success Response (200)
- **message** (string) - Confirmation of WorkOS Connect setup.

#### Response Example
{
  "message": "WorkOS Connect authentication enabled."
}
```

--------------------------------

### fastmcp-server-auth-providers: WorkOS Authentication

Source: https://gofastmcp.com/llms

Integrates WorkOS for authentication in the fastmcp server. WorkOS simplifies enterprise identity, including SSO and directory synchronization. This provider allows fastmcp to leverage WorkOS for user authentication.

```python
from fastmcp.server.auth_providers.workos import WorkOSAuthProvider

# Example usage:
auth_provider = WorkOSAuthProvider(api_key="your_api_key", client_id="your_client_id")

```

--------------------------------

### fastmcp-utilities: Exception Handling

Source: https://gofastmcp.com/llms

Defines custom exceptions and utilities for exception handling in fastmcp. This module helps in creating a consistent error reporting mechanism throughout the application. It improves the clarity and management of errors.

```python
from fastmcp.utilities.exceptions import MCPError

# Example usage:
# raise MCPError("An error occurred in the MCP system.")

```

--------------------------------

### FastMCP CLI Install Shared Module

Source: https://gofastmcp.com/llms

Provides shared functionalities or utilities for the install module in the FastMCP CLI. This might include common functions used across different installation commands.

```python
import click

def shared_utility():
    """A shared utility function."""
    return 'shared_data'
```

--------------------------------

### Define a Python Tool with @mcp.tool Decorator

Source: https://gofastmcp.com/servers/tools

Exposes a Python function 'add' as a tool for an LLM client using the FastMCP library. The `@mcp.tool` decorator automatically handles schema generation and parameter validation based on the function's signature and docstring.

```python
from fastmcp import FastMCP

mcp = FastMCP(name="CalculatorServer")

@mcp.tool
def add(a: int, b: int) -> int:
    """Adds two integer numbers together."""
    return a + b
```

--------------------------------

### FastMCP Prompt Manager

Source: https://gofastmcp.com/llms

Manages a collection of prompts and provides functionality for retrieving and formatting them. This class acts as a central hub for prompt management.

```python
from fastmcp.prompts.prompt import Prompt

class PromptManager:
    def __init__(self):
        self.prompts = {}

    def add_prompt(self, name: str, prompt: Prompt):
        self.prompts[name] = prompt

    def get_prompt(self, name: str, **kwargs) -> str:
        if name in self.prompts:
            return self.prompts[name].format(**kwargs)
        raise ValueError(f"Prompt '{name}' not found.")
```

--------------------------------

### FastMCP Resource Template

Source: https://gofastmcp.com/llms

Defines a template for creating resources. This class allows for structured creation of resources with predefined schemas.

```python
class ResourceTemplate:
    def __init__(self, schema: dict):
        self.schema = schema

    def create_resource(self, name: str, **kwargs) -> Resource:
        # Validate kwargs against schema and create Resource
        return Resource(name, kwargs)
```

--------------------------------

### fastmcp-server-middleware: Logging

Source: https://gofastmcp.com/llms

Implements logging middleware for the fastmcp server. This middleware captures request and response details, errors, and other events, writing them to logs. Effective logging is crucial for monitoring, debugging, and auditing.

```python
from fastmcp.server.middleware.logging import LoggingMiddleware

# Example usage:
# Assuming 'app' is your ASGI application
# app = LoggingMiddleware(app)

```

--------------------------------

### FastMCP CLI Install MCP JSON Command

Source: https://gofastmcp.com/llms

Command for installing or managing MCP JSON configuration tools within the FastMCP CLI. This assists in setting up JSON configuration generation.

```python
import click

@click.command()
def mcp_json():
    """Install or manage MCP JSON configuration tools."""
    click.echo('MCP JSON tools installed.')
```

--------------------------------

### FastMCP CLI Install Claude Desktop Command

Source: https://gofastmcp.com/llms

Command for installing or managing Claude desktop related functionalities within the FastMCP CLI. This could be for desktop applications leveraging Claude AI.

```python
import click

@click.command()
def claude_desktop():
    """Install or manage Claude desktop tools."""
    click.echo('Claude desktop installed.')
```

--------------------------------

### fastmcp-server-auth-providers: Introspection Authentication

Source: https://gofastmcp.com/llms

Utilizes token introspection for authentication in the fastmcp server. This method validates tokens by checking with an authorization server. It's a secure way to manage token validity and scopes.

```python
from fastmcp.server.auth_providers.introspection import IntrospectionAuthProvider

# Example usage:
auth_provider = IntrospectionAuthProvider(introspection_endpoint="http://auth.server/introspect")

```

--------------------------------

### Python Tool Decorator Example - FastMCP v2.7.0

Source: https://gofastmcp.com/changelog

Demonstrates the use of the '@mcp.tool' decorator in FastMCP v2.7.0. This version allows for 'naked' decorator usage, aligning with Pythonic practices. The decorator is applied directly to a function definition.

```python
import mcp

@mcp.tool
def my_tool():
    ...

```

--------------------------------

### fastmcp-server: Server Core

Source: https://gofastmcp.com/llms

Contains the core components and logic for the fastmcp server. This module is central to the server's operation, likely handling request routing, connection management, and overall server lifecycle. It forms the backbone of the framework.

```python
from fastmcp.server import Server

# Example usage:
server = Server(host="0.0.0.0", port=8000)
# server.run()

```

--------------------------------

### fastmcp-server-middleware: Tool Injection

Source: https://gofastmcp.com/llms

Handles tool injection as a middleware component in the fastmcp server. This allows for the dynamic injection of tools or functionalities into the request processing pipeline. It's useful for extending server capabilities modularly.

```python
from fastmcp.server.middleware.tool_injection import ToolInjectionMiddleware

# Example usage:
# Assuming 'app' is your ASGI application and 'tool_manager' is available
# app = ToolInjectionMiddleware(app, tool_manager=tool_manager)

```

--------------------------------

### FastMCP CLI Install Cursor Command

Source: https://gofastmcp.com/llms

Command for installing or managing Cursor related functionalities within the FastMCP CLI. This might relate to code editors or specific IDE integrations.

```python
import click

@click.command()
def cursor():
    """Install or manage Cursor integration."""
    click.echo('Cursor integration installed.')
```

--------------------------------

### fastmcp-server-auth-providers: GitHub Authentication

Source: https://gofastmcp.com/llms

Enables authentication using GitHub credentials for the fastmcp server. This allows users to log in or authorize actions using their GitHub accounts. It simplifies OAuth integration with GitHub.

```python
from fastmcp.server.auth_providers.github import GithubAuthProvider

# Example usage:
auth_provider = GithubAuthProvider(client_id="your_client_id", client_secret="your_client_secret")

```

--------------------------------

### Python: Annotating Tool Parameters with Advanced Metadata using Pydantic Field

Source: https://gofastmcp.com/servers/tools

Illustrates the use of Pydantic's `Field` class within `Annotated` for advanced parameter metadata, including descriptions, validation constraints (e.g., `ge`, `le`), and default values. This approach provides more control over parameter validation and documentation, suitable for complex requirements like range checks or specific format validations.

```python
from typing import Annotated, Literal
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

```python
@mcp.tool
def search_database(
    query: str = Field(description="Search query string"),
    limit: int = Field(10, description="Maximum number of results", ge=1, le=100)
) -> list:
    """Search the database with the provided query."""
    # Implementation...

```

--------------------------------

### FastMCP CLI Install Gemini CLI Command

Source: https://gofastmcp.com/llms

Command for installing or managing Gemini CLI tools within the FastMCP ecosystem. This likely involves setup for Google's Gemini AI models.

```python
import click

@click.command()
def gemini_cli():
    """Install or manage Gemini CLI tools."""
    click.echo('Gemini CLI tools installed.')
```

--------------------------------

### FastMCP Server JWT Issuer

Source: https://gofastmcp.com/llms

Handles the creation and signing of JSON Web Tokens (JWT) for authentication. This module is used to issue tokens to authenticated users.

```python
import jwt

SECRET_KEY = "your-secret-key"

def create_jwt_token(user_id: str) -> str:
    payload = {"user_id": user_id}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_jwt_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

--------------------------------

### FastMCP CLI Install Claude Code Command

Source: https://gofastmcp.com/llms

Command for installing or managing Claude code related functionalities within the FastMCP CLI. This might involve setting up specific AI models or tools.

```python
import click

@click.command()
def claude_code():
    """Install or manage Claude code tools."""
    click.echo('Claude code installed.')
```

--------------------------------

### fastmcp-server-middleware: Initialization

Source: https://gofastmcp.com/llms

Handles the initialization of middleware components for the fastmcp server. Middleware in web frameworks typically processes requests and responses before they reach the main application logic. This module sets up the middleware pipeline.

```python
from fastmcp.server.middleware import initialize_middleware

# Example usage:
app = ... # Your FastAPI or other ASGI application
initialized_app = initialize_middleware(app)

```

--------------------------------

### fastmcp-server-auth-providers: Google Authentication

Source: https://gofastmcp.com/llms

Implements authentication via Google accounts for the fastmcp server. This allows users to authenticate using their Google identity, leveraging Google's robust security infrastructure. It simplifies Google OAuth 2.0 integration.

```python
from fastmcp.server.auth_providers.google import GoogleAuthProvider

# Example usage:
auth_provider = GoogleAuthProvider(client_id="your_client_id", client_secret="your_client_secret")

```

--------------------------------

### FastMCP Server OIDC Proxy

Source: https://gofastmcp.com/llms

Acts as a proxy for handling OpenID Connect (OIDC) authentication flows on the server side. This module enables integration with OIDC identity providers.

--------------------------------

### MCP JSON Configuration

Source: https://gofastmcp.com/llms

Generate standard MCP configuration files for any compatible client using this tool.

```APIDOC
## MCP JSON Configuration

### Description
This tool helps in generating standard MCP configuration files compatible with various clients.

### Method
POST

### Endpoint
/integrations/mcp-json-configuration

### Parameters
#### Request Body
- **config_data** (object) - Required - The data to be used for generating the configuration file.

### Request Example
{
  "config_data": {
    "server_name": "my-mcp-server",
    "port": 8080
  }
}

### Response
#### Success Response (200)
- **file_content** (string) - The generated MCP JSON configuration file content.

#### Response Example
{
  "file_content": "{\"server_name\": \"my-mcp-server\", \"port\": 8080}"
}
```

--------------------------------

### fastmcp-server-middleware: Core Middleware

Source: https://gofastmcp.com/llms

Defines the core middleware functionalities for the fastmcp server. This module likely contains the base classes or fundamental middleware components used throughout the framework. It sets the foundation for request processing.

```python
from fastmcp.server.middleware import Middleware

# Example usage:
class CustomMiddleware(Middleware):
    async def dispatch(self, request, call_next):
        # ... process request ...
        response = await call_next(request)
        # ... process response ...
        return response

```

--------------------------------

### fastmcp-tools: Tool Manager

Source: https://gofastmcp.com/llms

Manages the lifecycle and registration of tools in the fastmcp framework. The ToolManager is responsible for discovering, loading, and providing access to available tools. It acts as a central registry for tool operations.

```python
from fastmcp.tools.tool_manager import ToolManager

# Example usage:
tool_manager = ToolManager()
tool_manager.register_tool(MyCustomTool())
result = tool_manager.run_tool("MyCustomTool", arg1="value")

```

--------------------------------

### fastmcp-utilities: Initialization

Source: https://gofastmcp.com/llms

Handles initialization for the utilities package in fastmcp. This typically involves setting up any necessary configurations or imports for the various utility modules. It ensures the utilities are ready for use.

```python
# __init__.py for fastmcp.utilities
# May contain package-level setup or imports.

```

--------------------------------

### fastmcp-server: Dependencies

Source: https://gofastmcp.com/llms

Handles dependency injection and management within the fastmcp server. Dependency injection is a design pattern that promotes loose coupling between objects. This module likely facilitates the configuration and resolution of dependencies.

```python
from fastmcp.server.dependencies import Depends

# Example usage:
def get_db():
    return "database_connection"

def process_data(db: str = Depends(get_db)):
    print(f"Using database: {db}")

```

--------------------------------

### fastmcp-server-auth-providers: Descope Authentication

Source: https://gofastmcp.com/llms

Integrates Descope for authentication within the fastmcp server. Descope is a modern authentication solution that simplifies user management and access control. This provider enables seamless integration with Descope's features.

```python
from fastmcp.server.auth_providers.descope import DescopeAuthProvider

# Example usage:
auth_provider = DescopeAuthProvider(project_id="your_project_id", management_key="your_management_key")

```

--------------------------------

### MCP JSON Configuration Generation for FastMCP

Source: https://gofastmcp.com/llms

Generate standard MCP configuration files compatible with any client. This utility simplifies the process of creating consistent configurations across different MCP environments.

```markdown
- [MCP JSON Configuration 🤝 FastMCP](https://gofastmcp.com/integrations/mcp-json-configuration.md): Generate standard MCP configuration files for any compatible client
```

--------------------------------

### fastmcp-utilities: CLI Utilities

Source: https://gofastmcp.com/llms

Offers utilities for building and managing Command Line Interfaces (CLIs) for fastmcp applications. This module helps in creating user-friendly command-line tools, handling arguments, and displaying output. It simplifies CLI development.

```python
from fastmcp.utilities.cli import command

# Example usage:
@command()
def greet(name: str):
    print(f"Hello, {name}!")

```

--------------------------------

### fastmcp-server-auth-providers: Debug Authentication

Source: https://gofastmcp.com/llms

Provides a debug authentication provider for the fastmcp server. This is useful during development and testing to bypass authentication mechanisms. It simplifies the process of testing different parts of the application without full authentication setup.

```python
from fastmcp.server.auth_providers.debug import DebugAuthProvider

# Example usage:
auth_provider = DebugAuthProvider()

```

--------------------------------

### Access MCP Context in Python Tools

Source: https://gofastmcp.com/servers/tools

Demonstrates how to access and utilize the `Context` object within a FastMCP tool function in Python. The `Context` object enables logging, reading resources, sampling LLM requests, and reporting progress. It requires adding a `Context` type hint to a tool function parameter.

```python
from fastmcp import FastMCP, Context

mcp = FastMCP(name="ContextDemo")

@mcp.tool
async def process_data(data_uri: str, ctx: Context) -> dict:
    """Process data from a resource with progress reporting."""
    await ctx.info(f"Processing data from {data_uri}")
    
    # Read a resource
    resource = await ctx.read_resource(data_uri)
    data = resource[0].content if resource else ""
    
    # Report progress
    await ctx.report_progress(progress=50, total=100)
    
    # Example request to the client's LLM for help
    summary = await ctx.sample(f"Summarize this in 10 words: {data[:200]}")
    
    await ctx.report_progress(progress=100, total=100)
    return {
        "length": len(data),
        "summary": summary.text
    }
```

--------------------------------

### General Utilities

Source: https://gofastmcp.com/llms

This section covers a broad range of utility functions and modules, including authentication utilities, CLI tools, component management, exception handling, HTTP utilities, introspection, JSON schema handling, logging, and MCP configurations.

```APIDOC
## General Utilities

This section details various utility modules and functions.

### Authentication Utilities
Provides utility functions for authentication tasks.

### CLI Utilities
Documentation for command-line interface utilities.

### Component Utilities
Information on managing and using components.

### Exception Handling Utilities
Details on exception handling mechanisms.

### HTTP Utilities
Utility functions for HTTP operations.

### Inspection Utilities
Documentation for inspecting various aspects of the SDK.

### JSON Schema Utilities
Information on generating and validating JSON schemas.

### JSON Schema Type Utilities
Details on utility functions for JSON schema types.

### Logging Utilities
Guides for using the logging utilities.

### MCP Configuration Utilities
Documentation for MCP configuration management.

### MCP Server Configuration Utilities
Details on utilities for MCP server configuration, including environments (base, uv) and sources (base, filesystem).

### OpenAPI Utilities
Information on utilities related to OpenAPI specifications.

### Testing Utilities
Provides utilities for testing SDK components.

### Type Utilities
Documentation for various type-related utility functions.

### UI Utilities
Details on utilities for UI interactions.
```

--------------------------------

### Tools and Utilities

Source: https://gofastmcp.com/llms

This section outlines the tools and utility modules available in the GoFastMCP SDK, including core tool functionality, tool management, and transformation.

```APIDOC
## Tools and Utilities

This section describes the available tools and utility modules.

### Core Tool Functionality
Documentation for the core functionalities of the tools module.

### Tool Manager
Information on managing and utilizing tools.

### Tool Transformation
Details on transforming tools and their configurations.
```

--------------------------------

### fastmcp-utilities: JSON Schema Utilities

Source: https://gofastmcp.com/llms

Offers utilities for working with JSON Schema, a vocabulary that allows you to annotate and validate JSON documents. This module helps in defining and validating data structures used within fastmcp applications. It ensures data integrity.

```python
from fastmcp.utilities.json_schema import validate_json

# Example usage:
schema = {"type": "object", "properties": {"name": {"type": "string"}}}
data = {"name": "example"}
if validate_json(data, schema):
    print("JSON is valid.")

```

--------------------------------

### fastmcp-server: Elicitation

Source: https://gofastmcp.com/llms

Facilitates data elicitation or gathering within the fastmcp server. This could involve prompting users for input, collecting data from external sources, or guiding a process. It's useful for interactive or data-driven workflows.

```python
from fastmcp.server.elicitation import elicit_input

# Example usage:
name = elicit_input("Enter your name: ")
print(f"Hello, {name}!")

```

--------------------------------

### Disable Tools Programmatically and at Creation

Source: https://gofastmcp.com/servers/tools

Demonstrates how to disable tools in FastMCP either during their creation using the 'enabled' parameter or programmatically after creation using .disable() and .enable() methods. Disabled tools are hidden from lists and raise errors if called.

```python
@mcp.tool(enabled=False)
def maintenance_tool():
    """This tool is currently under maintenance."""
    return "This tool is disabled."

@mcp.tool
def dynamic_tool():
    return "I am a dynamic tool."

# Disable and re-enable the tool
dynamic_tool.disable()
dynamic_tool.enable()
```

--------------------------------

### fastmcp-server-auth-providers: JWT Authentication

Source: https://gofastmcp.com/llms

Handles authentication using JSON Web Tokens (JWT) for the fastmcp server. JWTs are a standard for securely transmitting information between parties as a JSON object. This provider enables validation and parsing of JWTs.

```python
from fastmcp.server.auth_providers.jwt import JwtAuthProvider

# Example usage:
auth_provider = JwtAuthProvider(secret_key="your_secret_key")

```

--------------------------------

### Python: Annotating Tool Parameters with Simple String Descriptions

Source: https://gofastmcp.com/servers/tools

Demonstrates how to add simple string descriptions to tool parameters using Python's `Annotated` type hint. This method is concise for basic parameter explanations and is equivalent to using `Field(description=...)` for simple cases. It's applicable when the parameter requires only a human-readable explanation.

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

### Authentication Providers

Source: https://gofastmcp.com/llms

This section details the different authentication providers available in the GoFastMCP SDK, including Bearer, Debug, Descope, GitHub, Google, In-Memory, Introspection, JWT, ScaleKit, Supabase, and WorkOS.

```APIDOC
## Authentication Providers

This section provides details on various authentication methods supported by the GoFastMCP SDK.

### Bearer Token Authentication
Provides documentation for bearer token authentication.

### Debug Authentication
Details the debug authentication provider.

### Descope Authentication
Information on Descope authentication integration.

### GitHub Authentication
Guides for integrating GitHub as an authentication provider.

### Google Authentication
Documentation for using Google as an authentication provider.

### In-Memory Authentication
Explains the in-memory authentication mechanism.

### Introspection Authentication
Covers the introspection authentication endpoint.

### JWT Authentication
Details on JSON Web Token (JWT) based authentication.

### ScaleKit Authentication
Information regarding ScaleKit authentication.

### Supabase Authentication
Guides for integrating Supabase for authentication.

### WorkOS Authentication
Documentation for WorkOS authentication provider.
```

--------------------------------

### Tool List Change Notifications

Source: https://gofastmcp.com/servers/tools

Shows how FastMCP automatically sends 'notifications/tools/list_changed' when tools are added, removed, enabled, or disabled. This example highlights the operations that trigger these notifications and assumes an active MCP request context.

```python
@mcp.tool
def example_tool() -> str:
    return "Hello!"

# These operations trigger notifications:
mcp.add_tool(example_tool)     # Sends tools/list_changed notification
example_tool.disable()         # Sends tools/list_changed notification  
example_tool.enable()          # Sends tools/list_changed notification
mcp.remove_tool("example_tool") # Sends tools/list_changed notification
```

--------------------------------

### fastmcp-utilities: Inspection Utilities

Source: https://gofastmcp.com/llms

Provides utilities for inspecting Python objects, modules, or systems. This can be useful for debugging, introspection, or dynamic analysis. It helps in understanding the structure and state of the application.

```python
from fastmcp.utilities.inspect import get_function_signature

# Example usage:
def my_func(a, b=1):
    pass
signature = get_function_signature(my_func)
print(signature)

```

--------------------------------

### ToolResult Structured Content Example in Python

Source: https://gofastmcp.com/servers/tools

Shows how to provide structured data using the `structured_content` field in ToolResult. This dictionary is useful for programmatic processing by clients and can also serve as the primary content if `content` is omitted.

```python
ToolResult(
    content="Found 3 users",
    structured_content={"users": [{"name": "Alice"}, {"name": "Bob"}]}
)
```

--------------------------------

### Python Tool Returning Primitive Without Annotation

Source: https://gofastmcp.com/servers/tools

Illustrates a Python tool returning a primitive type (integer) without a return type annotation. In this case, FastMCP only generates traditional 'content' and no 'structuredContent' because it lacks schema information to serialize the primitive.

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

### Tool List Change Notifications

Source: https://gofastmcp.com/servers/tools

FastMCP automatically sends `notifications/tools/list_changed` notifications to connected clients when tools are added, removed, enabled, or disabled. This enables clients to stay updated with the current tool set without manual polling.

```APIDOC
## Notifications

FastMCP automatically sends `notifications/tools/list_changed` notifications to connected clients when tools are added, removed, enabled, or disabled. This allows clients to stay up-to-date with the current tool set without manually polling for changes.

### Example: Operations triggering notifications

```python
@mcp.tool
def example_tool() -> str:
    return "Hello!"

# These operations trigger notifications:
mcp.add_tool(example_tool)     # Sends tools/list_changed notification
example_tool.disable()         # Sends tools/list_changed notification  
example_tool.enable()          # Sends tools/list_changed notification
mcp.remove_tool("example_tool") # Sends tools/list_changed notification
```

Notifications are only sent when these operations occur within an active MCP request context (e.g., when called from within a tool or other MCP operation). Operations performed during server initialization do not trigger notifications.

Clients can handle these notifications using a [message handler](/clients/messages) to automatically refresh their tool lists or update their interfaces.
```

--------------------------------

### fastmcp-utilities: JSON Schema Type Utilities

Source: https://gofastmcp.com/llms

Provides utilities specifically for handling JSON Schema types. This module might offer functions to generate or manipulate schema definitions for various data types. It aids in precise data modeling and validation.

```python
from fastmcp.utilities.json_schema_type import StringSchema

# Example usage:
string_type = StringSchema(description="A string field")
print(string_type.to_dict())

```

--------------------------------

### fastmcp-utilities-mcp_server_config-v1: MCP Server Config

Source: https://gofastmcp.com/llms

Defines the main structure for MCP server configuration in version 1. This module aggregates various configuration aspects like environments, sources, and other server-specific settings. It provides a comprehensive configuration object.

```python
from fastmcp.utilities.mcp_server_config.v1.mcp_server_config import McpServerConfig

# Example usage:
# server_config = McpServerConfig()

```

--------------------------------

### Tool Disabling and Enabling

Source: https://gofastmcp.com/servers/tools

Control the visibility and availability of tools. Disabled tools are not listed and attempting to call them results in an error. Tools can be disabled upon creation or toggled programmatically.

```APIDOC
## Disabling Tools

You can control the visibility and availability of tools by enabling or disabling them. This is useful for feature flagging, maintenance, or dynamically changing the toolset available to a client. Disabled tools will not appear in the list of available tools returned by `list_tools`, and attempting to call a disabled tool will result in an "Unknown tool" error, just as if the tool did not exist.

By default, all tools are enabled. You can disable a tool upon creation using the `enabled` parameter in the decorator:

### Example: Disabling a tool at creation

```python
@mcp.tool(enabled=False)
def maintenance_tool():
    """This tool is currently under maintenance."""
    return "This tool is disabled."
```

You can also toggle a tool's state programmatically after it has been created:

### Example: Programmatically disabling and enabling a tool

```python
@mcp.tool
def dynamic_tool():
    return "I am a dynamic tool."

# Disable and re-enable the tool
dynamic_tool.disable()
dynamic_tool.enable()
```
```

--------------------------------

### fastmcp-utilities-mcp_server_config: Initialization

Source: https://gofastmcp.com/llms

Handles initialization for the MCP server configuration module. This likely sets up the structure or default values for server configuration settings. It's the entry point for server configuration management.

```python
# __init__.py for fastmcp.utilities.mcp_server_config
# May contain setup for the server config package.

```

--------------------------------

### Python Tool Returning Primitive With Annotation

Source: https://gofastmcp.com/servers/tools

Shows a Python tool returning a primitive type (integer) with a return type annotation (`-> int`). FastMCP generates 'structuredContent' by wrapping the primitive value in a 'result' key, adhering to JSON schema requirements for object-type roots.

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

### ToolResult Content Field Examples in Python

Source: https://gofastmcp.com/servers/tools

Illustrates different ways to use the `content` field in ToolResult. It can accept simple strings, lists of content blocks like TextContent and ImageContent, or other serializable values.

```python
# Simple string
ToolResult(content="Hello, world!")

# List of content blocks
ToolResult(content=[
    TextContent(type="text", text="Result: 42"),
    ImageContent(type="image", data="base64...", mimeType="image/png")
])
```

--------------------------------

### fastmcp-utilities-mcp_server_config-v1-environments: Initialization

Source: https://gofastmcp.com/llms

Handles initialization for environment-specific configurations within the v1 MCP server configuration. This module likely sets up how different environments (e.g., development, production) are configured. It allows for environment-specific settings.

```python
# __init__.py for fastmcp.utilities.mcp_server_config.v1.environments
# Setup for environment configurations.

```

--------------------------------

### ToolResult Meta Field Example in Python

Source: https://gofastmcp.com/servers/tools

Demonstrates the use of the `meta` field in ToolResult for including runtime metadata such as execution time, model version, and confidence scores. This data is separate from the tool's primary output and definition metadata.

```python
ToolResult(
    content="Analysis complete",
    structured_content={"result": "positive"},
    meta={
        "execution_time_ms": 145,
        "model_version": "2.1",
        "confidence": 0.95
    }
)
```

--------------------------------

### Decorator Recipe to Make Sync Functions Async

Source: https://gofastmcp.com/servers/tools

Provides a reusable decorator function `make_async_background` that transforms a synchronous function into an asynchronous one using `asyncer.asyncify`. This is useful for integrating blocking synchronous operations into an async framework like FastMCP without blocking the event loop. It takes any callable and returns an awaitable callable.

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

--------------------------------

### Override Tool Name and Description with @mcp.tool Arguments

Source: https://gofastmcp.com/servers/tools

Demonstrates how to use the 'name' and 'description' arguments of the @mcp.tool decorator to provide custom values for LLM interaction. This overrides the function's name and docstring respectively. It also shows optional 'tags' and 'meta' for further customization.

```python
import mcp

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

### fastmcp-utilities-mcp_server_config-v1-environments: UV Environment Config

Source: https://gofastmcp.com/llms

Specifies configuration settings for a 'UV' environment within the v1 MCP server configuration. This module tailors settings for a particular deployment scenario, possibly related to UV (e.g., UVicorn).

```python
from fastmcp.utilities.mcp_server_config.v1.environments.uv import UvicornEnvironmentConfig

# Example usage:
# uv_config = UvicornEnvironmentConfig()

```

--------------------------------

### fastmcp-utilities-mcp_server_config-v1-sources: Initialization

Source: https://gofastmcp.com/llms

Handles initialization for the configuration sources module within v1 MCP server configuration. This sets up how configuration data is loaded (e.g., from files, environment variables).

```python
# __init__.py for fastmcp
```

--------------------------------

### Exclude Arguments from Tool Schema

Source: https://gofastmcp.com/servers/tools

Demonstrates how to exclude specific arguments from a tool's schema presented to an LLM. This is useful for arguments injected at runtime, like user IDs or credentials. Only arguments with default values can be excluded; required arguments will cause an error if excluded.

```python
from fastmcp import mcp

@mcp.tool(
    name="get_user_details",
    exclude_args=["user_id"]
)
def get_user_details(user_id: str = None) -> str:
    # user_id will be injected by the server, not provided by the LLM
    ...

```

--------------------------------

### Handle Division by Zero with ToolError in Python

Source: https://gofastmcp.com/servers/tools

Illustrates how to use `ToolError` to provide specific, client-facing error messages, especially for critical issues like division by zero. Messages from `ToolError` are always sent to clients, irrespective of the `mask_error_details` setting.

```python
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

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

### fastmcp-utilities-mcp_server_config-v1: Initialization

Source: https://gofastmcp.com/llms

Initializes the version 1 (v1) of the MCP server configuration. This module likely defines the structure and logic for server configurations specific to version 1 of the MCP specification. It ensures backward compatibility or specific version features.

```python
# __init__.py for fastmcp.utilities.mcp_server_config.v1
# Package-level setup for v1 server config.

```

--------------------------------

### fastmcp-utilities-mcp_server_config-v1-environments: Base Environment Config

Source: https://gofastmcp.com/llms

Defines the base configuration settings for environments in v1 MCP server configuration. This module likely provides default or common settings applicable across all environments, forming a foundation for specific environment overrides.

```python
from fastmcp.utilities.mcp_server_config.v1.environments.base import BaseEnvironmentConfig

# Example usage:
class DevelopmentEnvironment(BaseEnvironmentConfig):
    debug = True

```
