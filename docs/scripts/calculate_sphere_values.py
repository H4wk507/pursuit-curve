#!/usr/bin/env python3
"""
Skrypt do obliczania wartości dla pościgu na sferze S^2 dla prezentacji.
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pursuit_curve.common import run_continuous_simulation
from pursuit_curve.sphere.continuous import ContinuousDirectPursuitSphere, ContinuousTargetSphereStrategy

R = 5.0  # promień sfery
dtheta = 0.1  # rad/s
dphi = np.pi / 4  # rad/s

target_speed_estimate = R * np.sqrt(dtheta**2 + dphi**2)
print(f"Promień sfery: R = {R}")
print(f"Prędkości kątowe celu: dθ/dt = {dtheta}, dφ/dt = {dphi:.4f}")
print(f"Szacowana prędkość liniowa celu: ~{target_speed_estimate:.2f}")

initial_pursuer = [R, np.pi / 4, 2.0]
initial_target = [R, 0.0, 0.0]
initial_state = initial_pursuer + initial_target

theta_p, phi_p = initial_pursuer[1], initial_pursuer[2]
theta_t, phi_t = initial_target[1], initial_target[2]
cos_dist = np.sin(theta_p) * np.sin(theta_t) + np.cos(theta_p) * np.cos(theta_t) * np.cos(phi_t - phi_p)
initial_angular_dist = np.arccos(np.clip(cos_dist, -1.0, 1.0))
print(f"Początkowa odległość kątowa: {initial_angular_dist:.3f} rad ({np.degrees(initial_angular_dist):.1f}°)")

velocity_ratios = [1.5, 2.0, 3.0]

for ratio in velocity_ratios:
    pursuer_speed = ratio * target_speed_estimate
    print(f"\n--- Stosunek prędkości v_p/v_t ≈ {ratio} (v_p = {pursuer_speed:.2f}) ---")

    target_strategy = ContinuousTargetSphereStrategy(dr=0.0, dtheta=dtheta, dphi=dphi)
    strategy = ContinuousDirectPursuitSphere(vel=pursuer_speed, target_strategy=target_strategy)

    try:
        solution = run_continuous_simulation(initial_state, strategy, t_span=(0, 120), max_step=0.01)
        catch_time = solution.t[-1]

        pursuer_theta = solution.y[1]
        pursuer_phi = solution.y[2]
        dtheta_traj = np.diff(pursuer_theta)
        dphi_traj = np.diff(pursuer_phi)
        sin_theta_avg = np.sin((pursuer_theta[:-1] + pursuer_theta[1:]) / 2)
        segment_lengths = np.sqrt(dtheta_traj**2 + (sin_theta_avg * dphi_traj) ** 2)
        trajectory_length = float(np.sum(segment_lengths))

        total_phi_change = np.abs(pursuer_phi[-1] - pursuer_phi[0])
        num_orbits = total_phi_change / (2 * np.pi)

        print(f"Czas pościgu: {catch_time:.2f} s")
        print(f"Długość trajektorii: {trajectory_length:.2f} rad")
        print(f"Liczba okrążeń: {num_orbits:.2f}")

    except Exception as e:
        print(f"Błąd: {e}")
