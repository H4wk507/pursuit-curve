import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pursuit_curve.common import Point2D
from pursuit_curve.discrete import ProportionalNavigation, Simulation, animate_pursuit

sim = Simulation(
    pursuer_start=Point2D(0.0, 0.0),
    target_start=Point2D(10.0, 3.0),
    pursuer_velocity=Point2D(2.2, 1.8),
    target_velocity=Point2D(1.5, -0.5),
    strategy=ProportionalNavigation(3.0),
    max_iters=100,
)
sim.run()
animate_pursuit(sim)
