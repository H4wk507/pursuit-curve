from scipy.integrate import solve_ivp

from .types import Strategy


def run_continuous_simulation(
    initial_state: list[float],
    strategy: Strategy,
    t_span: tuple[float, float] = (0, 50),
    max_step: float = 0.1,
):
    """
    initial_state: [pursuer_x, pursuer_y, ..., target_x, target_y, ...]
    strategy: Strategia z metodami dynamics() i stop_condition()
    t_span: Przedział czasu (t_start, t_end)
    max_step: Maksymalny krok czasowy solwera
    """
    solution = solve_ivp(
        fun=strategy.dynamics,
        t_span=t_span,
        y0=initial_state,
        events=strategy.stop_condition,
        dense_output=True,
        max_step=max_step,
    )

    print(f"Symulacja zakończona w czasie t={solution.t[-1]:.2f}s")
    print(f"Liczba kroków solwera: {len(solution.t)}")

    return solution
