from abc import ABC, abstractmethod

from pursuit_curve.common import Point2D


class Strategy(ABC):
    @abstractmethod
    def calculate_movement(self, pursuer: Point2D, target: Point2D, pursuer_velocity: Point2D) -> Point2D: ...


class TargetStrategy(ABC):
    @abstractmethod
    def calculate_movement(self, target: Point2D) -> Point2D: ...
