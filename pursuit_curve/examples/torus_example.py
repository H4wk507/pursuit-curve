import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
import numpy as np

from pursuit_curve.common import run_continuous_simulation
from pursuit_curve.torus.continuous import (
    ContinuousDirectPursuitTorus,
    ContinuousTargetTorusStrategy,
    animate_torus_pursuit_3d,
)

R = 2.0
r = 1.0
initial_state = [0.0, 0.0, np.pi / 2, np.pi / 2]
strategy = ContinuousDirectPursuitTorus(
    vel=2.0,
    target_strategy=ContinuousTargetTorusStrategy(omega_u=0.5, omega_v=1.0),
    R=R,
    r=r,
)
solution = run_continuous_simulation(initial_state, strategy, t_span=(0, 120))
animate_torus_pursuit_3d(solution, R=R, r=r, num_frames=200)
