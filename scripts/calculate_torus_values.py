#!/usr/bin/env python3
"""
Skrypt do obliczania wartości dla pościgu na torusie dla prezentacji.
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from pursuit_curve.common import run_continuous_simulation
from pursuit_curve.torus.continuous import ContinuousDirectPursuitTorus, ContinuousTargetTorusStrategy


def calculate_torus_values():
    print("=" * 80)
    print("POŚCIG NA TORUSIE")
    print("=" * 80)

    R = 3.0  # promień główny (odległość od osi do środka rurki)

    # Prędkości kątowe celu
    omega_u = 0.5  # wokół głównej osi
    omega_v = 0.3  # wokół rurki

    pursuer_speed = 1.5

    print(f"Promień główny R = {R}")
    print(f"Prędkości kątowe celu: ω_u = {omega_u}, ω_v = {omega_v}")
    print(f"Prędkość ścigającego: v_p = {pursuer_speed}")

    # Różne stosunki R/r
    ratios = [4.0, 2.0, 1.5, 1.0, 0.67]

    for ratio in ratios:
        r = R / ratio
        print(f"\n--- Stosunek R/r = {ratio:.2f} (r = {r:.2f}) ---")

        # Pozycje startowe (u, v) - przeciwne strony torusa
        initial_pursuer = [0.0, 0.0]
        initial_target = [np.pi, np.pi / 2]
        initial_state = initial_pursuer + initial_target

        # Oblicz szacowaną prędkość celu
        # v_t ≈ sqrt((R + r*cos(v))^2 * omega_u^2 + r^2 * omega_v^2)
        # Dla v=0: v_t = sqrt((R+r)^2 * omega_u^2 + r^2 * omega_v^2)
        v_t_max = np.sqrt((R + r) ** 2 * omega_u**2 + r**2 * omega_v**2)
        print(f"  Szacowana maks. prędkość celu: {v_t_max:.2f}")
        print(f"  Stosunek v_p/v_t_max: {pursuer_speed / v_t_max:.2f}")

        target_strategy = ContinuousTargetTorusStrategy(omega_u=omega_u, omega_v=omega_v)
        strategy = ContinuousDirectPursuitTorus(vel=pursuer_speed, target_strategy=target_strategy, R=R, r=r)

        try:
            solution = run_continuous_simulation(initial_state, strategy, t_span=(0, 50), max_step=0.02)
            catch_time = solution.t[-1]

            # Oblicz długość trajektorii
            pursuer_u = solution.y[0]
            pursuer_v = solution.y[1]
            du = np.diff(pursuer_u)
            dv = np.diff(pursuer_v)

            # Metryka: ds² = (R + r·cos(v))²·du² + r²·dv²
            v_avg = (pursuer_v[:-1] + pursuer_v[1:]) / 2
            segment_lengths = np.sqrt((R + r * np.cos(v_avg)) ** 2 * du**2 + r**2 * dv**2)
            trajectory_length = float(np.sum(segment_lengths))

            # Sprawdź czy przechwycono
            if catch_time >= 49.9:
                print("  Czas pościgu: >50 s (brak przechwycenia)")
                print(f"  Długość trajektorii: {trajectory_length:.2f}")
            else:
                print(f"  Czas pościgu: {catch_time:.2f} s")
                print(f"  Długość trajektorii: {trajectory_length:.2f}")

        except Exception as e:
            print(f"  Błąd: {e}")


def calculate_torus_values_v2():
    """Wersja z różnymi prędkościami ścigającego"""
    print("\n" + "=" * 80)
    print("POŚCIG NA TORUSIE - RÓŻNE PRĘDKOŚCI")
    print("=" * 80)

    R = 3.0
    r = 1.0  # stały promień rurki

    omega_u = 0.4
    omega_v = 0.3

    print(f"R = {R}, r = {r} (R/r = {R / r:.1f})")
    print(f"ω_u = {omega_u}, ω_v = {omega_v}")

    # Szacowana prędkość celu
    v_t_avg = np.sqrt((R) ** 2 * omega_u**2 + r**2 * omega_v**2)
    print(f"Szacowana średnia prędkość celu: {v_t_avg:.2f}")

    speeds = [1.5, 2.0, 2.5, 3.0]

    for v_p in speeds:
        print(f"\n--- v_p = {v_p} (v_p/v_t ≈ {v_p / v_t_avg:.2f}) ---")

        initial_state = [0.0, 0.0, np.pi, np.pi / 2]

        target_strategy = ContinuousTargetTorusStrategy(omega_u=omega_u, omega_v=omega_v)
        strategy = ContinuousDirectPursuitTorus(vel=v_p, target_strategy=target_strategy, R=R, r=r)

        try:
            solution = run_continuous_simulation(initial_state, strategy, t_span=(0, 30), max_step=0.02)
            catch_time = solution.t[-1]

            pursuer_u = solution.y[0]
            pursuer_v = solution.y[1]
            du = np.diff(pursuer_u)
            dv = np.diff(pursuer_v)
            v_avg = (pursuer_v[:-1] + pursuer_v[1:]) / 2
            segment_lengths = np.sqrt((R + r * np.cos(v_avg)) ** 2 * du**2 + r**2 * dv**2)
            trajectory_length = float(np.sum(segment_lengths))

            # Liczba okrążeń wokół głównej osi
            total_u_change = np.abs(pursuer_u[-1] - pursuer_u[0])
            orbits_u = total_u_change / (2 * np.pi)

            if catch_time >= 29.9:
                print(f"  Czas: >30 s | Długość: {trajectory_length:.2f} | Okrążenia: {orbits_u:.2f}")
            else:
                print(f"  Czas: {catch_time:.2f} s | Długość: {trajectory_length:.2f} | Okrążenia: {orbits_u:.2f}")

        except Exception as e:
            print(f"  Błąd: {e}")


if __name__ == "__main__":
    calculate_torus_values()
    calculate_torus_values_v2()
