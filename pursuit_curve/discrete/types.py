from abc import ABC, abstractmethod

from ..common import Point2D


class Strategy(ABC):
    @abstractmethod
    def calculate_movement(
        self, pursuer: Point2D, target: Point2D, pursuer_velocity: Point2D
    ) -> Point2D: ...
