import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pursuit_curve.common import Point2D
from pursuit_curve.d2.discrete import (
    DirectPursuit,
    Simulation,
    TargetCircleStrategy,
    animate_pursuit,
)

sim = Simulation(
    pursuer_start=Point2D(0.0, 0.0),
    target_start=Point2D(0.0, 1.0),
    pursuer_velocity=Point2D(1.5, 1.5),
    strategy=DirectPursuit(),
    target_strategy=TargetCircleStrategy(angular_velocity=0.1, dt=1.0),
    max_iters=100,
)
sim.run()
animate_pursuit(sim)
