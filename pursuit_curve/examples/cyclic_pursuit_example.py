# N punktów ustawionych na obwodzie okręgu o promieniu r i środku (0, 0)
# Punkt i ściga punkt i+1 (mod N)
# Każdy punkt ma tę samą wartość prędkości, która jest stała w czasie
# Kąt początkowy punktu i na okręgu θ_i = 2πi/N

import sys
from itertools import chain
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pursuit_curve.common import Point2D, run_continuous_simulation
from pursuit_curve.d2.continuous import ContinuousCyclicPursuit, cyclic_pursuit_animation

n = 18
r = 150.0
initial_state = list(
    chain.from_iterable([(r * np.cos(i * 2 * np.pi / n), r * np.sin(i * 2 * np.pi / n)) for i in range(n)])
)
strategy = ContinuousCyclicPursuit(velocity=Point2D(1.0, 1.0), n=n)
solution = run_continuous_simulation(
    initial_state,
    strategy,
    t_span=(0, 1200),
)


cyclic_pursuit_animation(solution)
