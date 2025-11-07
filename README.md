## Setup

1. Install uv package manager.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Sync deps from the lockfile.

```bash
uv sync
```

3. Run Jupyter Notebook from the commandline

```bash
uv run --with jupyter jupyter notebook
```

or just inside VSCode with correct venv.

## Project Structure
