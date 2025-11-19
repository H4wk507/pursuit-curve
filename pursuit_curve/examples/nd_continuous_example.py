import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pursuit_curve.common import PointND, run_continuous_simulation
from pursuit_curve.dn.continuous import (
    ContinuousDirectPursuitND,
    ContinuousTargetLinearStrategyND,
)

n = 1000

initial_state = [12.0 + i for i in range(n * 2)]
strategy = ContinuousDirectPursuitND(
    pursuer_velocity=PointND(tuple([2.0 for _ in range(n)])),
    target_strategy=ContinuousTargetLinearStrategyND(velocity=PointND(tuple([1.0 for _ in range(n)]))),
)
solution = run_continuous_simulation(initial_state, strategy, t_span=(0, 120))
print(solution)
