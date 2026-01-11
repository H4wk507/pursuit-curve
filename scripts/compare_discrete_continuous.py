import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pursuit_curve.common.continuous_simulation import run_continuous_simulation
from pursuit_curve.common.types import Point2D
from pursuit_curve.common.types import TargetStrategy as ContinuousTargetStrategy
from pursuit_curve.d2.continuous.strategies import (
    ContinuousDirectPursuit,
)
from pursuit_curve.d2.discrete import DirectPursuit as DiscreteDirectPursuit
from pursuit_curve.d2.discrete import Simulation as DiscreteSimulation
from pursuit_curve.d2.discrete import TargetCircleStrategy as DiscreteTargetCircular

# --- Configuration ---
PURSUER_START = Point2D(8.0, 0.0)
TARGET_START = Point2D(0.0, 5.0)
PURSUER_SPEED = 6.0
TARGET_RADIUS = np.sqrt(TARGET_START.x**2 + TARGET_START.y**2)
TARGET_ANGULAR_VELOCITY = 0.5
# Initial angle of the target is atan2(5, 0) = pi/2
TARGET_INITIAL_PHASE = np.arctan2(TARGET_START.y, TARGET_START.x)
T_MAX = 10.0
STOP_RADIUS = 0.5


# --- 1. Run Continuous Simulation (Ground Truth) ---


# Define a target strategy for the continuous simulation that respects the initial phase
class TargetCircularWithPhase(ContinuousTargetStrategy):
    def __init__(self, angular_velocity: float, radius: float, initial_phase: float):
        self.angular_velocity = angular_velocity
        self.radius = radius
        self.initial_phase = initial_phase

    def calculate_movement(self, t: float) -> np.ndarray:
        """Returns target velocity vector at time t."""
        angle = self.angular_velocity * t + self.initial_phase
        vx = -self.radius * self.angular_velocity * np.sin(angle)
        vy = self.radius * self.angular_velocity * np.cos(angle)
        return np.array([vx, vy], dtype=np.float32)

    def get_position(self, t: float) -> np.ndarray:
        """Returns target position vector at time t."""
        angle = self.angular_velocity * t + self.initial_phase
        x = self.radius * np.cos(angle)
        y = self.radius * np.sin(angle)
        return np.array([x, y], dtype=np.float32)


print("Running continuous simulation...")
# This strategy object contains all the logic for the solver
continuous_target_strategy = TargetCircularWithPhase(TARGET_ANGULAR_VELOCITY, TARGET_RADIUS, TARGET_INITIAL_PHASE)
# The continuous pursuit strategy needs the target strategy to calculate the full dynamics
continuous_pursuit_strategy = ContinuousDirectPursuit(Point2D(PURSUER_SPEED, PURSUER_SPEED), continuous_target_strategy)

# Set up the initial state vector for the solver
initial_state = [PURSUER_START.x, PURSUER_START.y, TARGET_START.x, TARGET_START.y]

solution = run_continuous_simulation(
    initial_state=initial_state,
    strategy=continuous_pursuit_strategy,
    t_span=(0, T_MAX),
    max_step=0.01,  # Use small steps for a good reference curve
)

# Extract continuous data
t_continuous = solution.t
pursuer_continuous = solution.y[:2, :]
# For the plot, we can get the target's true path from its own strategy
target_continuous = np.array([continuous_target_strategy.get_position(t) for t in t_continuous]).T
print(f"Continuous simulation finished at t={t_continuous[-1]:.2f}s")


# --- 2. Run Discrete Simulations with different dt ---
DT_VALUES = [0.25, 0.2, 0.05]
discrete_results = {}

print("\nRunning discrete simulations...")
for dt in DT_VALUES:
    # The discrete target strategy implicitly uses the initial position as the starting point
    # of the rotation, which is what we want.
    discrete_target_strat = DiscreteTargetCircular(TARGET_ANGULAR_VELOCITY)

    discrete_sim = DiscreteSimulation(
        pursuer_start=Point2D(PURSUER_START.x, PURSUER_START.y),
        target_start=Point2D(TARGET_START.x, TARGET_START.y),
        pursuer_velocity=Point2D(PURSUER_SPEED, PURSUER_SPEED),
        strategy=DiscreteDirectPursuit(),
        target_strategy=discrete_target_strat,
        dt=dt,
        max_iters=int(T_MAX / dt) + 1,
    )
    discrete_sim.run()
    discrete_results[dt] = {
        "pursuer": np.array(
            [[p.x for p in discrete_sim.pursuer_positions], [p.y for p in discrete_sim.pursuer_positions]]
        ),
    }
    print(f"Discrete simulation with dt={dt} finished.")


# --- 3. Plot Results ---
print("\nGenerating plot...")
plt.style.use("default")
fig, ax = plt.subplots(figsize=(8, 8))

# Plot continuous
ax.plot(
    pursuer_continuous[0, :],
    pursuer_continuous[1, :],
    label="Ciągła (referencja)",
    color="black",
    linestyle="--",
    linewidth=2,
)
ax.plot(target_continuous[0, :], target_continuous[1, :], color="gray", label="Trajektoria celu", linestyle=":")

# Plot discrete
colors = plt.cm.viridis(np.linspace(0.8, 0.2, len(DT_VALUES)))
for i, dt in enumerate(DT_VALUES):
    ax.plot(
        discrete_results[dt]["pursuer"][0, :],
        discrete_results[dt]["pursuer"][1, :],
        label=f"Dyskretna (dt={dt}s)",
        color=colors[i],
        marker=".",
        markersize=4,
        linestyle="-",
    )

# Mark points
ax.plot(PURSUER_START.x, PURSUER_START.y, "o", color="red", markersize=8, label="Start ścigającego")
ax.plot(TARGET_START.x, TARGET_START.y, "o", color="blue", markersize=8, label="Start celu")
ax.plot(
    pursuer_continuous[0, -1],
    pursuer_continuous[1, -1],
    "x",
    color="black",
    markersize=10,
    mew=2,
    label="Przechwycenie",
)


ax.set_title("Porównanie symulacji ciągłej i dyskretnej")
ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")
ax.legend()
ax.axis("equal")
ax.grid(True)

# Save figure
output_path = Path(__file__).parent.parent / "figures" / "discrete_vs_continuous.pdf"
plt.savefig(output_path, bbox_inches="tight")
print(f"Plot saved to {output_path}")

# --- 4. Calculate and Print Error ---
print("\n--- Analiza Błędu ---")
# Get the final position from the continuous simulation
final_pos_continuous = pursuer_continuous[:, -1]
final_time_continuous = t_continuous[-1]

print(f"Czas przechwycenia (ciągła): {final_time_continuous:.4f} s")
for dt in DT_VALUES:
    pursuer_discrete = discrete_results[dt]["pursuer"]
    final_pos_discrete = pursuer_discrete[:, -1]
    num_steps = pursuer_discrete.shape[1] - 1
    final_time_discrete = num_steps * dt

    error = np.linalg.norm(final_pos_continuous - final_pos_discrete)

    print(f"dt={dt:>4.2f}s | Czas: {final_time_discrete:.4f}s | Błąd pozycji końcowej: {error:.4f} m")
