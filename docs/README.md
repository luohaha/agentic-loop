# Documentation Index

Welcome to the Agentic Loop documentation! This directory contains comprehensive guides for using and extending the system.

## Getting Started

- **[Main README](../README.md)**: Quick start and overview
- **[Examples](examples.md)**: Detailed usage examples and patterns
- **[Configuration](configuration.md)**: Complete configuration guide

## Core Features

- **[Memory Management](memory-management.md)**: Intelligent token optimization system
- **[Advanced Features](advanced-features.md)**: Optimization and advanced techniques

## Extending the System

- **[Extending Guide](extending.md)**: How to add custom tools, agents, and LLM providers

## Distribution and Packaging

- **[Packaging Guide](packaging.md)**: Detailed guide for packaging and distribution

## Quick Navigation

### By Use Case

**I want to...**

- **Get started quickly** → [Main README](../README.md)
- **See usage examples** → [Examples](examples.md)
- **Configure the system** → [Configuration](configuration.md)
- **Optimize costs** → [Memory Management](memory-management.md)
- **Add custom tools** → [Extending: Adding Tools](extending.md#adding-new-tools)
- **Create custom agents** → [Extending: Creating Agents](extending.md#creating-new-agent-modes)
- **Understand retry behavior** → [Advanced: Retry](advanced-features.md#automatic-retry-with-exponential-backoff)
- **Switch LLM providers** → [Configuration: Providers](configuration.md#provider-specific-configuration)
- **Package and distribute** → [Packaging Guide](packaging.md)

### By Topic

**Agent Modes**
- [ReAct vs Plan-Execute comparison](../README.md#comparing-the-two-modes)
- [Agent examples](examples.md#comparing-react-vs-plan-execute)
- [Creating custom agents](extending.md#creating-new-agent-modes)

**Memory System**
- [Memory overview](memory-management.md#overview)
- [Compression strategies](memory-management.md#compression-strategies)
- [Token tracking](memory-management.md#token-tracking-and-costs)
- [Performance impact](memory-management.md#performance-impact)

**LLM Providers**
- [Provider setup](../README.md#quick-start)
- [Model selection](configuration.md#model-selection)
- [Custom base URLs](configuration.md#base-url-configuration)
- [Adding new providers](extending.md#adding-new-llm-providers)

**Tools**
- [Built-in tools](../README.md#features)
- [Tool examples](examples.md#file-operations)
- [Creating custom tools](extending.md#adding-new-tools)

**Optimization**
- [Cost optimization](advanced-features.md#cost-optimization)
- [Performance tuning](advanced-features.md#performance-optimization)
- [Memory tuning](memory-management.md#configuration)
- [Best practices](advanced-features.md#best-practices)

## Document Structure

Each guide is self-contained but cross-referenced for easy navigation:

1. **[examples.md](examples.md)** - Hands-on examples covering:
   - Simple calculations
   - File operations
   - Web search and research
   - Complex multi-step tasks
   - Different LLM providers
   - Error handling

2. **[configuration.md](configuration.md)** - Complete configuration reference:
   - Environment variables
   - LLM provider setup
   - Agent configuration
   - Memory settings
   - Configuration presets

3. **[memory-management.md](memory-management.md)** - Memory system documentation:
   - Architecture overview
   - Compression strategies
   - Token tracking
   - Cost optimization
   - Usage examples

4. **[advanced-features.md](advanced-features.md)** - Advanced topics:
   - Automatic retry with backoff
   - Multi-provider support
   - Custom base URLs
   - Performance optimization
   - Error handling patterns

5. **[extending.md](extending.md)** - Extension guide:
   - Adding custom tools
   - Creating new agent modes
   - Adding LLM providers
   - Best practices
   - Testing extensions

6. **[packaging.md](packaging.md)** - Distribution guide:
   - Building packages
   - Publishing to PyPI
   - Docker deployment
   - Creating executables

## Contributing to Documentation

When updating documentation:

1. Keep examples up-to-date with code
2. Add cross-references between related topics
3. Include code snippets where helpful
4. Test all commands and examples
5. Update this index when adding new docs

## Need Help?

- Check the relevant guide above
- See [examples.md](examples.md) for working code
- Review [configuration.md](configuration.md) for settings
- Consult [advanced-features.md](advanced-features.md) for troubleshooting

## Version History

- **v1.1** (2026-01-12): Added packaging documentation
  - Added packaging guide
  - Updated README with installation options
  - Added development and contribution sections

- **v1.0** (2025-01-07): Initial documentation split from main README
  - Added memory management documentation
  - Created separate guides for each topic
  - Reorganized for better navigation
