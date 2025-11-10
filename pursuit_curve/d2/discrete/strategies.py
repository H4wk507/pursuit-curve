import math

from pursuit_curve.common import Point2D

from .types import Strategy, TargetStrategy


class DirectPursuit(Strategy):
    """Kierunek wprost na cel."""

    def calculate_movement(self, pursuer: Point2D, target: Point2D, pursuer_velocity: Point2D) -> Point2D:
        w = target - pursuer
        norm = (w.x * w.x + w.y * w.y) ** 0.5
        return Point2D(pursuer_velocity.x * w.x / norm, pursuer_velocity.y * w.y / norm)


class ConstantBearing(Strategy):
    """Kierunek do celu, ale odchylony o dany kąt."""

    def __init__(self, bearing_angle_deg: float):
        self.bearing_angle = math.radians(bearing_angle_deg)

    def calculate_movement(self, pursuer: Point2D, target: Point2D, pursuer_velocity: Point2D) -> Point2D:
        w = target - pursuer
        angle_to_target = math.atan2(w.y, w.x)
        movement_angle = angle_to_target + self.bearing_angle
        return Point2D(
            pursuer_velocity.x * math.cos(movement_angle),
            pursuer_velocity.y * math.sin(movement_angle),
        )


class ProportionalNavigation(Strategy):
    """
    Używana w rakietach i pociskach.
    Prędkość kątowa ścigającego jest proporcjonalna do prędkości kątowej linii namiarowania (LOS).
    https://en.wikipedia.org/wiki/Proportional_navigation
    """

    def __init__(self, N: float = 3.0):
        self.N = N
        self.previous_los_angle: float | None = None
        self.previous_pursuer_vel: Point2D | None = None

    def calculate_movement(self, pursuer: Point2D, target: Point2D, pursuer_velocity: Point2D) -> Point2D:
        w = target - pursuer

        los_angle = math.atan2(w.y, w.x)
        if self.previous_los_angle is None:
            self.previous_los_angle = los_angle
            self.previous_pursuer_vel = Point2D(
                pursuer_velocity.x * math.cos(los_angle),
                pursuer_velocity.y * math.sin(los_angle),
            )
            return self.previous_pursuer_vel

        delta_los_angle = los_angle - self.previous_los_angle
        while delta_los_angle > math.pi:
            delta_los_angle -= 2 * math.pi
        while delta_los_angle < -math.pi:
            delta_los_angle += 2 * math.pi

        if self.previous_pursuer_vel is None:
            pursuer_angle = los_angle
        else:
            pursuer_angle = math.atan2(self.previous_pursuer_vel.y, self.previous_pursuer_vel.x)

        new_pursuer_angle = pursuer_angle + self.N * delta_los_angle
        new_vel = Point2D(
            pursuer_velocity.x * math.cos(new_pursuer_angle),
            pursuer_velocity.y * math.sin(new_pursuer_angle),
        )

        self.previous_los_angle = los_angle
        self.previous_pursuer_vel = new_vel
        return new_vel


class TargetCircleStrategy(TargetStrategy):
    """Strategia dla celu poruszającego się po okręgu."""

    def __init__(self, angular_velocity: float, dt: float):
        self.angular_velocity = angular_velocity
        self.dt = dt

    def calculate_movement(self, target: Point2D) -> Point2D:
        return Point2D(
            target.x * math.cos(self.angular_velocity * self.dt) - target.y * math.sin(self.angular_velocity * self.dt),
            target.x * math.sin(self.angular_velocity * self.dt) + target.y * math.cos(self.angular_velocity * self.dt),
        )
