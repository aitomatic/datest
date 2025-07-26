# Linting Configuration Consistency

This document describes the comprehensive linting configuration implemented across all development environments for the Datest project.

## 🎯 Overview

We have implemented a **consistent linting configuration** across all environments to ensure that critical code quality issues (E722, F821) are caught and reported consistently, regardless of where code is being developed or checked.

## ✅ Critical Rules Implemented

### **Blocking Rules (E722, F821)**
- **E722**: Do not use bare `except` - catches dangerous exception handling
- **F821**: Undefined name - catches typos and missing imports

### **Important Rules (F841, B017)**
- **F841**: Local variable assigned but never used
- **B017**: Use `assert` in tests only

## 🔧 Configuration Files Updated

### **1. Core Configuration**
- ✅ `pyproject.toml` - Main Ruff configuration with critical rules
- ✅ `.pre-commit-config.yaml` - Pre-commit hooks with local critical checks
- ✅ `.github/workflows/lint.yml` - GitHub CI with staged linting
- ✅ `.vscode/settings.json` - IDE linting settings
- ✅ `.vscode/settings.json.example` - Template for new developers
- ✅ `Makefile` - Local development commands

### **2. File Scope Consistency**
All environments now use the same file scope:
```bash
datest/ tests/  # Consistent across all tools
```

**Never used:**
- ❌ `ruff check .` (includes too many files)
- ❌ `ruff check *.py` (misses subdirectories)

## 🚀 Environment-Specific Configurations

### **GitHub CI (`.github/workflows/lint.yml`)**
```yaml
- name: Critical checks (E722, F821)
  run: ruff check datest/ tests/ --select=E722,F821

- name: Important checks (F841, B017)
  run: ruff check datest/ tests/ --select=F841,B017

- name: Style checks
  run: ruff check datest/ tests/ --select=E,F,W,UP
```

### **Pre-commit Hooks (`.pre-commit-config.yaml`)**
```yaml
- repo: local
  hooks:
    - id: ruff-critical
      name: Critical lint checks (E722, F821)
      entry: ruff check datest/ tests/ --select=E722,F821
      language: system
      types: [python]
      pass_filenames: false
      always_run: true

    - id: ruff-important
      name: Important lint checks (F841, B017)
      entry: ruff check datest/ tests/ --select=F841,B017
      language: system
      types: [python]
      pass_filenames: false
      always_run: true
```

### **VS Code Settings (`.vscode/settings.json`)**
```json
{
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.linting.pylint": false,
  "python.linting.flake8": false,
  "python.linting.mypy": false,
  "python.linting.lintOnSave": true,
  "python.linting.ruffArgs": ["--select=E722,F821,F841,B017", "--exclude=*.na"],
  "python.analysis.typeCheckingMode": "strict",
  "python.analysis.diagnosticSeverityOverrides": {
    "reportUndefinedVariable": "warning",
    "reportMissingImports": "warning",
    "reportGeneralTypeIssues": "warning"
  }
}
```

### **Makefile Targets**
```makefile
lint: ## Check code style and quality
 @echo "🔍 Running linting checks..."
 @echo "  Critical checks (E722, F821)..."
 ruff check datest/ tests/ --select=E722,F821
 @echo "  Important checks (F841, B017)..."
 ruff check datest/ tests/ --select=F841,B017
 @echo "  Style checks..."
 ruff check datest/ tests/ --select=E,F,W,UP

lint-critical: ## Run critical lint checks (E722, F821)
 @echo "🔍 Running critical lint checks..."
 ruff check datest/ tests/ --select=E722,F821

lint-important: ## Run important lint checks (F841, B017)
 @echo "🔍 Running important lint checks..."
 ruff check datest/ tests/ --select=F841,B017

ci-check: lint-critical test ## Run CI checks locally
 @echo "✅ CI checks completed!"
```

## 🧪 Validation Commands

### **Local Development**
```bash
# Run critical checks only
make lint-critical

# Run important checks only
make lint-important

# Run all linting checks
make lint

# Run CI checks locally
make ci-check

# Run pre-commit hooks
pre-commit run --all-files
```

### **Verification Tests**
```bash
# Test critical rules (should fail with intentional errors)
ruff check test_file.py --select=E722,F821

# Test important rules (should fail with intentional errors)
ruff check test_file.py --select=F841,B017
```

## 🔍 Debugging Inconsistencies

### **If errors appear in CI but not locally:**

1. **Check file scope:** Ensure both use `datest/ tests/`
2. **Check rule selection:** Ensure both use `--select=E722,F821`
3. **Check IDE settings:** Verify Ruff is enabled and configured
4. **Check pre-commit:** Ensure local hook runs the same command
5. **Check Makefile:** Verify targets match CI commands exactly

### **If IDE doesn't show errors:**

1. **Check Python extension:** Ensure Ruff extension is installed
2. **Check settings.json:** Verify `python.linting.ruffEnabled: true`
3. **Check ruffArgs:** Ensure they match CI `--select` and `--exclude`
4. **Reload VS Code:** Sometimes needed after config changes
5. **Check language server:** Restart Python language server

## 📋 Maintenance Checklist

**After any linting configuration changes:**

- [ ] Update `pyproject.toml`
- [ ] Update `.pre-commit-config.yaml`
- [ ] Update `.github/workflows/lint.yml`
- [ ] Update `.vscode/settings.json`
- [ ] Update `.vscode/settings.json.example`
- [ ] Update `Makefile` targets
- [ ] Test locally with `make ci-check`
- [ ] Test pre-commit hooks
- [ ] Verify IDE shows errors correctly
- [ ] Commit and push changes
- [ ] Verify CI passes

## 🎉 Benefits Achieved

1. **Consistent Error Detection**: E722 and F821 errors are caught everywhere
2. **Staged Linting**: Critical issues fail fast, less critical issues are reported
3. **IDE Integration**: Real-time error reporting in VS Code/Cursor
4. **CI/CD Alignment**: Local and CI environments use identical checks
5. **Developer Experience**: Clear, actionable error messages
6. **Maintainability**: Single source of truth for linting rules

## 🚨 Common Pitfalls Avoided

**❌ Don't:**
- Use different `--select` rules in different environments
- Use different file scopes (`datest/` vs `.`)
- Suppress F821 in `pyproject.toml` ignore list
- Use `python.analysis.typeCheckingMode: "basic"` in IDE
- Set diagnostic overrides to `"none"` for undefined variables

**✅ Do:**
- Use identical Ruff commands across all environments
- Keep `F821` in the select list (not ignore)
- Use `"strict"` type checking in IDE
- Set diagnostic overrides to `"warning"` for undefined variables

## 📊 Current Status

- ✅ **Critical Rules (E722, F821)**: Implemented and tested
- ✅ **Important Rules (F841, B017)**: Implemented and tested
- ✅ **Style Rules (E, F, W, UP)**: Implemented and tested
- ✅ **All Environments**: Consistent configuration
- ✅ **Pre-commit Hooks**: Working correctly
- ✅ **CI/CD Pipeline**: Aligned with local development
- ✅ **IDE Integration**: Real-time error reporting

The linting configuration is now **production-ready** and ensures consistent code quality across all development environments. 