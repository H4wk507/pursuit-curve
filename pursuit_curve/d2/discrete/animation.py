import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from .simulation import Simulation


def animate_pursuit(simulation: Simulation) -> None:
    """Animuj wyniki symulacji dyskretnej."""
    tps = simulation.target_positions
    pps = simulation.pursuer_positions

    fig, ax = plt.subplots(figsize=(8, 8))

    all_x = [point.x for point in tps] + [point.x for point in pps]
    all_y = [point.y for point in tps] + [point.y for point in pps]
    ax.set_xlim(min(all_x) - 1, max(all_x) + 1)
    ax.set_ylim(min(all_y) - 1, max(all_y) + 1)

    (line_target,) = ax.plot([], [], "ro-", label="Target (Cel)", linewidth=2, markersize=8)
    (line_pursuer,) = ax.plot([], [], "bo-", label="Pursuer (Ścigający)", linewidth=2, markersize=8)

    (current_target,) = ax.plot([], [], "ro", markersize=15, alpha=0.7)
    (current_pursuer,) = ax.plot([], [], "bo", markersize=15, alpha=0.7)

    ax.legend()
    ax.grid(True)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Discrete Pursuit Simulation")

    def init() -> tuple[Line2D, Line2D, Line2D, Line2D]:
        line_target.set_data([], [])
        line_pursuer.set_data([], [])
        current_target.set_data([], [])
        current_pursuer.set_data([], [])
        return line_target, line_pursuer, current_target, current_pursuer

    def animate_frame(frame: int) -> tuple[Line2D, Line2D, Line2D, Line2D]:
        x_coords_target = [tps[i].x for i in range(frame + 1)]
        y_coords_target = [tps[i].y for i in range(frame + 1)]
        line_target.set_data(x_coords_target, y_coords_target)

        x_coords_pursuer = [pps[i].x for i in range(frame + 1)]
        y_coords_pursuer = [pps[i].y for i in range(frame + 1)]
        line_pursuer.set_data(x_coords_pursuer, y_coords_pursuer)

        current_target.set_data([tps[frame].x], [tps[frame].y])
        current_pursuer.set_data([pps[frame].x], [pps[frame].y])

        return line_target, line_pursuer, current_target, current_pursuer

    anim = animation.FuncAnimation(
        fig,
        animate_frame,
        init_func=init,
        frames=len(tps),
        interval=50,
        blit=True,
        repeat=True,
    )
    anim.save("animation.mp4", writer="ffmpeg", fps=30)
    plt.close(fig)
