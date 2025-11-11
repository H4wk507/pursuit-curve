import numpy as np
from numpy.typing import NDArray

from pursuit_curve.common import Strategy, TargetStrategy
from pursuit_curve.sphere.utils import spherical_to_cartesian


class ContinuousDirectPursuitSphere(Strategy):
    def __init__(self, vel: float, target_strategy: TargetStrategy):
        self.vel = vel
        self.target_strategy = target_strategy

    def tangent_direction_cart(
        self, pos_p_sph: NDArray[np.float32], pos_t_sph: NDArray[np.float32]
    ) -> NDArray[np.float32]:
        r_p, theta_p, phi_p = pos_p_sph
        r_t, theta_t, phi_t = pos_t_sph

        pos_p_cart = spherical_to_cartesian(r_p, theta_p, phi_p)
        pos_t_cart = spherical_to_cartesian(r_t, theta_t, phi_t)

        direction_3d = pos_t_cart - pos_p_cart
        radial_comp = np.dot(direction_3d, pos_p_cart) / (r_p * r_p)
        tangent_3d = direction_3d - radial_comp * pos_p_cart

        norm = np.linalg.norm(tangent_3d)
        if norm < 1e-6:
            return np.array([0.0, 0.0, 0.0], dtype=np.float32)
        return tangent_3d / norm

    def cart_vel_to_sph(self, pos_sph: NDArray[np.float32], vel_cart: NDArray[np.float32]) -> NDArray[np.float32]:
        """Konwertuje wektor prędkości w R^3 na pochodne współrzędnych sferycznych"""
        r, theta, phi = pos_sph
        vx, vy, vz = vel_cart

        dr_dt = np.cos(theta) * np.cos(phi) * vx + np.cos(theta) * np.sin(phi) * vy + np.sin(theta) * vz
        dtheta_dt = (-np.sin(theta) * np.cos(phi) * vx - np.sin(theta) * np.sin(phi) * vy + np.cos(theta) * vz) / r
        if abs(np.sin(theta)) < 1e-6:
            dphi_dt = 0.0
        else:
            dphi_dt = (-np.sin(phi) * vx + np.cos(phi) * vy) / (r * np.cos(theta))
        return np.array([dr_dt, dtheta_dt, dphi_dt], dtype=np.float32)

    def dynamics(self, t: float, y: NDArray[np.float32]) -> np.ndarray:
        # r, theta, phi
        pursuer_pos = y[0:3]
        target_pos = y[3:6]

        target_vel = self.target_strategy.calculate_movement(t)
        tangent_direction = self.tangent_direction_cart(pursuer_pos, target_pos)
        pursuer_vel_cart = self.vel * tangent_direction
        pursuer_vel = self.cart_vel_to_sph(pursuer_pos, pursuer_vel_cart)

        return np.concatenate([pursuer_vel, target_vel])

    def stop_condition(self, t: float, y: list[float]) -> np.float32:
        pursuer_pos = np.array(y[0:3], dtype=np.float32)
        target_pos = np.array(y[3:6], dtype=np.float32)
        _, theta_p, phi_p = pursuer_pos
        _, theta_t, phi_t = target_pos
        cos_dist = np.sin(theta_p) * np.sin(theta_t) + np.cos(theta_p) * np.cos(theta_t) * np.cos(phi_t - phi_p)
        cos_dist = np.clip(cos_dist, -1.0, 1.0)
        angular_distance = np.arccos(cos_dist)
        return angular_distance - 0.1

    stop_condition.terminal = True
    stop_condition.direction = -1


class ContinuousTargetSphereStrategy(TargetStrategy):
    def __init__(self, dr: float, dtheta: float, dphi: float):
        self.dr = dr
        self.dtheta = dtheta
        self.dphi = dphi

    def calculate_movement(self, t: float) -> np.ndarray:
        return np.array(
            [
                self.dr,
                self.dtheta,
                self.dphi,
            ],
            dtype=np.float32,
        )
