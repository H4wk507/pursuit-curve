import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D
from matplotlib.text import Text


def animate_continuous_pursuit(solution, num_frames: int = 200) -> None:
    t_eval = np.linspace(solution.t[0], solution.t[-1], num_frames)
    y_interp = solution.sol(t_eval)

    pursuer_x = y_interp[0]
    pursuer_y = y_interp[1]
    target_x = y_interp[2]
    target_y = y_interp[3]

    fig, ax = plt.subplots(figsize=(10, 8))

    all_x = np.concatenate([pursuer_x, target_x])
    all_y = np.concatenate([pursuer_y, target_y])
    margin = 1.0
    ax.set_xlim(all_x.min() - margin, all_x.max() + margin)
    ax.set_ylim(all_y.min() - margin, all_y.max() + margin)

    (line_target,) = ax.plot([], [], "r-", label="Target (Cel)", linewidth=2, alpha=0.6)
    (line_pursuer,) = ax.plot(
        [], [], "b-", label="Pursuer (Ścigający)", linewidth=2, alpha=0.6
    )

    (current_target,) = ax.plot([], [], "ro", markersize=15, alpha=0.8)
    (current_pursuer,) = ax.plot([], [], "bo", markersize=15, alpha=0.8)

    ax.plot(target_x[0], target_y[0], "r^", markersize=12, label="Start T")
    ax.plot(pursuer_x[0], pursuer_y[0], "b^", markersize=12, label="Start P")
    ax.plot(target_x[-1], target_y[-1], "rx", markersize=12, label="End T")
    ax.plot(pursuer_x[-1], pursuer_y[-1], "bx", markersize=12, label="End P")

    time_text = ax.text(
        0.02,
        0.98,
        "",
        transform=ax.transAxes,
        verticalalignment="top",
        fontsize=12,
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    )

    ax.grid(True, alpha=0.3)
    ax.set_xlabel("X", fontsize=12)
    ax.set_ylabel("Y", fontsize=12)
    ax.set_title("Continuous Pursuit Simulation", fontsize=14)
    ax.set_aspect("equal")

    def init() -> tuple[Line2D, Line2D, Line2D, Line2D, Text]:
        line_target.set_data([], [])
        line_pursuer.set_data([], [])
        current_target.set_data([], [])
        current_pursuer.set_data([], [])
        time_text.set_text("")
        return line_target, line_pursuer, current_target, current_pursuer, time_text

    def animate_frame(frame: int) -> tuple[Line2D, Line2D, Line2D, Line2D, Text]:
        line_target.set_data(target_x[: frame + 1], target_y[: frame + 1])
        line_pursuer.set_data(pursuer_x[: frame + 1], pursuer_y[: frame + 1])

        current_target.set_data([target_x[frame]], [target_y[frame]])
        current_pursuer.set_data([pursuer_x[frame]], [pursuer_y[frame]])

        time_text.set_text(f"Time: {t_eval[frame]:.2f}s")

        return line_target, line_pursuer, current_target, current_pursuer, time_text

    anim = animation.FuncAnimation(
        fig,
        animate_frame,
        init_func=init,
        frames=num_frames,
        interval=50,
        blit=True,
        repeat=True,
    )
    anim.save("animation.mp4", writer="ffmpeg", fps=30)
    plt.close(fig)
