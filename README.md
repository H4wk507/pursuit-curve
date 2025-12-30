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

The project is organized into several directories, each with a specific purpose.

```
.
├── pursuit_curve/
│   ├── common/           # Shared types and simulation framework
│   ├── d2/               # 2D pursuit algorithms (discrete and continuous)
│   ├── d3/               # 3D pursuit algorithms (continuous)
│   ├── dn/               # N-dimensional pursuit algorithms (continuous)
│   ├── sphere/           # Pursuit algorithms on a sphere
│   ├── torus/            # Pursuit algorithms on a torus
│   └── examples/         # Example scripts demonstrating different simulations
├── scripts/              # Scripts for generating figures and values for documentation
├── figures/              # Output directory for generated figures
├── main.ipynb            # Jupyter Notebook for experimentation
├── dokumentacja.tex      # LaTeX source for the project documentation
├── Makefile              # Makefile with commands for linting, formatting, etc.
└── pyproject.toml        # Project configuration and dependencies
```

## Opis Projektu

Ten projekt eksploruje i implementuje różne algorytmy do rozwiązywania problemów związanych z krzywymi pościgowymi. Dostarcza framework do symulacji scenariuszy pościgowych w różnych wymiarach i na różnych powierzchniach geometrycznych.

## Kluczowe Funkcjonalności

- **Wiele strategii pościgu:**
  - Pościg bezpośredni (Direct Pursuit)
  - Pościg ze stałym namiarem (Constant Bearing)
  - Nawigacja proporcjonalna (Proportional Navigation)
  - Pościg cykliczny (Cyclic Pursuit)
- **Wsparcie dla różnych geometrii:**
  - Przestrzeń Euklidesowa 2D, 3D i n-wymiarowa
  - Geometria sferyczna
  - Geometria torusa
- **Elastyczny framework symulacji:** Oparty na `scipy.integrate.solve_ivp` z wykrywaniem zdarzeń.
- **Wizualizacja i animacja:** Animacje trajektorii w czasie rzeczywistym przy użyciu `matplotlib`.

## Uruchamianie Przykładów

Przykładowe skrypty znajdują się w katalogu `pursuit_curve/examples/`. Aby uruchomić jeden z nich, użyj `uv run`:

```bash
uv run python pursuit_curve/examples/2d_continuous_direct_pursuit_example.py
```

## Development

Projekt wykorzystuje `Makefile` do typowych zadań deweloperskich:

- `make lint`: Sprawdza jakość kodu za pomocą `ruff`.
- `make format`: Formatuje kod za pomocą `ruff`.
- `make clean`: Usuwa pliki cache.

## Generowanie Dokumentacji

Dokumentacja projektu jest pisana w LaTeX. Aby wygenerować plik PDF:

```bash
make tex
```

Wygenerowany plik `dokumentacja.pdf` pojawi się w głównym katalogu projektu.