.PHONY: install lint format typecheck test cov run-eneve clean

install:
	uv sync --extra dev

lint:
	uv run ruff check src/ tests/
	uv run ruff format --check src/ tests/

format:
	uv run ruff check --fix src/ tests/
	uv run ruff format src/ tests/

typecheck:
	uv run mypy src/solstein

test:
	uv run pytest -q

cov:
	uv run pytest --cov=solstein --cov-report=term-missing --cov-report=html

run-eneve:
	uv run solstein run --universe tests/fixtures/eneve.json --output out/

clean:
	rm -rf out/ .pytest_cache/ .ruff_cache/ htmlcov/ .coverage dist/ build/
	find . -type d -name __pycache__ -exec rm -rf {} +
