# Datest 🧪

> **Simple testing framework for Dana language files (.na)**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.md)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

Datest is a minimal testing framework for Dana (.na) files. It provides basic test discovery and execution for neurosymbolic agent systems written in the Dana language.

**Status: Early MVP** - Basic functionality for discovering and validating Dana test files.

---

## 🚀 Quick Start

```bash
# Install and setup
git clone https://github.com/aitomatic/datest.git
cd datest
make quickstart

# Run datest (currently shows help and validates setup)
datest

# Future: Basic Dana file testing
datest test_example.na           # Run a Dana test file
datest tests/                    # Run all .na files in directory
```

---

## 🧪 What Datest Does

Datest is a **barebones MVP** that focuses on the essentials:

### **Basic Test Discovery**
- Finds `.na` files in directories
- Follows simple naming patterns (`test_*.na`)
- Basic file validation

### **Simple Dana Test Format**
```dana
// test_example.na - Basic Dana test
test "simple reasoning" {
    reason("What is 2 + 2?")
    expect(contains("4"))
}

test "basic memory" {
    remember("fact", "sky is blue")
    reason("What color is the sky?")
    expect(contains("blue"))
}
```

---

## ✨ Core Features (MVP)

- **🔍 File Discovery**: Finds Dana test files in directories
- **📄 Basic Parsing**: Validates Dana test file syntax 
- **📋 Simple Output**: Basic pass/fail reporting
- **🎯 Minimal**: Focused on essential functionality only

**Not Included (Yet):**
- ❌ Advanced assertions
- ❌ Parallel execution  
- ❌ Complex reporting
- ❌ Plugin system
- ❌ Coverage analysis

---

## 🛠️ Installation

### **From PyPI (Recommended)**
```bash
# Install the latest release
pip install datest

# Or with optional dependencies
pip install "datest[llm]"  # Include LLM integration
pip install "datest[dev]"  # Include development tools
```

### **From Source**
```bash
# Quick setup
git clone https://github.com/aitomatic/datest.git
cd datest
make setup-dev
```

Or install directly:
```bash
pip install -e .
```

---

## 📖 Basic Usage

### **Current Commands**
```bash
# Show help and validate installation
datest

# Check version
datest --version

# Verbose output
datest --verbose
```

### **Planned Commands (Simple)**
```bash
# Run Dana test files
datest test_example.na           # Single file
datest tests/                    # Directory of .na files
datest --list                    # Show discovered tests
```

---

## 🧪 Writing Dana Tests (Basic)

### **Simple Test Structure**
```dana
// test_basic.na
test "addition" {
    reason("What is 5 + 3?")
    expect(contains("8"))
}

test "memory recall" {
    remember("name", "Alice")
    reason("What name did I remember?")
    expect(contains("Alice"))
}
```

### **Basic Assertions (Planned)**
- `expect(contains("text"))` - Check if response contains text
- `expect(equals("exact"))` - Exact match
- `expect(not_empty())` - Response is not empty

**That's it.** No complex patterns, no advanced features - just the basics.

---

## 🏗️ Current Status

### **What Works Now (v0.1.0)**
- ✅ CLI framework with basic argument parsing
- ✅ Project structure and packaging
- ✅ Development tooling setup
- ✅ Installation and basic validation

### **Next Steps (v0.2.0)**
- 🚧 Simple Dana file discovery
- 🚧 Basic Dana test parsing
- 🚧 Minimal test execution
- 🚧 Simple pass/fail output

### **Future (Maybe)**
- 📋 More assertion types
- 📋 Better error messages
- 📋 Configuration files
- 📋 Integration with other tools

---

## 🔧 Configuration (Minimal)

### **Basic datest.toml**
```toml
# datest.toml - Simple configuration
[tool.datest]
test_dirs = ["tests"]
test_pattern = "test_*.na"
```

That's all the configuration needed for the MVP.

---

## 🤝 Contributing

This is a minimal MVP, so contributions should focus on:

### **Core Priorities**
1. **Dana file parsing** - Basic syntax validation
2. **Test discovery** - Find .na files reliably  
3. **Simple execution** - Run tests and report results
4. **Error handling** - Clear error messages

### **Non-Priorities (For Now)**
- Advanced features
- Complex reporting
- Performance optimization
- Plugin systems

### **Getting Started**
```bash
git clone https://github.com/your-username/datest.git
cd datest
make setup-dev
make test
```

---

## 📊 Why This MVP Approach?

### **Keep It Simple**
- Focus on core Dana testing needs
- Get basic functionality working first
- Avoid feature creep early on

### **Learn First**
- Understand how Dana tests should work
- Get feedback from real usage
- Build features that are actually needed

### **Sustainable Development**
- Small, manageable codebase
- Clear scope and expectations
- Room to grow based on user needs

---

## 🔗 Resources

- **Repository**: [github.com/aitomatic/datest](https://github.com/aitomatic/datest)
- **Issues**: [Report bugs and simple feature requests](https://github.com/aitomatic/datest/issues)
- **Discussions**: [Basic usage questions](https://github.com/aitomatic/datest/discussions)

---

## 📄 License

MIT License - see [LICENSE.md](LICENSE.md) for details.

---

<p align="center">
  <strong>Built with ❤️ by <a href="https://aitomatic.com">Aitomatic</a></strong>
  <br/>
  <em>Simple Dana testing, one step at a time</em>
</p>

