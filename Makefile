.PHONY: help test test-docker test-act test-all docker-build install lint format clean

help:
	@echo "Skill Doctor - Make Commands"
	@echo ""
	@echo "Testing:"
	@echo "  make test          - Run Python unit tests"
	@echo "  make test-docker   - Test Docker build and run"
	@echo "  make test-act      - Run GitHub Actions locally with Act"
	@echo "  make test-all      - Run all tests"
	@echo ""
	@echo "Development:"
	@echo "  make install       - Install dependencies"
	@echo "  make lint          - Run all linters"
	@echo "  make format        - Format code"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make clean         - Clean build artifacts"

test:
	@echo "Running Python unit tests..."
	uv run pytest --cov --cov-report=term

test-docker:
	@echo "Running Docker tests..."
	./scripts/test-docker-local.sh

test-act:
	@echo "Running GitHub Actions locally..."
	./scripts/test-with-act.sh

test-all: test test-docker
	@echo ""
	@echo "✅ All tests passed!"

docker-build:
	@echo "Building Docker image..."
	docker build -t skill-doctor:dev .

install:
	@echo "Installing dependencies..."
	uv sync --all-extras

lint:
	@echo "Running pre-commit checks..."
	uv run pre-commit run --all-files

format:
	@echo "Formatting code with pre-commit..."
	uv run pre-commit run --all-files

clean:
	@echo "Cleaning build artifacts..."
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
