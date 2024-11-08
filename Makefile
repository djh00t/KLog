.PHONY: install develop test coverage clean build release

install:
	@echo "Installing dependencies with Poetry..."
	poetry install

develop:
	@echo "Setting up development environment..."
	poetry install --with dev

test:
	@echo "Running tests and uploading coverage to Codecov..."
	poetry run pytest --cov=klingon_log --cov-report=xml
	poetry run codecov

coverage:
	@echo "Generating detailed coverage report..."
	@make test
	@echo "Coverage report generated in htmlcov/index.html"
	@echo "Opening coverage report in browser..."
	@open htmlcov/index.html

clean:
	@echo "Cleaning up..."
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name "__pytest__" -exec rm -r {} +
	find . -type f -name "*.pyc" -exec rm -f {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +

build:
	@echo "Building the project..."
	poetry build

release:
	@echo "Releasing the project..."
	poetry publish
