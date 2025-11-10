import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pursuit_curve.common import Point2D, run_continuous_simulation
from pursuit_curve.d2.continuous import (
    ContinuousConstantBearing,
    ContinuousTargetCircleStrategy,
    animate_continuous_pursuit,
)

initial_state = [15.0, 0.0, 5.0, 0.0]
strategy = ContinuousConstantBearing(
    pursuer_velocity=Point2D(1.5, 1.5),
    target_strategy=ContinuousTargetCircleStrategy(angular_velocity=0.3, r=5.0),
    bearing_angle_deg=30.0,
)

solution = run_continuous_simulation(initial_state, strategy, t_span=(0, 120))
animate_continuous_pursuit(solution, num_frames=200)
