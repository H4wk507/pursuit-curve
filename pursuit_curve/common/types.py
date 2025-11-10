from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np


@dataclass
class Point2D:
    x: float
    y: float

    def __add__(self, val: Point2D) -> Point2D:
        return Point2D(self.x + val.x, self.y + val.y)

    def __sub__(self, val: Point2D) -> Point2D:
        return Point2D(self.x - val.x, self.y - val.y)


@dataclass
class Point3D:
    x: float
    y: float
    z: float

    def __add__(self, val: Point3D) -> Point3D:
        return Point3D(self.x + val.x, self.y + val.y, self.z + val.z)

    def __sub__(self, val: Point3D) -> Point3D:
        return Point3D(self.x - val.x, self.y - val.y, self.z - val.z)


@dataclass(frozen=True)
class PointND:
    _coordinates: tuple[float, ...]

    @property
    def dim(self) -> int:
        return len(self._coordinates)

    def to_list(self) -> list[float]:
        return list(self._coordinates)


class Strategy(ABC):
    @abstractmethod
    def dynamics(self, t: float, y: np.ndarray) -> np.ndarray: ...

    @abstractmethod
    def stop_condition(self, t: float, y: list[float]) -> np.float32: ...


class TargetStrategy(ABC):
    @abstractmethod
    def calculate_movement(self, t: float) -> np.ndarray: ...
