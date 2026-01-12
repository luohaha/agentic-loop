# Packaging and Distribution Guide

This guide explains how to package and distribute agentic-loop.

## 📦 Quick Start - Local Installation

### Install for Development

```bash
# Install in editable mode
./scripts/install_local.sh

# Or manually
pip install -e .
```

Now you can use it globally:
```bash
agentic-loop --help
agentic-loop interactive
```

## 🚀 Publishing to PyPI

### 1. Build the Package

```bash
./scripts/build.sh
```

This creates distribution files in `dist/`:
- `agentic_loop-0.1.0-py3-none-any.whl` (wheel)
- `agentic_loop-0.1.0.tar.gz` (source distribution)

### 2. Test Locally

```bash
# Install from wheel
pip install dist/agentic_loop-0.1.0-py3-none-any.whl

# Test it
agentic-loop interactive
```

### 3. Publish to Test PyPI (Recommended First)

```bash
# Create account at https://test.pypi.org/
# Get API token from account settings

# Upload to test PyPI
twine upload --repository testpypi dist/*

# Install from test PyPI
pip install --index-url https://test.pypi.org/simple/ agentic-loop
```

### 4. Publish to Production PyPI

```bash
# Create account at https://pypi.org/
# Get API token

# Upload
./scripts/publish.sh

# Now anyone can install
pip install agentic-loop
```

## 🐳 Docker Distribution

### Build Docker Image

```bash
docker build -t agentic-loop:latest .
```

### Run with Docker

```bash
# Interactive mode
docker run -it --rm \
  -e ANTHROPIC_API_KEY=your_key \
  -v $(pwd)/data:/app/data \
  agentic-loop interactive

# Single task
docker run --rm \
  -e ANTHROPIC_API_KEY=your_key \
  agentic-loop --mode react "Analyze this code"
```

### Publish Docker Image

```bash
# Tag for Docker Hub
docker tag agentic-loop:latest yourusername/agentic-loop:0.1.0
docker tag agentic-loop:latest yourusername/agentic-loop:latest

# Push
docker push yourusername/agentic-loop:0.1.0
docker push yourusername/agentic-loop:latest
```

## 📱 Standalone Executable (Optional)

For users without Python, create a standalone executable:

### Using PyInstaller

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile \
  --name agentic-loop \
  --add-data ".env.example:." \
  --hidden-import anthropic \
  --hidden-import openai \
  --hidden-import google.genai \
  main.py

# Executable will be in dist/agentic-loop
```

**Note**: The executable will be ~50-100MB and platform-specific.

## 📋 Release Checklist

Before publishing a new version:

- [ ] Update version in `pyproject.toml`
- [ ] Update CHANGELOG.md
- [ ] Run tests: `pytest`
- [ ] Build package: `./scripts/build.sh`
- [ ] Test locally: `pip install dist/*.whl`
- [ ] Create git tag: `git tag v0.1.0 && git push --tags`
- [ ] Publish to PyPI: `./scripts/publish.sh`
- [ ] Create GitHub release with changelog

## 🔧 Troubleshooting

### Import Errors After Installation

If you get import errors, make sure all packages are included in `pyproject.toml`:
```toml
[tool.setuptools]
packages = ["agent", "llm", "memory", "tools", "utils"]
```

### Missing Files

Add them to `MANIFEST.in`:
```
include important_file.txt
recursive-include data *.json
```

### Version Conflicts

Use constraints file:
```bash
pip install agentic-loop -c constraints.txt
```

## 📚 Distribution Methods Summary

| Method | Command | Use Case |
|--------|---------|----------|
| **Local Dev** | `pip install -e .` | Development, testing |
| **PyPI** | `pip install agentic-loop` | Public distribution |
| **Docker** | `docker run agentic-loop` | Containerized deployment |
| **Executable** | `./agentic-loop` | Non-Python users |
| **GitHub** | `pip install git+https://github.com/user/repo` | Direct from source |

## 🎯 Recommended Workflow

1. **Development**: Use `pip install -e .`
2. **Testing**: Build and test with `./scripts/build.sh`
3. **Distribution**: Publish to PyPI
4. **Users**: Install with `pip install agentic-loop`
