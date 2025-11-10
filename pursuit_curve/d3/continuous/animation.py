import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.text import Text


def animate_continuous_pursuit_3d(solution, num_frames: int = 200) -> None:
    """Animacja 3D dla symulacji ciągłej pościgu."""
    t_eval = np.linspace(solution.t[0], solution.t[-1], num_frames)
    y_interp = solution.sol(t_eval)

    pursuer_x = y_interp[0]
    pursuer_y = y_interp[1]
    pursuer_z = y_interp[2]
    target_x = y_interp[3]
    target_y = y_interp[4]
    target_z = y_interp[5]

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection="3d")

    # Zakres osi
    all_x = np.concatenate([pursuer_x, target_x])
    all_y = np.concatenate([pursuer_y, target_y])
    all_z = np.concatenate([pursuer_z, target_z])
    margin = 1.0

    ax.set_xlim(all_x.min() - margin, all_x.max() + margin)
    ax.set_ylim(all_y.min() - margin, all_y.max() + margin)
    ax.set_zlim(all_z.min() - margin, all_z.max() + margin)

    # Linie trajektorii
    (line_target,) = ax.plot([], [], [], "r-", label="Target (Cel)", linewidth=2, alpha=0.6)
    (line_pursuer,) = ax.plot([], [], [], "b-", label="Pursuer (Ścigający)", linewidth=2, alpha=0.6)

    # Aktualna pozycja
    (current_target,) = ax.plot([], [], [], "ro", markersize=10, alpha=0.8)
    (current_pursuer,) = ax.plot([], [], [], "bo", markersize=10, alpha=0.8)

    # Start i koniec
    ax.plot(
        [target_x[0]],
        [target_y[0]],
        [target_z[0]],
        "r^",
        markersize=12,
        label="Start T",
    )
    ax.plot(
        [pursuer_x[0]],
        [pursuer_y[0]],
        [pursuer_z[0]],
        "b^",
        markersize=12,
        label="Start P",
    )
    ax.plot(
        [target_x[-1]],
        [target_y[-1]],
        [target_z[-1]],
        "rx",
        markersize=12,
        label="End T",
    )
    ax.plot(
        [pursuer_x[-1]],
        [pursuer_y[-1]],
        [pursuer_z[-1]],
        "bx",
        markersize=12,
        label="End P",
    )

    # Tekst czasu
    time_text = ax.text2D(
        0.02,
        0.98,
        "",
        transform=ax.transAxes,
        verticalalignment="top",
        fontsize=12,
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    )

    ax.legend(loc="upper right")
    ax.set_xlabel("X", fontsize=12)
    ax.set_ylabel("Y", fontsize=12)
    ax.set_zlabel("Z", fontsize=12)
    ax.set_title("3D Continuous Pursuit Simulation", fontsize=14)

    def init() -> tuple[Line2D, Line2D, Line2D, Line2D, Text]:
        line_target.set_data([], [])
        line_target.set_3d_properties([])  # type: ignore [attr-defined]

        line_pursuer.set_data([], [])
        line_pursuer.set_3d_properties([])  # type: ignore [attr-defined]

        current_target.set_data([], [])
        current_target.set_3d_properties([])  # type: ignore [attr-defined]

        current_pursuer.set_data([], [])
        current_pursuer.set_3d_properties([])  # type: ignore [attr-defined]

        time_text.set_text("")
        return line_target, line_pursuer, current_target, current_pursuer, time_text

    def animate_frame(frame: int) -> tuple[Line2D, Line2D, Line2D, Line2D, Text]:
        # Trajektorie
        line_target.set_data(target_x[: frame + 1], target_y[: frame + 1])
        line_target.set_3d_properties(target_z[: frame + 1])  # type: ignore [attr-defined]

        line_pursuer.set_data(pursuer_x[: frame + 1], pursuer_y[: frame + 1])
        line_pursuer.set_3d_properties(pursuer_z[: frame + 1])  # type: ignore [attr-defined]

        # Aktualna pozycja
        current_target.set_data([target_x[frame]], [target_y[frame]])
        current_target.set_3d_properties([target_z[frame]])  # type: ignore [attr-defined]

        current_pursuer.set_data([pursuer_x[frame]], [pursuer_y[frame]])
        current_pursuer.set_3d_properties([pursuer_z[frame]])  # type: ignore [attr-defined]

        # Czas
        time_text.set_text(f"Time: {t_eval[frame]:.2f}s")

        # Obróć kamerę dla lepszego efektu
        ax.view_init(elev=20, azim=frame * 0.3)

        return line_target, line_pursuer, current_target, current_pursuer, time_text

    anim = animation.FuncAnimation(
        fig,
        animate_frame,
        init_func=init,
        frames=num_frames,
        interval=50,
        blit=False,  # blit musi być False dla 3D
        repeat=True,
    )

    filename = "animation_3d.mp4"
    anim.save(filename, writer="ffmpeg", fps=30)
    plt.close(fig)
    print(f"Animacja 3D zapisana do: {filename}")
