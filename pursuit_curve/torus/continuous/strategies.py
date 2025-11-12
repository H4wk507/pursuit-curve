import numpy as np
from numpy.typing import NDArray

from pursuit_curve.common import Strategy, TargetStrategy


class ContinuousDirectPursuitTorus(Strategy):
    def __init__(self, vel: float, target_strategy: TargetStrategy, R: float, r: float):
        self.vel = vel
        self.target_strategy = target_strategy
        self.R = R
        self.r = r

    def shortest_angular_distance(self, angle_from: float, angle_to: float) -> float:
        """
        Out: [-pi, pi]  [rad]
        """
        d = angle_to - angle_from
        return np.arctan2(np.sin(d), np.cos(d))

    def tangent_direction(self, pos_p: NDArray[np.float32], pos_t: NDArray[np.float32]) -> NDArray[np.float32]:
        p_u, p_v = pos_p
        t_u, t_v = pos_t

        delta_u = self.shortest_angular_distance(p_u, t_u)
        delta_v = self.shortest_angular_distance(p_v, t_v)

        # Kierunek w przestrzeni stycznej z metryką Riemanna
        # Metryka Riemanna dla torusa: ds² = (R + r·cos(v))²·du² + r²·dv²
        d_u = (self.R + self.r * np.cos(p_v)) * delta_u
        d_v = self.r * delta_v

        norm = np.sqrt(d_u**2 + d_v**2)
        if norm < 1e-6:
            return np.array([0.0, 0.0], dtype=np.float32)
        return np.array([d_u / norm, d_v / norm], dtype=np.float32)

    def tangent_to_angular_vel(self, pos: NDArray[np.float32], tangent: NDArray[np.float32]) -> NDArray[np.float32]:
        _, v = pos
        t_u, t_v = tangent

        # Prędkości kątowe z uwzględnieniem metryki
        # Dzielimy przez długości wektorów bazowych
        du_dt = self.vel * t_u / (self.R + self.r * np.cos(v))
        dv_dt = self.vel * t_v / self.r

        return np.array([du_dt, dv_dt], dtype=np.float32)

    def dynamics(self, t: float, y: NDArray[np.float32]) -> np.ndarray:
        # u, v
        pursuer_pos = y[0:2]
        target_pos = y[2:4]

        target_vel = self.target_strategy.calculate_movement(t)

        tangent = self.tangent_direction(pursuer_pos, target_pos)
        pursuer_vel = self.tangent_to_angular_vel(pursuer_pos, tangent)

        return np.concatenate([pursuer_vel, target_vel])

    def stop_condition(self, t: float, y: list[float]) -> np.float32:
        pursuer_pos = np.array(y[0:2], dtype=np.float32)
        target_pos = np.array(y[2:4], dtype=np.float32)

        p_u, p_v = pursuer_pos
        t_u, t_v = target_pos

        delta_u = self.shortest_angular_distance(p_u, t_u)
        delta_v = self.shortest_angular_distance(p_v, t_v)

        # Odległość w metryce Riemanna ds² = (R + r·cos(v))²·du² + r²·dv²
        dist = np.sqrt(
            (self.R + self.r * np.cos(p_v)) ** 2 * delta_u**2 + self.r**2 * delta_v**2,
        )

        return dist - 0.1

    stop_condition.terminal = True
    stop_condition.direction = -1


class ContinuousTargetTorusStrategy(TargetStrategy):
    def __init__(self, omega_u: float, omega_v: float):
        """
        omega_u - Predkość kątowa wokół głównej osi torusa [rad/s]
        omega_v - Predkość kątowa wokół rurki [rad/s]
        """
        self.omega_u = omega_u
        self.omega_v = omega_v

    def calculate_movement(self, t: float) -> np.ndarray:
        return np.array([self.omega_u, self.omega_v], dtype=np.float32)
