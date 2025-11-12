import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def animate_torus_pursuit_3d(solution, R: float, r: float, num_frames: int = 200) -> None:
    t_eval = np.linspace(solution.t[0], solution.t[-1], num_frames)
    y_interp = solution.sol(t_eval)

    p_u, p_v = y_interp[0:2]
    t_u, t_v = y_interp[2:4]

    def torus_to_cartesian(u: np.ndarray, v: np.ndarray) -> np.ndarray:
        x = (R + r * np.cos(v)) * np.cos(u)
        y = (R + r * np.cos(v)) * np.sin(u)
        z = r * np.sin(v)
        return np.array([x, y, z])

    p_x, p_y, p_z = torus_to_cartesian(p_u, p_v)
    t_x, t_y, t_z = torus_to_cartesian(t_u, t_v)

    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(111, projection="3d")

    u_surf = np.linspace(0, 2 * np.pi, 100)
    v_surf = np.linspace(0, 2 * np.pi, 100)
    U, V = np.meshgrid(u_surf, v_surf)

    X, Y, Z = torus_to_cartesian(U, V)

    colors = np.sin(V)

    ax.plot_surface(
        X,
        Y,
        Z,
        facecolors=plt.cm.viridis(colors),  # type: ignore
        alpha=0.3,
        rstride=2,
        cstride=2,
        linewidth=0,
        antialiased=True,
        shade=True,
    )

    limit = R + r + 1
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_zlim(-limit, limit)

    (line_target,) = ax.plot([], [], [], "r-", label="Cel", linewidth=3, alpha=0.8)
    (line_pursuer,) = ax.plot([], [], [], "b-", label="Ścigający", linewidth=3, alpha=0.8)
    (current_target,) = ax.plot(
        [], [], [], "ro", markersize=15, alpha=1.0, markeredgecolor="darkred", markeredgewidth=2
    )
    (current_pursuer,) = ax.plot(
        [], [], [], "bo", markersize=15, alpha=1.0, markeredgecolor="darkblue", markeredgewidth=2
    )

    ax.plot(
        [t_x[0]],
        [t_y[0]],
        [t_z[0]],
        "r^",
        markersize=15,
        markeredgecolor="darkred",
        markeredgewidth=2,
        label="Start T",
    )
    ax.plot(
        [p_x[0]],
        [p_y[0]],
        [p_z[0]],
        "b^",
        markersize=15,
        markeredgecolor="darkblue",
        markeredgewidth=2,
        label="Start P",
    )

    ax.plot([t_x[-1]], [t_y[-1]], [t_z[-1]], "rx", markersize=18, markeredgewidth=4, label="Koniec T")
    ax.plot([p_x[-1]], [p_y[-1]], [p_z[-1]], "bx", markersize=18, markeredgewidth=4, label="Koniec P")

    time_text = ax.text2D(
        0.02,
        0.98,
        "",
        transform=ax.transAxes,
        verticalalignment="top",
        fontsize=14,
        fontweight="bold",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )

    ax.set_xlabel("X", fontsize=12, labelpad=10)
    ax.set_ylabel("Y", fontsize=12, labelpad=10)
    ax.set_zlabel("Z", fontsize=12, labelpad=10)
    ax.set_title(f"Pościg na torusie (R={R}, r={r})", fontsize=16, fontweight="bold", pad=20)
    ax.legend(loc="upper right", fontsize=11, framealpha=0.9)

    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    ax.set_box_aspect([1, 1, 1])

    def init():
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

    def animate_frame(frame):
        line_target.set_data(t_x[: frame + 1], t_y[: frame + 1])
        line_target.set_3d_properties(t_z[: frame + 1])  # type: ignore [attr-defined]

        line_pursuer.set_data(p_x[: frame + 1], p_y[: frame + 1])
        line_pursuer.set_3d_properties(p_z[: frame + 1])  # type: ignore [attr-defined]

        current_target.set_data([t_x[frame]], [t_y[frame]])
        current_target.set_3d_properties([t_z[frame]])  # type: ignore [attr-defined]

        current_pursuer.set_data([p_x[frame]], [p_y[frame]])
        current_pursuer.set_3d_properties([p_z[frame]])  # type: ignore [attr-defined]

        distance = np.sqrt(
            (p_x[frame] - t_x[frame]) ** 2 + (p_y[frame] - t_y[frame]) ** 2 + (p_z[frame] - t_z[frame]) ** 2
        )

        time_text.set_text(f"Czas: {t_eval[frame]:.2f}s\nOdległość: {distance:.2f}")

        # Obrót kamery
        ax.view_init(elev=20, azim=30 + frame * 360 / num_frames)

        return line_target, line_pursuer, current_target, current_pursuer, time_text

    anim = FuncAnimation(
        fig,
        animate_frame,
        init_func=init,
        frames=num_frames,
        interval=50,
        blit=False,
        repeat=True,
    )

    file = "torus_pursuit.mp4"
    anim.save(file, writer="ffmpeg", fps=30)
    plt.close(fig)
    print(f"Animacja zapisana do: {file}")
