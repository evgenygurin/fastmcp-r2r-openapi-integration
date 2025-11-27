# FastMCP Pipelines & ctx.sample Patterns

**Based on R2R RAG analysis with 20 sources per query**

This document describes advanced FastMCP patterns for pipeline composition and LLM sampling, implemented in the R2R MCP server.

---

## 📚 Overview

### What is ctx.sample?

`ctx.sample()` is an asynchronous method in FastMCP's `Context` object that allows MCP tools to request text generation from an LLM. By default, requests are sent to the client's LLM, but a fallback handler can be configured on the server.

**Key Benefits:**
- ✅ Leverage AI capabilities within tools
- ✅ Offload complex reasoning to LLMs
- ✅ Generate dynamic content
- ✅ Maintain context within user interactions

### What are FastMCP Pipelines?

Pipelines are a pattern for composing and chaining multiple tools, resources, and operations into cohesive workflows. They enable:
- ✅ Multi-step processing
- ✅ Tool composition
- ✅ Error handling across steps
- ✅ Progress tracking
- ✅ Result passing between steps

---

## 🔬 ctx.sample API

### Method Signature

```python
async def sample(
    messages: str | list[str | SamplingMessage],
    system_prompt: str | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
    model_preferences: ModelPreferences | str | list[str] | None = None
) -> TextContent | ImageContent
```

### Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `messages` | `str \| list` | Prompt(s) to send to LLM | Required |
| `system_prompt` | `str \| None` | System prompt to guide behavior | `None` |
| `temperature` | `float \| None` | Randomness (0.0-1.0) | `None` |
| `max_tokens` | `int \| None` | Maximum response tokens | 512 |
| `model_preferences` | Various | Model selection preferences | `None` |

### Return Value

- `TextContent`: Object with `.text` attribute containing generated text
- `ImageContent`: For image generation (less common)

---

## 💡 ctx.sample Patterns

### Pattern 1: Basic Text Generation

```python
@mcp.tool()
async def generate_summary(content: str, ctx: Context) -> str:
    """Generate a concise summary."""
    prompt = f"Summarize this content:\n\n{content}"
    response = await ctx.sample(prompt)
    return response.text
```

**Use Cases:**
- Summaries
- Explanations
- Simple transformations

---

### Pattern 2: System Prompt for Role-Based Responses

```python
@mcp.tool()
async def analyze_as_expert(
    data: str,
    expert_role: str,
    ctx: Context
) -> str:
    """Analyze data from expert perspective."""
    response = await ctx.sample(
        messages=f"Analyze this data:\n\n{data}",
        system_prompt=f"You are an expert {expert_role}. Provide detailed analysis.",
        temperature=0.3,  # Lower for focused responses
        max_tokens=1000
    )
    return response.text
```

**Use Cases:**
- Role-based analysis
- Domain-specific insights
- Guided generation

**Temperature Guidelines:**
- `0.0-0.3`: Focused, deterministic (analysis, code)
- `0.4-0.7`: Balanced (general tasks)
- `0.8-1.0`: Creative (brainstorming, stories)

---

### Pattern 3: Structured Output

```python
@mcp.tool()
async def extract_json(text: str, schema: dict, ctx: Context) -> dict:
    """Extract structured data as JSON."""
    prompt = f"""Extract information from this text according to the schema.
Return ONLY valid JSON.

Text: {text}
Schema: {json.dumps(schema)}"""
    
    response = await ctx.sample(
        messages=prompt,
        temperature=0.2,  # Very low for structured output
        max_tokens=2000
    )
    
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {"raw": response.text, "error": "JSON parse failed"}
```

**Use Cases:**
- Data extraction
- Schema validation
- Structured information retrieval

**Best Practices:**
- Use low temperature (0.1-0.3)
- Explicit output format instructions
- Error handling for invalid JSON
- Consider fallback strategies

---

### Pattern 4: Multi-Turn Conversations

```python
@mcp.tool()
async def conversational_query(
    question: str,
    history: list[dict],
    ctx: Context
) -> str:
    """Handle multi-turn conversations."""
    # history = [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    
    messages = [msg["content"] for msg in history]
    messages.append(question)
    
    response = await ctx.sample(
        messages=messages,
        temperature=0.7,
        max_tokens=1500
    )
    
    return response.text
```

**Use Cases:**
- Chat interfaces
- Follow-up questions
- Context-aware responses

---

### Pattern 5: Retry with Exponential Backoff

```python
async def sample_with_retry(
    ctx: Context,
    prompt: str,
    max_retries: int = 3
) -> str:
    """Robust sampling with retry logic."""
    for attempt in range(max_retries):
        try:
            await ctx.debug(f"Attempt {attempt + 1}/{max_retries}")
            
            response = await ctx.sample(
                messages=prompt,
                temperature=0.5,
                max_tokens=1000
            )
            
            return response.text
            
        except Exception as e:
            await ctx.error(f"Attempt {attempt + 1} failed: {e}")
            
            if attempt == max_retries - 1:
                raise
            
            # Exponential backoff
            await asyncio.sleep(2 ** attempt)
```

**Use Cases:**
- Network instability
- Rate limiting
- Transient errors

---

## 🔗 Pipeline Patterns

### Pattern 1: Linear Pipeline

**Sequential execution of steps with result passing:**

```python
class Pipeline:
    """Chain multiple operations sequentially."""
    
    def __init__(self, ctx: Context | None = None):
        self.ctx = ctx
        self.steps: list[dict] = []
        self.results: dict[str, Any] = {}
    
    def add_step(self, name: str, func: callable, **kwargs) -> "Pipeline":
        """Add a step to the pipeline."""
        self.steps.append({"name": name, "func": func, "kwargs": kwargs})
        return self
    
    async def execute(self) -> dict[str, Any]:
        """Execute all steps in order."""
        for idx, step in enumerate(self.steps):
            # Pass previous results to each step
            step["kwargs"]["previous_results"] = self.results
            
            # Execute
            result = await step["func"](**step["kwargs"])
            self.results[step["name"]] = result
        
        return self.results
```

**Usage Example:**

```python
@mcp.tool()
async def research_pipeline(query: str, ctx: Context) -> dict:
    """Multi-step research: search → analyze → summarize."""
    
    pipeline = Pipeline(ctx)
    
    results = await (
        pipeline
        .add_step("search", search_documents, query=query)
        .add_step("analyze", analyze_with_llm)
        .add_step("summarize", create_summary)
        .execute()
    )
    
    return results
```

**Benefits:**
- ✅ Clean, fluent API
- ✅ Result passing between steps
- ✅ Progress tracking
- ✅ Centralized error handling

---

### Pattern 2: Conditional Pipeline

**Execute steps based on previous results:**

```python
class ConditionalPipeline:
    """Pipeline with conditional step execution."""
    
    def add_step(
        self,
        name: str,
        func: callable,
        condition: callable | None = None,
        **kwargs
    ) -> "ConditionalPipeline":
        """Add step with optional condition."""
        self.steps.append({
            "name": name,
            "func": func,
            "condition": condition,
            "kwargs": kwargs
        })
        return self
    
    async def execute(self) -> dict:
        """Execute steps conditionally."""
        for step in self.steps:
            # Check condition
            if step["condition"] and not step["condition"](self.results):
                await self.ctx.info(f"⏭️  Skipping {step['name']}")
                continue
            
            # Execute
            result = await step["func"](**step["kwargs"])
            self.results[step["name"]] = result
        
        return self.results
```

**Usage Example:**

```python
pipeline = ConditionalPipeline(ctx)
pipeline.add_step("search", search_func)
pipeline.add_step(
    "detailed_analysis",
    analyze_func,
    condition=lambda r: len(r["search"]["results"]) > 10  # Only if many results
)
pipeline.add_step("summarize", summarize_func)
```

**Use Cases:**
- Dynamic workflows
- Resource optimization
- Adaptive processing

---

### Pattern 3: Parallel Processing Pipeline

**Process multiple items concurrently:**

```python
async def parallel_pipeline(
    items: list[dict],
    ctx: Context
) -> list[dict]:
    """Process items in parallel using LLM."""
    
    async def process_item(item: dict, idx: int) -> dict:
        """Process single item."""
        await ctx.debug(f"Processing item {idx + 1}")
        
        response = await ctx.sample(
            messages=f"Analyze: {item['text']}",
            temperature=0.3,
            max_tokens=500
        )
        
        return {
            "id": item["id"],
            "analysis": response.text,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    # Execute all in parallel
    tasks = [process_item(item, i) for i, item in enumerate(items)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Filter out exceptions
    successful = [r for r in results if not isinstance(r, Exception)]
    
    await ctx.info(f"✓ Processed {len(successful)}/{len(items)} items")
    
    return successful
```

**Benefits:**
- ✅ Concurrent execution
- ✅ Faster processing
- ✅ Exception isolation

**Use Cases:**
- Batch document analysis
- Multiple query comparison
- Large-scale processing

---

### Pattern 4: Pipeline with Fallback

**Primary operation with fallback on failure:**

```python
async def pipeline_with_fallback(
    primary_func: callable,
    fallback_func: callable,
    ctx: Context,
    **kwargs
) -> Any:
    """Execute with fallback on error."""
    
    try:
        await ctx.info("⚡ Attempting primary operation")
        result = await primary_func(ctx=ctx, **kwargs)
        await ctx.info("✓ Primary successful")
        return result
        
    except Exception as e:
        await ctx.error(f"❌ Primary failed: {e}")
        await ctx.info("🔄 Using fallback")
        
        result = await fallback_func(ctx=ctx, **kwargs)
        await ctx.info("✓ Fallback successful")
        return result
```

**Usage Example:**

```python
# Try expensive LLM, fallback to rule-based
result = await pipeline_with_fallback(
    primary_func=expensive_llm_analysis,
    fallback_func=simple_rule_based_analysis,
    ctx=ctx,
    data=my_data
)
```

**Use Cases:**
- Graceful degradation
- Cost optimization
- Availability assurance

---

### Pattern 5: Cached Pipeline Steps

**Cache expensive operations:**

```python
_cache: dict[str, tuple[Any, datetime]] = {}

async def cached_pipeline_step(
    cache_key: str,
    func: callable,
    ttl_seconds: int = 300,
    ctx: Context | None = None,
    **kwargs
) -> Any:
    """Execute with caching."""
    
    # Check cache
    if cache_key in _cache:
        result, cached_time = _cache[cache_key]
        age = (datetime.utcnow() - cached_time).total_seconds()
        
        if age < ttl_seconds:
            await ctx.info(f"📦 Cache hit (age: {age:.1f}s)")
            return result
    
    # Execute
    await ctx.info(f"🔄 Cache miss, executing")
    result = await func(ctx=ctx, **kwargs)
    
    # Store
    _cache[cache_key] = (result, datetime.utcnow())
    
    return result
```

**Use Cases:**
- Expensive LLM calls
- Repetitive queries
- Performance optimization

---

## 🎯 Real-World Examples

### Example 1: Research Pipeline

**Complete research workflow with search, analysis, and summarization:**

```python
@mcp.tool()
async def research_pipeline(
    query: str,
    depth: str = "standard",  # "quick", "standard", "deep"
    ctx: Context | None = None
) -> dict:
    """Multi-step research pipeline."""
    
    # Configure depth
    config = {
        "quick": {"limit": 5, "tokens": 500},
        "standard": {"limit": 10, "tokens": 1000},
        "deep": {"limit": 20, "tokens": 2000}
    }[depth]
    
    # Create pipeline
    pipeline = Pipeline(ctx)
    
    # Execute
    results = await (
        pipeline
        .add_step("search", search_r2r, query=query, limit=config["limit"])
        .add_step("analyze", analyze_with_llm, max_tokens=config["tokens"])
        .add_step("summarize", create_summary, max_tokens=300)
        .execute()
    )
    
    return {
        "query": query,
        "depth": depth,
        "summary": results["summarize"]["summary"],
        "analysis": results["analyze"]["analysis"],
        "results_count": len(results["search"]["results"])
    }
```

**Steps:**
1. **Search**: Query R2R knowledge base
2. **Analyze**: LLM analyzes search results (ctx.sample)
3. **Summarize**: Generate executive summary (ctx.sample)

**Benefits:**
- Configurable depth
- Progress tracking
- Structured output

---

### Example 2: Comparative Analysis

**Compare multiple queries side-by-side:**

```python
@mcp.tool()
async def comparative_analysis(
    queries: list[str],
    criteria: list[str] | None = None,
    ctx: Context | None = None
) -> dict:
    """Compare multiple queries."""
    
    # Search each query
    search_results = {}
    for query in queries:
        results = await search_r2r(query=query, limit=10)
        search_results[query] = results
    
    # Build comparison prompt
    comparison_text = "\n\n".join([
        f"Query: {q}\nResults: {r}"
        for q, r in search_results.items()
    ])
    
    prompt = f"""Compare these search queries and results:

{comparison_text}

Criteria: {', '.join(criteria or [])}

Provide:
1. Key similarities and differences
2. Strengths and limitations
3. Best use cases
4. Recommendation"""
    
    # Use LLM for comparison
    response = await ctx.sample(
        messages=prompt,
        system_prompt="You are an expert analyst specializing in comparative analysis.",
        temperature=0.4,
        max_tokens=2000
    )
    
    return {
        "queries": queries,
        "comparison": response.text,
        "criteria": criteria
    }
```

**Features:**
- Multi-query processing
- Structured comparison
- Criteria-based analysis

---

### Example 3: Structured Data Extraction

**Extract structured information from documents:**

```python
@mcp.tool()
async def extract_structured_data(
    document_id: str,
    schema: dict,
    ctx: Context | None = None
) -> dict:
    """Extract data according to schema."""
    
    # Fetch document
    document = await get_document(document_id)
    
    # Build extraction prompt
    prompt = f"""Extract information from this document according to the schema.
Return ONLY valid JSON matching the schema.

Document:
{document["content"]}

Schema:
{json.dumps(schema, indent=2)}

JSON:"""
    
    # Use LLM for extraction
    response = await ctx.sample(
        messages=prompt,
        temperature=0.2,  # Very low for structured output
        max_tokens=2000
    )
    
    # Parse JSON
    try:
        extracted = json.loads(response.text)
    except json.JSONDecodeError:
        extracted = {"raw": response.text, "error": "Parse failed"}
    
    return {
        "document_id": document_id,
        "schema": schema,
        "extracted_data": extracted
    }
```

**Use Cases:**
- Data migration
- Information extraction
- Schema validation

---

### Example 4: Question Generation

**Generate follow-up questions for exploration:**

```python
@mcp.tool()
async def generate_followup_questions(
    initial_query: str,
    num_questions: int = 5,
    ctx: Context | None = None
) -> dict:
    """Generate intelligent follow-up questions."""
    
    prompt = f"""Based on the query: "{initial_query}"

Generate {num_questions} insightful follow-up questions.

Questions should:
1. Build on the initial query
2. Cover different aspects
3. Be specific and answerable
4. Progress from basic to advanced

Format as numbered list."""
    
    response = await ctx.sample(
        messages=prompt,
        system_prompt="You are an expert at generating insightful questions.",
        temperature=0.7,  # Higher for creativity
        max_tokens=800
    )
    
    # Parse questions
    questions = [
        line.strip()
        for line in response.text.split('\n')
        if line.strip() and line.strip()[0].isdigit()
    ]
    
    return {
        "initial_query": initial_query,
        "follow_up_questions": questions,
        "count": len(questions)
    }
```

**Use Cases:**
- Research guidance
- Topic exploration
- Learning paths

---

## 🎓 Best Practices

### ctx.sample Best Practices

1. **Temperature Selection**
   - Analysis/Code: 0.0-0.3
   - General tasks: 0.4-0.7
   - Creative work: 0.8-1.0

2. **Token Management**
   - Short answers: 100-300 tokens
   - Detailed responses: 500-1000 tokens
   - Long-form content: 1500-3000 tokens

3. **System Prompts**
   - Define role clearly
   - Specify expertise level
   - Include output format instructions

4. **Error Handling**
   - Always wrap in try-except
   - Implement retry logic
   - Have fallback strategies

5. **Context Logging**
   ```python
   await ctx.info("Starting operation")
   await ctx.debug("Internal details")
   await ctx.error("Error occurred")
   ```

### Pipeline Best Practices

1. **Step Design**
   - Single responsibility per step
   - Clear input/output contracts
   - Independent execution when possible

2. **Progress Tracking**
   ```python
   await ctx.report_progress(current, total)
   ```

3. **Error Recovery**
   - Graceful degradation
   - Partial results on failure
   - Comprehensive error messages

4. **Performance**
   - Parallel processing when possible
   - Caching for repeated operations
   - Conditional execution to skip unnecessary work

5. **Testing**
   ```python
   # Test individual steps
   result = await step_func(ctx=mock_ctx, **test_kwargs)
   assert result["status"] == "success"
   
   # Test full pipeline
   pipeline = Pipeline(mock_ctx)
   results = await pipeline.execute()
   assert "search" in results
   assert "analyze" in results
   ```

---

## 📊 Performance Considerations

### ctx.sample Performance

| Factor | Impact | Recommendation |
|--------|--------|----------------|
| **Temperature** | Higher = slower | Use lowest acceptable |
| **Max Tokens** | Proportional | Request only what needed |
| **Model** | Varies greatly | Choose appropriate model |
| **Prompt Length** | Slight impact | Keep prompts focused |

### Pipeline Performance

| Pattern | Speed | Use Case |
|---------|-------|----------|
| **Linear** | Slowest | Sequential dependencies |
| **Parallel** | Fastest | Independent operations |
| **Conditional** | Variable | Dynamic workflows |
| **Cached** | Fast (hits) | Repetitive operations |

---

## 🔗 Integration with R2R

### Pattern: R2R Search + LLM Analysis

```python
async def search_and_analyze(query: str, ctx: Context) -> dict:
    """Search R2R and analyze with LLM."""
    
    # 1. Search R2R
    search_response = await _client.post(
        f"{_r2r_base_url}/v3/retrieval/search",
        json={"query": query, "search_settings": {"limit": 10}}
    )
    results = search_response.json()
    
    # 2. Format for LLM
    results_text = "\n\n".join([
        f"Result {i+1}: {r['text']}"
        for i, r in enumerate(results["chunk_search_results"])
    ])
    
    # 3. Analyze with LLM
    analysis = await ctx.sample(
        messages=f"Analyze these search results:\n\n{results_text}",
        temperature=0.4,
        max_tokens=1500
    )
    
    return {
        "search_results": results,
        "analysis": analysis.text
    }
```

---

## 📝 Summary

### Key Takeaways

1. **ctx.sample enables AI-powered tools**
   - Request LLM completions
   - Configure temperature, tokens, system prompts
   - Handle responses and errors

2. **Pipelines compose complex workflows**
   - Chain multiple operations
   - Pass results between steps
   - Track progress and handle errors

3. **Patterns for every use case**
   - Linear for sequential processing
   - Conditional for dynamic workflows
   - Parallel for batch operations
   - Cached for performance

4. **Production-ready features**
   - Retry logic
   - Fallback strategies
   - Progress reporting
   - Error recovery

---

## 🔗 References

- **R2R RAG Analysis**: 4 queries with 20 sources each
- **FastMCP Documentation**: https://gofastmcp.com
- **Context API**: https://gofastmcp.com/servers/context
- **Sampling**: https://gofastmcp.com/servers/sampling
- **R2R API**: https://r2r-docs.sciphi.ai

---

## 📦 Code Location

- **Pipelines Module**: `src/pipelines.py` (600+ lines)
- **Integration**: `src/server.py` (4 pipeline-based tools)
- **Examples**: See this document

**Total Implementation:** ~900 lines of production-ready pipeline patterns

