install:
	uv add --dev flake8 mypy

run:
	uv run python3 main.py ${MAP}

debug:
	uv run python -m pdb main.py ${MAP}

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

lint: install
	uv run flake8 . -v --exclude=.venv --ignore=
	uv run mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--explicit-package-bases \
		--exclude '^(venv|\.venv|env)/'

lint-strict:
	uv run flake8 --exclude=.venv
	uv run mypy . \
		--strict \
		--explicit-package-bases \
		--exclude '^(venv|\.venv|env)/'

.PHONY: install run debug clean lint