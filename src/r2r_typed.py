"""Type-safe wrapper around httpx client for R2R API.

This module provides typed interfaces to R2R API while maintaining
DynamicBearerAuth compatibility for serverless environments.

Architecture:
- TypedDicts for request/response types (IDE autocomplete, mypy checking)
- Async methods matching R2R API structure
- Error handling with structured exceptions
- Maintains httpx control (timeout, headers, etc.)

Benefits over R2RClient SDK:
✅ Request-time authentication (serverless compatible)
✅ Full control over HTTP requests
✅ Type hints for better DX
✅ OpenAPI auto-generation compatibility
✅ Minimal dependencies

Benefits over raw httpx:
✅ Type hints and autocomplete
✅ Structured request/response types
✅ Less boilerplate code
✅ Consistent error handling
"""

from typing import Any, Literal, TypedDict, cast

import httpx

# ============================================================================
# REQUEST TYPES - TypedDicts for API parameters
# ============================================================================


class SearchSettings(TypedDict, total=False):
    """Search configuration settings."""

    limit: int
    offset: int
    use_hybrid_search: bool
    use_semantic_search: bool
    use_fulltext_search: bool
    search_strategy: Literal["vanilla", "hyde", "rag_fusion"]
    filters: dict[str, Any]
    chunk_settings: dict[str, Any]
    graph_settings: dict[str, Any]
    hybrid_settings: dict[str, Any]


class SearchRequest(TypedDict, total=False):
    """Search request parameters."""

    query: str
    search_settings: SearchSettings


class RAGSettings(TypedDict, total=False):
    """RAG generation settings."""

    max_tokens: int
    model: str
    temperature: float
    stream: bool
    include_citations: bool


class RAGRequest(TypedDict, total=False):
    """RAG request parameters."""

    query: str
    rag_generation_config: RAGSettings
    search_settings: SearchSettings


class AgentMessage(TypedDict):
    """Agent conversation message."""

    role: Literal["user", "assistant", "system"]
    content: str


class AgentRequest(TypedDict, total=False):
    """Agent request parameters."""

    message: AgentMessage | str
    messages: list[AgentMessage]
    conversation_id: str
    mode: Literal["rag", "research"]
    max_tokens: int
    stream: bool
    rag_tools: list[str]


class DocumentMetadata(TypedDict, total=False):
    """Document metadata."""

    title: str
    description: str
    tags: list[str]
    custom: dict[str, Any]


class CollectionRequest(TypedDict, total=False):
    """Collection creation request."""

    name: str
    description: str
    metadata: dict[str, Any]


# ============================================================================
# RESPONSE TYPES - TypedDicts for API responses
# ============================================================================


class ChunkResult(TypedDict, total=False):
    """Search result chunk."""

    id: str
    document_id: str
    text: str
    score: float
    metadata: dict[str, Any]


class SearchResponse(TypedDict, total=False):
    """Search API response."""

    results: dict[str, Any]
    chunk_search_results: list[ChunkResult]


class RAGResponse(TypedDict, total=False):
    """RAG API response."""

    answer: str
    citations: list[dict[str, Any]]
    search_results: SearchResponse


class AgentResponse(TypedDict, total=False):
    """Agent API response."""

    response: str
    conversation_id: str
    tool_calls: list[dict[str, Any]]


class DocumentResponse(TypedDict, total=False):
    """Document API response."""

    document_id: str
    title: str
    metadata: dict[str, Any]
    created_at: str
    updated_at: str


class CollectionResponse(TypedDict, total=False):
    """Collection API response."""

    collection_id: str
    name: str
    description: str
    document_count: int
    created_at: str


# ============================================================================
# TYPED CLIENT - Type-safe wrapper around httpx.AsyncClient
# ============================================================================


class R2RTypedClient:
    """Type-safe wrapper around httpx.AsyncClient for R2R API.

    Provides typed methods for R2R API operations while maintaining:
    - DynamicBearerAuth compatibility (serverless)
    - Full HTTP control (timeout, headers, etc.)
    - Async/await pattern
    - Error handling

    Usage:
        from src.r2r_typed import R2RTypedClient

        _http_client = httpx.AsyncClient(auth=DynamicBearerAuth())
        r2r = R2RTypedClient(_http_client)

        results = await r2r.search(query="machine learning", limit=10)
    """

    def __init__(self, client: httpx.AsyncClient):
        """Initialize typed client with httpx client.

        Args:
            client: Configured httpx.AsyncClient with auth, base_url, etc.
        """
        self._client = client

    # ========================================================================
    # RETRIEVAL METHODS - Search, RAG, Agent
    # ========================================================================

    async def search(
        self,
        query: str,
        limit: int = 10,
        use_hybrid_search: bool = True,
        search_strategy: Literal["vanilla", "hyde", "rag_fusion"] = "vanilla",
        filters: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> SearchResponse:
        """Semantic search over R2R knowledge base.

        Args:
            query: Search query string
            limit: Maximum number of results (default: 10)
            use_hybrid_search: Combine semantic + fulltext (default: True)
            search_strategy: Search algorithm (default: "vanilla")
            filters: Optional metadata filters
            **kwargs: Additional search settings

        Returns:
            SearchResponse with chunk_search_results

        Example:
            results = await r2r.search(
                query="machine learning best practices",
                limit=5,
                use_hybrid_search=True
            )
        """
        search_settings: SearchSettings = {
            "limit": limit,
            "use_hybrid_search": use_hybrid_search,
            "search_strategy": search_strategy,
        }

        if filters:
            search_settings["filters"] = filters

        # Merge additional kwargs
        if kwargs:
            search_settings.update(cast(SearchSettings, kwargs))  # type: ignore[typeddict-item]

        payload: SearchRequest = {
            "query": query,
            "search_settings": search_settings,
        }

        response = await self._client.post("/v3/retrieval/search", json=payload)
        response.raise_for_status()

        return response.json()

    async def rag(
        self,
        query: str,
        max_tokens: int = 4000,
        temperature: float = 0.1,
        include_citations: bool = True,
        search_limit: int | None = None,
        **kwargs: Any,
    ) -> RAGResponse:
        """Retrieval-Augmented Generation query.

        Args:
            query: Question or prompt
            max_tokens: Maximum tokens to generate (default: 4000)
            temperature: Sampling temperature (default: 0.1)
            include_citations: Include source citations (default: True)
            search_limit: Limit search results for context (default: None)
            **kwargs: Additional RAG settings

        Returns:
            RAGResponse with answer and optional citations

        Example:
            answer = await r2r.rag(
                query="What is RAG?",
                max_tokens=2000,
                temperature=0.2
            )
            print(answer["answer"])
        """
        rag_config: RAGSettings = {
            "max_tokens": max_tokens,
            "temperature": temperature,
            "include_citations": include_citations,
        }

        payload: RAGRequest = {
            "query": query,
            "rag_generation_config": rag_config,
        }

        if search_limit:
            payload["search_settings"] = {"limit": search_limit}

        # Merge additional kwargs
        if kwargs:
            payload["rag_generation_config"].update(cast(RAGSettings, kwargs))  # type: ignore[typeddict-item]

        response = await self._client.post("/v3/retrieval/rag", json=payload)
        response.raise_for_status()

        return response.json()

    async def agent(
        self,
        message: str | dict[str, str],
        conversation_id: str | None = None,
        mode: Literal["rag", "research"] = "research",
        max_tokens: int = 4000,
        stream: bool = False,
        **kwargs: Any,
    ) -> AgentResponse:
        """Multi-turn conversational agent with reasoning.

        Args:
            message: User message (string or dict with role/content)
            conversation_id: Continue existing conversation (default: new)
            mode: Agent mode - "rag" or "research" (default: "research")
            max_tokens: Maximum tokens for response (default: 4000)
            stream: Stream response tokens (default: False)
            **kwargs: Additional agent settings (rag_tools, etc.)

        Returns:
            AgentResponse with response and conversation_id

        Example:
            # New conversation
            response = await r2r.agent(
                message="What are the key concepts in this document?",
                mode="research"
            )

            # Continue conversation
            follow_up = await r2r.agent(
                message="Can you elaborate on point 2?",
                conversation_id=response["conversation_id"]
            )
        """
        # Format message
        if isinstance(message, str):
            msg: AgentMessage = {"role": "user", "content": message}
        else:
            msg = message  # type: ignore

        payload: AgentRequest = {
            "message": msg,
            "mode": mode,
            "max_tokens": max_tokens,
            "stream": stream,
        }

        if conversation_id:
            payload["conversation_id"] = conversation_id

        # Merge additional kwargs
        if kwargs:
            payload.update(cast(AgentRequest, kwargs))  # type: ignore[typeddict-item]

        response = await self._client.post("/v3/retrieval/agent", json=payload)
        response.raise_for_status()

        return response.json()

    # ========================================================================
    # DOCUMENT METHODS - Upload, retrieve, delete
    # ========================================================================

    async def create_document(
        self,
        file_path: str | None = None,
        content: str | None = None,
        metadata: DocumentMetadata | None = None,
        collection_ids: list[str] | None = None,
    ) -> DocumentResponse:
        """Upload document to R2R.

        Args:
            file_path: Path to file (for file upload)
            content: Raw text content (alternative to file)
            metadata: Document metadata (title, tags, etc.)
            collection_ids: Collections to add document to

        Returns:
            DocumentResponse with document_id

        Example:
            doc = await r2r.create_document(
                file_path="paper.pdf",
                metadata={"title": "Research Paper", "tags": ["AI", "ML"]}
            )
        """
        if file_path:
            with open(file_path, "rb") as f:
                files = {"file": f}
                data: dict[str, Any] = {}
                if metadata:
                    data["metadata"] = metadata  # type: ignore[assignment]
                if collection_ids:
                    data["collection_ids"] = collection_ids

                response = await self._client.post(
                    "/v3/documents", files=files, data=data
                )
        elif content:
            payload: dict[str, Any] = {"content": content}
            if metadata:
                payload["metadata"] = metadata
            if collection_ids:
                payload["collection_ids"] = collection_ids

            response = await self._client.post("/v3/documents", json=payload)
        else:
            raise ValueError("Either file_path or content must be provided")

        response.raise_for_status()
        return response.json()

    async def get_document(self, document_id: str) -> DocumentResponse:
        """Retrieve document metadata by ID.

        Args:
            document_id: Document UUID

        Returns:
            DocumentResponse with metadata

        Example:
            doc = await r2r.get_document("uuid-here")
            print(doc["title"])
        """
        response = await self._client.get(f"/v3/documents/{document_id}")
        response.raise_for_status()
        return response.json()

    async def delete_document(self, document_id: str) -> dict[str, str]:
        """Delete document from R2R.

        Args:
            document_id: Document UUID

        Returns:
            Success message

        Example:
            result = await r2r.delete_document("uuid-here")
        """
        response = await self._client.delete(f"/v3/documents/{document_id}")
        response.raise_for_status()
        return response.json()

    async def list_documents(
        self, limit: int = 100, offset: int = 0
    ) -> list[DocumentResponse]:
        """List all documents.

        Args:
            limit: Maximum documents to return (default: 100)
            offset: Pagination offset (default: 0)

        Returns:
            List of DocumentResponse

        Example:
            docs = await r2r.list_documents(limit=10)
            for doc in docs:
                print(doc["title"])
        """
        response = await self._client.get(
            "/v3/documents", params={"limit": limit, "offset": offset}
        )
        response.raise_for_status()
        return response.json()

    # ========================================================================
    # COLLECTION METHODS - Create, manage, query
    # ========================================================================

    async def create_collection(
        self, name: str, description: str = "", metadata: dict[str, Any] | None = None
    ) -> CollectionResponse:
        """Create new collection.

        Args:
            name: Collection name
            description: Collection description (optional)
            metadata: Additional metadata (optional)

        Returns:
            CollectionResponse with collection_id

        Example:
            collection = await r2r.create_collection(
                name="Research Papers",
                description="AI research papers collection"
            )
        """
        payload: CollectionRequest = {"name": name, "description": description}

        if metadata:
            payload["metadata"] = metadata

        response = await self._client.post("/v3/collections", json=payload)
        response.raise_for_status()
        return response.json()

    async def list_collections(
        self, limit: int = 100, offset: int = 0
    ) -> list[CollectionResponse]:
        """List all collections.

        Args:
            limit: Maximum collections to return (default: 100)
            offset: Pagination offset (default: 0)

        Returns:
            List of CollectionResponse

        Example:
            collections = await r2r.list_collections()
            for col in collections:
                print(f"{col['name']}: {col['document_count']} docs")
        """
        response = await self._client.get(
            "/v3/collections", params={"limit": limit, "offset": offset}
        )
        response.raise_for_status()
        return response.json()

    async def get_collection(self, collection_id: str) -> CollectionResponse:
        """Get collection details.

        Args:
            collection_id: Collection UUID

        Returns:
            CollectionResponse with details

        Example:
            col = await r2r.get_collection("uuid-here")
            print(f"{col['name']}: {col['document_count']} documents")
        """
        response = await self._client.get(f"/v3/collections/{collection_id}")
        response.raise_for_status()
        return response.json()

    # ========================================================================
    # UTILITY METHODS - Health, info, etc.
    # ========================================================================

    async def health(self) -> dict[str, str]:
        """Check R2R API health status.

        Returns:
            Health status

        Example:
            status = await r2r.health()
            print(status)  # {"status": "ok"}
        """
        response = await self._client.get("/health")
        response.raise_for_status()
        return response.json()

    # ========================================================================
    # ADVANCED: Low-level HTTP access
    # ========================================================================

    async def request(
        self,
        method: str,
        path: str,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Low-level HTTP request for custom operations.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            json: JSON payload
            params: Query parameters
            **kwargs: Additional httpx request options

        Returns:
            Response JSON

        Example:
            # Custom endpoint not yet wrapped
            result = await r2r.request(
                "POST",
                "/v3/custom/endpoint",
                json={"param": "value"}
            )
        """
        response = await self._client.request(
            method, path, json=json, params=params, **kwargs
        )
        response.raise_for_status()
        return response.json()


# ============================================================================
# HELPER FUNCTIONS - Common patterns
# ============================================================================


def format_search_results(response: SearchResponse, limit: int | None = None) -> str:
    """Format search results for display.

    Args:
        response: SearchResponse from r2r.search()
        limit: Limit formatted results (default: all)

    Returns:
        Formatted string with results

    Example:
        results = await r2r.search(query="AI")
        print(format_search_results(results, limit=3))
    """
    chunks: list[ChunkResult] = response.get("results", {}).get("chunk_search_results", [])  # type: ignore

    if not chunks:
        return "No results found"

    formatted: list[str] = []
    for i, chunk in enumerate(chunks[:limit] if limit else chunks):
        formatted.append(f"""
Result {i + 1}:
  Score: {chunk.get('score', 0):.3f}
  Text: {chunk.get('text', '')[:200]}...
  Document: {chunk.get('document_id', 'N/A')}
""")

    return "\n".join(formatted)


def extract_citations(response: RAGResponse) -> list[str]:
    """Extract citation sources from RAG response.

    Args:
        response: RAGResponse from r2r.rag()

    Returns:
        List of citation sources

    Example:
        answer = await r2r.rag(query="What is RAG?")
        citations = extract_citations(answer)
        for citation in citations:
            print(f"Source: {citation}")
    """
    citations = response.get("citations", [])
    return [c.get("text", "")[:100] for c in citations]
