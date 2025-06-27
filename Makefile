PYTHON=python3

.PHONY: fmt lint test

fmt:
	ruff check src/ tests/ --fix --unsafe-fixes
	ruff format src/ tests/

lint:
	ruff check src/ tests/
	mypy src/ tests/

test:
	pytest 