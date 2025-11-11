import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
import numpy as np

from pursuit_curve.common import run_continuous_simulation
from pursuit_curve.sphere.continuous import (
    ContinuousDirectPursuitSphere,
    ContinuousTargetSphereStrategy,
    animate_sphere_pursuit_3d,
)

initial_state = [5.0, np.pi / 4, 2.0, 5.0, 0.0, 0.0]
strategy = ContinuousDirectPursuitSphere(
    vel=1.5,
    target_strategy=ContinuousTargetSphereStrategy(dr=0.0, dtheta=0.1, dphi=np.pi / 4),
)
solution = run_continuous_simulation(initial_state, strategy, t_span=(0, 120))
animate_sphere_pursuit_3d(solution, num_frames=200)
