# Makefile - Natest Development Commands
# Copyright © 2025 Aitomatic, Inc. Licensed under the MIT License.

# =============================================================================
# Natest Development Makefile - Essential Commands Only
# =============================================================================

# Simplified dependency management - using standard pip

# Default target
.DEFAULT_GOAL := help

# All targets are phony (don't create files)
.PHONY: help help-more quickstart install setup-dev sync test dana clean lint format fix check mypy \
	install-ollama start-ollama install-vllm start-vllm install-vscode install-cursor install-vim install-emacs \
	docs-serve docs-build docs-deps test-fast test-cov update-deps dev security validate-config release-check

# =============================================================================
# Help & Quick Start
# =============================================================================

help: ## Show essential Natest commands
	@echo ""
	@echo "\033[1m\033[34mNatest Development Commands\033[0m"
	@echo "\033[1m======================================\033[0m"
	@echo ""
	@echo "\033[1mGetting Started:\033[0m"
	@echo "  \033[36mquickstart\033[0m      🚀 Get Natest running in 30 seconds!"
	@echo "  \033[36minstall\033[0m         📦 Install package and dependencies"
	@echo "  \033[36msetup-dev\033[0m       🛠️  Install with development dependencies"
	@echo ""
	@echo "\033[1mUsing Natest:\033[0m"
	@echo "  \033[36mnatest\033[0m          🚀 Start the Natest framework"
	@echo "  \033[36mtest\033[0m            🧪 Run all tests"
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
	@echo ""

help-more: ## Show all available commands including advanced ones
	@echo ""
	@echo "\033[1m\033[34mNatest Development Commands (Complete)\033[0m"
	@echo "\033[1m===========================================\033[0m"
	@echo ""
	@echo "\033[1mGetting Started:\033[0m"
	@awk 'BEGIN {FS = ":.*?## "} /^(quickstart|install|setup-dev|sync).*:.*?## / {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
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

quickstart: ## 🚀 QUICK START: Get Natest running in 30 seconds!
	@echo ""
	@echo "🚀 \033[1m\033[32mNatest Quick Start\033[0m"
	@echo "===================="
	@echo ""
	@echo "📦 Installing dependencies..."
	@pip install -e .
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
	@echo "  \033[36mmake natest\033[0m  # Start Natest framework"
	@echo "  \033[36mmake test\033[0m    # Run tests"
	@echo ""
	@echo "\033[33m💡 Tip: Run 'open .env' to edit your API keys\033[0m"
	@echo ""

# =============================================================================
# Setup & Installation
# =============================================================================

install: ## Install package and dependencies
	@echo "📦 Installing dependencies..."
	pip install -e .

setup-dev: ## Install with development dependencies and setup tools
	@echo "🛠️  Installing development dependencies..."
	pip install -e ".[dev]"
	@echo "🔧 Setting up development tools..."
	pre-commit install
	@echo "✅ Development environment ready!"

install-llm: ## Install optional LLM integration for testing reason() calls
	@echo "🤖 Installing LLM integration..."
	pip install -e ".[llm]"

# =============================================================================
# Usage
# =============================================================================

natest: ## Start the Natest framework
	@echo "🚀 Starting Natest framework..."
	natest

test: ## Run all tests
	@echo "🧪 Running tests..."
	pytest tests/

# =============================================================================
# Code Quality
# =============================================================================

lint: ## Check code style and quality
	@echo "🔍 Running linting checks..."
	ruff check .

format: ## Format code automatically
	@echo "✨ Formatting code..."
	ruff format .

check: lint ## Run all code quality checks
	@echo "📝 Checking code formatting..."
	ruff format --check .
	@echo "✅ All quality checks completed!"

fix: ## Auto-fix all fixable code issues
	@echo "🔧 Auto-fixing code issues..."
	ruff check --fix .
	ruff format .
	@echo "🔧 Applied all auto-fixes!"

mypy: ## Run type checking
	@echo "🔍 Running type checks..."
	mypy .

# =============================================================================
# Optional Extensions
# =============================================================================

install-llm: ## Install optional LLM integration for testing reason() calls
	@echo "🤖 Installing LLM integration..."
	pip install -e ".[llm]"

# =============================================================================
# Maintenance & Documentation
# =============================================================================

clean: ## Clean build artifacts and caches
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .ruff_cache/ .mypy_cache/

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
	pip install -e ".[docs]"

# =============================================================================
# Advanced/Comprehensive Targets (shown in help-more)
# =============================================================================

test-fast: ## MORE: Run fast tests only
	@echo "⚡ Running fast tests..."
	pytest -m "not slow" tests/

test-cov: ## MORE: Run tests with coverage report
	@echo "📊 Running tests with coverage..."
	pytest --cov=natest --cov-report=html --cov-report=term tests/
	@echo "📈 Coverage report generated in htmlcov/"

dev: setup-dev check test-fast ## MORE: Complete development setup and verification
	@echo ""
	@echo "🎉 \033[1m\033[32mDevelopment environment is ready!\033[0m"
	@echo ""
	@echo "Next steps:"
	@echo "  • Run '\033[36mmake natest\033[0m' to start the Natest framework"
	@echo "  • Run '\033[36mmake test\033[0m' to run tests"
	@echo "  • Run '\033[36mmake check\033[0m' for code quality checks"
	@echo ""

security: ## MORE: Run security checks on codebase
	@echo "🔒 Running security checks..."
	@if command -v bandit >/dev/null 2>&1; then \
		bandit -r natest/ || echo "⚠️  Security issues found"; \
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
		python3 -c "import yaml; yaml.safe_load(open('mkdocs.yml')); print('✅ mkdocs.yml is valid')"; \
	fi

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
run: natest ## Alias for 'natest' command
