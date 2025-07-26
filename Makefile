# Makefile - Datest Development Commands
# Copyright © 2025 Aitomatic, Inc. Licensed under the MIT License.

# =============================================================================
# Datest Development Makefile - Essential Commands Only
# =============================================================================

# Modern dependency management - using uv (with pip fallback)

# Default target
.DEFAULT_GOAL := help

# All targets are phony (don't create files)
.PHONY: help help-more quickstart install setup-dev sync test clean clean-datest lint format fix check mypy \
	install-llm docs-serve docs-build docs-deps test-fast test-cov dev security validate-config check-structure release-check \
	sync-dev lock-deps check-uv build dist check-dist publish run datest-test

# =============================================================================
# Help & Quick Start
# =============================================================================

help: ## Show essential Datest commands
	@echo ""
	@echo "\033[1m\033[34mDatest Development Commands\033[0m"
	@echo "\033[1m======================================\033[0m"
	@echo ""
	@echo "\033[1mGetting Started:\033[0m"
	@echo "  \033[36mquickstart\033[0m      🚀 Get Datest running in 30 seconds!"
	@echo "  \033[36minstall\033[0m         📦 Install package and dependencies (uv preferred)"
	@echo "  \033[36msetup-dev\033[0m       🛠️  Install with development dependencies"
	@echo "  \033[36msync\033[0m            ⚡ Fast dependency sync with uv"
	@echo ""
	@echo "\033[1mUsing Datest:\033[0m"
	@echo "  \033[36mdatest\033[0m          🚀 Start the Datest framework"
	@echo "  \033[36mtest\033[0m            🧪 Run all tests"
	@echo "  \033[36mdatest-test\033[0m     🧪 Run datest-specific tests and validation"
	@echo ""
	@echo "\033[1mCode Quality:\033[0m"
	@echo "  \033[36mlint\033[0m            🔍 Check code style and quality"
	@echo "  \033[36mformat\033[0m          ✨ Format code automatically"
	@echo "  \033[36mfix\033[0m             🔧 Auto-fix all fixable code issues"
	@echo ""
	@echo "\033[1mOptional Extensions:\033[0m"
	@echo "  \033[36minstall-llm\033[0m     🤖 Install LLM integration for testing reason() calls"
	@echo ""
	@echo "\033[1mMaintenance:\033[0m"
	@echo "  \033[36mclean\033[0m           🧹 Clean build artifacts and caches"
	@echo ""
	@echo "\033[33mTip: Run 'make help-more' for additional commands\033[0m"
	@echo "\033[33mNote: Install uv for faster dependency management: pip install uv\033[0m"
	@echo ""

help-more: ## Show all available commands including advanced ones
	@echo ""
	@echo "\033[1m\033[34mDatest Development Commands (Complete)\033[0m"
	@echo "\033[1m===========================================\033[0m"
	@echo ""
	@echo "\033[1mGetting Started:\033[0m"
	@awk 'BEGIN {FS = ":.*?## "} /^(quickstart|install|setup-dev|sync|sync-dev|lock-deps|check-uv).*:.*?## / {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "\033[1mUsing Dana:\033[0m"
	@awk 'BEGIN {FS = ":.*?## "} /^(dana|test|run).*:.*?## / {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "\033[1mAdvanced Testing:\033[0m"
	@awk 'BEGIN {FS = ":.*?## MORE: "} /^test.*:.*?## MORE:/ {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "\033[1mCode Quality:\033[0m"
	@awk 'BEGIN {FS = ":.*?## "} /^(lint|format|check|fix|mypy).*:.*?## / {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "\033[1mOptional Extensions:\033[0m"
	@awk 'BEGIN {FS = ":.*?## "} /^(install-llm).*:.*?## / {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "\033[1mDevelopment & Release:\033[0m"
	@awk 'BEGIN {FS = ":.*?## MORE: "} /^(update-deps|dev|security|validate-config|release-check|docs-build|docs-deps).*:.*?## MORE:/ {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "\033[1mMaintenance:\033[0m"
	@awk 'BEGIN {FS = ":.*?## "} /^(clean|docs-serve).*:.*?## / {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""

quickstart: ## 🚀 QUICK START: Get Datest running in 30 seconds!
	@echo ""
	@echo "🚀 \033[1m\033[32mDatest Quick Start\033[0m"
	@echo "===================="
	@echo ""
	@echo "📦 Installing dependencies..."
	@if command -v uv >/dev/null 2>&1; then \
		uv pip install -e .; \
	else \
		echo "⚠️  uv not found, falling back to pip..."; \
		pip install -e .; \
	fi
	@echo "🔧 Setting up environment..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "📝 Created .env file from template"; \
	else \
		echo "📝 .env file already exists"; \
	fi
	@echo ""
	@echo "🎉 \033[1m\033[32mReady to go!\033[0m"
	@echo ""
	@echo "\033[1mNext: Add your API key to .env, then:\033[0m"
	@echo "  \033[36mmake datest\033[0m  # Start Datest framework"
	@echo "  \033[36mmake test\033[0m    # Run tests"
	@echo ""
	@echo "\033[33m💡 Tip: Run 'open .env' to edit your API keys\033[0m"
	@echo "\033[33m💡 For faster installs, install uv: pip install uv\033[0m"
	@echo ""

# =============================================================================
# Setup & Installation
# =============================================================================

install: ## Install package and dependencies
	@echo "📦 Installing dependencies..."
	@if command -v uv >/dev/null 2>&1; then \
		echo "⚡ Using uv for fast installation..."; \
		uv pip install -e .; \
	else \
		echo "⚠️  uv not found, using pip (install uv for faster builds: pip install uv)"; \
		pip install -e .; \
	fi

setup-dev: ## Install with development dependencies and setup tools
	@echo "🛠️  Installing development dependencies..."
	@if command -v uv >/dev/null 2>&1; then \
		echo "⚡ Using uv for fast installation..."; \
		uv pip install -e ".[dev]"; \
	else \
		echo "⚠️  uv not found, using pip (install uv for faster builds: pip install uv)"; \
		pip install -e ".[dev]"; \
	fi
	@echo "🔧 Setting up development tools..."
	pre-commit install
	@echo "✅ Development environment ready!"

sync: check-uv ## Fast dependency sync with uv
	@echo "⚡ Syncing dependencies with uv..."
	uv pip sync pyproject.toml

sync-dev: check-uv ## Fast sync with development dependencies
	@echo "⚡ Syncing development dependencies with uv..."
	uv pip install -e ".[dev]"

lock-deps: check-uv ## Generate/update dependency lock file
	@echo "🔒 Locking dependencies..."
	@if [ -f requirements.in ]; then \
		uv pip compile requirements.in -o requirements.txt; \
	else \
		echo "📝 No requirements.in found, using pyproject.toml"; \
		uv pip compile pyproject.toml -o requirements-lock.txt; \
	fi

check-uv: ## Check if uv is available
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "❌ uv not found!"; \
		echo "💡 Install with: pip install uv"; \
		echo "🌐 Or visit: https://docs.astral.sh/uv/"; \
		exit 1; \
	fi

install-llm: ## Install optional LLM integration for testing reason() calls
	@echo "🤖 Installing LLM integration..."
	@if command -v uv >/dev/null 2>&1; then \
		uv pip install -e ".[llm]"; \
	else \
		pip install -e ".[llm]"; \
	fi

# =============================================================================
# Usage
# =============================================================================

datest: ## Start the Datest framework
	@echo "🚀 Starting Datest framework..."
	datest

test: ## Run all tests
	@echo "🧪 Running tests..."
	pytest tests/

datest-test: ## Run datest-specific tests and validation
	@echo "🧪 Running Datest framework tests..."
	@echo "📋 Testing datest CLI..."
	@if command -v datest >/dev/null 2>&1; then \
		datest --help >/dev/null && echo "✅ datest CLI works"; \
	else \
		echo "⚠️  datest command not found, run 'make install' first"; \
	fi
	@echo "📋 Testing datest discovery..."
	@if [ -d tests/fixtures ]; then \
		echo "✅ Test fixtures directory found"; \
		ls tests/fixtures/*.na 2>/dev/null | wc -l | xargs echo "📁 Found .na test files:"; \
	else \
		echo "⚠️  No test fixtures directory found"; \
	fi
	@echo "📋 Running pytest with datest plugin..."
	pytest tests/ -v

# =============================================================================
# Code Quality
# =============================================================================

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

format: ## Format code automatically
	@echo "✨ Formatting code..."
	ruff format datest/ tests/

check: lint ## Run all code quality checks
	@echo "📝 Checking code formatting..."
	ruff format --check datest/ tests/
	@echo "✅ All quality checks completed!"

fix: ## Auto-fix all fixable code issues
	@echo "🔧 Auto-fixing code issues..."
	ruff check --fix datest/ tests/
	ruff format datest/ tests/
	@echo "🔧 Applied all auto-fixes!"

mypy: ## Run type checking
	@echo "🔍 Running type checks..."
	mypy datest/ tests/

ci-check: lint-critical test ## Run CI checks locally
	@echo "✅ CI checks completed!"

# =============================================================================
# Optional Extensions
# =============================================================================

# =============================================================================
# Maintenance & Documentation
# =============================================================================

clean: ## Clean build artifacts and caches
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .ruff_cache/ .mypy_cache/

clean-datest: ## Clean up datest directory (keeps datest)
	@echo "🧹 Cleaning up datest directory..."
	@if [ -d datest ]; then \
		echo "📁 Removing datest directory..."; \
		rm -rf datest/; \
		echo "✅ datest directory removed"; \
	else \
		echo "ℹ️  datest directory not found"; \
	fi

docs-serve: ## Serve documentation locally
	@echo "📚 Serving docs at http://localhost:8000"
	@if [ -f mkdocs.yml ]; then \
		mkdocs serve; \
	else \
		echo "❌ mkdocs.yml not found. Documentation not configured."; \
	fi

docs-build: ## MORE: Build documentation
	@echo "📖 Building documentation..."
	@if [ -f mkdocs.yml ]; then \
		mkdocs build; \
	else \
		echo "❌ mkdocs.yml not found. Documentation not configured."; \
	fi

docs-deps: ## MORE: Install documentation dependencies
	@echo "📚 Installing documentation dependencies..."
	@if command -v uv >/dev/null 2>&1; then \
		uv pip install -e ".[docs]"; \
	else \
		pip install -e ".[docs]"; \
	fi

# =============================================================================
# Advanced/Comprehensive Targets (shown in help-more)
# =============================================================================

test-fast: ## MORE: Run fast tests only
	@echo "⚡ Running fast tests..."
	pytest -m "not slow" tests/

test-cov: ## MORE: Run tests with coverage report
	@echo "📊 Running tests with coverage..."
	pytest --cov=datest --cov-report=html --cov-report=term tests/
	@echo "📈 Coverage report generated in htmlcov/"

dev: setup-dev check test-fast ## MORE: Complete development setup and verification
	@echo ""
	@echo "🎉 \033[1m\033[32mDevelopment environment is ready!\033[0m"
	@echo ""
	@echo "Next steps:"
	@echo "  • Run '\033[36mmake datest\033[0m' to start the Datest framework"
	@echo "  • Run '\033[36mmake test\033[0m' to run tests"
	@echo "  • Run '\033[36mmake check\033[0m' for code quality checks"
	@echo ""

security: ## MORE: Run security checks on codebase
	@echo "🔒 Running security checks..."
	@if command -v bandit >/dev/null 2>&1; then \
		bandit -r datest/ || echo "⚠️  Security issues found"; \
	else \
		echo "❌ bandit not available. Install with: pip install bandit"; \
	fi

validate-config: ## MORE: Validate project configuration files
	@echo "⚙️  Validating configuration..."
	@echo "📝 Checking pyproject.toml..."
	@python3 -c "import tomllib; tomllib.load(open('pyproject.toml','rb')); print('✅ pyproject.toml is valid')"
	@if [ -f dana_config.json ]; then \
		echo "📝 Checking dana_config.json..."; \
		python3 -c "import json; json.load(open('dana_config.json')); print('✅ dana_config.json is valid')"; \
	fi
	@if [ -f mkdocs.yml ]; then \
		echo "📝 Checking mkdocs.yml..."; \
		if [ -r mkdocs.yml ]; then \
			echo "✅ mkdocs.yml exists and is readable"; \
		else \
			echo "❌ mkdocs.yml exists but is not readable"; \
		fi; \
	fi

check-structure: ## MORE: Check project structure and setup
	@echo "🏗️  Checking project structure..."
	@echo "📁 Core directories:"
	@if [ -d datest ]; then echo "  ✅ datest/ - Main package directory"; else echo "  ❌ datest/ - Missing!"; fi
	@if [ -d tests ]; then echo "  ✅ tests/ - Test directory"; else echo "  ❌ tests/ - Missing!"; fi
	@if [ -d docs ]; then echo "  ✅ docs/ - Documentation directory"; else echo "  ❌ docs/ - Missing!"; fi
	@if [ -d examples ]; then echo "  ✅ examples/ - Examples directory"; else echo "  ❌ examples/ - Missing!"; fi
	@echo "📁 Key files:"
	@if [ -f pyproject.toml ]; then echo "  ✅ pyproject.toml - Project configuration"; else echo "  ❌ pyproject.toml - Missing!"; fi
	@if [ -f README.md ]; then echo "  ✅ README.md - Project documentation"; else echo "  ❌ README.md - Missing!"; fi
	@if [ -f datest/__init__.py ]; then echo "  ✅ datest/__init__.py - Package init"; else echo "  ❌ datest/__init__.py - Missing!"; fi
	@if [ -f datest/cli.py ]; then echo "  ✅ datest/cli.py - CLI interface"; else echo "  ❌ datest/cli.py - Missing!"; fi
	@echo "📁 Test fixtures:"
	@if [ -d tests/fixtures ]; then \
		echo "  ✅ tests/fixtures/ - Test fixtures directory"; \
		ls tests/fixtures/*.na 2>/dev/null | wc -l | xargs echo "    📄 .na test files:"; \
	else \
		echo "  ❌ tests/fixtures/ - Missing!"; \
	fi
	@echo "📁 Legacy cleanup:"
	@if [ -d datest ]; then echo "  ⚠️  datest/ - Legacy directory (run 'make clean-datest' to remove)"; else echo "  ✅ No legacy datest directory"; fi

release-check: clean check test-fast security validate-config ## MORE: Complete pre-release validation
	@echo ""
	@echo "🚀 \033[1m\033[32mRelease validation completed!\033[0m"
	@echo "=================================="
	@echo ""
	@echo "✅ Code quality checks passed"
	@echo "✅ Tests passed"
	@echo "✅ Security checks completed"
	@echo "✅ Configuration validated"
	@echo ""
	@echo "\033[33m🎯 Ready for release!\033[0m"
	@echo ""

# =============================================================================
# Package Building & Publishing
# =============================================================================

build: ## Build package distribution files
	@echo "📦 Building package..."
	python -m build

dist: clean build ## Clean and build distribution files
	@echo "✅ Distribution files ready in dist/"

check-dist: ## Validate built distribution files
	@echo "🔍 Checking distribution files..."
	twine check dist/*

publish: check-dist ## Upload to PyPI
	@echo "🚀 Publishing to PyPI..."
	twine upload --verbose dist/*
run: datest ## Alias for 'datest' command
