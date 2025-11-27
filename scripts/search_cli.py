#!/usr/bin/env python3
"""Interactive CLI for R2R search using R2RClient.

Simple command-line interface for searching and exploring R2R knowledge base.

Usage:
    python scripts/search_cli.py
    python scripts/search_cli.py "machine learning" --limit 5
"""

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from r2r import R2RClient
except ImportError:
    print("❌ R2R SDK not installed. Install with: pip install r2r")
    sys.exit(1)

load_dotenv()


def create_client() -> R2RClient:
    """Create R2RClient with credentials from environment."""
    base_url = os.getenv("R2R_BASE_URL", "http://localhost:7272")
    api_key = os.getenv("R2R_API_KEY")

    if not api_key:
        print("⚠️  Warning: R2R_API_KEY not set")

    return R2RClient(base_url=base_url, api_key=api_key)


def search(client: R2RClient, query: str, limit: int = 5, json_output: bool = False):
    """Execute search and display results."""
    try:
        print(f"🔍 Searching for: '{query}'")
        print()

        results = client.retrieval.search(query=query, limit=limit)

        if json_output:
            print(json.dumps(results, indent=2))
            return

        chunks = results.get("results", {}).get("chunk_search_results", [])

        if not chunks:
            print("❌ No results found")
            return

        print(f"✓ Found {len(chunks)} results:")
        print()

        for i, chunk in enumerate(chunks, 1):
            score = chunk.get("score", 0)
            text = chunk.get("text", "")
            doc_id = chunk.get("document_id", "N/A")

            print(f"{'=' * 80}")
            print(f"Result {i} | Score: {score:.3f} | Document: {doc_id[:8]}...")
            print(f"{'=' * 80}")
            print(text[:300])
            if len(text) > 300:
                print("...")
            print()

    except Exception as e:
        print(f"❌ Search failed: {e}")
        sys.exit(1)


def rag(client: R2RClient, query: str, max_tokens: int = 2000):
    """Execute RAG query and display answer."""
    try:
        print(f"💬 Asking: '{query}'")
        print()

        response = client.retrieval.rag(query=query, max_tokens=max_tokens)

        answer = response.get("answer", "")
        citations = response.get("citations", [])

        print("Answer:")
        print("=" * 80)
        print(answer)
        print("=" * 80)
        print()

        if citations:
            print(f"Sources ({len(citations)}):")
            for i, citation in enumerate(citations[:3], 1):
                text = citation.get("text", "")[:100]
                print(f"  {i}. {text}...")
            print()

    except Exception as e:
        print(f"❌ RAG query failed: {e}")
        sys.exit(1)


def interactive_mode(client: R2RClient):
    """Interactive REPL for R2R search."""
    print("R2R Interactive Search")
    print("=" * 80)
    print("Commands:")
    print("  search <query>  - Search knowledge base")
    print("  rag <query>     - Ask a question (RAG)")
    print("  quit / exit     - Exit")
    print("=" * 80)
    print()

    while True:
        try:
            command = input("> ").strip()

            if not command:
                continue

            if command.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            parts = command.split(maxsplit=1)
            cmd = parts[0].lower()

            if len(parts) < 2:
                print("❌ Usage: <command> <query>")
                continue

            query = parts[1]

            if cmd == "search":
                search(client, query)
            elif cmd == "rag":
                rag(client, query)
            else:
                print(f"❌ Unknown command: {cmd}")
                print("Available commands: search, rag, quit")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            break


def main():
    parser = argparse.ArgumentParser(description="R2R Search CLI")
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--limit", type=int, default=5, help="Max results (default: 5)")
    parser.add_argument("--rag", action="store_true", help="Use RAG instead of search")
    parser.add_argument("--max-tokens", type=int, default=2000, help="Max tokens for RAG")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")

    args = parser.parse_args()

    client = create_client()

    if args.interactive or not args.query:
        interactive_mode(client)
    elif args.rag:
        rag(client, args.query, args.max_tokens)
    else:
        search(client, args.query, args.limit, args.json)


if __name__ == "__main__":
    main()
