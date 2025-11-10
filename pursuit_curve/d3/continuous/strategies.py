import math

import numpy as np
from numpy.typing import NDArray

from pursuit_curve.common import Point3D, Strategy, TargetStrategy


class ContinuousDirectPursuit3D(Strategy):
    def __init__(self, pursuer_velocity: Point3D, target_strategy: TargetStrategy):
        self.pursuer_velocity = pursuer_velocity
        self.target_strategy = target_strategy

    def dynamics(self, t: float, y: NDArray[np.float32]) -> np.ndarray:
        pursuer_pos = y[0:3]
        target_pos = y[3:6]

        target_vel = self.target_strategy.calculate_movement(t)

        direction = target_pos - pursuer_pos
        distance = np.linalg.norm(direction)
        if distance < 1e-6:
            pursuer_vel = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        else:
            pursuer_vel = (direction / distance) * np.array(
                [
                    self.pursuer_velocity.x,
                    self.pursuer_velocity.y,
                    self.pursuer_velocity.z,
                ],
                dtype=np.float32,
            )

        return np.concatenate([pursuer_vel, target_vel])

    def stop_condition(self, t: float, y: list[float]) -> np.float32:
        pursuer_pos = np.array(y[0:3], dtype=np.float32)
        target_pos = np.array(y[3:6], dtype=np.float32)
        distance = np.linalg.norm(target_pos - pursuer_pos)
        return distance - 0.5

    stop_condition.terminal = True
    stop_condition.direction = -1


class ContinuousTargetLinearStrategy3D(TargetStrategy):
    """Strategia dla celu poruszającego się liniowo."""

    def __init__(self, velocity: Point3D):
        self.velocity = velocity

    def calculate_movement(self, t: float) -> np.ndarray:
        return np.array(
            [self.velocity.x, self.velocity.y, self.velocity.z],
            dtype=np.float32,
        )


class ContinuousTargetHelixStrategy(TargetStrategy):
    """Strategia dla celu poruszającego się po helisie."""

    # x(t) = rcos(ωt)
    # y(t) = rsin(ωt)
    # z(t) = v_z*t

    def __init__(self, r: float, angular_velocity: float, vertical_velocity: float):
        self.r = r
        self.angular_velocity = angular_velocity
        self.vertical_velocity = vertical_velocity

    def calculate_movement(self, t: float) -> np.ndarray:
        return np.array(
            [
                self.r * math.cos(self.angular_velocity * t),
                self.r * math.sin(self.angular_velocity * t),
                self.vertical_velocity * t,
            ],
            dtype=np.float32,
        )


class ContinuousTargetLissajousStrategy(TargetStrategy):
    """Strategia dla celu poruszającego się po krzywej Lissajous."""

    # x(t) = A_x*sin(ω_x*t)
    # y(t) = A_y*sin(ω_y*t)
    # z(t) = A_z*sin(ω_z*t)

    def __init__(self, A: Point3D, angular_velocity: Point3D):
        self.A = A
        self.angular_velocity = angular_velocity

    def calculate_movement(self, t: float) -> np.ndarray:
        return np.array(
            [
                self.A.x * math.sin(self.angular_velocity.x * t),
                self.A.y * math.sin(self.angular_velocity.y * t),
                self.A.z * math.sin(self.angular_velocity.z * t),
            ],
            dtype=np.float32,
        )
