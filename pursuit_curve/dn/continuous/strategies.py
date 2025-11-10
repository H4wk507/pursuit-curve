import numpy as np
from numpy.typing import NDArray

from pursuit_curve.common import PointND, Strategy, TargetStrategy


class ContinuousDirectPursuitND(Strategy):
    def __init__(self, pursuer_velocity: PointND, target_strategy: TargetStrategy):
        self.n = pursuer_velocity.dim
        self.pursuer_velocity = pursuer_velocity
        self.target_strategy = target_strategy

    def dynamics(self, t: float, y: NDArray[np.float32]) -> np.ndarray:
        pursuer_pos = y[0 : self.n]
        target_pos = y[self.n : 2 * self.n]

        target_vel = self.target_strategy.calculate_movement(t)

        direction = target_pos - pursuer_pos
        distance = np.linalg.norm(direction)
        if distance < 1e-6:
            pursuer_vel = np.zeros(self.n, dtype=np.float32)
        else:
            pursuer_vel = (direction / distance) * np.array(
                self.pursuer_velocity.to_list(),
                dtype=np.float32,
            )

        return np.concatenate([pursuer_vel, target_vel])

    def stop_condition(self, t: float, y: list[float]) -> np.float32:
        pursuer_pos = np.array(y[0 : self.n], dtype=np.float32)
        target_pos = np.array(y[self.n : 2 * self.n], dtype=np.float32)
        distance = np.linalg.norm(target_pos - pursuer_pos)
        return distance - 0.5

    stop_condition.terminal = True
    stop_condition.direction = -1


class ContinuousTargetLinearStrategyND(TargetStrategy):
    """Strategia dla celu poruszającego się liniowo w przestrzeni N-wymiarowej."""

    def __init__(self, velocity: PointND):
        self.velocity = velocity

    def calculate_movement(self, t: float) -> np.ndarray:
        return np.array(self.velocity.to_list(), dtype=np.float32)
