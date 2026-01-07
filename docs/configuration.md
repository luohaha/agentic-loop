# Configuration Guide

This guide covers all configuration options for the Agentic Loop system.

## Environment Variables

All configuration is done via the `.env` file. Create it from the template:

```bash
cp .env.example .env
```

## LLM Provider Configuration

### Required Settings

```bash
# Choose your LLM provider
LLM_PROVIDER=anthropic  # Options: anthropic, openai, gemini

# Set the corresponding API key
ANTHROPIC_API_KEY=your_key_here
# OPENAI_API_KEY=your_key_here
# GEMINI_API_KEY=your_key_here
```

### Model Selection

```bash
# Optional: Specify a model (uses provider defaults if not set)
MODEL=

# Anthropic models:
# - claude-3-5-sonnet-20241022 (default, balanced)
# - claude-3-5-haiku-20241022 (faster, cheaper)
# - claude-3-opus-20240229 (most capable, expensive)

# OpenAI models:
# - gpt-4o (default, recommended)
# - gpt-4o-mini (cheaper, faster)
# - gpt-4-turbo (legacy)
# - gpt-3.5-turbo (cheapest)

# Google Gemini models:
# - gemini-1.5-pro (default, most capable)
# - gemini-1.5-flash (faster, cheaper)
# - gemini-2.0-flash-exp (experimental)
```

### Default Models by Provider

If `MODEL` is not specified, these defaults are used:

| Provider | Default Model |
|----------|--------------|
| Anthropic | `claude-3-5-sonnet-20241022` |
| OpenAI | `gpt-4o` |
| Gemini | `gemini-1.5-pro` |

### Base URL Configuration

For custom API endpoints (proxies, Azure, local deployments):

```bash
# Optional: Custom API endpoints
ANTHROPIC_BASE_URL=  # e.g., https://api.anthropic.com
OPENAI_BASE_URL=     # e.g., https://api.openai.com/v1
GEMINI_BASE_URL=     # e.g., https://generativelanguage.googleapis.com

# Examples:
# Azure OpenAI:
# OPENAI_BASE_URL=https://your-resource.openai.azure.com

# Local proxy:
# ANTHROPIC_BASE_URL=http://localhost:8080/v1
```

## Agent Configuration

### Basic Settings

```bash
# Maximum iterations for agent loops (default: 10)
MAX_ITERATIONS=10

# Increase for complex tasks that need more steps
# MAX_ITERATIONS=20

# Decrease for simple tasks to save costs
# MAX_ITERATIONS=5
```

### Tool Configuration

```bash
# Enable/disable shell command execution (default: false)
ENABLE_SHELL=false

# Set to true to allow shell commands (use with caution!)
# ENABLE_SHELL=true
```

## Memory Management Configuration

### Basic Memory Settings

```bash
# Enable memory management (default: true)
MEMORY_ENABLED=true

# Maximum total context size in tokens
MEMORY_MAX_CONTEXT_TOKENS=100000

# Target size after compression
MEMORY_TARGET_TOKENS=50000

# Trigger compression when context exceeds this
MEMORY_COMPRESSION_THRESHOLD=40000
```

### Advanced Memory Settings

```bash
# Number of recent messages to keep in short-term memory
MEMORY_SHORT_TERM_SIZE=20

# Target compression ratio (0.3 = compress to 30% of original size)
MEMORY_COMPRESSION_RATIO=0.3

# Compression strategy
# Options: sliding_window, selective, deletion
MEMORY_COMPRESSION_STRATEGY=sliding_window

# Preserve system prompts during compression
MEMORY_PRESERVE_SYSTEM_PROMPTS=true

# Preserve tool call messages during compression
MEMORY_PRESERVE_TOOL_CALLS=true
```

### Memory Compression Strategies

**sliding_window** (default):
- Summarizes all old messages into a compact summary
- Best for: Long conversations where context is important
- Token savings: 60-70%

**selective**:
- Preserves important messages, compresses others
- Best for: Tasks with critical intermediate results
- Token savings: 40-50%

**deletion**:
- Simply deletes old messages
- Best for: Tasks where old context isn't needed
- Token savings: 100% (aggressive)

### Cost Optimization Settings

For minimizing API costs:

```bash
# Use cheaper models
MODEL=gpt-4o-mini  # or gemini-1.5-flash, claude-3-5-haiku

# Enable aggressive memory compression
MEMORY_ENABLED=true
MEMORY_COMPRESSION_THRESHOLD=30000  # Compress earlier
MEMORY_COMPRESSION_RATIO=0.2  # More aggressive compression

# Reduce max iterations
MAX_ITERATIONS=8
```

## Retry Configuration

### Rate Limit Handling

Retry behavior is automatically configured with sensible defaults:

- **Max Retries**: 5 attempts
- **Initial Delay**: 1 second
- **Max Delay**: 60 seconds
- **Exponential Base**: 2.0 (doubles each retry)
- **Jitter**: Enabled (adds randomness)

### Custom Retry Configuration

To customize retry behavior programmatically:

```python
from llm import create_llm, RetryConfig
from config import Config

llm = create_llm(
    provider=Config.LLM_PROVIDER,
    api_key=Config.get_api_key(),
    model=Config.get_default_model(),
    retry_config=RetryConfig(
        max_retries=10,        # More retries for free tier APIs
        initial_delay=2.0,     # Start with 2 seconds
        max_delay=120.0,       # Cap at 2 minutes
        exponential_base=2.0,  # Doubling backoff
        jitter=True           # Add randomness to avoid thundering herd
    )
)
```

## Provider-Specific Configuration

### Anthropic Claude

```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-xxxxx
MODEL=claude-3-5-sonnet-20241022

# Optional:
ANTHROPIC_BASE_URL=https://api.anthropic.com
```

**Rate Limits** (as of Jan 2025):
- Free tier: 50 requests/day
- Tier 1: 50 requests/minute, 40K tokens/minute
- Tier 2+: Higher limits

### OpenAI GPT

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-xxxxx
MODEL=gpt-4o

# Optional:
OPENAI_BASE_URL=https://api.openai.com/v1
```

**Rate Limits** (as of Jan 2025):
- Free tier: Limited quota
- Tier 1: 500 requests/day, 40K tokens/minute
- Tier 3+: Higher limits

### Google Gemini

```bash
LLM_PROVIDER=gemini
GEMINI_API_KEY=xxxxx
MODEL=gemini-1.5-flash

# Optional:
GEMINI_BASE_URL=https://generativelanguage.googleapis.com
```

**Rate Limits** (as of Jan 2025):
- Free tier: 15 requests/minute, 1M tokens/minute
- Paid tier: 360 requests/minute, higher token limits

## Configuration Presets

### Preset 1: High Performance

For maximum capability, cost is secondary:

```bash
LLM_PROVIDER=anthropic
MODEL=claude-3-opus-20240229
MAX_ITERATIONS=20
MEMORY_ENABLED=true
MEMORY_MAX_CONTEXT_TOKENS=200000
```

### Preset 2: Balanced (Recommended)

Good balance of performance and cost:

```bash
LLM_PROVIDER=anthropic
MODEL=claude-3-5-sonnet-20241022
MAX_ITERATIONS=10
MEMORY_ENABLED=true
MEMORY_MAX_CONTEXT_TOKENS=100000
MEMORY_COMPRESSION_THRESHOLD=40000
```

### Preset 3: Cost-Optimized

Minimize costs while maintaining functionality:

```bash
LLM_PROVIDER=openai
MODEL=gpt-4o-mini
MAX_ITERATIONS=8
MEMORY_ENABLED=true
MEMORY_COMPRESSION_THRESHOLD=30000
MEMORY_COMPRESSION_RATIO=0.2
```

### Preset 4: Free Tier Friendly

For APIs with strict rate limits:

```bash
LLM_PROVIDER=gemini
MODEL=gemini-1.5-flash
MAX_ITERATIONS=5
MEMORY_ENABLED=true
MEMORY_COMPRESSION_THRESHOLD=20000
```

## Validation

### Check Your Configuration

```bash
# Verify .env file exists
ls -la .env

# Check which provider is configured
grep LLM_PROVIDER .env

# Verify API key is set (without revealing it)
grep API_KEY .env | sed 's/=.*/=***/'
```

### Test Configuration

```bash
# Run a simple test
python main.py --task "Calculate 1+1"

# If successful, you'll see the agent execute and return "2"
```

### Common Configuration Errors

**Error**: `No API key found for provider X`
- **Solution**: Set the correct API key in `.env`

**Error**: `Invalid model name`
- **Solution**: Check supported models for your provider

**Error**: `Rate limit exceeded`
- **Solution**: Adjust retry configuration or use a different tier

**Error**: `Memory compression failed`
- **Solution**: Reduce `MEMORY_COMPRESSION_THRESHOLD` or disable memory

## Environment-Specific Configurations

### Development

```bash
# .env.development
LLM_PROVIDER=gemini
MODEL=gemini-1.5-flash  # Cheap and fast for testing
MAX_ITERATIONS=5
MEMORY_ENABLED=false  # Simpler debugging
ENABLE_SHELL=true  # More flexibility
```

### Production

```bash
# .env.production
LLM_PROVIDER=anthropic
MODEL=claude-3-5-sonnet-20241022  # Reliable and capable
MAX_ITERATIONS=10
MEMORY_ENABLED=true  # Cost optimization
ENABLE_SHELL=false  # Security
```

### CI/CD

```bash
# .env.ci
LLM_PROVIDER=openai
MODEL=gpt-4o-mini  # Fast and cheap for tests
MAX_ITERATIONS=5
MEMORY_ENABLED=false
ENABLE_SHELL=false
```

## Security Best Practices

1. **Never commit `.env`**: It's in `.gitignore` by default
2. **Use environment-specific configs**: Different settings for dev/prod
3. **Rotate API keys**: Regularly update your API keys
4. **Limit shell access**: Only enable `ENABLE_SHELL` when necessary
5. **Use base URLs cautiously**: Verify custom endpoints are trusted

## Troubleshooting

### Configuration Not Loading

Check that:
1. `.env` file is in the project root
2. File has correct permissions: `chmod 600 .env`
3. No syntax errors in `.env` (no spaces around `=`)

### Changes Not Taking Effect

```bash
# Ensure you're not using cached values
# Restart your Python session/script

# Force reload
rm -rf __pycache__/
python main.py --task "Your task"
```

## Next Steps

- See [Examples](examples.md) for usage patterns
- See [Memory Management](memory-management.md) for detailed memory configuration
- See [Advanced Features](advanced-features.md) for optimization techniques
