"""
Skrypt generujący obrazek dla slajdu prezentacji:
Pościg bezpośredni (Direct Pursuit) - cel porusza się po linii prostej.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pursuit_curve.common import Point2D, run_continuous_simulation
from pursuit_curve.d2.continuous import (
    ContinuousDirectPursuit,
    ContinuousTargetLinearStrategy,
)


def generate_direct_pursuit_image():
    # Cel porusza się poziomo, ścigający startuje poniżej
    # To da charakterystyczną zakrzywioną trajektorię pościgu
    initial_state = [0.0, 0.0, 5.0, 8.0]  # [pursuer_x, pursuer_y, target_x, target_y]

    target_strategy = ContinuousTargetLinearStrategy(velocity=Point2D(1.0, 0.0))  # cel idzie w prawo
    strategy = ContinuousDirectPursuit(
        pursuer_velocity=Point2D(1.3, 1.3),  # ścigający trochę szybszy
        target_strategy=target_strategy,
    )

    solution = run_continuous_simulation(initial_state, strategy, t_span=(0, 20))

    # Interpolacja dla gładkich krzywych
    num_points = 500
    t_eval = np.linspace(solution.t[0], solution.t[-1], num_points)
    y_interp = solution.sol(t_eval)

    pursuer_x = y_interp[0]
    pursuer_y = y_interp[1]
    target_x = y_interp[2]
    target_y = y_interp[3]

    # Tworzenie wykresu
    fig, ax = plt.subplots(figsize=(10, 7))

    # Trajektoria celu (linia prosta) - czerwona
    ax.plot(target_x, target_y, "r-", linewidth=2.5, label="Cel (ruch liniowy)", zorder=2)

    # Trajektoria ścigającego (krzywa pościgu) - niebieska
    ax.plot(pursuer_x, pursuer_y, "b-", linewidth=2.5, label="Ścigający (direct pursuit)", zorder=2)

    # Punkty startowe
    ax.plot(pursuer_x[0], pursuer_y[0], "bo", markersize=12, zorder=3)
    ax.plot(target_x[0], target_y[0], "ro", markersize=12, zorder=3)

    # Etykiety punktów startowych
    ax.annotate(
        "Start P",
        (pursuer_x[0], pursuer_y[0]),
        textcoords="offset points",
        xytext=(-15, -20),
        fontsize=11,
        fontweight="bold",
    )
    ax.annotate(
        "Start C",
        (target_x[0], target_y[0]),
        textcoords="offset points",
        xytext=(10, 10),
        fontsize=11,
        fontweight="bold",
    )

    # Punkt końcowy (przechwycenie)
    ax.plot(pursuer_x[-1], pursuer_y[-1], "g*", markersize=18, zorder=4, label="Przechwycenie")

    # Dodanie wektorów prędkości ścigającego (kierunek na cel) co jakiś krok
    num_arrows = 6
    arrow_indices = np.linspace(20, len(pursuer_x) - 40, num_arrows, dtype=int)
    arrow_length = 1.8  # stała długość strzałki

    for i in arrow_indices:
        dx = target_x[i] - pursuer_x[i]
        dy = target_y[i] - pursuer_y[i]
        dist = np.sqrt(dx**2 + dy**2)
        if dist > 0.1:
            # Normalizuj i skaluj do stałej długości
            dx_norm = (dx / dist) * arrow_length
            dy_norm = (dy / dist) * arrow_length
            ax.arrow(
                pursuer_x[i],
                pursuer_y[i],
                dx_norm,
                dy_norm,
                head_width=0.4,
                head_length=0.25,
                fc="navy",
                ec="navy",
                alpha=0.85,
                zorder=5,
                linewidth=2,
            )

    # Ustawienia wykresu
    ax.set_xlabel("X", fontsize=13)
    ax.set_ylabel("Y", fontsize=13)
    ax.set_title("Pościg bezpośredni (Direct Pursuit)", fontsize=15, fontweight="bold")
    ax.legend(loc="lower right", fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_aspect("equal")

    # Marginesy
    margin = 1.0
    all_x = np.concatenate([pursuer_x, target_x])
    all_y = np.concatenate([pursuer_y, target_y])
    ax.set_xlim(all_x.min() - margin, all_x.max() + margin)
    ax.set_ylim(all_y.min() - margin, all_y.max() + margin)

    plt.tight_layout()

    # Zapis do pliku PDF
    output_path = Path(__file__).parent.parent / "figures" / "direct_pursuit_linear.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, bbox_inches="tight", facecolor="white")
    print(f"Obrazek zapisany: {output_path}")


if __name__ == "__main__":
    generate_direct_pursuit_image()
