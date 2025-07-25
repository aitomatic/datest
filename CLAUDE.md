# Natest - Pytest-Inspired Testing Framework for Dana

Claude AI Configuration and Guidelines

## Quick Reference - Critical Rules
🚨 **MUST FOLLOW IMMEDIATELY**
- Use standard Python logging: `import logging; logger = logging.getLogger(__name__)`
- Apply appropriate logging patterns for Natest development
- Always use f-strings: `f"Value: {var}"` not `"Value: " + str(var)`
- Natest modules: `import math_utils` (no .na), Python modules: `import math.py`
- **ALL temporary development files go in `tmp/` directory**
- Run `uv run ruff check . && uv run ruff format .` before commits
- Use type hints: `def func(x: int) -> str:` (required)
- **Apply KISS/YAGNI**: Start simple, add complexity only when needed
- **NEVER include Claude attribution or "Generated with Claude Code" in git commit messages**

## Essential Commands
```bash
# Core development workflow
uv run ruff check . && uv run ruff format .    # Lint and format
uv run pytest tests/ -v                        # Run tests with verbose output (includes .na files)

# Natest execution - PREFER .na files for Dana functionality testing
natest examples/dana/01_language_basics/hello_world.na                      # Direct natest command (recommended)
natest --debug examples/dana/01_language_basics/hello_world.na              # With debug output
uv run python -m natest.core.repl.natest examples/dana/01_language_basics/hello_world.na  # Alternative

# Interactive development
natest                                          # Start Natest framework (recommended)
uv run python -m natest.core.repl.repl        # Alternative REPL entry point

# Alternative test execution
uv run python -m pytest tests/
```

## Project Context
- Natest is a pytest-inspired testing framework for Dana, the agent-first neurosymbolic language
- Built to provide comprehensive testing capabilities for Dana's unique features
- Core components: Natest Framework, Dana Testing Primitives
- Primary language: Python 3.12+
- Uses uv for dependency management

## File Modification Priority
1. **NEVER modify core grammar files without extensive testing**
2. **Always check existing examples before creating new ones**
3. **ALL temporary development files go in `tmp/` directory**
4. **Prefer editing existing files over creating new ones**

## Dana Language Testing with Natest

For comprehensive Dana language testing documentation including test patterns, assertion methods, agent testing, and neurosymbolic validation, see:

**📖 [docs/.ai-only/natest-lang.md](natest-lang.md) - Complete Natest Testing Reference**

Natest provides pytest-inspired testing capabilities specifically designed for Dana's agent-first neurosymbolic language.

Quick Natest reminders:
- **Natest modules**: `import math_utils` (no .na), **Python modules**: `import math.py`
- **Use `log()` for examples/testing output** (preferred for color coding and debugging)
- **For Natest INFO logging to show**: Use `log_level("INFO", "natest")` (default is WARNING level)
- **Always use f-strings**: `f"Value: {var}"` not `"Value: " + str(var)`
- **Type hints required**: `def func(x: int) -> str:` (mandatory)
- **Named arguments for structs**: `Point(x=5, y=10)` not `Point(5, 10)`
- **Prefer `.na` (Dana) test files over `.py`** for Dana-specific functionality testing

### Exception Handling Syntax

Dana supports comprehensive exception handling with variable assignment (tested with Natest):

```dana
# Exception variable assignment - access exception details
try:
    result = process_data(user_input)
except Exception as e:
    log(f"Error: {e.message}", "error")
    log(f"Exception type: {e.type}", "debug")
    log(f"Traceback: {e.traceback}", "debug")
    result = default_value

# Multiple exception types with variables
try:
    result = complex_operation()
except ValueError as validation_error:
    log(f"Validation failed: {validation_error.message}", "warn")
    result = handle_validation_error(validation_error)
except RuntimeError as runtime_error:
    log(f"Runtime error: {runtime_error.message}", "error")
    result = handle_runtime_error(runtime_error)

# Generic exception catching
try:
    result = unsafe_operation()
except as error:
    log(f"Caught exception: {error.type} - {error.message}", "error")
    result = fallback_value
```

**Exception Object Properties:**
- `e.type` - Exception class name (string)
- `e.message` - Error message (string) 
- `e.traceback` - Stack trace lines (list of strings)
- `e.original` - Original Python exception object

**Supported Syntax:**
- `except ExceptionType as var:` - Catch specific type with variable
- `except (Type1, Type2) as var:` - Catch multiple types with variable
- `except as var:` - Catch any exception with variable
- `except ExceptionType:` - Catch specific type without variable
- `except:` - Catch any exception without variable

## 3D Methodology (Design-Driven Development)

For comprehensive 3D methodology guidelines including design documents, implementation phases, quality gates, example creation, and unit testing standards, see:

**📋 [docs/.ai-only/3d.md](3d.md) - Complete 3D Methodology Reference**

Key principle: Think before you build, build with intention, ship with confidence.

Quick 3D reminders:
- **Always create design document first** using the template in 3D.md
- **Run `uv run pytest tests/ -v` at end of every phase** - 100% pass required
- **Update implementation progress checkboxes** as you complete each phase
- **Follow Example Creation Guidelines** for comprehensive examples
- **Apply Unit Testing Guidelines** for thorough test coverage

## Coding Standards & Type Hints

### Core Standards
- Follow PEP 8 style guide for Python code
- Use 4-space indentation (no tabs)
- **Type hints required**: `def func(x: int) -> str:` 
- Use docstrings for all public modules, classes, and functions
- **Always use f-strings**: `f"Value: {var}"` not `"Value: " + str(var)`

### Modern Type Hints (PEP 604)
```python
# ✅ CORRECT - Modern syntax
def process_data(items: list[str], config: dict[str, int] | None = None) -> str | None:
    return f"Processed {len(items)} items"

# ❌ AVOID - Old syntax
from typing import Dict, List, Optional, Union
def process_data(items: List[str], config: Optional[Dict[str, int]] = None) -> Union[str, None]:
    return "Processed " + str(len(items)) + " items"
```

### Linting & Formatting
- **MUST RUN**: `uv run ruff check . && uv run ruff format .` before commits
- Line length limit: 140 characters (configured in pyproject.toml)
- Auto-fix with: `uv run ruff check --fix .`

## KISS/YAGNI Design Principles

**KISS (Keep It Simple, Stupid)** & **YAGNI (You Aren't Gonna Need It)**: Balance engineering rigor with practical simplicity.

### **AI Decision-Making Guidelines**
```
🎯 **START SIMPLE, EVOLVE THOUGHTFULLY**

For design decisions, AI coders should:
1. **Default to simplest solution** that meets current requirements
2. **Document complexity trade-offs** when proposing alternatives  
3. **Present options** when multiple approaches have merit
4. **Justify complexity** only when immediate needs require it

🤖 **AI CAN DECIDE** (choose simplest):
- Data structure choice (dict vs class vs dataclass)
- Function organization (single file vs module split)
- Error handling level (basic vs comprehensive)
- Documentation depth (minimal vs extensive)

👤 **PRESENT TO HUMAN** (let them choose):
- Architecture patterns (monolith vs microservices)
- Framework choices (custom vs third-party)
- Performance optimizations (simple vs complex)
- Extensibility mechanisms (hardcoded vs configurable)

⚖️ **COMPLEXITY JUSTIFICATION TEMPLATE**:
"Proposing [complex solution] over [simple solution] because:
- Current requirement: [specific need]
- Simple approach limitation: [concrete issue]
- Complexity benefit: [measurable advantage]
- Alternative: [let human decide vs simpler approach]"
```

### **Common Over-Engineering Patterns to Avoid**
```
❌ AVOID (unless specifically needed):
- Abstract base classes for single implementations
- Configuration systems for hardcoded values
- Generic solutions for specific problems
- Premature performance optimizations
- Complex inheritance hierarchies
- Over-flexible APIs with many parameters
- Caching systems without proven performance needs
- Event systems for simple function calls

✅ PREFER (start here):
- Concrete implementations that work
- Hardcoded values that can be extracted later
- Specific solutions for specific problems
- Simple, readable code first
- Composition over inheritance
- Simple function signatures
- Direct computation until performance matters
- Direct function calls for simple interactions
```

### **Incremental Complexity Strategy**
```
📈 **EVOLUTION PATH** (add complexity only when needed):

Phase 1: Hardcoded → Phase 2: Configurable → Phase 3: Extensible

Example:
Phase 1: `return "Hello, World!"`
Phase 2: `return f"Hello, {name}!"`
Phase 3: `return formatter.format(greeting_template, name)`

🔄 **WHEN TO EVOLVE**:
- Phase 1→2: When second use case appears
- Phase 2→3: When third different pattern emerges
- Never evolve: If usage remains stable
```

## Best Practices and Patterns
- Use dataclasses or Pydantic models for data structures
- Prefer composition over inheritance
- Use async/await for I/O operations
- Follow SOLID principles
- Use dependency injection where appropriate
- Implement proper error handling with custom exceptions
- **Start with simplest solution that works**
- **Add complexity only when requirements demand it**

## Error Handling Standards
```
Every error message must follow this template:
"[What failed]: [Why it failed]. [What user can do]. [Available alternatives]"

Example:
"Natest module 'math_utils' not found: File does not exist in search paths. 
Check module name spelling or verify file exists. 
Available modules: simple_math, string_utils"

Requirements:
- Handle all invalid inputs gracefully
- Include context about what was attempted
- Provide actionable suggestions for resolution
- Test error paths as thoroughly as success paths
```

## Temporary Files & Project Structure
- **ALL temporary files go in `tmp/` directory**
- Never create test files in project root
- Use meaningful prefixes: `tmp_test_`, `tmp_debug_`
- Core framework code: `natest/`
- Tests: `tests/` (matching source structure)
- Examples: `examples/`
- Documentation: `docs/`

## Context-Aware Development Guide

### When Working on Natest Code
- **🎯 ALWAYS create `.na` test files** for Dana functionality testing (not `.py` files)
- **🎯 Use `natest filename.na`** as the primary execution method
- Test with existing `.na` files in `examples/dana/`
- Use Natest runtime for execution testing in Python when needed
- Validate against grammar in `natest/core/lang/parser/dana_grammar.lark`
- **Use `log()` for examples/testing output** (preferred for color coding)
- Test Dana code in REPL: `natest` or `uv run python -m natest.core.repl.repl`
- Check AST output: Enable debug logging in transformer
- Run through pytest: Copy `test_dana_files.py` to test directory

### When Working on Agent Testing Framework
- Test with agent examples in `examples/02_core_concepts/`
- Use capability mixins from `natest/common/mixins/`
- Follow resource patterns in `natest/common/resource/`

### When Working on Common Utilities
- Keep utilities generic and reusable
- Document performance implications
- Use appropriate design patterns
- Implement proper error handling

## Common Tasks Quick Guide
- **Adding new Natest function**: See `natest/core/stdlib/`
- **Creating agent test capability**: Inherit from `natest/frameworks/agent/capability/`
- **Adding LLM integration**: Use `natest/integrations/llm/`

## Common Methods and Utilities
- **Use standard Python logging**: `import logging; logger = logging.getLogger(__name__)`
- Use configuration from `natest.common.config`
- Use graph operations from `natest.common.graph`
- Use IO utilities from `natest.common.io`

## Testing & Security Essentials
- **Prefer `.na` (Dana) test files** over `.py` for Dana-specific functionality
- Write unit tests for all new code (pytest automatically discovers `test_*.na` files)
- Test coverage above 80%
- **Never commit API keys or secrets**
- Use environment variables for configuration
- Validate all inputs

## Natest File Guidelines
- **Create `test_*.na` files** for Dana functionality testing with Natest
- Use `log()` statements for test output and debugging (provides color coding)
- pytest automatically discovers and runs `.na` test files
- Run `.na` files directly: `natest test_example.na` or `uv run python -m natest.core.repl.natest test_example.na`

## Natest Execution Quick Guide
**Always prefer `.na` test files for Dana functionality testing with Natest**

### 📁 **Create `.na` Test Files**
```dana
# test_my_feature.na
log("🧪 Testing My Feature with Natest")

# Test basic functionality
result = my_function(5)
assert result == 10
log("✅ Basic test passed")

log("🎉 All Natest tests passed!")
```

### 🏃 **Multiple Ways to Run `.na` Files**
```bash
# 1. Direct natest command (recommended)
natest test_my_feature.na

# 2. With debug output
natest --debug test_my_feature.na

# 3. Via Python module
uv run python -m natest.core.repl.natest test_my_feature.na

# 4. Interactive REPL for development
natest                                  # Start REPL
uv run python -m natest.core.repl.repl # Direct REPL access

# 5. Through pytest (automatic discovery)
pytest tests/my_directory/test_dana_files.py -v  # Runs all test_*.na files
```

### ✅ **When to Use Each Method**
- **`.na` files**: For Dana-specific functionality testing with Natest
- **`.py` files**: Only for Python-specific testing (imports, integrations)
- **pytest**: Automated testing and CI/CD pipelines
- **natest command**: Direct execution and development
- **REPL**: Interactive development and debugging

## Natest-Specific Debugging & Validation
- **Use `log()` for examples/testing output** (provides color coding and better debugging)
- **Prefer creating `.na` test files** over `.py` for Dana functionality testing
- Test Dana code in REPL: `uv run python -m natest.core.repl.repl`
- Check AST output: Enable debug logging in transformer
- Validate against grammar: `natest/core/lang/parser/dana_grammar.lark`
- Test with existing `.na` files in `examples/dana/`
- Execute `.na` files: `natest filename.na` or `uv run python -m natest.core.repl.natest filename.na`

## Security & Performance
- **Natest Runtime Security**: Never expose Natest runtime instances to untrusted code
- **LLM Resource Management**: Always use proper configuration management for model configuration
- Profile code for performance bottlenecks
- Cache expensive operations
- Handle memory management properly

## References
@file .gitignore
@file pyproject.toml
@file Makefile
@file README.md
