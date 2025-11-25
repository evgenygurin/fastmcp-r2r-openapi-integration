# R2R MCP Server - Usage Examples

Practical examples demonstrating all features of the R2R MCP server, including auto-generated tools, custom resources, prompts, and pipeline-based tools.

---

## 🚀 Quick Start

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "r2r": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/fastapi-r2r-openapi-integration",
        "run",
        "python",
        "-m",
        "src.server"
      ],
      "env": {
        "R2R_BASE_URL": "http://localhost:7272",
        "R2R_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

---

## 📁 Resource Examples

### Static Resources

**Get Server Information:**
```
User: Show me the server info
Claude: [Reads r2r://server/info]

{
  "server": {
    "name": "R2R MCP Server",
    "version": "1.0.0"
  },
  "configuration": {
    "base_url": "http://localhost:7272",
    "auth_configured": true
  },
  "openapi": {
    "total_endpoints": 81
  }
}
```

**Get Route Mappings:**
```
User: How are routes mapped?
Claude: [Reads r2r://server/routes]

Shows route mapping rules and examples.
```

---

### Resource Templates

**Get Document Details:**
```
User: Show document abc-123-def
Claude: [Reads r2r://documents/abc-123-def]

{
  "id": "abc-123-def",
  "metadata": {...},
  "status": "success",
  "created_at": "2025-11-25T10:00:00"
}
```

**Get Collection Summary:**
```
User: Summarize collection xyz-789
Claude: [Reads r2r://collections/xyz-789/summary]

{
  "collection_id": "xyz-789",
  "collection_info": {...},
  "document_count": 42,
  "fetched_at": "2025-11-25T12:00:00"
}
```

**Search with Parameters:**
```
User: Search for "machine learning" limited to 20 results
Claude: [Reads r2r://search/results/machine learning?limit=20]

{
  "query": "machine learning",
  "limit": 20,
  "results": {...},
  "searched_at": "2025-11-25T12:00:00"
}
```

---

## 💬 Prompt Examples

### RAG Query Prompt

```
User: Help me create a RAG query about quantum computing
Claude: [Uses rag_query_prompt]

Generated Prompt:
"Please answer the following question using the R2R knowledge base:

Question: What is quantum computing?

Please provide:
1. A clear, concise answer based on retrieved documents
2. Citations to specific sources
3. Confidence level (high/medium/low)"
```

**With Context:**
```
User: Ask about quantum computing focusing on cryptography applications
Claude: [Uses rag_query_prompt with context]

Generated Prompt:
"...
Question: What is quantum computing?

Additional Context: Focus on applications in cryptography
..."
```

---

### Document Analysis Prompt

**Summary Analysis:**
```
User: Generate analysis prompt for document abc-123
Claude: [Uses document_analysis_prompt with type="summary"]

"Please analyze the document with ID abc-123 and provide a summary.

Focus on:
- Main topics and themes
- Key insights and findings
- Important conclusions

Provide a concise summary (200-300 words)."
```

**Entity Extraction:**
```
User: Extract entities from document abc-123
Claude: [Uses document_analysis_prompt with type="entities"]

"Please analyze the document with ID abc-123 and extract entities.

Focus on:
- Named entities (people, organizations, locations)
- Key concepts and technical terms
- Relationships between entities

Provide a structured list of entities with descriptions."
```

**Other Analysis Types:**
- `topics` - Identify main themes
- `sentiment` - Analyze sentiment and tone

---

## 🔧 Tool Examples

### Basic Tools

**Enhanced Search:**
```
User: Search for "GraphRAG" with progress tracking
Claude: [Calls enhanced_search]

🔍 Starting enhanced search...
[Progress: ████░░░░░░ 30%] Search payload prepared
[Progress: ████████░░ 80%] API request complete
[Progress: ██████████ 100%] Results processed

✓ Found 15 results

{
  "query": "GraphRAG",
  "search_type": "hybrid",
  "result_count": 15,
  "results": {...}
}
```

**Analyze Search Results:**
```
User: Search and analyze "knowledge graphs" using AI
Claude: [Calls analyze_search_results]

🔍 Searching R2R...
✓ Found 8 results
🤖 Requesting LLM analysis...
✓ Analysis complete

Analysis:
"Key themes identified:
1. Graph construction and entity extraction
2. Relationship mapping and community detection
3. GraphRAG for enhanced retrieval

Main insights:
- Knowledge graphs improve search accuracy by 30-50%
- Community detection enables hierarchical organization
- Graph-enhanced RAG provides better context

Recommended follow-up questions:
- How to implement entity extraction?
- What algorithms are used for community detection?
- How does GraphRAG compare to standard RAG?"
```

---

### Pipeline Tools

**Research Pipeline:**

**Quick Research (1-2 minutes):**
```
User: Quick research on "FastMCP best practices"
Claude: [Calls research_pipeline with depth="quick"]

🔬 Starting research pipeline: FastMCP best practices
Analysis depth: quick

🔄 Starting pipeline with 3 steps
⚙️ Step 1: search
⚙️ Step 2: analyze  
🤖 Analyzing results with LLM...
⚙️ Step 3: summarize
📝 Creating summary...

✅ Research pipeline complete

{
  "query": "FastMCP best practices",
  "analysis_depth": "quick",
  "summary": "FastMCP best practices include...",
  "full_analysis": "Detailed analysis...",
  "search_results_count": 5
}
```

**Deep Research (5-10 minutes):**
```
User: Deep research on "R2R knowledge graphs"
Claude: [Calls research_pipeline with depth="deep"]

...processes with 20 search results...
...more detailed LLM analysis (2000 tokens)...

Result includes comprehensive summary and full analysis.
```

---

**Comparative Analysis:**

```
User: Compare "RAG vs fine-tuning" and "RAG vs prompt engineering"
Claude: [Calls comparative_analysis]

🔍 Comparative analysis of 2 queries
Searching: RAG vs fine-tuning
Searching: RAG vs prompt engineering
🤖 Generating comparative analysis...

✅ Comparative analysis complete

{
  "queries": [
    "RAG vs fine-tuning",
    "RAG vs prompt engineering"
  ],
  "comparison": "
    Key Similarities:
    - Both enhance LLM capabilities
    - Both reduce hallucinations
    
    Key Differences:
    - RAG uses retrieval, fine-tuning modifies weights
    - RAG is dynamic, fine-tuning is static
    
    Best Use Cases:
    - RAG: Frequently updated information
    - Fine-tuning: Specialized domain knowledge
    
    Recommendation:
    Use RAG for dynamic knowledge bases,
    fine-tuning for specific behavior patterns
  "
}
```

**With Criteria:**
```
User: Compare those focusing on cost, accuracy, and ease of implementation
Claude: [Calls comparative_analysis with criteria]

...includes analysis based on specified criteria...
```

---

**Extract Structured Data:**

```
User: Extract title, authors, and key findings from document abc-123
Claude: [Calls extract_structured_data]

📄 Extracting structured data from document abc-123
🔍 Analyzing document with schema...

✅ Extraction complete

{
  "document_id": "abc-123",
  "schema": {
    "title": "string",
    "authors": ["string"],
    "key_findings": ["string"],
    "date": "YYYY-MM-DD"
  },
  "extracted_data": {
    "title": "Advances in Quantum Computing",
    "authors": ["Dr. Smith", "Dr. Jones"],
    "key_findings": [
      "Quantum algorithms show 100x speedup",
      "Error correction breakthrough achieved"
    ],
    "date": "2024-01-15"
  }
}
```

**Custom Schema:**
```json
{
  "summary": "string (max 200 chars)",
  "topics": ["string"],
  "sentiment": "positive|neutral|negative",
  "technical_level": "beginner|intermediate|advanced"
}
```

---

**Generate Follow-up Questions:**

```
User: What questions should I ask to explore "GraphRAG" deeper?
Claude: [Calls generate_followup_questions]

💡 Generating 5 follow-up questions

✅ Questions generated

{
  "initial_query": "What is GraphRAG?",
  "follow_up_questions": [
    "1. How does GraphRAG differ from standard RAG approaches?",
    "2. What are the key components of a knowledge graph in GraphRAG?",
    "3. How is community detection used in GraphRAG?",
    "4. What are the performance implications of using GraphRAG?",
    "5. How do you implement entity extraction for GraphRAG?"
  ],
  "count": 5
}
```

**More Questions:**
```
User: Generate 10 follow-up questions about "R2R deployment"
Claude: [Calls generate_followup_questions with num_questions=10]

...generates 10 progressive questions from basic to advanced...
```

---

## 🎯 Advanced Use Cases

### Use Case 1: Document Research Workflow

```
User: I need to research "FastMCP middleware patterns"

Step 1: Initial search
Claude: [Calls enhanced_search]
       "Found 12 results about middleware patterns"

Step 2: Deep analysis
User: Do a deep research pipeline on this
Claude: [Calls research_pipeline with depth="deep"]
       "Comprehensive analysis complete with:
        - 20 search results analyzed
        - Key patterns identified
        - Implementation recommendations
        - Executive summary"

Step 3: Follow-up exploration  
User: What questions should I ask next?
Claude: [Calls generate_followup_questions]
       "Generated 5 insightful follow-up questions"

Step 4: Comparative analysis
User: Compare "error handling middleware" vs "rate limiting middleware"
Claude: [Calls comparative_analysis]
       "Side-by-side comparison with use cases and recommendations"
```

---

### Use Case 2: Document Analysis

```
User: Analyze my research paper

Step 1: Get document details
Claude: [Reads r2r://documents/{doc_id}]
       "Document uploaded successfully"

Step 2: Extract structured info
User: Extract title, authors, abstract, and key findings
Claude: [Calls extract_structured_data with schema]
       "Extracted structured data in JSON format"

Step 3: Generate analysis  
User: Analyze the paper for main topics
Claude: [Uses document_analysis_prompt with type="topics"]
       "Generated analysis focusing on main themes"

Step 4: Get follow-up questions
User: What should I explore further?
Claude: [Calls generate_followup_questions]
       "Generated 8 follow-up questions based on content"
```

---

### Use Case 3: Multi-Query Research

```
User: I'm comparing different AI approaches

Step 1: Define queries
User: Compare "RAG", "fine-tuning", and "prompt engineering"
Claude: [Calls comparative_analysis with 3 queries]
       "Comprehensive comparison:
        - Similarities and differences
        - Strengths and limitations
        - Best use cases for each
        - Overall recommendations"

Step 2: Deep dive into winner
User: Do deep research on RAG
Claude: [Calls research_pipeline with depth="deep"]
       "In-depth RAG analysis with 20 sources"

Step 3: Practical implementation
User: Search for RAG implementation examples
Claude: [Calls enhanced_search with specific query]
       "Found 18 implementation examples"
```

---

## 🔬 Pipeline Pattern Examples

### Linear Pipeline Pattern

```python
# Example: Search → Analyze → Summarize
from src.pipelines import Pipeline

async def my_research(query: str, ctx: Context):
    pipeline = Pipeline(ctx)
    
    results = await (
        pipeline
        .add_step("search", search_func, query=query)
        .add_step("analyze", analyze_func)
        .add_step("summarize", summarize_func)
        .execute()
    )
    
    return results
```

**Console Output:**
```
🔄 Starting pipeline with 3 steps
⚙️ Step 1: search
⚙️ Step 2: analyze
🤖 Analyzing results with LLM...
⚙️ Step 3: summarize
📝 Creating summary...
✅ Pipeline complete: 3 results
```

---

### Conditional Pipeline Pattern

```python
# Example: Search → (Analyze if >10 results) → Summarize
from src.pipelines import ConditionalPipeline

async def adaptive_research(query: str, ctx: Context):
    pipeline = ConditionalPipeline(ctx)
    
    results = await (
        pipeline
        .add_step("search", search_func, query=query)
        .add_step(
            "detailed_analysis",
            analyze_func,
            condition=lambda r: len(r["search"]["results"]) > 10
        )
        .add_step("summarize", summarize_func)
        .execute()
    )
    
    return results
```

**Console Output (many results):**
```
🔄 Starting conditional pipeline
⚙️ Executing step: search
⚙️ Executing step: detailed_analysis  # Condition met
⚙️ Executing step: summarize
```

**Console Output (few results):**
```
🔄 Starting conditional pipeline
⚙️ Executing step: search
⏭️ Skipping step detailed_analysis (condition not met)
⚙️ Executing step: summarize
```

---

### Parallel Processing Pattern

```python
# Example: Analyze multiple documents simultaneously
from src.pipelines import pipeline_parallel_analysis

async def batch_analyze(documents: list[dict], ctx: Context):
    results = await pipeline_parallel_analysis(documents, ctx)
    return results
```

**Usage:**
```python
docs = [
    {"id": "1", "text": "Document 1 content..."},
    {"id": "2", "text": "Document 2 content..."},
    {"id": "3", "text": "Document 3 content..."},
]

results = await batch_analyze(docs, ctx)
# Processes all 3 documents in parallel
```

---

### Cached Pipeline Pattern

```python
# Example: Cache expensive LLM calls
from src.pipelines import cached_pipeline_step

async def cached_analysis(query: str, ctx: Context):
    result = await cached_pipeline_step(
        cache_key=f"analysis:{query}",
        func=expensive_llm_analysis,
        ttl_seconds=600,  # Cache for 10 minutes
        ctx=ctx,
        query=query
    )
    
    return result
```

**First Call:**
```
🔄 Executing (cache miss): analysis:machine learning
...performs LLM analysis...
💾 Cached result: analysis:machine learning
```

**Subsequent Calls (within 10 min):**
```
📦 Cache hit: analysis:machine learning (age: 45.3s)
```

---

### Fallback Pattern

```python
# Example: Try expensive LLM, fallback to rule-based
from src.pipelines import pipeline_with_fallback

async def robust_analysis(data: str, ctx: Context):
    result = await pipeline_with_fallback(
        primary_func=llm_analysis,      # Expensive but accurate
        fallback_func=rule_based_analysis,  # Fast but simpler
        ctx=ctx,
        data=data
    )
    
    return result
```

**Successful Primary:**
```
⚡ Attempting primary operation
✓ Primary operation successful
```

**Fallback on Error:**
```
⚡ Attempting primary operation
❌ Primary operation failed: TimeoutError
🔄 Falling back to alternative
✓ Fallback operation successful
```

---

## 🎯 Real-World Workflows

### Workflow 1: Research Paper Analysis

```
# Step 1: Upload document
User: I uploaded my research paper
Claude: [Uses r2r://documents/{id}]
       "Document processed successfully"

# Step 2: Extract metadata
User: Extract the title, authors, abstract, and keywords
Claude: [Calls extract_structured_data]
       Schema: {title, authors, abstract, keywords}
       "Extracted structured metadata"

# Step 3: Deep analysis
User: Do a deep research pipeline on the content
Claude: [Calls research_pipeline with depth="deep"]
       "Analyzed 20 relevant sources
        Summary: [executive summary]
        Full analysis: [detailed insights]"

# Step 4: Generate questions
User: What aspects should I explore further?
Claude: [Calls generate_followup_questions]
       "Generated 8 follow-up questions:
        1. How does your methodology compare to...
        2. What are the limitations of...
        3. Could you elaborate on...
        [etc.]"

# Step 5: Comparative analysis
User: Compare my approach with standard methods
Claude: [Calls comparative_analysis]
       "Comparison of your approach vs standard:
        [detailed comparison]"
```

---

### Workflow 2: Knowledge Base Exploration

```
# Step 1: Search
User: Search for information about "vector databases"
Claude: [Calls enhanced_search]
       "Found 24 results"

# Step 2: Analyze
User: Analyze these results
Claude: [Calls analyze_search_results]
       "AI Analysis:
        - Main concept: efficient similarity search
        - Key technologies: HNSW, IVFFlat
        - Use cases: semantic search, RAG"

# Step 3: Deep dive
User: Research the HNSW algorithm in depth
Claude: [Calls research_pipeline with depth="deep"]
       "Comprehensive HNSW research complete"

# Step 4: Compare approaches
User: Compare HNSW vs IVFFlat
Claude: [Calls comparative_analysis]
       "Side-by-side comparison with recommendations"
```

---

### Workflow 3: Multi-Document Processing

```
# Using pipelines for batch operations

# Step 1: Get collection
User: Show collection summary for my-docs
Claude: [Reads r2r://collections/my-docs/summary]
       "Collection: my-docs
        Documents: 15"

# Step 2: Batch extraction
User: Extract key themes from all documents
Claude: [Uses pipeline_parallel_analysis]
       "Processing 15 documents in parallel...
        [Progress: 15/15]
        ✓ Completed 15/15 items"

# Step 3: Synthesize findings  
User: Synthesize the findings across all documents
Claude: [Uses ctx.sample with all extracted themes]
       "Synthesis:
        Common themes: [...]
        Trends: [...]
        Insights: [...]"
```

---

## 📊 Feature Comparison

| Feature | Basic Tool | Pipeline Tool | Benefit |
|---------|-----------|---------------|---------|
| **Search** | `enhanced_search` | `research_pipeline` | Multi-step analysis |
| **Analysis** | `analyze_search_results` | LLM sampling pattern | Customizable prompts |
| **Comparison** | N/A | `comparative_analysis` | Side-by-side insights |
| **Extraction** | N/A | `extract_structured_data` | Schema-driven |
| **Exploration** | N/A | `generate_followup_questions` | Guided discovery |

---

## 🎓 Tips and Tricks

### Tip 1: Use Appropriate Analysis Depth

```
Quick (1-2 min):   Simple questions, quick overviews
Standard (3-5 min): Most research tasks, balanced depth
Deep (5-10 min):   Complex topics, comprehensive analysis
```

### Tip 2: Leverage Follow-up Questions

```
After any search or analysis:
→ Call generate_followup_questions
→ Explore suggested topics
→ Build deeper understanding
```

### Tip 3: Combine Resources and Tools

```
1. Get document → r2r://documents/{id}
2. Extract data → extract_structured_data
3. Analyze → research_pipeline
4. Compare → comparative_analysis
```

### Tip 4: Use Caching for Repeated Queries

```
Same query within 10 minutes → instant cache hit
Different parameters → new request
```

### Tip 5: Optimize with Criteria

```
Comparative analysis with specific criteria:
→ More focused comparison
→ Better recommendations
→ Actionable insights
```

---

## 🔗 Component Summary

### Auto-Generated (114 routes)
- All R2R API endpoints as MCP components
- GET → Resources/Templates
- POST/PUT/DELETE → Tools

### Custom Static (2 resources)
- `r2r://server/info`
- `r2r://server/routes`

### Custom Templates (3 resources)
- `r2r://documents/{id}`
- `r2r://collections/{id}/summary`
- `r2r://search/results/{query}{?limit}`

### Prompts (2)
- `rag_query_prompt`
- `document_analysis_prompt`

### Tools (6)
**Basic (2):**
- `enhanced_search`
- `analyze_search_results`

**Pipelines (4):**
- `research_pipeline`
- `comparative_analysis`
- `extract_structured_data`
- `generate_followup_questions`

### Pipelines Module (13 components)
**Sampling Patterns (5):**
- Basic generation
- System prompts
- Structured output
- Multi-turn conversation
- Retry logic

**Pipeline Classes (2):**
- Pipeline (linear)
- ConditionalPipeline

**Pipeline Steps (3):**
- Search
- Analyze
- Summarize

**Utilities (3):**
- Fallback
- Caching
- Parallel processing

---

## 📈 Total Capabilities

```
Auto-Generated:  114 routes
Custom:          13 components  
Pipelines:       13 reusable patterns
Documentation:   3600+ lines

Total:           ~140 MCP components + patterns
```

---

## 🚀 Next Steps

1. **Explore GraphRAG** (Priority 1 from ROADMAP.md)
   - Entity extraction
   - Relationship detection
   - Community building
   - Graph-enhanced search

2. **Add Agent Features** (Priority 2)
   - Conversational agent
   - Research mode
   - Extended thinking

3. **Production Features** (Priority 3)
   - Error handling middleware
   - Rate limiting
   - Monitoring

See `docs/ROADMAP.md` for complete implementation plan.

---

## 📚 References

- **Enhanced Features**: `docs/ENHANCED_FEATURES.md`
- **Development Roadmap**: `docs/ROADMAP.md`
- **Pipeline Patterns**: `docs/PIPELINES.md`
- **FastMCP Docs**: https://gofastmcp.com
- **R2R Docs**: https://r2r-docs.sciphi.ai
