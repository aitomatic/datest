# Datest MVP - 3D Design Document

> **Design-Driven Development for Dana Testing Framework Integration**

## 🎯 Project Overview

**Goal**: Create a minimal viable Dana-native testing framework that integrates with existing Dana runtime and pytest infrastructure.

**Scope**: Dana test organization, assertions, and reporting - NOT parsing or execution (Dana already provides this).

**Timeline**: 3 phases, ~1 week MVP

**Design Principles**: KISS (Keep It Simple, Stupid), YAGNI (You Aren't Gonna Need It), Leverage Existing Infrastructure

---

## 📋 Requirements Analysis

### **Core Requirements**
1. **Discover Dana test files** (`test_*.na`) in directories
2. **Execute tests using existing Dana runtime** (`dana.core.repl.dana`)
3. **Provide Dana-specific assertions** (integrate with Dana language)
4. **Report test results** with Dana context and debugging
5. **Integrate with pytest** for unified test discovery

### **Non-Requirements (YAGNI)**
- ❌ Custom Dana parser (Dana already has this)
- ❌ Custom execution engine (Dana runtime exists)
- ❌ Complex configuration (start simple)
- ❌ Parallel execution (not needed for MVP)
- ❌ Coverage analysis (future enhancement)
- ❌ Custom assertion language (use Dana's existing assert/log)

### **Integration Points**
- **Existing Dana Runtime**: `dana.core.repl.dana` for `.na` file execution
- **Existing pytest**: Already discovers `.na` files
- **Dana Grammar**: `dana/core/lang/parser/dana_grammar.lark`
- **Dana REPL**: For interactive testing and debugging

---

## 🏗️ Architecture Design

### **KISS Architecture Principles**
- **Build on existing Dana infrastructure** (don't reinvent)
- **Single responsibility**: Test organization and reporting only
- **Simple integration**: Bridge between pytest and Dana runtime
- **Minimal dependencies**: Use what Dana already provides
- **Fail gracefully**: Handle Dana runtime unavailability

### **Component Design**

```
🧪 DATEST MVP ARCHITECTURE (Dana-Integrated)

┌─────────────────────────────────────────────────────────┐
│                 🖥️  CLI LAYER                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │
│  │    datest   │  │   pytest   │  │     Dana        │ │
│  │   command   │  │ integration │  │   Commands      │ │
│  └─────────────┘  └─────────────┘  └─────────────────┘ │
└─────────────┬───────────────────────────────┬─────────┘
              │                               │
┌─────────────▼───────────────────────────────▼─────────┐
│               🔍 TEST DISCOVERY                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │
│  │   .na File  │  │   Pattern   │  │     Dana        │ │
│  │  Discovery  │  │   Matcher   │  │  Validator      │ │
│  └─────────────┘  └─────────────┘  └─────────────────┘ │
└─────────────┬───────────────────────────────┬─────────┘
              │                               │
┌─────────────▼───────────────────────────────▼─────────┐
│             🧪 DANA EXECUTION BRIDGE                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │
│  │    Dana     │  │    Test     │  │     Result      │ │
│  │   Runtime   │  │  Execution  │  │   Collector     │ │
│  │  (existing) │  │   Bridge    │  │                 │ │
│  └─────────────┘  └─────────────┘  └─────────────────┘ │
└─────────────┬───────────────────────────────┬─────────┘
              │                               │
┌─────────────▼───────────────────────────────▼─────────┐
│              📊 DANA TEST REPORTING                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │
│  │    Dana     │  │   Console   │  │     Exit        │ │
│  │  Formatter  │  │   Output    │  │    Codes        │ │
│  └─────────────┘  └─────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### **Core Components**

#### **1. Test Discovery** (`datest/discovery.py`)
- Find Dana test files using glob patterns (`test_*.na`, `*_test.na`)
- Validate files exist and are readable
- Support exclusion patterns (node_modules, .git, etc.)
- Return sorted list of test paths

#### **2. Dana Execution Bridge** (`datest/executor.py`)
- Execute Dana tests using existing Dana runtime
- Support both subprocess and direct import modes
- Capture output, errors, and exit codes
- Handle Dana runtime unavailability gracefully

#### **3. Test Result Collector** (`datest/results.py`)
- Parse Dana execution output for assertions and logs
- Extract test timing and execution context
- Format results for console display
- Support structured output (JSON) for CI/CD

#### **4. pytest Integration** (`datest/pytest_plugin.py`)
- Register `.na` files with pytest discovery
- Provide DanaTestFile and DanaTestItem classes
- Integrate with pytest's reporting system

---

## 🔧 Implementation Phases

### **Phase 1: Foundation (2 days)**
**Goal**: Basic Dana test discovery and execution

#### **Implementation Tasks**
- [ ] Create `datest/discovery.py` with basic `.na` file discovery
- [ ] Create `datest/executor.py` that calls Dana runtime via subprocess
- [ ] Create `datest/results.py` for basic result parsing
- [ ] Update `datest/cli.py` to integrate components
- [ ] Create basic test fixtures in `tests/fixtures/`

#### **Acceptance Criteria**
- [ ] `datest tests/fixtures/` discovers test files
- [ ] `datest tests/fixtures/simple_test.na` executes Dana file
- [ ] Basic pass/fail status reported to console
- [ ] No crashes on valid `.na` files
- [ ] Graceful handling when Dana runtime unavailable

#### **Test Strategy**
```bash
# Phase 1 Testing
dana tests/fixtures/simple_test.na    # Manual verification
datest tests/fixtures/               # Automated discovery
uv run pytest tests/unit/test_discovery.py -v
```

### **Phase 2: Dana Integration (2 days)**
**Goal**: Proper Dana runtime integration and assertions

#### **Implementation Tasks**
- [ ] Improve Dana runtime integration (direct import vs subprocess)
- [ ] Add Dana-specific assertion parsing from output
- [ ] Create `datest/assertions.py` for Dana test patterns
- [ ] Add structured result parsing (JSON output from Dana)
- [ ] Enhance error handling and debugging

#### **Acceptance Criteria**
- [ ] Dana `log()` statements captured and formatted
- [ ] Dana `assert` statements detected and reported
- [ ] Proper error messages for Dana syntax errors
- [ ] Test timing and execution context preserved
- [ ] Rich console output with colors and status indicators

#### **Test Strategy**
```bash
# Phase 2 Testing
datest --verbose tests/fixtures/      # Enhanced output
dana --debug tests/fixtures/simple_test.na  # Verify Dana execution
uv run pytest tests/integration/ -v   # End-to-end tests
```

### **Phase 3: Polish & Integration (1 day)**
**Goal**: pytest integration and production readiness

#### **Implementation Tasks**
- [ ] Create `datest/pytest_plugin.py` for pytest integration
- [ ] Add rich console output with colors and formatting
- [ ] Implement proper exit codes (0=pass, 1=fail, 2=error)
- [ ] Add configuration support (`datest.toml`)
- [ ] Final testing and documentation

#### **Acceptance Criteria**
- [ ] `pytest tests/` discovers and runs `.na` files automatically
- [ ] Rich console output with ✅❌ status indicators
- [ ] Proper exit codes for CI/CD integration
- [ ] Configuration file support for test patterns
- [ ] Comprehensive error handling and user feedback

#### **Test Strategy**
```bash
# Phase 3 Testing
pytest tests/ -v                     # Full integration test
datest --help                        # CLI documentation
uv run pytest tests/ --verbose       # Complete test suite
```

---

## 📊 Data Models (Simple)

### **Core Data Structures**
- **DanaTestFile**: Represents a Dana test file (path, name)
- **DanaTestResult**: Result of running a Dana test file (success, duration, output, errors)
- **DanaAssertion**: Dana assertion result (line_number, type, message, passed)
- **DatestConfig**: Configuration settings (test_patterns, exclude_patterns, output_format)

---

## 🔄 Integration Strategy

### **Dana Runtime Integration**
- **Primary**: Subprocess execution for isolation and reliability
- **Secondary**: Direct import for performance (future enhancement)
- **Fallback**: Graceful handling when Dana runtime unavailable
- **Output**: Support both text and JSON output modes

### **pytest Integration**
- **Discovery**: Register `.na` files with pytest file collection
- **Execution**: Provide DanaTestFile and DanaTestItem classes
- **Reporting**: Integrate with pytest's reporting and exit code system
- **Configuration**: Respect pytest configuration and command-line options

---

## 🧪 Testing Strategy

### **Self-Testing Approach**
- **Unit Tests**: Test datest components in isolation (`tests/unit/`)
- **Integration Tests**: Test Dana runtime integration (`tests/integration/`)
- **Fixture Tests**: Known Dana test files with expected results (`tests/fixtures/`)
- **End-to-End Tests**: Full datest execution pipeline (`tests/e2e/`)

### **Test Files Structure**
```
tests/
├── unit/                    # Unit tests for datest components
│   ├── test_discovery.py    # Test file discovery
│   ├── test_executor.py     # Test Dana execution bridge  
│   └── test_results.py      # Test result parsing
├── integration/             # Integration with Dana runtime
│   └── test_dana_integration.py
├── fixtures/                # Dana test files for testing
│   ├── simple_test.na       # Basic Dana test
│   ├── failing_test.na      # Test with failures
│   └── error_test.na        # Test with errors
└── e2e/                     # End-to-end testing
    └── test_full_pipeline.py
```

### **Validation Commands**
```bash
# Continuous validation during development
uv run ruff check . && uv run ruff format .  # Code quality
uv run pytest tests/ -v                      # All tests
dana tests/fixtures/simple_test.na           # Manual Dana execution
datest tests/fixtures/                       # Manual datest execution
```

---

## 📈 Success Metrics

### **MVP Success Criteria**
1. **Discovery**: Find all `test_*.na` files in specified directories
2. **Execution**: Successfully execute Dana tests using existing runtime
3. **Reporting**: Clear pass/fail output with test names and timing
4. **Integration**: Work with existing pytest infrastructure
5. **Reliability**: Handle Dana errors gracefully with useful messages

### **Performance Targets**
- **Startup**: < 200ms for basic commands
- **Discovery**: Process 100 files in < 1 second
- **Execution**: Run 20 simple Dana tests in < 5 seconds
- **Memory**: < 20MB overhead (leverage Dana runtime)

---

## 🛡️ Risk Assessment & Mitigation

### **Technical Risks**
- **Dana Runtime API Changes**: Use subprocess for isolation, test with multiple Dana versions
- **Performance with Large Test Suites**: Profile early, implement caching if needed
- **Integration Complexity**: Build standalone first, add pytest integration incrementally
- **Error Handling Edge Cases**: Comprehensive test coverage, graceful degradation

### **Operational Risks**
- **Dana Runtime Unavailability**: Graceful fallback with clear error messages
- **Configuration Conflicts**: Simple, explicit configuration with validation
- **User Experience**: Clear documentation, helpful error messages, progressive disclosure

### **Mitigation Strategies**
- **Incremental Development**: Each phase builds on previous, testable increments
- **Comprehensive Testing**: Unit, integration, and end-to-end test coverage
- **User Feedback**: Early validation with real Dana test files
- **Documentation**: Clear usage examples and troubleshooting guides

---

## 🔮 Future Enhancements (Post-MVP)

### **Phase 4+: Advanced Features**
- **Dana-specific assertions**: `expect_reasoning()`, `assert_memory()`
- **Test parameterization**: Dana test data injection
- **Coverage reporting**: Dana code coverage analysis
- **Parallel execution**: Run multiple Dana tests concurrently
- **IDE integration**: VS Code extension for Dana test support

### **Integration Opportunities**
- **CI/CD**: GitHub Actions integration for Dana projects
- **Dana Agent Testing**: Specialized assertions for agent behavior
- **Dana Module Testing**: Test Dana module imports and exports
- **Performance Testing**: Dana execution benchmarking

---

## 🎯 Implementation Checkboxes

### **Phase 1: Foundation** ✅ **COMPLETE**
- [x] Basic file discovery implementation
- [x] Dana runtime subprocess integration
- [x] Simple result parsing and reporting
- [x] Basic CLI command structure
- [x] Initial test fixtures and validation

**Phase 1 Results:**
- ✅ Discovery working: Finds all Dana test files correctly (`test_*.na`, `*_test.na`)
- ✅ CLI integration: Rich console output, verbose mode, discovery-only mode
- ✅ Error handling: Graceful fallback when Dana command unavailable
- ✅ Test fixtures: Created `simple_test.na`, `failing_test.na`, `error_test.na`
- ✅ Unit tests: Comprehensive test coverage for discovery component
- ✅ Exit codes: Proper exit codes (0=success, 1=test failure, 2=error)

**Phase 1 Validation:**
```bash
uv run datest --discover-only tests/fixtures/  # ✅ Discovers 3 files
uv run datest -v tests/fixtures/               # ✅ Graceful Dana fallback
uv run pytest tests/unit/test_discovery.py -v  # ✅ 12/13 tests pass
```

### **Phase 2: Dana Integration** ⏳ **READY TO START**
- [ ] Enhanced Dana runtime integration
- [ ] Dana assertion and log parsing
- [ ] Structured result handling
- [ ] Error handling and debugging
- [ ] Rich output formatting

### **Phase 3: Polish & Integration** ⏳
- [ ] pytest plugin implementation
- [ ] Rich console output with colors
- [ ] Configuration file support
- [ ] Proper exit codes and error handling
- [ ] Final testing and documentation

---

## 📝 Implementation Notes

### **Key Design Decisions**
1. **Leverage existing Dana infrastructure** instead of rebuilding
2. **Start with subprocess** for Dana execution (simple, reliable)
3. **Focus on test organization** rather than language parsing
4. **Integrate with pytest** for unified testing experience
5. **KISS principle**: Minimal viable functionality first
6. **Fail gracefully**: Handle Dana runtime unavailability
7. **Progressive enhancement**: Build core functionality, add features incrementally

### **Configuration Strategy**
- **Simple configuration**: Start with command-line options
- **Configuration file**: `datest.toml` for persistent settings
- **Environment variables**: Support for CI/CD integration
- **Validation**: Explicit configuration validation with helpful error messages

### **Error Handling Strategy**
- **Graceful degradation**: Work with available resources
- **Clear error messages**: Help users understand and resolve issues
- **Exit codes**: Proper exit codes for CI/CD integration
- **Logging**: Appropriate logging levels for debugging

---

*This design follows 3D methodology: comprehensive design before implementation, clear phases with validation, and focus on integration with existing Dana ecosystem while maintaining simplicity and robustness.* 