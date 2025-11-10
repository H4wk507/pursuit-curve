import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


def cyclic_pursuit_animation(solution, num_frames: int = 200) -> None:
    t_eval = np.linspace(solution.t[0], solution.t[-1], num_frames)
    y_interp = solution.sol(t_eval)

    num_points = y_interp.shape[0] // 2

    paths_x = [y_interp[i] for i in range(0, num_points * 2, 2)]
    paths_y = [y_interp[i] for i in range(1, num_points * 2, 2)]

    all_x = y_interp[::2].flatten()
    all_y = y_interp[1::2].flatten()

    fig, ax = plt.subplots(figsize=(10, 8))

    margin = 1.0
    ax.set_xlim(all_x.min() - margin, all_x.max() + margin)
    ax.set_ylim(all_y.min() - margin, all_y.max() + margin)

    lines_history = []
    lines_current = []

    colors = plt.cm.jet(np.linspace(0, 1, num_points))  # type: ignore

    for i in range(num_points):
        color = colors[i]

        (line_hist,) = ax.plot([], [], "-", color=color, linewidth=2, alpha=0.6)
        lines_history.append(line_hist)

        (line_curr,) = ax.plot([], [], "o", color=color, markersize=10, alpha=0.8)
        lines_current.append(line_curr)

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
    ax.set_title("Symulacja Pościgu (Wszystkie Punkty)", fontsize=14)
    ax.set_aspect("equal")

    def init() -> tuple:
        for line in lines_history:
            line.set_data([], [])
        for line in lines_current:
            line.set_data([], [])
        time_text.set_text("")

        return (*lines_history, *lines_current, time_text)

    def animate_frame(frame: int) -> tuple:
        for i in range(num_points):
            x_path = paths_x[i]
            y_path = paths_y[i]

            lines_history[i].set_data(x_path[: frame + 1], y_path[: frame + 1])

            lines_current[i].set_data([x_path[frame]], [y_path[frame]])

        time_text.set_text(f"Time: {t_eval[frame]:.2f}s")

        return (*lines_history, *lines_current, time_text)

    anim = animation.FuncAnimation(
        fig,
        animate_frame,
        init_func=init,
        frames=num_frames,
        interval=50,
        blit=True,
        repeat=True,
    )

    file = "animation.mp4"
    anim.save(file, writer="ffmpeg", fps=30)
    print(f"Animacja zapisana pomyślnie jako '{file}'.")

    plt.close(fig)
