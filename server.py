"""Entrypoint for FastMCP Cloud deployment."""

from src.server import mcp

# Export mcp instance for FastMCP Cloud
__all__ = ["mcp"]
