     STDIN
   1 # Changelog
   2 
   3 All notable changes to R2R MCP Server project.
   4 
   5 ## [1.2.0] - 2025-11-25
   6 
   7 ### Added - Pipelines & Advanced Patterns
   8 
   9 **New Module: src/pipelines.py (663 lines)**
  10 - 5 ctx.sample patterns (basic, system prompts, structured, multi-turn, retry)
  11 - 2 Pipeline classes (Pipeline, ConditionalPipeline)
  12 - 3 Pipeline steps (search, analyze, summarize)
  13 - 3 Utility functions (fallback, caching, parallel)
  14 
  15 **New Pipeline Tools in server.py (4 tools)**
  16 - research_pipeline - Multi-step research with configurable depth
  17 - comparative_analysis - Multi-query comparison with LLM
  18 - extract_structured_data - Schema-driven extraction
  19 - generate_followup_questions - AI-powered question generation
  20 
  21 **New Documentation (1600+ lines)**
  22 - docs/PIPELINES.md (700 lines) - ctx.sample & pipeline patterns
  23 - docs/EXAMPLES.md (911 lines) - Usage examples & workflows
  24 
  25 **Server Updates**
  26 - Moved pipeline imports to top-level
  27 - Removed unused variables
  28 - Enhanced component count logging
  29 
  30 ### Changed
  31 - Server now reports 6 tools (2 basic + 4 pipelines)
  32 - Total custom components: 11 (3 templates + 2 prompts + 6 tools)
  33 
  34 ---
  35 
  36 ## [1.1.0] - 2025-11-25
  37 
  38 ### Added - Enhanced Features & Roadmap
  39 
  40 **New Components (7 total)**
  41 - 3 Resource templates (documents, collections, search with RFC 6570)
  42 - 2 Prompts (rag_query, document_analysis)
  43 - 2 Enhanced tools (enhanced_search, analyze_search_results)
  44 
  45 **New Documentation (2000+ lines)**
  46 - docs/ENHANCED_FEATURES.md (640 lines)
  47 - docs/ROADMAP.md (1067 lines)
  48 
  49 **Features Demonstrated**
  50 - Context integration (logging, progress, sampling)
  51 - LLM sampling in tools
  52 - Resource annotations
  53 - RFC 6570 query parameters
  54 
  55 ---
  56 
  57 ## [1.0.1] - 2025-11-25
  58 
  59 ### Fixed
  60 - Enabled experimental FastMCP parser
  61 - Resolved ChunkSearchSettings error
  62 - Added type ignore for experimental imports
  63 
  64 ---
  65 
  66 ## [1.0.0] - 2025-11-25
  67 
  68 ### Added - Initial Release
  69 
  70 **Core Features**
  71 - Auto-generated MCP server from R2R OpenAPI spec
  72 - 114 routes from 81 endpoints
  73 - Dynamic Bearer authentication
  74 - 3 semantic route mapping rules
  75 - 2 custom static resources (server/info, server/routes)
  76 
  77 **Configuration**
  78 - Environment-based configuration
  79 - Debug logging support
  80 - Experimental parser support with fallback
  81 
  82 **Documentation**
  83 - Comprehensive README
  84 - Workspace rules
  85 - Environment example
  86 
  87 ---
  88 
  89 ## Statistics
  90 
  91 ### Total Project Size
  92 - **Code**: 1,637 lines (server.py: 972, pipelines.py: 663, __init__.py: 3)
  93 - **Documentation**: 4,518 lines across 4 docs
  94 - **Total**: 6,155+ lines
  95 
  96 ### Component Counts
  97 - **Auto-generated**: 114 MCP routes
  98 - **Custom**: 11 components (3 templates + 2 prompts + 6 tools)
  99 - **Pipelines**: 13 reusable patterns
 100 - **Total**: 140+ MCP capabilities
 101 
 102 ### Development Timeline
 103 - Nov 25, 2025: v1.0.0 - Initial release
 104 - Nov 25, 2025: v1.0.1 - Parser fix
 105 - Nov 25, 2025: v1.1.0 - Enhanced features
 106 - Nov 25, 2025: v1.2.0 - Pipelines & patterns
 107 
 108 Total development time: 1 day
 109 Commits: 5
 110 Lines added: 6000+
 111 R2R RAG queries: 10+
