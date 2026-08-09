.PHONY: install test lint run clean

install:
	./install.sh

test:
	./test.sh

lint:
	flake8 . --max-line-length=120 --extend-ignore=E203,W503
	black --check --line-length 120 .
	isort --check-only .

run:
	./prime-agent.sh

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache htmlcov .coverage
