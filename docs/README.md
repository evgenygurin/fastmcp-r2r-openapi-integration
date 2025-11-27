# FastMCP + R2R Integration Documentation

**Production-ready MCP server** интегрирующий R2R v3 RAG API через FastMCP 2.x framework.

## 📚 Содержание документации

Документация организована в логической последовательности от быстрого старта до production deployment:

### 1. [Quick Start](./01-QUICKSTART.md) 🚀
**5-минутный старт** с установкой, настройкой и первыми шагами.

**Для кого**: Новые пользователи, быстрое тестирование
**Содержание**:
- Установка и настройка среды
- Конфигурация Claude Desktop
- Базовая верификация
- Первые примеры использования

### 2. [Architecture](./02-ARCHITECTURE.md) 🏛️
**Архитектура и ключевые концепции** - глубокое понимание системы.

**Для кого**: Разработчики, архитекторы
**Содержание**:
- **DynamicBearerAuth Pattern** - request-time authentication для serverless
- **ctx.sample Patterns** - 7 типов LLM-powered операций
- **Pipeline & Middleware** - композиция и хуки
- **OpenAPI Auto-Generation** - semantic routing
- **4-Layer Architecture** - структура интеграции

### 3. [Patterns](./03-PATTERNS.md) 🔄
**ctx.sample и pipeline patterns** - продвинутые техники композиции.

**Для кого**: Разработчики MCP серверов
**Содержание**:
- 7 ctx.sample паттернов (basic, system prompt, structured output, multi-turn, retry, model preferences, fallback)
- Pipeline composition (базовый, conditional, parallel)
- Middleware architecture (on_request, on_call_tool, on_read_resource)
- Error handling и retry logic
- Caching strategies

### 4. [Features](./04-FEATURES.md) ✨
**Custom MCP components** - расширенные возможности сервера.

**Для кого**: Пользователи, интеграторы
**Содержание**:
- 2 Static Resources (server info, routes)
- 3 Resource Templates (documents, collections, search)
- 2 Prompts (rag_query, document_analysis)
- 6 Enhanced Tools (search, analysis, research, comparative, extraction, followup)

### 5. [R2R Client](./05-R2R-CLIENT.md) 🔌
**Type-safe R2R integration** - сравнение httpx vs R2R SDK.

**Для кого**: Разработчики Python клиентов
**Содержание**:
- httpx + DynamicBearerAuth vs R2R Python SDK
- Type-safe wrapper (R2RTypedClient)
- 13 typed methods с autocomplete
- Integration recommendations
- Serverless compatibility

### 6. [Deployment](./06-DEPLOYMENT.md) 🚀
**Production deployment** - FastMCP Cloud, Docker, мониторинг.

**Для кого**: DevOps, production engineers
**Содержание**:
- FastMCP Cloud deployment
- Docker containerization
- Environment variables
- Monitoring и logging
- Troubleshooting

### 7. [Roadmap](./07-ROADMAP.md) 🗺️
**Development priorities** - планы развития проекта.

**Для кого**: Контрибьюторы, планирование
**Содержание**:
- 6 приоритетов (Knowledge Graph, Agent, Production, Search, Documents, Collections)
- Implementation timelines
- Feature requests
- Community feedback

---

## 🎯 Рекомендуемые траектории чтения

### Для новых пользователей
```text
Quick Start → Architecture → Features
```

**Цель**: Понять основы, запустить сервер, попробовать features.

### Для разработчиков
```text
Quick Start → Patterns → R2R Client → Deployment
```

**Цель**: Научиться создавать продвинутые MCP компоненты и деплоить в production.

### Для контрибьюторов
```text
Architecture → Patterns → Roadmap
```

**Цель**: Понять архитектуру, изучить паттерны, выбрать задачу из roadmap.

### Для архитекторов
```text
Architecture → R2R Client → Deployment
```

**Цель**: Оценить архитектурные решения, понять integration points, спланировать deployment.

---

## 🔍 Быстрый поиск

### По темам

**Authentication & Security**:
- [DynamicBearerAuth Pattern](./02-ARCHITECTURE.md#-1-dynamicbearerauth-pattern)
- [Serverless Compatibility](./05-R2R-CLIENT.md#serverless-compatibility)

**LLM Operations**:
- [ctx.sample Patterns](./02-ARCHITECTURE.md#-2-ctxsample-patterns)
- [Advanced Sampling](./03-PATTERNS.md#pattern-1-advanced-ctxsample-usage)

**Pipeline & Composition**:
- [Pipeline Architecture](./02-ARCHITECTURE.md#-3-pipeline--middleware)
- [Pipeline Patterns](./03-PATTERNS.md#pattern-2-pipeline-composition)

**MCP Components**:
- [Custom Resources](./04-FEATURES.md#resource-templates)
- [Enhanced Tools](./04-FEATURES.md#enhanced-tools)

**Integration**:
- [OpenAPI Auto-Generation](./02-ARCHITECTURE.md#-4-openapi-auto-generation)
- [Type-Safe Client](./05-R2R-CLIENT.md#r2rtypedclient)

**Deployment**:
- [FastMCP Cloud](./06-DEPLOYMENT.md#fastmcp-cloud-deployment)
- [Docker Setup](./06-DEPLOYMENT.md#docker-deployment)

---

## 📖 О документации

### Структура документов

Каждый документ следует единому стилю:
- **Эмодзи в заголовках** для визуальной навигации
- **Практические примеры** с code snippets
- **Русский текст** + английские термины/API
- **Cross-references** для связанных тем
- **Table of Contents** для быстрого поиска

### Нумерация файлов

Файлы нумерованы в рекомендуемой последовательности чтения:
- `01-` - Setup и Quick Start
- `02-` - Core Concepts и Architecture
- `03-` - Implementation Patterns
- `04-` - Features и Components
- `05-` - Integration Details
- `06-` - Deployment
- `07-` - Future Planning

### Навигация

В каждом документе:
- **В начале**: Ссылка на README (← Back to Index)
- **В конце**: Ссылки Previous/Next для последовательного чтения

---

## 🛠️ Технический стек

- **R2R v3** - Production RAG система
- **FastMCP 2.x** - Pythonic MCP framework
- **httpx** - Async HTTP client с DynamicBearerAuth
- **Python 3.10+** - Type hints, async/await
- **Claude Desktop** - MCP client для тестирования

---

## 📝 Обновление документации

Документация синхронизирована с кодом в `src/`:
- `src/server.py` - Реализация OpenAPI auto-generation, DynamicBearerAuth
- `src/r2r_typed.py` - Type-safe R2R client
- `src/pipelines.py` - ctx.sample и pipeline patterns

При изменении кода обновляй соответствующие разделы документации.

---

## 🔗 Полезные ссылки

### Проектная документация
- [CLAUDE.md](../CLAUDE.md) - Инструкции для Claude Code
- [pyproject.toml](../pyproject.toml) - Python зависимости
- [Makefile](../Makefile) - Development команды

### Внешняя документация
- [R2R Documentation](https://r2r-docs.sciphi.ai/) - R2R API reference
- [FastMCP Documentation](https://github.com/jlowin/fastmcp) - FastMCP framework
- [MCP Specification](https://modelcontextprotocol.io/) - Model Context Protocol

---

## ❓ Нужна помощь?

1. **Начни с Quick Start** - большинство вопросов решаются быстрым стартом
2. **Проверь Architecture** - понимание core concepts решает 80% проблем
3. **Изучи примеры** - практические примеры в каждом разделе
4. **Проверь Issues** - возможно, проблема уже известна

---

**Приятного чтения!** 📚
