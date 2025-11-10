clean:
	find . \( -type d -name __pycache__ -o -name "*.pyc" -o -type d -name .mypy_cache -o -type d -name .ruff_cache \) -prune -exec rm -rfv {} \;

lint: 
	ruff check .

format:
	ruff format .