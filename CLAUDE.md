# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python mathematical simulation library for pursuit curve algorithms. It implements various pursuit strategies (direct pursuit, constant bearing, proportional navigation, cyclic pursuit) in multiple dimensions (2D, 3D, N-dimensional) and geometric spaces (Euclidean, sphere, torus).

## Development Commands

```bash
# Environment setup
uv sync                    # Install dependencies from lockfile
uv run --with jupyter jupyter notebook  # Start Jupyter notebook

# Code quality
make lint                  # Run ruff linter
make format               # Format code with ruff
make clean                # Remove cache files (__pycache__, .mypy_cache, etc.)

# Documentation
make tex                  # Compile LaTeX documentation to PDF
```

## Architecture & Structure

### Core Components

**Strategy Pattern Implementation:**
- `pursuit_curve/common/types.py` - Base abstract classes `Strategy` and `TargetStrategy`
- Each dimension/geometry implements these interfaces with specific pursuit algorithms

**Modular Organization by Dimension/Geometry:**
- `pursuit_curve/d2/` - 2D Euclidean space (discrete & continuous)
- `pursuit_curve/d3/` - 3D Euclidean space (continuous only)  
- `pursuit_curve/dn/` - N-dimensional space (continuous only)
- `pursuit_curve/sphere/` - Spherical geometry (S²)
- `pursuit_curve/torus/` - Toroidal geometry

**Simulation Types:**
- `discrete/` - Step-by-step discrete simulations
- `continuous/` - ODE-based continuous simulations using `scipy.integrate.solve_ivp`

### Key Pursuit Strategies

1. **Direct Pursuit** - Pursuer moves directly toward target
2. **Constant Bearing** - Pursuer maintains constant angle offset
3. **Proportional Navigation** - Used in missiles; angular velocity proportional to line-of-sight rate
4. **Cyclic Pursuit** - N objects in circle, each chasing the next

### Simulation Framework

**Continuous Simulations:**
- Use `run_continuous_simulation()` from `pursuit_curve.common`
- Implement `Strategy.dynamics(t, y)` returning derivatives for ODE solver
- Implement `Strategy.stop_condition(t, y)` for termination events

**Animation System:**
- Each module provides `animate_*` functions using matplotlib
- Support for interactive animations in Jupyter notebooks
- 3D visualizations use plotly for spherical/toroidal geometries

### Mathematical Foundations

The library implements pursuit curves as systems of differential equations. For 2D direct pursuit:
- `dx_p/dt = v_p * (target - pursuer) / ||target - pursuer||`
- Target movement defined by `TargetStrategy`

Supports various target movement patterns:
- Linear motion (`ContinuousTargetLinearStrategy`)
- Circular motion (`ContinuousTargetCircleStrategy`) 
- Custom spherical/toroidal geodesics

### Examples Usage Pattern

All examples follow this pattern:
1. Import required strategies and animation functions
2. Define initial state (positions in flattened array format)
3. Create strategy with pursuer velocity and target movement
4. Run simulation with `run_continuous_simulation(initial_state, strategy, t_span)`
5. Animate results with appropriate animation function

The main entry point is `main.ipynb` which demonstrates discrete vs continuous comparison.
