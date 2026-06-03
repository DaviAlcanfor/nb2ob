run:
	uv run main.py

install:
	uv sync

lint:
	uv run ruff check .