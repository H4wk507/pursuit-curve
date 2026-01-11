# Krzywe Pościgu

Ten projekt eksploruje i implementuje różne algorytmy do rozwiązywania problemów związanych z krzywymi pościgu. Dostarcza framework do symulacji scenariuszy pościgu w różnych wymiarach i na różnych powierzchniach geometrycznych.

## Instalacja

1. Zainstaluj menedżer pakietów `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Zsynchronizuj zależności z pliku lockfile:

```bash
uv sync
```

3. Uruchom Jupyter Notebook z linii poleceń:

```bash
uv run --with jupyter jupyter notebook
```

lub bezpośrednio w VSCode z odpowiednim środowiskiem wirtualnym.

## Struktura Projektu

Projekt jest zorganizowany w kilka katalogów, z których każdy ma określone przeznaczenie:

```
.
├── pursuit_curve/
│   ├── common/           # Współdzielone typy i framework symulacji
│   ├── d2/               # Algorytmy pościgu 2D (dyskretne i ciągłe)
│   ├── d3/               # Algorytmy pościgu 3D (ciągłe)
│   ├── dn/               # Algorytmy pościgu n-wymiarowe (ciągłe)
│   ├── sphere/           # Algorytmy pościgu na sferze
│   ├── torus/            # Algorytmy pościgu na torusie
│   └── examples/         # Przykładowe skrypty demonstracyjne
├── docs/                 # Pliki dokumentacji
│   ├── dokumentacja.tex  # Źródło LaTeX dokumentacji projektu
│   ├── prezentacja.tex   # Źródło LaTeX prezentacji
│   ├── scripts/          # Skrypty do generowania figur i wartości
│   ├── figures/          # Katalog wyjściowy dla wygenerowanych figur
│   └── images/           # Obrazy do dokumentacji
├── playground.ipynb      # Notatnik Jupyter do eksperymentów
├── Makefile              # Makefile z poleceniami do lintowania, formatowania itp.
└── pyproject.toml        # Konfiguracja projektu i zależności
```

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

Przykładowe skrypty znajdują się w katalogu `pursuit_curve/examples/`. Aby uruchomić jeden z nich:

```bash
uv run python pursuit_curve/examples/2d_continuous_direct_pursuit_example.py
```

## Development

Projekt wykorzystuje `Makefile` do typowych zadań deweloperskich:

- `make lint` - sprawdza jakość kodu za pomocą `ruff`
- `make format` - formatuje kod za pomocą `ruff`
- `make clean` - usuwa pliki cache

## Generowanie Dokumentacji

Dokumentacja projektu jest pisana w LaTeX. Aby wygenerować pliki PDF:

```bash
make tex   # kompiluje dokumentację
make prez  # kompiluje prezentację
```

Wygenerowane pliki PDF pojawią się w katalogu `docs/`.
