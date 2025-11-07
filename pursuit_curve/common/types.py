from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Point2D:
    x: float
    y: float

    def __add__(self, val: Point2D) -> Point2D:
        return Point2D(self.x + val.x, self.y + val.y)

    def __sub__(self, val: Point2D) -> Point2D:
        return Point2D(self.x - val.x, self.y - val.y)
