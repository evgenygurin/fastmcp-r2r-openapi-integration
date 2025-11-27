"""FastMCP Pipelines - Advanced ctx.sample patterns and tool composition.

This module demonstrates advanced FastMCP patterns based on R2R RAG analysis:
- ctx.sample for LLM-powered operations
- Pipeline patterns for tool composition
- Middleware chaining
- Multi-step workflows

Based on R2R RAG queries with 20 sources per query covering:
- FastMCP Context sampling
- Pipeline composition patterns
- Middleware architecture
- Tool transformation
"""

import asyncio
import json
from collections.abc import Callable
from datetime import datetime
from typing import Any

from fastmcp import Context

# ============================================================================
# PATTERN 1: Advanced ctx.sample Usage
# ============================================================================


async def sample_basic_generation(ctx: Context, prompt: str) -> str:
    """Basic LLM sampling - simple text generation.

    Example:
        result = await sample_basic_generation(ctx, "Explain quantum computing")
    """
    response = await ctx.sample(prompt)
    return response.text


async def sample_with_system_prompt(
    ctx: Context,
    user_message: str,
    system_role: str = "expert data analyst"
) -> str:
    """Sampling with system prompt for role-based responses.

    Example:
        result = await sample_with_system_prompt(
            ctx,
            "Analyze this data: [...]",
            system_role="statistician"
        )
    """
    response = await ctx.sample(
        messages=user_message,
        system_prompt=f"You are an {system_role}. Provide detailed, accurate analysis.",
        temperature=0.3,  # Lower for more focused responses
        max_tokens=1000
    )
    return response.text


async def sample_structured_output(
    ctx: Context,
    data: dict,
    output_format: str = "json"
) -> dict:
    """Request structured output from LLM (JSON, markdown, etc.).

    Example:
        result = await sample_structured_output(
            ctx,
            {"items": [1, 2, 3]},
            output_format="json"
        )
    """
    prompt = f"""Analyze the following data and return results in {output_format} format:

Data: {json.dumps(data, indent=2)}

Please structure your response as valid {output_format}."""

    response = await ctx.sample(
        messages=prompt,
        temperature=0.2,  # Very low for structured output
        max_tokens=2000
    )

    # Parse JSON if requested
    if output_format == "json":
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            # Fallback: return as-is
            return {"raw_response": response.text}

    return {"response": response.text}


async def sample_multi_turn_conversation(
    ctx: Context,
    conversation_history: list[dict]
) -> str:
    """Multi-turn conversation using message history.

    Args:
        conversation_history: List of {"role": "user"|"assistant", "content": "..."}

    Example:
        history = [
            {"role": "user", "content": "What is RAG?"},
            {"role": "assistant", "content": "RAG stands for..."},
            {"role": "user", "content": "How does it work?"}
        ]
        result = await sample_multi_turn_conversation(ctx, history)
    """
    # Convert to sampling messages format
    messages = [msg["content"] for msg in conversation_history]

    response = await ctx.sample(
        messages=messages,
        temperature=0.7,
        max_tokens=1500
    )

    return response.text


async def sample_with_retry(
    ctx: Context,
    prompt: str,
    max_retries: int = 3
) -> str:
    """Sampling with retry logic for robustness.

    Example:
        result = await sample_with_retry(ctx, "Complex analysis task")
    """
    for attempt in range(max_retries):
        try:
            await ctx.debug(f"Sampling attempt {attempt + 1}/{max_retries}")

            response = await ctx.sample(
                messages=prompt,
                temperature=0.5,
                max_tokens=1000
            )

            await ctx.debug(f"✓ Sampling successful on attempt {attempt + 1}")
            return response.text

        except Exception as e:
            await ctx.error(f"Sampling failed on attempt {attempt + 1}: {e}")

            if attempt == max_retries - 1:
                raise

            # Exponential backoff
            await asyncio.sleep(2 ** attempt)

    return ""  # Should never reach here


# ============================================================================
# PATTERN 2: Pipeline Composition
# ============================================================================


class Pipeline:
    """Pipeline for chaining multiple operations with context.

    Example:
        pipeline = Pipeline(ctx)
        result = await (
            pipeline
            .add_step("search", search_documents, query="AI")
            .add_step("analyze", analyze_results)
            .add_step("summarize", summarize_findings)
            .execute()
        )
    """

    def __init__(self, ctx: Context | None = None):
        self.ctx = ctx
        self.steps: list[dict] = []
        self.results: dict[str, Any] = {}

    def add_step(
        self,
        name: str,
        func: Callable,
        **kwargs
    ) -> "Pipeline":
        """Add a step to the pipeline.

        Args:
            name: Step identifier
            func: Async function to execute
            **kwargs: Arguments to pass to function
        """
        self.steps.append({
            "name": name,
            "func": func,
            "kwargs": kwargs
        })
        return self

    async def execute(self) -> dict[str, Any]:
        """Execute all pipeline steps in order.

        Returns:
            Dict with results from each step
        """
        if self.ctx:
            await self.ctx.info(f"🔄 Starting pipeline with {len(self.steps)} steps")
            await self.ctx.report_progress(0, len(self.steps))

        for idx, step in enumerate(self.steps):
            name = step["name"]
            func = step["func"]
            kwargs = step["kwargs"]

            if self.ctx:
                await self.ctx.info(f"⚙️  Step {idx + 1}: {name}")

            try:
                # Pass context if function accepts it
                if "ctx" in func.__code__.co_varnames:
                    kwargs["ctx"] = self.ctx

                # Pass previous results
                kwargs["previous_results"] = self.results

                # Execute step
                result = await func(**kwargs)
                self.results[name] = result

                if self.ctx:
                    await self.ctx.report_progress(idx + 1, len(self.steps))
                    await self.ctx.debug(f"✓ Step {name} complete")

            except Exception as e:
                if self.ctx:
                    await self.ctx.error(f"❌ Step {name} failed: {e}")
                raise

        if self.ctx:
            await self.ctx.info(f"✅ Pipeline complete: {len(self.results)} results")

        return self.results


# ============================================================================
# PATTERN 3: LLM-Powered Pipeline Steps
# ============================================================================


async def pipeline_search_and_analyze(
    query: str,
    ctx: Context | None = None,
    previous_results: dict | None = None
) -> dict:
    """Pipeline step: Search documents.

    This would call R2R search API in real implementation.
    """
    if ctx:
        await ctx.info(f"🔍 Searching: {query}")

    # Simulate search results
    results = {
        "query": query,
        "results": [
            {"id": "1", "text": "Sample result 1"},
            {"id": "2", "text": "Sample result 2"},
        ]
    }

    return results


async def pipeline_llm_analyze(
    ctx: Context | None = None,
    previous_results: dict | None = None
) -> dict:
    """Pipeline step: Analyze search results using LLM sampling.

    Uses ctx.sample to perform AI analysis of previous step results.
    """
    if not ctx:
        raise ValueError("Context required for LLM analysis")

    if not previous_results or "search" not in previous_results:
        raise ValueError("No search results to analyze")

    search_results = previous_results["search"]

    await ctx.info("🤖 Analyzing results with LLM...")

    # Prepare analysis prompt
    results_text = "\n\n".join([
        f"Result {i + 1}: {r['text']}"
        for i, r in enumerate(search_results["results"])
    ])

    prompt = f"""Analyze the following search results and provide:
1. Key themes and patterns
2. Main insights
3. Recommended follow-up questions

Search Query: {search_results['query']}

Results:
{results_text}

Please provide a structured analysis."""

    # Use LLM sampling
    response = await ctx.sample(
        messages=prompt,
        system_prompt="You are an expert data analyst specializing in information synthesis.",
        temperature=0.4,
        max_tokens=1500
    )

    analysis = response.text

    await ctx.info(f"✓ Analysis complete: {len(analysis)} characters")

    return {
        "analysis": analysis,
        "timestamp": datetime.utcnow().isoformat()
    }


async def pipeline_llm_summarize(
    ctx: Context | None = None,
    previous_results: dict | None = None
) -> dict:
    """Pipeline step: Summarize analysis using LLM.

    Final step that creates executive summary from analysis.
    """
    if not ctx:
        raise ValueError("Context required for summarization")

    if not previous_results or "analyze" not in previous_results:
        raise ValueError("No analysis to summarize")

    analysis = previous_results["analyze"]["analysis"]

    await ctx.info("📝 Creating summary...")

    prompt = f"""Create a concise executive summary (2-3 sentences) of this analysis:

{analysis}

Focus on the most important insights and actionable recommendations."""

    response = await ctx.sample(
        messages=prompt,
        temperature=0.3,
        max_tokens=300
    )

    summary = response.text

    await ctx.info(f"✓ Summary created: {len(summary)} characters")

    return {
        "summary": summary,
        "full_analysis": analysis,
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================================================
# PATTERN 4: Parallel Processing Pipeline
# ============================================================================


async def pipeline_parallel_analysis(
    data: list[dict],
    ctx: Context | None = None
) -> list[dict]:
    """Process multiple items in parallel using LLM sampling.

    Example:
        items = [
            {"text": "Document 1 content..."},
            {"text": "Document 2 content..."},
        ]
        results = await pipeline_parallel_analysis(items, ctx)
    """
    if ctx:
        await ctx.info(f"🔄 Processing {len(data)} items in parallel")

    async def analyze_item(item: dict, idx: int) -> dict:
        """Analyze single item."""
        if ctx:
            await ctx.debug(f"Analyzing item {idx + 1}")

        prompt = f"Analyze this content and extract key points:\n\n{item['text']}"

        response = await ctx.sample(
            messages=prompt,
            temperature=0.3,
            max_tokens=500
        ) if ctx else None

        return {
            "id": item.get("id", idx),
            "analysis": response.text if response else "No analysis (no context)",
            "timestamp": datetime.utcnow().isoformat()
        }

    # Process all items in parallel
    tasks = [analyze_item(item, i) for i, item in enumerate(data)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out exceptions
    successful_results = [
        r for r in results
        if not isinstance(r, Exception)
    ]

    if ctx:
        await ctx.info(f"✓ Completed {len(successful_results)}/{len(data)} items")

    return successful_results


# ============================================================================
# PATTERN 5: Conditional Pipeline
# ============================================================================


class ConditionalPipeline:
    """Pipeline with conditional execution based on step results.

    Example:
        pipeline = ConditionalPipeline(ctx)
        pipeline.add_step("search", search_func)
        pipeline.add_step("analyze", analyze_func, condition=lambda r: len(r["search"]["results"]) > 0)
        results = await pipeline.execute()
    """

    def __init__(self, ctx: Context | None = None):
        self.ctx = ctx
        self.steps: list[dict] = []
        self.results: dict[str, Any] = {}

    def add_step(
        self,
        name: str,
        func: Callable,
        condition: Callable | None = None,
        **kwargs
    ) -> "ConditionalPipeline":
        """Add a conditional step.

        Args:
            name: Step identifier
            func: Function to execute
            condition: Optional function that takes results dict and returns bool
            **kwargs: Arguments for function
        """
        self.steps.append({
            "name": name,
            "func": func,
            "condition": condition,
            "kwargs": kwargs
        })
        return self

    async def execute(self) -> dict[str, Any]:
        """Execute pipeline with conditional steps."""
        if self.ctx:
            await self.ctx.info("🔄 Starting conditional pipeline")

        for step in self.steps:
            name = step["name"]
            func = step["func"]
            condition = step["condition"]
            kwargs = step["kwargs"]

            # Check condition
            if condition and not condition(self.results):
                if self.ctx:
                    await self.ctx.info(f"⏭️  Skipping step {name} (condition not met)")
                continue

            if self.ctx:
                await self.ctx.info(f"⚙️  Executing step: {name}")

            # Execute step
            if "ctx" in func.__code__.co_varnames:
                kwargs["ctx"] = self.ctx

            kwargs["previous_results"] = self.results

            result = await func(**kwargs)
            self.results[name] = result

            if self.ctx:
                await self.ctx.debug(f"✓ Step {name} complete")

        return self.results


# ============================================================================
# PATTERN 6: Error Recovery Pipeline
# ============================================================================


async def pipeline_with_fallback(
    primary_func: Callable,
    fallback_func: Callable,
    ctx: Context | None = None,
    **kwargs
) -> Any:
    """Execute function with fallback on error.

    Example:
        result = await pipeline_with_fallback(
            primary_func=expensive_llm_call,
            fallback_func=simple_rule_based,
            ctx=ctx,
            prompt="Analyze this..."
        )
    """
    try:
        if ctx:
            await ctx.info("⚡ Attempting primary operation")

        result = await primary_func(ctx=ctx, **kwargs)

        if ctx:
            await ctx.info("✓ Primary operation successful")

        return result

    except Exception as e:
        if ctx:
            await ctx.error(f"❌ Primary operation failed: {e}")
            await ctx.info("🔄 Falling back to alternative")

        try:
            result = await fallback_func(ctx=ctx, **kwargs)

            if ctx:
                await ctx.info("✓ Fallback operation successful")

            return result

        except Exception as fallback_error:
            if ctx:
                await ctx.error(f"❌ Fallback also failed: {fallback_error}")
            raise


# ============================================================================
# PATTERN 7: Caching Pipeline
# ============================================================================


_pipeline_cache: dict[str, Any] = {}


async def cached_pipeline_step(
    cache_key: str,
    func: callable,
    ttl_seconds: int = 300,
    ctx: Context | None = None,
    **kwargs
) -> Any:
    """Execute pipeline step with caching.

    Example:
        result = await cached_pipeline_step(
            cache_key="search:ai",
            func=expensive_search,
            ttl_seconds=600,
            ctx=ctx,
            query="AI"
        )
    """
    # Check cache
    if cache_key in _pipeline_cache:
        cached_result, cached_time = _pipeline_cache[cache_key]
        age = (datetime.utcnow() - cached_time).total_seconds()

        if age < ttl_seconds:
            if ctx:
                await ctx.info(f"📦 Cache hit: {cache_key} (age: {age:.1f}s)")
            return cached_result
        else:
            if ctx:
                await ctx.debug(f"🗑️  Cache expired: {cache_key}")
            del _pipeline_cache[cache_key]

    # Execute function
    if ctx:
        await ctx.info(f"🔄 Executing (cache miss): {cache_key}")

    if "ctx" in func.__code__.co_varnames:
        kwargs["ctx"] = ctx

    result = await func(**kwargs)

    # Store in cache
    _pipeline_cache[cache_key] = (result, datetime.utcnow())

    if ctx:
        await ctx.debug(f"💾 Cached result: {cache_key}")

    return result


# ============================================================================
# Example: Complete Pipeline Usage
# ============================================================================


async def example_complete_pipeline(ctx: Context) -> dict:
    """Example of a complete pipeline combining search, analysis, and summarization.

    This demonstrates the full power of pipeline composition with LLM sampling.
    """
    pipeline = Pipeline(ctx)

    result = await (
        pipeline
        .add_step("search", pipeline_search_and_analyze, query="machine learning")
        .add_step("analyze", pipeline_llm_analyze)
        .add_step("summarize", pipeline_llm_summarize)
        .execute()
    )

    return result


# Export key patterns
__all__ = [
    "ConditionalPipeline",
    # Pipeline classes
    "Pipeline",
    "cached_pipeline_step",
    # Example
    "example_complete_pipeline",
    "pipeline_llm_analyze",
    "pipeline_llm_summarize",
    "pipeline_parallel_analysis",
    # Pipeline steps
    "pipeline_search_and_analyze",
    # Utilities
    "pipeline_with_fallback",
    # Sampling patterns
    "sample_basic_generation",
    "sample_multi_turn_conversation",
    "sample_structured_output",
    "sample_with_retry",
    "sample_with_system_prompt",
]
