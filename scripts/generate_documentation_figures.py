#!/usr/bin/env python3
"""
Skrypt do generowania wizualizacji dla dokumentacji.
Generuje wykresy trajektorii pościgu dla różnych strategii i scenariuszy.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from pursuit_curve.common import Point2D, Point3D, run_continuous_simulation
from pursuit_curve.d2.continuous import (
    ContinuousConstantBearing,
    ContinuousCyclicPursuit,
    ContinuousDirectPursuit,
    ContinuousProportionalNavigation,
    ContinuousTargetCircleStrategy,
    ContinuousTargetLinearStrategy,
)
from pursuit_curve.d3.continuous import (
    ContinuousDirectPursuit3D,
    ContinuousTargetHelixStrategy,
    ContinuousTargetLissajousStrategy,
)
from pursuit_curve.sphere.continuous import (
    ContinuousDirectPursuitSphere,
    ContinuousTargetSphereStrategy,
)
from pursuit_curve.torus.continuous import (
    ContinuousDirectPursuitTorus,
    ContinuousTargetTorusStrategy,
)

# Utwórz katalog na figury
FIGURES_DIR = Path(__file__).parent.parent / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

# Styl wykresów - profesjonalny wygląd
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

# Paleta kolorów
COLORS = {
    "direct": "#2563eb",  # niebieski
    "bearing_15": "#16a34a",  # zielony
    "bearing_30": "#ea580c",  # pomarańczowy
    "bearing_45": "#dc2626",  # czerwony
    "pn_2": "#7c3aed",  # fioletowy
    "pn_3": "#0891b2",  # cyjan
    "pn_5": "#be185d",  # różowy
    "target": "#6b7280",  # szary
    "pursuer": "#1e40af",  # ciemnoniebieski
}


def generate_strategy_comparison_linear_target():
    """
    Generuje wykres porównawczy strategii pościgu dla celu liniowego.
    """
    print("Generowanie wykresu: porównanie strategii (cel liniowy)...")

    fig, ax = plt.subplots(figsize=(10, 8))

    # Parametry
    initial_state = [8.0, 2.0, 0.0, 0.0]
    pursuer_speed = 2.0
    capture_distance = 0.1  # Zmniejszona tolerancja przechwycenia
    target_strategy = ContinuousTargetLinearStrategy(velocity=Point2D(0.8, 0.6))

    strategies = [
        (
            "Direct Pursuit",
            ContinuousDirectPursuit(
                pursuer_velocity=Point2D(pursuer_speed, pursuer_speed),
                target_strategy=target_strategy,
                capture_distance=capture_distance,
            ),
            COLORS["direct"],
        ),
        (
            "Constant Bearing β=15°",
            ContinuousConstantBearing(
                pursuer_velocity=Point2D(pursuer_speed, pursuer_speed),
                target_strategy=target_strategy,
                bearing_angle_deg=15,
                capture_distance=capture_distance,
            ),
            COLORS["bearing_15"],
        ),
        (
            "Constant Bearing β=30°",
            ContinuousConstantBearing(
                pursuer_velocity=Point2D(pursuer_speed, pursuer_speed),
                target_strategy=target_strategy,
                bearing_angle_deg=30,
                capture_distance=capture_distance,
            ),
            COLORS["bearing_30"],
        ),
        (
            "Proportional Nav. N=3",
            ContinuousProportionalNavigation(
                pursuer_velocity=Point2D(pursuer_speed, pursuer_speed),
                target_strategy=target_strategy,
                N=3,
                capture_distance=capture_distance,
            ),
            COLORS["pn_3"],
        ),
    ]

    # Rysuj trajektorie
    for name, strategy, color in strategies:
        solution = run_continuous_simulation(initial_state.copy(), strategy, t_span=(0, 30))
        ax.plot(solution.y[0], solution.y[1], color=color, label=name, linewidth=2)
        # Punkt startowy
        ax.scatter(
            [initial_state[0]], [initial_state[1]], color=color, s=80, zorder=5, edgecolors="white", linewidth=1.5
        )
        # Punkt przechwycenia (końcowy punkt trajektorii)
        intercept_x, intercept_y = solution.y[0][-1], solution.y[1][-1]
        ax.scatter(
            [intercept_x],
            [intercept_y],
            color=color,
            s=100,
            marker="X",
            zorder=6,
            edgecolors="white",
            linewidth=1.0,
        )

    # Trajektoria celu
    t_end = 6.0
    t_vals = np.linspace(0, t_end, 100)
    target_x = 0.0 + 0.8 * t_vals
    target_y = 0.0 + 0.6 * t_vals
    ax.plot(target_x, target_y, "--", color=COLORS["target"], linewidth=2, label="Trajektoria celu")
    ax.scatter([0.0], [0.0], color=COLORS["target"], s=100, marker="s", zorder=5, edgecolors="white", linewidth=1.5)

    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_title("Porównanie strategii pościgu dla celu liniowego")
    ax.legend(loc="upper left")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "strategy_comparison_linear.pdf", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Zapisano: {FIGURES_DIR / 'strategy_comparison_linear.pdf'}")


def generate_strategy_comparison_circular_target():
    """
    Generuje wykres porównawczy strategii pościgu dla celu na okręgu.
    """
    print("Generowanie wykresu: porównanie strategii (cel na okręgu)...")

    fig, ax = plt.subplots(figsize=(10, 10))

    # Parametry
    r = 3.0
    omega = 0.5
    pursuer_speed = 2.0
    capture_distance = 0.1  # Zmniejszona tolerancja przechwycenia
    initial_state = [8.0, 0.0, r, 0.0]  # pursuer w (8,0), cel w (r, 0)
    target_strategy = ContinuousTargetCircleStrategy(angular_velocity=omega, r=r)

    strategies = [
        (
            "Direct Pursuit",
            ContinuousDirectPursuit(
                pursuer_velocity=Point2D(pursuer_speed, pursuer_speed),
                target_strategy=target_strategy,
                capture_distance=capture_distance,
            ),
            COLORS["direct"],
        ),
        (
            "Constant Bearing β=15°",
            ContinuousConstantBearing(
                pursuer_velocity=Point2D(pursuer_speed, pursuer_speed),
                target_strategy=target_strategy,
                bearing_angle_deg=15,
                capture_distance=capture_distance,
            ),
            COLORS["bearing_15"],
        ),
        (
            "Proportional Nav. N=3",
            ContinuousProportionalNavigation(
                pursuer_velocity=Point2D(pursuer_speed, pursuer_speed),
                target_strategy=target_strategy,
                N=3,
                capture_distance=capture_distance,
            ),
            COLORS["pn_3"],
        ),
    ]

    # Rysuj okrąg celu
    theta = np.linspace(0, 2 * np.pi, 200)
    circle_x = r * np.cos(theta)
    circle_y = r * np.sin(theta)
    ax.plot(circle_x, circle_y, "--", color=COLORS["target"], linewidth=1.5, alpha=0.7, label="Orbita celu")

    # Rysuj trajektorie
    for name, strategy, color in strategies:
        solution = run_continuous_simulation(initial_state.copy(), strategy, t_span=(0, 20))
        ax.plot(solution.y[0], solution.y[1], color=color, label=name, linewidth=2)
        ax.scatter(
            [initial_state[0]], [initial_state[1]], color=color, s=80, zorder=5, edgecolors="white", linewidth=1.5
        )
        # Punkt przechwycenia (końcowy punkt trajektorii)
        intercept_x, intercept_y = solution.y[0][-1], solution.y[1][-1]
        ax.scatter(
            [intercept_x],
            [intercept_y],
            color=color,
            s=100,
            marker="X",
            zorder=6,
            edgecolors="white",
            linewidth=1.0,
        )

        # Trajektoria celu dla tej symulacji
        target_x = r * np.cos(omega * solution.t)
        target_y = r * np.sin(omega * solution.t)
        ax.plot(target_x, target_y, ":", color=color, linewidth=1, alpha=0.5)

    # Punkt startowy celu
    ax.scatter(
        [r],
        [0.0],
        color=COLORS["target"],
        s=100,
        marker="s",
        zorder=5,
        edgecolors="white",
        linewidth=1.5,
        label="Start celu",
    )

    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_title("Porównanie strategii pościgu dla celu na okręgu")
    ax.legend(loc="upper left")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "strategy_comparison_circular.pdf", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Zapisano: {FIGURES_DIR / 'strategy_comparison_circular.pdf'}")


def generate_cyclic_pursuit():
    """
    Generuje wykres pościgu cyklicznego dla różnej liczby agentów.
    """
    print("Generowanie wykresu: pościg cykliczny...")

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    R = 5.0
    v = 1.0
    agent_counts = [3, 4, 6]
    colors_agents = plt.cm.Set1(np.linspace(0, 1, max(agent_counts)))

    for idx, n in enumerate(agent_counts):
        ax = axes[idx]

        # Pozycje początkowe na okręgu
        angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
        initial_positions = []
        for angle in angles:
            initial_positions.extend([R * np.cos(angle), R * np.sin(angle)])

        strategy = ContinuousCyclicPursuit(velocity=Point2D(v, v), n=n, capture_distance=0.1)
        T_theory = R / (v * np.sin(np.pi / n))

        solution = run_continuous_simulation(
            initial_positions,
            strategy,
            t_span=(0, T_theory * 2),
            max_step=0.01,
        )

        # Rysuj okrąg początkowy
        theta = np.linspace(0, 2 * np.pi, 100)
        ax.plot(R * np.cos(theta), R * np.sin(theta), "--", color="gray", alpha=0.3, linewidth=1)

        # Rysuj trajektorie agentów
        for i in range(n):
            agent_x = solution.y[2 * i]
            agent_y = solution.y[2 * i + 1]
            color = colors_agents[i]
            ax.plot(agent_x, agent_y, color=color, linewidth=1.5, alpha=0.8)
            # Punkt startowy
            ax.scatter([agent_x[0]], [agent_y[0]], color=color, s=60, zorder=5, edgecolors="white", linewidth=1)
            # Punkt końcowy
            ax.scatter([agent_x[-1]], [agent_y[-1]], color=color, s=40, marker="x", zorder=5)

        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
        ax.set_title(f"Pościg cykliczny: n = {n} agentów")
        ax.set_aspect("equal", adjustable="box")
        ax.grid(True, alpha=0.3)
        ax.set_xlim(-R * 1.3, R * 1.3)
        ax.set_ylim(-R * 1.3, R * 1.3)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "cyclic_pursuit.pdf", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Zapisano: {FIGURES_DIR / 'cyclic_pursuit.pdf'}")


def generate_helix_pursuit_3d():
    """
    Generuje wykres 3D pościgu dla celu na helisie.
    Ulepszona wizualizacja z punktami przechwycenia i lepszą widocznością 3D.
    """
    print("Generowanie wykresu: pościg 3D (helisa)...")

    fig = plt.figure(figsize=(14, 11))
    ax = fig.add_subplot(111, projection="3d")

    # Parametry
    pursuer_start = [8.0, 0.0, 2.0]
    target_start = [3.0, 0.0, 0.0]
    initial_state = pursuer_start + target_start

    r = 3.0
    omega = 0.4
    pursuer_speed = 2.5

    vertical_velocities = [0.0, 0.5, 1.0, 1.5]
    colors_vz = ["#2563eb", "#16a34a", "#ea580c", "#dc2626"]

    # Czas dla pełnej trajektorii celu (dłuższy niż symulacja)
    t_full = np.linspace(0, 15, 500)

    # Najpierw rysujemy pełne trajektorie celu na szaro
    for vz in vertical_velocities:
        target_x_full = r * np.cos(omega * t_full)
        target_y_full = r * np.sin(omega * t_full)
        target_z_full = vz * t_full
        label_target = "Trajektoria celu (pełna)" if vz == vertical_velocities[0] else None
        ax.plot(
            target_x_full,
            target_y_full,
            target_z_full,
            color="#888888",
            linewidth=2.0,
            alpha=0.7,
            zorder=1,
            label=label_target,
        )

    # Przechowuj punkty przechwycenia
    capture_points = []

    for vz, color in zip(vertical_velocities, colors_vz):
        target_strategy = ContinuousTargetHelixStrategy(r=r, angular_velocity=omega, vertical_velocity=vz)
        strategy = ContinuousDirectPursuit3D(
            pursuer_velocity=Point3D(pursuer_speed, pursuer_speed, pursuer_speed),
            target_strategy=target_strategy,
            capture_distance=0.01,
        )

        solution = run_continuous_simulation(initial_state.copy(), strategy, t_span=(0, 15), max_step=0.05)

        # Trajektoria ścigającego - grubsza linia z efektem głębi
        ax.plot(
            solution.y[0],
            solution.y[1],
            solution.y[2],
            color=color,
            linewidth=2.5,
            label=f"Ścigający ($v_z$={vz} m/s)",
            zorder=10,
        )

        # Punkt przechwycenia (końcowy punkt symulacji)
        capture_x = solution.y[0][-1]
        capture_y = solution.y[1][-1]
        capture_z = solution.y[2][-1]
        capture_points.append((capture_x, capture_y, capture_z, color, vz))

    # Punkty startowe - większe i bardziej wyraźne
    ax.scatter(
        [pursuer_start[0]],
        [pursuer_start[1]],
        [pursuer_start[2]],
        color="#1e40af",
        s=180,
        marker="o",
        label="Start ścigającego",
        edgecolors="white",
        linewidth=2,
        zorder=20,
        depthshade=False,
    )
    ax.scatter(
        [target_start[0]],
        [target_start[1]],
        [target_start[2]],
        color="#b91c1c",
        s=180,
        marker="s",
        label="Start celu",
        edgecolors="white",
        linewidth=2,
        zorder=20,
        depthshade=False,
    )

    # Punkty przechwycenia - gwiazdki z konturem
    for i, (cx, cy, cz, color, vz) in enumerate(capture_points):
        label = "Punkt przechwycenia" if i == 0 else None
        ax.scatter(
            [cx],
            [cy],
            [cz],
            color=color,
            s=300,
            marker="*",
            edgecolors="black",
            linewidth=1.5,
            zorder=25,
            depthshade=False,
            label=label,
        )

    # Siatka projekcji na płaszczyznę XY dla lepszej orientacji 3D
    z_min = ax.get_zlim()[0]
    for vz, color in zip(vertical_velocities, colors_vz):
        target_strategy = ContinuousTargetHelixStrategy(r=r, angular_velocity=omega, vertical_velocity=vz)
        strategy = ContinuousDirectPursuit3D(
            pursuer_velocity=Point3D(pursuer_speed, pursuer_speed, pursuer_speed),
            target_strategy=target_strategy,
            capture_distance=0.01,
        )
        solution = run_continuous_simulation(initial_state.copy(), strategy, t_span=(0, 15), max_step=0.05)
        # Projekcja trajektorii na płaszczyznę XY (cień)
        ax.plot(
            solution.y[0],
            solution.y[1],
            [z_min] * len(solution.y[0]),
            color=color,
            linewidth=0.8,
            alpha=0.25,
            linestyle=":",
        )

    ax.set_xlabel("x [m]", fontsize=12, labelpad=10)
    ax.set_ylabel("y [m]", fontsize=12, labelpad=10)
    ax.set_zlabel("z [m]", fontsize=12, labelpad=10)
    ax.set_title("Pościg 3D: cel na trajektorii helisoidalnej", fontsize=14, fontweight="bold", pad=15)

    # Lepszy kąt widzenia dla 3D
    ax.view_init(elev=25, azim=45)

    # Siatka tła
    ax.xaxis.pane.fill = True
    ax.yaxis.pane.fill = True
    ax.zaxis.pane.fill = True
    ax.xaxis.pane.set_facecolor((0.95, 0.95, 0.98, 0.8))
    ax.yaxis.pane.set_facecolor((0.92, 0.92, 0.96, 0.8))
    ax.zaxis.pane.set_facecolor((0.90, 0.90, 0.94, 0.8))

    # Legenda poza wykresem
    ax.legend(loc="upper left", bbox_to_anchor=(0.02, 0.98), fontsize=10, framealpha=0.95, edgecolor="gray")

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "helix_pursuit_3d.pdf", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Zapisano: {FIGURES_DIR / 'helix_pursuit_3d.pdf'}")


def generate_lissajous_pursuit_3d():
    """
    Generuje wykres 3D pościgu dla celu na krzywej Lissajous.
    """
    print("Generowanie wykresu: pościg 3D (Lissajous)...")

    fig = plt.figure(figsize=(15, 5))

    # Parametry
    pursuer_start = [5.0, 5.0, 5.0]
    target_start = [0.0, 0.0, 0.0]
    initial_state = pursuer_start + target_start

    A = Point3D(3.0, 3.0, 3.0)
    pursuer_speed = 3.0
    capture_distance = 0.1

    frequency_ratios = [
        ("1:1:1", Point3D(1.0, 1.0, 1.0)),
        ("1:2:1", Point3D(1.0, 2.0, 1.0)),
        ("2:3:5", Point3D(2.0, 3.0, 5.0)),
    ]

    for idx, (ratio_name, omega) in enumerate(frequency_ratios):
        ax = fig.add_subplot(1, 3, idx + 1, projection="3d")

        target_strategy = ContinuousTargetLissajousStrategy(A=A, angular_velocity=omega)
        strategy = ContinuousDirectPursuit3D(
            pursuer_velocity=Point3D(pursuer_speed, pursuer_speed, pursuer_speed),
            target_strategy=target_strategy,
            capture_distance=capture_distance,
        )

        solution = run_continuous_simulation(initial_state.copy(), strategy, t_span=(0, 30), max_step=0.02)

        # Sprawdź czy nastąpiło przechwycenie
        final_pursuer = np.array([solution.y[0][-1], solution.y[1][-1], solution.y[2][-1]])
        final_target_pos = np.array(
            [
                A.x * np.sin(omega.x * solution.t[-1]),
                A.y * np.sin(omega.y * solution.t[-1]),
                A.z * np.sin(omega.z * solution.t[-1]),
            ]
        )
        final_distance = np.linalg.norm(final_target_pos - final_pursuer)
        captured = final_distance <= capture_distance * 1.5  # Mały margines

        # Pełna trajektoria Lissajous (na szaro, jako tło)
        # Użyj odpowiedniego okresu dla pełnej krzywej
        lcm_period = 2 * np.pi * max(1, int(np.lcm.reduce([int(omega.x), int(omega.y), int(omega.z)])))
        t_full = np.linspace(0, lcm_period, 1000)
        target_x_full = A.x * np.sin(omega.x * t_full)
        target_y_full = A.y * np.sin(omega.y * t_full)
        target_z_full = A.z * np.sin(omega.z * t_full)
        ax.plot(
            target_x_full,
            target_y_full,
            target_z_full,
            "-",
            color="gray",
            linewidth=1.5,
            alpha=0.4,
            label="Pełna krzywa Lissajous",
            zorder=1,
        )

        # Faktyczna trajektoria celu podczas symulacji (czerwona)
        target_x_sim = A.x * np.sin(omega.x * solution.t)
        target_y_sim = A.y * np.sin(omega.y * solution.t)
        target_z_sim = A.z * np.sin(omega.z * solution.t)
        ax.plot(
            target_x_sim,
            target_y_sim,
            target_z_sim,
            "-",
            color=COLORS["target"],
            linewidth=2,
            alpha=0.9,
            label="Trajektoria celu",
            zorder=2,
        )

        # Trajektoria ścigającego (niebieska)
        ax.plot(
            solution.y[0],
            solution.y[1],
            solution.y[2],
            color=COLORS["pursuer"],
            linewidth=2.5,
            label="Ścigający",
            zorder=3,
        )

        # Punkty startowe
        ax.scatter(
            [pursuer_start[0]],
            [pursuer_start[1]],
            [pursuer_start[2]],
            color=COLORS["pursuer"],
            s=80,
            marker="o",
            edgecolors="white",
            linewidth=1.5,
            zorder=5,
            label="Start ścigającego",
        )
        ax.scatter(
            [target_start[0]],
            [target_start[1]],
            [target_start[2]],
            color=COLORS["target"],
            s=80,
            marker="s",
            edgecolors="white",
            linewidth=1.5,
            zorder=5,
            label="Start celu",
        )

        # Punkt przechwycenia (jeśli nastąpiło)
        if captured:
            ax.scatter(
                [final_pursuer[0]],
                [final_pursuer[1]],
                [final_pursuer[2]],
                color="lime",
                s=120,
                marker="*",
                edgecolors="darkgreen",
                linewidth=1.5,
                zorder=6,
                label=f"Przechwycenie (t={solution.t[-1]:.2f}s)",
            )
            capture_text = f"t = {solution.t[-1]:.2f}s"
        else:
            capture_text = "brak"

        ax.set_xlabel("x [m]", fontsize=9)
        ax.set_ylabel("y [m]", fontsize=9)
        ax.set_zlabel("z [m]", fontsize=9)
        ax.set_title(f"ω = {ratio_name}\nPrzechwycenie: {capture_text}", fontsize=10)

        # Ustaw ładniejszy kąt widzenia
        ax.view_init(elev=20, azim=45 + idx * 30)

        if idx == 0:
            ax.legend(loc="upper left", fontsize=7, framealpha=0.9)

    plt.suptitle("Pościg 3D: cel na krzywych Lissajous", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "lissajous_pursuit_3d.pdf", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Zapisano: {FIGURES_DIR / 'lissajous_pursuit_3d.pdf'}")


def generate_velocity_ratio_trajectories():
    """
    Generuje wykres trajektorii dla różnych stosunków prędkości.
    """
    print("Generowanie wykresu: trajektorie stosunku prędkości...")

    fig, ax = plt.subplots(figsize=(10, 10))

    # Parametry
    r = 3.0
    omega = 0.5
    target_speed = r * omega
    capture_distance = 0.05  # Zmniejszona tolerancja przechwycenia
    initial_state = [8.0, 0.0, r, 0.0]

    velocity_ratios = [1.1, 1.5, 2.0, 3.0]
    colors_ratio = ["#dc2626", "#ea580c", "#16a34a", "#2563eb"]

    # Rysuj okrąg celu
    theta = np.linspace(0, 2 * np.pi, 200)
    circle_x = r * np.cos(theta)
    circle_y = r * np.sin(theta)
    ax.plot(circle_x, circle_y, "--", color="gray", alpha=0.5, linewidth=1, label="Orbita celu")

    for ratio, color in zip(velocity_ratios, colors_ratio):
        pursuer_speed = ratio * target_speed
        target_strategy = ContinuousTargetCircleStrategy(angular_velocity=omega, r=r)
        strategy = ContinuousDirectPursuit(
            pursuer_velocity=Point2D(pursuer_speed, pursuer_speed),
            target_strategy=target_strategy,
            capture_distance=capture_distance,
        )

        solution = run_continuous_simulation(initial_state.copy(), strategy, t_span=(0, 20), rtol=1e-6)

        ax.plot(
            solution.y[0], solution.y[1], color=color, linewidth=2, label=f"ρ = {ratio} (vp = {pursuer_speed:.2f} m/s)"
        )

        # Punkt przechwycenia z adnotacją
        intercept_x, intercept_y = solution.y[0][-1], solution.y[1][-1]
        ax.scatter(
            [intercept_x],
            [intercept_y],
            color=color,
            s=120,
            marker="X",
            zorder=6,
            edgecolors="white",
            linewidth=1.5,
        )
        # Adnotacja z czasem przechwycenia
        ax.annotate(
            f"t={solution.t[-1]:.2f}s",
            (intercept_x, intercept_y),
            textcoords="offset points",
            xytext=(8, 8),
            fontsize=8,
            color=color,
            fontweight="bold",
        )

    ax.scatter(
        [initial_state[0]],
        [initial_state[1]],
        color="blue",
        s=100,
        marker="o",
        zorder=5,
        edgecolors="white",
        linewidth=1.5,
        label="Start ścigającego",
    )
    ax.scatter(
        [r], [0], color="red", s=100, marker="s", zorder=5, edgecolors="white", linewidth=1.5, label="Start celu"
    )

    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_title("Trajektorie dla różnych stosunków prędkości ρ = vp/vt")
    ax.legend(loc="upper left", fontsize=9)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "velocity_ratio_trajectories.pdf", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Zapisano: {FIGURES_DIR / 'velocity_ratio_trajectories.pdf'}")


def generate_velocity_ratio_times():
    """
    Generuje wykres słupkowy czasów przechwycenia dla różnych stosunków prędkości.
    """
    print("Generowanie wykresu: czasy przechwycenia stosunku prędkości...")

    fig, ax = plt.subplots(figsize=(10, 7))

    # Parametry
    r = 3.0
    omega = 0.5
    target_speed = r * omega
    capture_distance = 0.1
    initial_state = [8.0, 0.0, r, 0.0]

    velocity_ratios = [1.1, 1.5, 2.0, 3.0]
    colors_ratio = ["#dc2626", "#ea580c", "#16a34a", "#2563eb"]

    capture_times = []

    for ratio, color in zip(velocity_ratios, colors_ratio):
        pursuer_speed = ratio * target_speed
        target_strategy = ContinuousTargetCircleStrategy(angular_velocity=omega, r=r)
        strategy = ContinuousDirectPursuit(
            pursuer_velocity=Point2D(pursuer_speed, pursuer_speed),
            target_strategy=target_strategy,
            capture_distance=capture_distance,
        )

        solution = run_continuous_simulation(initial_state.copy(), strategy, t_span=(0, 20), rtol=1e-6)
        capture_times.append((ratio, solution.t[-1]))

    ratios = [ct[0] for ct in capture_times]
    times = [ct[1] for ct in capture_times]
    T_orbit = 2 * np.pi * r / target_speed
    normalized_times = [t / T_orbit for t in times]

    ax.bar(range(len(ratios)), normalized_times, color=colors_ratio, edgecolor="black", linewidth=1)
    ax.set_xticks(range(len(ratios)))
    ax.set_xticklabels([f"ρ = {ratio}" for ratio in ratios])
    ax.set_ylabel("Czas przechwycenia [T_orbit]")
    ax.set_title("Znormalizowany czas przechwycenia dla różnych stosunków prędkości")
    ax.grid(True, alpha=0.3, axis="y")

    # Dodaj wartości na słupkach
    for i, (ratio, nt) in enumerate(zip(ratios, normalized_times)):
        ax.text(i, nt + 0.02, f"{nt:.2f}", ha="center", fontsize=10)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "velocity_ratio_times.pdf", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Zapisano: {FIGURES_DIR / 'velocity_ratio_times.pdf'}")


def generate_bearing_angle_effect():
    """
    Generuje wykres wpływu kąta namiarowania na trajektorię.
    """
    print("Generowanie wykresu: wpływ kąta namiarowania...")

    fig, ax = plt.subplots(figsize=(16, 7))

    # Parametry
    initial_state = [8.0, 2.0, 0.0, 0.0]
    pursuer_speed = 2.0
    capture_distance = 0.1
    target_strategy = ContinuousTargetLinearStrategy(velocity=Point2D(0.8, 0.6))

    bearing_angles = [0, 15, 30, 45, 60]
    colors_bearing = plt.cm.viridis(np.linspace(0.1, 0.9, len(bearing_angles)))

    for angle, color in zip(bearing_angles, colors_bearing):
        if angle == 0:
            strategy = ContinuousDirectPursuit(
                pursuer_velocity=Point2D(pursuer_speed, pursuer_speed),
                target_strategy=target_strategy,
                capture_distance=capture_distance,
            )
            label = "Direct Pursuit (β=0°)"
        else:
            strategy = ContinuousConstantBearing(
                pursuer_velocity=Point2D(pursuer_speed, pursuer_speed),
                target_strategy=target_strategy,
                bearing_angle_deg=angle,
                capture_distance=capture_distance,
            )
            label = f"β = {angle}°"

        solution = run_continuous_simulation(initial_state.copy(), strategy, t_span=(0, 30))
        ax.plot(solution.y[0], solution.y[1], color=color, linewidth=2, label=label)

        # Punkt przechwycenia (końcowy punkt trajektorii)
        intercept_x, intercept_y = solution.y[0][-1], solution.y[1][-1]
        ax.scatter(
            [intercept_x],
            [intercept_y],
            color=color,
            s=80,
            marker="X",
            zorder=6,
            edgecolors="white",
            linewidth=1.0,
        )

    # Trajektoria celu
    t_vals = np.linspace(0, 10, 100)
    target_x = 0.8 * t_vals
    target_y = 0.6 * t_vals
    ax.plot(target_x, target_y, "--", color="gray", linewidth=2, label="Cel")

    ax.scatter(
        [initial_state[0]],
        [initial_state[1]],
        color="blue",
        s=100,
        marker="o",
        zorder=5,
        edgecolors="white",
        linewidth=1.5,
    )
    ax.scatter([0], [0], color="red", s=100, marker="s", zorder=5, edgecolors="white", linewidth=1.5)

    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_title("Trajektorie dla różnych kątów namiarowania β")
    ax.legend(loc="upper left")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "bearing_angle_effect.pdf", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Zapisano: {FIGURES_DIR / 'bearing_angle_effect.pdf'}")


def torus_to_cartesian(u: np.ndarray, v: np.ndarray, R: float, r: float):
    """Konwertuje współrzędne toroidalne (u, v) na kartezjańskie (x, y, z)."""
    x = (R + r * np.cos(v)) * np.cos(u)
    y = (R + r * np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    return x, y, z


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


def generate_torus_pursuit_3d():
    """
    Generuje wykres 3D pościgu na torusie.
    """
    print("Generowanie wykresu: pościg na torusie 3D...")

    fig = plt.figure(figsize=(14, 6))

    # Parametry torusa
    R = 3.0  # promień główny
    r = 1.2  # promień rurki

    # Dwie różne konfiguracje
    configs = [
        {
            "title": "Cel na okręgu głównym",
            "omega_u": 0.5,
            "omega_v": 0.0,
            "initial_state": [0.0, 0.0, np.pi, 0.0],
            "pursuer_speed": 1.5,
            "t_span": (0, 15),
        },
        {
            "title": "Cel spiralny (ωu=0.3, ωv=0.5)",
            "omega_u": 0.3,
            "omega_v": 0.5,
            "initial_state": [0.0, 0.0, np.pi, np.pi / 2],
            "pursuer_speed": 1.5,
            "t_span": (0, 25),
        },
    ]

    for idx, config in enumerate(configs):
        ax = fig.add_subplot(1, 2, idx + 1, projection="3d")

        # Rysuj powierzchnię torusa
        u_grid = np.linspace(0, 2 * np.pi, 60)
        v_grid = np.linspace(0, 2 * np.pi, 40)
        U, V = np.meshgrid(u_grid, v_grid)
        X, Y, Z = torus_to_cartesian(U, V, R, r)

        ax.plot_surface(X, Y, Z, alpha=0.15, color="gray", edgecolor="none")

        # Rysuj siatki pomocnicze na torusie
        for u_line in np.linspace(0, 2 * np.pi, 12, endpoint=False):
            v_vals = np.linspace(0, 2 * np.pi, 100)
            x, y, z = torus_to_cartesian(np.full_like(v_vals, u_line), v_vals, R, r)
            ax.plot(x, y, z, color="gray", alpha=0.2, linewidth=0.5)

        for v_line in np.linspace(0, 2 * np.pi, 8, endpoint=False):
            u_vals = np.linspace(0, 2 * np.pi, 100)
            x, y, z = torus_to_cartesian(u_vals, np.full_like(u_vals, v_line), R, r)
            ax.plot(x, y, z, color="gray", alpha=0.2, linewidth=0.5)

        # Symulacja pościgu
        target_strategy = ContinuousTargetTorusStrategy(omega_u=config["omega_u"], omega_v=config["omega_v"])
        strategy = ContinuousDirectPursuitTorus(
            vel=config["pursuer_speed"],
            target_strategy=target_strategy,
            R=R,
            r=r,
        )

        solution = run_continuous_simulation(
            config["initial_state"].copy(),
            strategy,
            t_span=config["t_span"],
            max_step=0.02,
        )

        # Trajektoria ścigającego
        pursuer_u = solution.y[0]
        pursuer_v = solution.y[1]
        px, py, pz = torus_to_cartesian(pursuer_u, pursuer_v, R, r)
        ax.plot(px, py, pz, color="#2563eb", linewidth=2.5, label="Ścigający")

        # Trajektoria celu
        target_u = solution.y[2]
        target_v = solution.y[3]
        tx, ty, tz = torus_to_cartesian(target_u, target_v, R, r)
        ax.plot(tx, ty, tz, color="#dc2626", linewidth=2.5, label="Cel", linestyle="--")

        # Punkty startowe
        px0, py0, pz0 = torus_to_cartesian(np.array([pursuer_u[0]]), np.array([pursuer_v[0]]), R, r)
        tx0, ty0, tz0 = torus_to_cartesian(np.array([target_u[0]]), np.array([target_v[0]]), R, r)

        ax.scatter(px0, py0, pz0, color="#2563eb", s=100, marker="o", edgecolors="white", linewidth=1.5, zorder=5)
        ax.scatter(tx0, ty0, tz0, color="#dc2626", s=100, marker="s", edgecolors="white", linewidth=1.5, zorder=5)

        # Punkty końcowe
        px_end, py_end, pz_end = torus_to_cartesian(np.array([pursuer_u[-1]]), np.array([pursuer_v[-1]]), R, r)
        ax.scatter(
            px_end,
            py_end,
            pz_end,
            color="#16a34a",
            s=80,
            marker="*",
            edgecolors="white",
            linewidth=1,
            zorder=5,
            label="Przechwycenie",
        )

        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
        ax.set_zlabel("z [m]")
        ax.set_title(config["title"])
        ax.legend(loc="upper left", fontsize=9)

        # Ustaw proporcje
        max_range = R + r + 0.5
        ax.set_xlim(-max_range, max_range)
        ax.set_ylim(-max_range, max_range)
        ax.set_zlim(-r - 0.5, r + 0.5)

    plt.suptitle("Pościg na torusie (R=3.0 m, r=1.2 m)", fontsize=14)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "torus_pursuit_3d.pdf", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Zapisano: {FIGURES_DIR / 'torus_pursuit_3d.pdf'}")


def main():
    print("=" * 60)
    print("Generowanie wizualizacji dla dokumentacji")
    print("=" * 60)
    print(f"Katalog wyjściowy: {FIGURES_DIR}")
    print()

    # Generuj wszystkie wykresy
    generate_strategy_comparison_linear_target()
    generate_strategy_comparison_circular_target()
    generate_velocity_ratio_trajectories()
    generate_velocity_ratio_times()
    generate_bearing_angle_effect()
    generate_cyclic_pursuit()
    generate_helix_pursuit_3d()
    generate_lissajous_pursuit_3d()
    generate_sphere_pursuit_3d()
    generate_torus_pursuit_3d()

    print()
    print("=" * 60)
    print("Wszystkie wizualizacje wygenerowane!")
    print("=" * 60)

    # Lista wygenerowanych plików
    print("\nWygenerowane pliki:")
    for f in sorted(FIGURES_DIR.glob("*.pdf")):
        print(f"  - {f.name}")


if __name__ == "__main__":
    main()
