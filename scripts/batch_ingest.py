#!/usr/bin/env python3
"""Batch document ingestion script using R2RClient.

This script demonstrates R2RClient usage for standalone operations
where serverless compatibility is not required.

Use case: Batch processing, data migration, one-time uploads

NOT suitable for: FastMCP servers (use httpx + DynamicBearerAuth instead)
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

# Add parent directory to path for imports
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
        print("⚠️  Warning: R2R_API_KEY not set. API requests may fail.")

    client = R2RClient(base_url=base_url, api_key=api_key)
    print(f"✓ Connected to R2R at {base_url}")

    return client


def batch_upload(
    client: R2RClient, directory: Path, pattern: str = "*.pdf", collection_id: str | None = None
) -> list[dict[str, Any]]:
    """Upload all files matching pattern from directory.

    Args:
        client: R2RClient instance
        directory: Directory containing files
        pattern: Glob pattern (default: "*.pdf")
        collection_id: Optional collection to add documents to

    Returns:
        List of upload results
    """
    files = list(directory.glob(pattern))

    if not files:
        print(f"❌ No files matching '{pattern}' found in {directory}")
        return []

    print(f"📁 Found {len(files)} files matching '{pattern}'")
    print()

    results = []
    for i, file_path in enumerate(files, 1):
        try:
            print(f"[{i}/{len(files)}] Uploading {file_path.name}...", end=" ", flush=True)

            # Upload document
            result = client.documents.create(
                file_path=str(file_path),
                metadata={"filename": file_path.name, "source": "batch_ingest"},
            )

            document_id = result.get("document_id")

            # Add to collection if specified
            if collection_id and document_id:
                client.collections.add_document(
                    collection_id=collection_id, document_id=document_id
                )

            results.append(result)
            print(f"✓ {document_id}")

        except Exception as e:
            print(f"❌ Error: {e}")
            continue

    print()
    print(f"✓ Successfully uploaded {len(results)}/{len(files)} documents")

    return results


def main():
    parser = argparse.ArgumentParser(description="Batch upload documents to R2R")
    parser.add_argument("directory", type=Path, help="Directory containing documents")
    parser.add_argument(
        "--pattern", default="*.pdf", help="File pattern (default: *.pdf)"
    )
    parser.add_argument("--collection", help="Collection ID to add documents to")
    parser.add_argument("--dry-run", action="store_true", help="List files without uploading")

    args = parser.parse_args()

    if not args.directory.exists():
        print(f"❌ Directory not found: {args.directory}")
        sys.exit(1)

    if not args.directory.is_dir():
        print(f"❌ Not a directory: {args.directory}")
        sys.exit(1)

    files = list(args.directory.glob(args.pattern))

    if args.dry_run:
        print(f"Dry run: Found {len(files)} files")
        for file in files:
            print(f"  - {file.name}")
        return

    client = create_client()
    batch_upload(client, args.directory, args.pattern, args.collection)


if __name__ == "__main__":
    main()
