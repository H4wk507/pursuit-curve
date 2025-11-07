import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pursuit_curve.continuous import (
    ContinuousProportionalNavigation,
    run_continuous_simulation,
    animate_continuous_pursuit,
)
from pursuit_curve.common import Point2D

initial_state = [0.0, 0.0, 10.0, 3.0]
strategy = ContinuousProportionalNavigation(
    target_velocity=Point2D(1.5, -0.5),
    pursuer_velocity=Point2D(np.sqrt(2.2**2 + 1.8**2), np.sqrt(2.2**2 + 1.8**2)),
    N=3.0,
)

solution = run_continuous_simulation(initial_state, strategy)
animate_continuous_pursuit(solution, num_frames=200)
