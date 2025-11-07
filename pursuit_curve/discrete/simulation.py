from ..common import Point2D
from .types import Strategy


class Simulation:
    def __init__(
        self,
        pursuer_start: Point2D,
        target_start: Point2D,
        pursuer_velocity: Point2D,
        target_velocity: Point2D,
        strategy: Strategy,
        max_iters: int = 1000,
    ):
        self.pursuer_positions = [pursuer_start]
        self.target_positions = [target_start]
        self.pursuer_velocity = pursuer_velocity
        self.target_velocity = target_velocity
        self.strategy = strategy
        self.max_iters = max_iters

    def _step(self) -> tuple[Point2D, Point2D]:
        target = self.target_positions[-1]
        target += self.target_velocity
        self.target_positions.append(target)

        pursuer = self.pursuer_positions[-1]
        movement = self.strategy.calculate_movement(
            pursuer, target, self.pursuer_velocity
        )
        pursuer += movement
        self.pursuer_positions.append(pursuer)

        return pursuer, target

    def _should_stop(self, pursuer: Point2D, target: Point2D) -> bool:
        dx = target.x - pursuer.x
        dy = target.y - pursuer.y
        dist = (dx * dx + dy * dy) ** 0.5
        return dist < 0.45

    def run(self) -> None:
        caught = False
        for i in range(self.max_iters):
            p, t = self._step()
            if self._should_stop(p, t):
                print(f"Złapano cel po {i} krokach.")
                caught = True
                break
        if not caught:
            print(f"Nie udało się złapać celu po {self.max_iters} krokach.")
