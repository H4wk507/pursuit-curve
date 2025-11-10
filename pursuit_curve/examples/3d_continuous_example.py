import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pursuit_curve.common import Point3D, run_continuous_simulation
from pursuit_curve.d3.continuous import (
    ContinuousDirectPursuit3D,
    ContinuousTargetLissajousStrategy,
    animate_continuous_pursuit_3d,
)

initial_state = [12.0, 12.0, 12.0, 5.0, 0.0, 0.0]
strategy = ContinuousDirectPursuit3D(
    pursuer_velocity=Point3D(2.5, 2.5, 2.5),
    target_strategy=ContinuousTargetLissajousStrategy(
        A=Point3D(5.0, 5.0, 5.0),
        angular_velocity=Point3D(2.0, 3.0, 5.0),
    ),
)
solution = run_continuous_simulation(initial_state, strategy, t_span=(0, 120))
animate_continuous_pursuit_3d(solution, num_frames=200)
