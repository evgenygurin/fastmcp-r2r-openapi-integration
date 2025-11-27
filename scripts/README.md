# R2R Standalone Scripts

Example scripts demonstrating **R2RClient** usage for standalone operations, batch processing, and administration tasks.

## ⚠️ Important: When to Use These Scripts

### ✅ **Use R2RClient** (these scripts) for:
- Batch document ingestion
- Data migration
- One-time operations
- Administration tasks
- Local development utilities
- Testing

### ❌ **DON'T use R2RClient** for:
- FastMCP MCP servers (serverless incompatible)
- Production MCP endpoints
- Real-time LLM integrations

**For FastMCP servers:** Use `httpx + DynamicBearerAuth + R2RTypedClient` (see `src/server.py` and `src/r2r_typed.py`)

---

## 📋 Available Scripts

### 1. `batch_ingest.py` - Batch Document Upload

Upload multiple documents to R2R in batch mode.

**Usage:**
```bash
# Upload all PDFs from directory
python scripts/batch_ingest.py /path/to/documents --pattern "*.pdf"

# Upload to specific collection
python scripts/batch_ingest.py /path/to/documents --collection <collection_id>

# Dry run (list files without uploading)
python scripts/batch_ingest.py /path/to/documents --dry-run

# Custom pattern
python scripts/batch_ingest.py /path/to/documents --pattern "*.txt"
```

**Example:**
```bash
$ python scripts/batch_ingest.py ./papers --pattern "*.pdf"
✓ Connected to R2R at http://localhost:7272
📁 Found 5 files matching '*.pdf'

[1/5] Uploading paper1.pdf... ✓ doc_uuid_1
[2/5] Uploading paper2.pdf... ✓ doc_uuid_2
[3/5] Uploading paper3.pdf... ✓ doc_uuid_3
[4/5] Uploading paper4.pdf... ✓ doc_uuid_4
[5/5] Uploading paper5.pdf... ✓ doc_uuid_5

✓ Successfully uploaded 5/5 documents
```

---

### 2. `search_cli.py` - Interactive Search CLI

Command-line interface for searching R2R knowledge base and RAG queries.

**Usage:**
```bash
# One-shot search
python scripts/search_cli.py "machine learning" --limit 5

# RAG query
python scripts/search_cli.py "What is RAG?" --rag --max-tokens 2000

# JSON output
python scripts/search_cli.py "AI" --json

# Interactive mode
python scripts/search_cli.py --interactive
```

**Interactive Mode:**
```bash
$ python scripts/search_cli.py -i
R2R Interactive Search
================================================================================
Commands:
  search <query>  - Search knowledge base
  rag <query>     - Ask a question (RAG)
  quit / exit     - Exit
================================================================================

> search machine learning
🔍 Searching for: 'machine learning'

✓ Found 3 results:

================================================================================
Result 1 | Score: 0.923 | Document: doc_1234...
================================================================================
Machine learning is a subset of artificial intelligence that enables
computers to learn from data without being explicitly programmed...

> rag What is deep learning?
💬 Asking: 'What is deep learning?'

Answer:
================================================================================
Deep learning is a subset of machine learning that uses artificial
neural networks with multiple layers (hence "deep") to progressively
extract higher-level features from raw input...
================================================================================

Sources (2):
  1. Deep learning architectures consist of multiple processing layers...
  2. The term "deep learning" was coined in the 1980s...

> quit
Goodbye!
```

---

## 🔧 Setup

### Prerequisites

```bash
# Install R2R SDK
pip install r2r

# Or with uv
uv pip install r2r
```

### Configuration

Create `.env` file in project root:

```env
R2R_BASE_URL=http://localhost:7272
R2R_API_KEY=your_api_key_here
```

### Make Scripts Executable (optional)

```bash
chmod +x scripts/*.py
```

---

## 📖 R2RClient API Reference

### Common Operations

#### Search

```python
from r2r import R2RClient

client = R2RClient(base_url="http://localhost:7272")

results = client.retrieval.search(
    query="machine learning",
    limit=10
)
```

#### RAG

```python
answer = client.retrieval.rag(
    query="What is RAG?",
    max_tokens=2000
)
print(answer["answer"])
```

#### Documents

```python
# Upload
doc = client.documents.create(file_path="paper.pdf")

# Get metadata
metadata = client.documents.get(document_id="uuid")

# Delete
client.documents.delete(document_id="uuid")
```

#### Collections

```python
# Create
collection = client.collections.create(
    name="Research Papers",
    description="AI research papers"
)

# Add document
client.collections.add_document(
    collection_id=collection["collection_id"],
    document_id="doc_uuid"
)

# List
collections = client.collections.list()
```

---

## 🎯 Use Cases

### 1. Initial Data Migration

```bash
# Migrate existing documents to R2R
python scripts/batch_ingest.py ./old_documents --pattern "*.pdf"
```

### 2. Periodic Batch Updates

```bash
# Cron job for nightly document uploads
0 2 * * * cd /path/to/project && python scripts/batch_ingest.py /data/new_docs
```

### 3. Manual Testing

```bash
# Quick search without starting MCP server
python scripts/search_cli.py "test query" --limit 3
```

### 4. Bulk Collection Management

```python
#!/usr/bin/env python3
"""Create collections from directory structure."""
from r2r import R2RClient
from pathlib import Path

client = R2RClient()

for category_dir in Path("./data").iterdir():
    if category_dir.is_dir():
        collection = client.collections.create(
            name=category_dir.name,
            description=f"Documents from {category_dir.name}"
        )

        print(f"Created collection: {collection['name']}")
```

---

## ⚙️ Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `R2R_BASE_URL` | Yes | `http://localhost:7272` | R2R API base URL |
| `R2R_API_KEY` | Yes | - | API key for authentication |

---

## 🚀 Next Steps

### For Production MCP Servers

If you need to integrate R2R with FastMCP for LLM applications:

1. Use `src/server.py` as template (httpx + DynamicBearerAuth)
2. Use `src/r2r_typed.py` for type-safe wrappers
3. See `docs/R2R_CLIENT_ANALYSIS.md` for detailed comparison

### For Advanced Scripting

Check out:
- `docs/R2R_FASTMCP_INTEGRATION.md` - Integration patterns
- `docs/r2r/README.md` - R2R documentation
- `.claude/scripts/` - Bash CLI tools

---

## 📝 Notes

- These scripts use R2RClient directly (no DynamicBearerAuth)
- API key is read at module import time (not request time)
- **Not compatible with serverless environments** (FastMCP Cloud, AWS Lambda)
- For serverless, use typed wrappers in `src/r2r_typed.py`

---

**Questions?** See `docs/R2R_CLIENT_ANALYSIS.md` for detailed analysis of R2RClient vs httpx approaches.
