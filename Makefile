.PHONY: run install clean check  runner
.DEFAULT_GOAL:=runner

run: install
	cd src; python3 runner_builder.py

install: pyproject.toml
	poetry install --no-root

clean:
	rm -rf `find . -type d -name __pycache__`
	rm -rf .ruff_cache

check: 
	flake8 src/
	ruff check src/

runner: check run clean