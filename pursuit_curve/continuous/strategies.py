import numpy as np
from numpy.typing import NDArray
from ..common import Point2D
from .types import Strategy, TargetStrategy

import math


class ContinuousDirectPursuit(Strategy):
    """Kierunek wprost na cel - wersja ciągła."""

    def __init__(self, pursuer_velocity: Point2D, target_strategy: TargetStrategy):
        self.pursuer_velocity = pursuer_velocity
        self.target_strategy = target_strategy

    def dynamics(self, t: float, y: NDArray[np.float32]) -> np.ndarray:
        """
        t - czas
        y = [pursuer_x, pursuer_y, target_x, target_y] w czasie t
        Zwraca pochodne: [dx_p/dt, dy_p/dt, dx_t/dt, dy_t/dt]
        """
        pursuer_pos = y[0:2]
        target_pos = y[2:4]

        target_vel = self.target_strategy.calculate_movement(t)

        direction = target_pos - pursuer_pos
        distance = np.linalg.norm(direction)

        if distance < 1e-6:
            pursuer_vel = np.array([0.0, 0.0], dtype=np.float32)
        else:
            pursuer_vel = (direction / distance) * np.array(
                [self.pursuer_velocity.x, self.pursuer_velocity.y], dtype=np.float32
            )

        return np.concatenate([pursuer_vel, target_vel])

    def stop_condition(self, t: float, y: list[float]) -> np.float32:
        """Zatrzymaj gdy odległość < 0.5"""
        pursuer_pos = np.array(y[0:2], dtype=np.float32)
        target_pos = np.array(y[2:4], dtype=np.float32)
        distance = np.linalg.norm(target_pos - pursuer_pos)
        return distance - 0.5

    stop_condition.terminal = True
    stop_condition.direction = -1


class ContinuousConstantBearing(Strategy):
    """Constant bearing - wersja ciągła."""

    def __init__(
        self,
        pursuer_velocity: Point2D,
        target_strategy: TargetStrategy,
        bearing_angle_deg: float,
    ):
        self.pursuer_velocity = pursuer_velocity
        self.target_strategy = target_strategy
        self.bearing_angle = np.radians(bearing_angle_deg)

    def dynamics(self, t: float, y: NDArray[np.float32]) -> np.ndarray:
        pursuer_pos = y[0:2]
        target_pos = y[2:4]

        target_vel = self.target_strategy.calculate_movement(t)

        direction = target_pos - pursuer_pos
        angle_to_target = np.arctan2(direction[1], direction[0])
        movement_angle = angle_to_target + self.bearing_angle

        pursuer_vel = np.array(
            [
                self.pursuer_velocity.x * np.cos(movement_angle),
                self.pursuer_velocity.y * np.sin(movement_angle),
            ]
        )

        return np.concatenate([pursuer_vel, target_vel])

    def stop_condition(self, t: float, y: list[float]) -> np.float32:
        pursuer_pos = np.array(y[0:2], dtype=np.float32)
        target_pos = np.array(y[2:4], dtype=np.float32)
        distance = np.linalg.norm(target_pos - pursuer_pos)
        return distance - 0.5

    stop_condition.terminal = True
    stop_condition.direction = -1


class ContinuousProportionalNavigation(Strategy):
    """
    Proportional Navigation - wersja ciągła.
    Używana w rakietach i pociskach.
    Prędkość kątowa ścigającego jest proporcjonalna do prędkości kątowej linii namiarowania (LOS).
    https://en.wikipedia.org/wiki/Proportional_navigation
    """

    def __init__(
        self, pursuer_velocity: Point2D, target_strategy: TargetStrategy, N: float = 3.0
    ):
        self.pursuer_velocity = pursuer_velocity
        self.target_strategy = target_strategy
        self.N = N
        self.previous_los_angle: float | None = None
        self.previous_pursuer_vel: NDArray[np.float32] | None = None

    def dynamics(self, t: float, y: NDArray[np.float32]) -> np.ndarray:
        pursuer_pos = y[0:2]
        target_pos = y[2:4]

        target_vel = self.target_strategy.calculate_movement(t)

        direction = target_pos - pursuer_pos
        los_angle = np.arctan2(direction[1], direction[0])
        if self.previous_los_angle is None:
            self.previous_los_angle = los_angle
            self.previous_pursuer_vel = np.array(
                [
                    self.pursuer_velocity.x * np.cos(los_angle),
                    self.pursuer_velocity.y * np.sin(los_angle),
                ],
                dtype=np.float32,
            )
            return np.concatenate([self.previous_pursuer_vel, target_vel])

        delta_los_angle = los_angle - self.previous_los_angle
        while delta_los_angle > np.pi:
            delta_los_angle -= 2 * np.pi
        while delta_los_angle < -np.pi:
            delta_los_angle += 2 * np.pi

        if self.previous_pursuer_vel is None:
            pursuer_angle = los_angle
        else:
            pursuer_angle = np.arctan2(
                self.previous_pursuer_vel[1], self.previous_pursuer_vel[0]
            )

        new_pursuer_angle = pursuer_angle + self.N * delta_los_angle
        new_vel = np.array(
            [
                self.pursuer_velocity.x * np.cos(new_pursuer_angle),
                self.pursuer_velocity.y * np.sin(new_pursuer_angle),
            ],
            dtype=np.float32,
        )

        self.previous_los_angle = los_angle
        self.previous_pursuer_vel = new_vel
        return np.concatenate([new_vel, target_vel])

    def stop_condition(self, t: float, y: list[float]) -> np.float32:
        pursuer_pos = np.array(y[0:2], dtype=np.float32)
        target_pos = np.array(y[2:4], dtype=np.float32)
        distance = np.linalg.norm(target_pos - pursuer_pos)
        return distance - 0.5

    stop_condition.terminal = True
    stop_condition.direction = -1


class ContinuousTargetCircleStrategy(TargetStrategy):
    """Strategia dla celu poruszającego się po okręgu."""

    def __init__(self, angular_velocity: float, r: float):
        self.angular_velocity = angular_velocity
        self.r = r

    def calculate_movement(self, t: float) -> np.ndarray:
        return np.array(
            [
                self.r * math.cos(self.angular_velocity * t),
                self.r * math.sin(self.angular_velocity * t),
            ],
            dtype=np.float32,
        )


class ContinuousTargetLinearStrategy(TargetStrategy):
    """Strategia dla celu poruszającego się liniowo."""

    def __init__(self, velocity: Point2D):
        self.velocity = velocity

    def calculate_movement(self, t: float) -> np.ndarray:
        return np.array(
            [self.velocity.x, self.velocity.y],
            dtype=np.float32,
        )
