import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pursuit_curve.common import PointND, run_continuous_simulation
from pursuit_curve.dn.continuous import (
    ContinuousDirectPursuitND,
    ContinuousTargetLinearStrategyND,
)

initial_state = [12.0, 12.0, 12.0, 12.0, 12.0, 5.0, 0.0, 0.0, 0.0, 0.0]
strategy = ContinuousDirectPursuitND(
    pursuer_velocity=PointND((2.5, 2.5, 2.5, 2.5, 2.5)),
    target_strategy=ContinuousTargetLinearStrategyND(velocity=PointND((1.0, 0.5, 0.0, 1.0, 0.5))),
)
solution = run_continuous_simulation(initial_state, strategy, t_span=(0, 120))
print(solution)
