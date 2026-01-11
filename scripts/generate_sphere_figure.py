#!/usr/bin/env python3
"""
Skrypt do generowania tylko wykresu sfery.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from pursuit_curve.common import run_continuous_simulation
from pursuit_curve.sphere.continuous import (
    ContinuousDirectPursuitSphere,
    ContinuousTargetSphereStrategy,
)

# Utwórz katalog na figury
FIGURES_DIR = Path(__file__).parent.parent / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

# Styl wykresów
plt.rcParams.update(
    {
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "legend.fontsize": 10,
        "figure.titlesize": 14,
        "lines.linewidth": 1.8,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "figure.facecolor": "white",
        "axes.facecolor": "#fafafa",
        "axes.edgecolor": "#333333",
    }
)


def generate_sphere_pursuit_3d():
    """
    Generuje wykres 3D pościgu na sferze.
    """
    print("Generowanie wykresu: pościg na sferze 3D...")

    fig = plt.figure(figsize=(14, 6))

    # Promień sfery
    R = 5.0

    # Dwie różne konfiguracje
    configs = [
        {
            # Prosty przypadek - cel na równiku, szybkie przechwycenie
            "title": "Prosty przypadek (cel na równiku)",
            "dtheta": 0.0,
            "dphi": 0.3,
            "initial_pursuer": [R, np.pi / 6, np.pi],  # r, theta, phi
            "initial_target": [R, 0.0, 0.0],
            "pursuer_speed": 2.5,
            "t_span": (0, 15),
        },
        {
            # Ciekawszy przypadek - spiralny ruch celu, dłuższy pościg
            "title": "Złożony przypadek ($v_p/v_t \\approx 1.2$)",
            "dtheta": 0.15,
            "dphi": 0.4,
            "initial_pursuer": [R, np.pi / 2, 0.0],  # start na równiku
            "initial_target": [R, -np.pi / 4, np.pi],  # cel na przeciwnej stronie
            "pursuer_speed": 2.5,  # mała przewaga -> dłuższy pościg
            "t_span": (0, 25),
        },
    ]

    for idx, config in enumerate(configs):
        ax = fig.add_subplot(1, 2, idx + 1, projection="3d")

        # Rysuj powierzchnię sfery z lepszą przezroczystością
        u_grid = np.linspace(0, 2 * np.pi, 60)
        v_grid = np.linspace(-np.pi / 2, np.pi / 2, 40)
        U, V = np.meshgrid(u_grid, v_grid)
        X = R * np.cos(V) * np.cos(U)
        Y = R * np.cos(V) * np.sin(U)
        Z = R * np.sin(V)

        ax.plot_surface(X, Y, Z, alpha=0.12, color="lightblue", edgecolor="none")

        # Rysuj siatki pomocnicze - równoleżniki
        for theta_line in np.linspace(-np.pi / 3, np.pi / 3, 5):
            phi_vals = np.linspace(0, 2 * np.pi, 100)
            x = R * np.cos(theta_line) * np.cos(phi_vals)
            y = R * np.cos(theta_line) * np.sin(phi_vals)
            z = R * np.sin(theta_line) * np.ones_like(phi_vals)
            ax.plot(x, y, z, color="gray", alpha=0.25, linewidth=0.5)

        # Rysuj siatki pomocnicze - południki
        for phi_line in np.linspace(0, 2 * np.pi, 12, endpoint=False):
            theta_vals = np.linspace(-np.pi / 2, np.pi / 2, 50)
            x = R * np.cos(theta_vals) * np.cos(phi_line)
            y = R * np.cos(theta_vals) * np.sin(phi_line)
            z = R * np.sin(theta_vals)
            ax.plot(x, y, z, color="gray", alpha=0.25, linewidth=0.5)

        # Rysuj równik wyraźniej
        phi_equator = np.linspace(0, 2 * np.pi, 100)
        x_eq = R * np.cos(phi_equator)
        y_eq = R * np.sin(phi_equator)
        z_eq = np.zeros_like(phi_equator)
        ax.plot(x_eq, y_eq, z_eq, color="darkgray", alpha=0.5, linewidth=1.0)

        # Symulacja pościgu
        initial_state = config["initial_pursuer"] + config["initial_target"]
        target_strategy = ContinuousTargetSphereStrategy(dr=0.0, dtheta=config["dtheta"], dphi=config["dphi"])
        strategy = ContinuousDirectPursuitSphere(vel=config["pursuer_speed"], target_strategy=target_strategy)

        solution = run_continuous_simulation(
            initial_state.copy(),
            strategy,
            t_span=config["t_span"],
            max_step=0.01,
        )

        # Trajektoria ścigającego
        pursuer_r = solution.y[0]
        pursuer_theta = solution.y[1]
        pursuer_phi = solution.y[2]
        px = pursuer_r * np.cos(pursuer_theta) * np.cos(pursuer_phi)
        py = pursuer_r * np.cos(pursuer_theta) * np.sin(pursuer_phi)
        pz = pursuer_r * np.sin(pursuer_theta)
        ax.plot(px, py, pz, color="#2563eb", linewidth=2.5, label="Ścigający", zorder=3)

        # Trajektoria celu
        target_r = solution.y[3]
        target_theta = solution.y[4]
        target_phi = solution.y[5]
        tx = target_r * np.cos(target_theta) * np.cos(target_phi)
        ty = target_r * np.cos(target_theta) * np.sin(target_phi)
        tz = target_r * np.sin(target_theta)
        ax.plot(tx, ty, tz, color="#dc2626", linewidth=2.5, label="Cel", linestyle="--", zorder=3)

        # Punkty startowe (większe)
        ax.scatter(
            [px[0]],
            [py[0]],
            [pz[0]],
            color="#2563eb",
            s=150,
            marker="o",
            edgecolors="white",
            linewidth=2,
            zorder=5,
            label="Start ścigającego",
        )
        ax.scatter(
            [tx[0]],
            [ty[0]],
            [tz[0]],
            color="#dc2626",
            s=150,
            marker="s",
            edgecolors="white",
            linewidth=2,
            zorder=5,
            label="Start celu",
        )

        # Punkt przechwycenia (znacznie większy)
        ax.scatter(
            [px[-1]],
            [py[-1]],
            [pz[-1]],
            color="#16a34a",
            s=400,
            marker="*",
            edgecolors="black",
            linewidth=1.5,
            zorder=10,
            label="Przechwycenie",
        )

        ax.set_xlabel("x", fontsize=10)
        ax.set_ylabel("y", fontsize=10)
        ax.set_zlabel("z", fontsize=10)
        ax.set_title(config["title"], fontsize=12)
        ax.legend(loc="upper left", fontsize=8, framealpha=0.9)

        # Ustaw proporcje
        ax.set_xlim(-R * 1.15, R * 1.15)
        ax.set_ylim(-R * 1.15, R * 1.15)
        ax.set_zlim(-R * 1.15, R * 1.15)

        # Lepszy kąt widzenia
        ax.view_init(elev=25, azim=45)

    plt.suptitle("Pościg na sferze $S^2$ (R=5.0, współrzędne sferyczne)", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "sphere_pursuit_3d.pdf", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Zapisano: {FIGURES_DIR / 'sphere_pursuit_3d.pdf'}")


if __name__ == "__main__":
    generate_sphere_pursuit_3d()
