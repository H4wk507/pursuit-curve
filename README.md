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

## TODO:

### Podstawy teoretyczne

1. Implementacja klasycznej krzywej pościgu
  - Zaimplementować rozwiązanie równań różniczkowych dla pojedynczego ścigającego i uciekającego
  - Cel poruszający się po linii prostej ze stałą prędkością
  - dx/dt = v * (target - position) / dist(target, position)

2. Analiza matematycznych strategii pościgu
  - [X] Pure pursuit (pościg bezpośredni) - kierunek wprost na cel
  - [X] Constant bearing (stały namiar) - prowadzi do logarytmicznej spirali
  - [X] Proporcjonalna nawigacja - kierunek proporcjonalny do zmiany kąta
  - Porównanie efektywności i czasu pościgu dla różnych strategii

3. Analiza optymalności trajektorii
  - Obliczanie długości krzywej pościgu (całka po krzywej)
  - Porównanie z długością najkrótszej ścieżki (odcinek)
  - Analiza czasu pościgu w funkcji parametrów
  - Obliczanie "kosztu" pościgu (np. energia, praca)

4. Krzywa pościgu dla celu po okręgu w 2D
  - Cel poruszający się po trajektorii kołowej
  - Porównanie rozwiązania numerycznego z analitycznym (jeśli istnieje)
  - Analiza spirali logarytmicznej jako przypadku szczególnego
  - Badanie wpływu prędkości obrotowej celu na kształt trajektorii


### Aspekty numeryczne

1. Implementacja metod numerycznych
  - Metoda Eulera (podstawowa)
  - Runge-Kutta 4 rzędu (RK4)
  - Opcjonalnie: metoda Adamsa-Bashfortha
  - Analiza błędu numerycznego dla każdej metody
  - Porównanie dokładności i czasu obliczeń

### Wizualizacja

1. Interaktywna animacja 2D
  - Animacja using matplotlib.animation lub plotly
  - Ślady trajektorii z efektem zanikania (fading trail)
  - Wizualizacja wektorów prędkości obu obiektów
  - Oznaczenia pozycji ścigającego i uciekającego
  - Kontrolki start/stop/reset

2. Interaktywny dashboard z parametrami
  - ipywidgets w Jupyter Notebook
  - Slidery do parametrów: prędkość ścigającego, prędkość celu, strategia pościgu
  - Dropdown do wyboru typu trajektorii celu (linia prosta, okrąg, losowa)
  - Live update animacji przy zmianie parametrów
  - Wyświetlanie metryk w czasie rzeczywistym (dystans, czas)

3. Wykresy analityczne
  - Wykres dystans vs czas
  - Wykres prędkości vs czas
  - Wykres krzywizny trajektorii vs czas
  - Wykres energii/pracy wykonanej vs czas
  - Wszystkie wykresy w jednym układzie (subplots) dla porównania

### Uogólnienia wymiarowe

1. Pościg w przestrzeni 3D
 - Rozszerzenie równań różniczkowych na 3 wymiary
 - Przypadki testowe: cel po helisie, spirali 3D, trajektorii Lissajous
 - Analiza krzywizny i skręcenia (torsion) trajektorii 3D
 - Obliczanie długości krzywej w 3D
 - Porównanie efektywności pościgu 2D vs 3D

2. Wizualizacja pościgu 3D
  - Plotly 3D z interaktywną animacją w czasie rzeczywistym
  - Wizualizacja wektorów prędkości i przyspieszenia w 3D
  - Ślady trajektorii z zanikaniem (gradient kolorów)
  - Interaktywne obracanie kamery podczas animacji
  - Multi-view: projekcje na płaszczyzny XY, XZ, YZ jako subplots

3. Pościg w przestrzeni n-wymiarowej (N-D)
  - Uogólnienie algorytmu na dowolną liczbę wymiarów N
  - Implementacja używająca numpy dla wektorów N-wymiarowych
  - Testy dla N = 2, 3, 4, 5, 10, 100 wymiarów
  - Analiza złożoności obliczeniowej vs liczba wymiarów
  - Badanie "curse of dimensionality" w kontekście pościgu

4. Metryki i analiza N-D
  - Obliczanie normy euklidesowej w N wymiarach
  - Długość krzywej w przestrzeni N-D
  - Czas zbieżności vs liczba wymiarów
  - Analiza jak wymiarowość wpływa na efektywność pościgu
  - Wykresy zależności metryk od N

5. Wizualizacja N-D (projekcje i redukcja wymiarowości)
  - Macierz scatter plots dla par wymiarów (np. dla 4D: 6 wykresów)
  - Projekcja na główne składowe (PCA) do 2D/3D
  - t-SNE lub UMAP dla wysokich wymiarów (opcjonalnie)
  - Animowane projekcje obrotowe (rotating projections)
  - Parallel coordinates plot dla trajektorii N-D
  - Heatmap korelacji między wymiarami

### Dokumentacja i prezentacja

1. Teoria matematyczna w notebooku
  - Wprowadzenie teoretyczne z równaniami w LaTeX
  - Wyprowadzenie równań różniczkowych dla krzywej pościgu
  - Uogólnienie na N wymiarów z formalnym zapisem
  - Opis metod numerycznych z analizą błędu
  - Sekcja z przykładami i interpretacją wyników
  - Bibliografia i źródła

2. Rzeczywiste aplikacje krzywej pościgu
  - **2D/3D**: Nawigacja rakiet i pocisków, robotyka mobilna, gry komputerowe, zachowania biologiczne
  - **N-D**: Optymalizacja wielowymiarowa, portfolio optimization, machine learning hyperparameters, przestrzenie konfiguracyjne robotów

### Zaawansowane (nice to have)

1. Pościg cykliczny n-obiektów
  - N obiektów ustawionych w okrąg, każdy ściga kolejny
  - Analiza zbieżności do punktu centralnego
  - Wizualizacja dla n=3,4,5,6 obiektów
  - Dowód matematyczny czasu zbieżności
  - Animacja z zanikającymi śladami dla wszystkich obiektów

2. Wizualizacja 3D z osią czasu (X,Y,t) lub (X,Y,Z,t)
  - Plotly 3D gdzie trzeci wymiar to czas (dla przypadku 2D)
  - Lub 4D jako animacja w 3D (dla przypadku 3D)
  - Pokazanie całej historii pościgu w jednej wizualizacji
  - Kolorowanie trajektorii według prędkości/czasu

### Geometrie alternatywne (nice to have)

1. Pościg na sferze (S²)
  - Geodezyjne krzywe pościgu na powierzchni kuli
  - Współrzędne sferyczne (θ, φ) i metryka sferyczna
  - Great circle distance jako miara odległości
  - Równania różniczkowe w geometrii Riemanna
  - Zastosowania: nawigacja globalna, satelity LEO
  - Wizualizacja na 3D sferze z teksturą Ziemi

2. Pościg na torusie i innych rozmaitościach
  - Geometria torusa (identyfikacja brzegów)
  - Metryka Riemanna dla ogólnych rozmaitości
  - Przykłady: torus, butelka Kleina, powierzchnie wyższego rodzaju
  - Geodezyjne jako krzywe pościgu
  - Wizualizacja z embedded 3D representations

3. Pościg z przeszkodami
  - Dodanie statycznych przeszkód na płaszczyźnie
  - Algorytm omijania przeszkód (potential fields, A*)
  - Optymalizacja trajektorii
  - Analiza wpływu przeszkód na czas pościgu
  - Wizualizacja z przeszkodami

4. Pościg z ograniczeniami kinematycznymi
  - Maksymalne przyspieszenie i prędkość kątowa
  - Realistyczny model pojazdu (np. model Dubinsa)
  - Ograniczenia na promień skrętu
  - Porównanie z idealnym pościgiem
  - Analiza osiągalności celu

5. Wydajność i optymalizacja dla wysokich wymiarów
  - Wykorzystanie numpy broadcasting i vectorization
  - Numba JIT compilation dla pętli czasowych
  - Sparse representations gdzie możliwe
  - Benchmarking: czas obliczeń vs N (wykresy)
  - Memory profiling dla N = 1000+ wymiarów
