from abc import ABC, abstractmethod
from numpy.typing import NDArray
import numpy as np


class Strategy(ABC):
    @abstractmethod
    def dynamics(self, t: float, y: NDArray[np.float32]) -> np.ndarray: ...

    @abstractmethod
    def stop_condition(self, t: float, y: list[float]) -> np.float32: ...


class TargetStrategy(ABC):
    @abstractmethod
    def calculate_movement(self, t: float) -> NDArray[np.float32]: ...
