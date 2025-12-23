# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Package Management
- **Install dependencies**: `uv sync` (installs from lockfile)
- **Run with dependencies**: `uv run <command>` (e.g., `uv run python script.py`)
- **Jupyter notebook**: `uv run --with jupyter jupyter notebook`

### Code Quality
- **Lint code**: `make lint` or `ruff check .`
- **Format code**: `make format` or `ruff format .`
- **Clean cache**: `make clean` (removes __pycache__, .mypy_cache, .ruff_cache)

### Documentation
- **Build LaTeX docs**: `make tex` (compiles dokumentacja.tex to PDF)

## Project Architecture

### Core Structure
The project implements pursuit curve algorithms across multiple dimensions and geometric spaces:

```
pursuit_curve/
├── common/           # Shared types and simulation framework
├── d2/              # 2D pursuit algorithms
├── d3/              # 3D pursuit algorithms  
├── dn/              # N-dimensional pursuit algorithms
├── sphere/          # Spherical geometry pursuit
├── torus/           # Torus geometry pursuit
└── examples/        # Demonstration scripts
```

### Key Components

**Base Types** (`common/types.py`):
- `Strategy` ABC: Defines `dynamics()` and `stop_condition()` for ODE solvers
- `TargetStrategy` ABC: Defines target movement patterns
- `Point2D`, `Point3D`, `PointND`: Coordinate representations

**Simulation Framework** (`common/continuous_simulation.py`):
- `run_continuous_simulation()`: Uses scipy's `solve_ivp` with event detection
- Integrates pursuit strategies with configurable time spans and step sizes

**Pursuit Strategies** (`*/strategies.py`):
- **Direct Pursuit**: Moves directly toward target
- **Constant Bearing**: Maintains fixed angle relative to target direction
- **Proportional Navigation**: Used in missile guidance systems
- **Cyclic Pursuit**: N objects chasing each other in sequence

**Geometric Variants**:
- **2D/3D Euclidean**: Standard Cartesian coordinate systems
- **Spherical**: Great circle distances on sphere surface
- **Torus**: Pursuit on torus manifold with periodic boundary conditions
- **N-dimensional**: Generalized to arbitrary dimensions

### Animation System
Each geometry module includes visualization:
- matplotlib-based animations with trajectory trails
- 3D plotting for sphere/torus geometries
- Real-time parameter adjustment capabilities

### Mathematical Foundation
The project implements differential equation systems where:
- State vector: `[pursuer_coords..., target_coords...]`
- Dynamics: `dy/dt = strategy.dynamics(t, y)`
- Termination: `strategy.stop_condition(t, y) = 0` (distance threshold)

## Key Implementation Notes

- Uses `scipy.integrate.solve_ivp` for numerical integration
- Event-driven simulation termination when pursuer reaches target
- Strategy pattern allows swapping pursuit algorithms without changing simulation code
- NumPy arrays used throughout for efficient vector operations
- Type hints and dataclasses for better code clarity
