.PHONY: run_builder run_inference install clean check  runner
.DEFAULT_GOAL:=runner_inference

run_builder: install
	cd src; python3 runner_builder.py

run_inference: install
	cd src; python3 runner_inference.py

install: pyproject.toml
	poetry install --no-root

clean:
	rm -rf `find . -type d -name __pycache__`
	rm -rf .ruff_cache

check: 
	flake8 src/
	ruff check src/

runner_builder: check run_builder clean
runner_inference: check run_inference clean