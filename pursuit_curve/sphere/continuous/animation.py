import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from pursuit_curve.sphere.utils import spherical_to_cartesian


def animate_sphere_pursuit_3d(solution, num_frames: int = 200) -> None:
    t_eval = np.linspace(solution.t[0], solution.t[-1], num_frames)
    y_interp = solution.sol(t_eval)

    p_r, p_theta, p_phi = y_interp[0:3]
    t_r, t_theta, t_phi = y_interp[3:6]

    p_x, p_y, p_z = spherical_to_cartesian(p_r, p_theta, p_phi)
    t_x, t_y, t_z = spherical_to_cartesian(t_r, t_theta, t_phi)

    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection="3d")

    radius = t_r[0]  # Zakładamy, że cel jest na stałym promieniu
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    sphere_x = radius * np.outer(np.sin(v), np.cos(u))
    sphere_y = radius * np.outer(np.sin(v), np.sin(u))
    sphere_z = radius * np.outer(np.cos(v), np.ones(np.size(u)))

    ax.plot_surface(sphere_x, sphere_y, sphere_z, alpha=0.1, color="lightblue", linewidth=0, antialiased=True)

    all_coords = np.concatenate([p_x, p_y, p_z, t_x, t_y, t_z])
    margin = 2.0
    limit = max(abs(all_coords.max()), abs(all_coords.min())) + margin
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_zlim(-limit, limit)

    (line_target,) = ax.plot([], [], [], "r-", label="Cel", linewidth=2.5, alpha=0.7)
    (line_pursuer,) = ax.plot([], [], [], "b-", label="Ścigający", linewidth=2.5, alpha=0.7)
    (current_target,) = ax.plot([], [], [], "ro", markersize=12, alpha=0.9)
    (current_pursuer,) = ax.plot([], [], [], "bo", markersize=12, alpha=0.9)

    # Punkty startowe i końcowe
    ax.plot(
        [t_x[0]],
        [t_y[0]],
        [t_z[0]],
        "r^",
        markersize=15,
        label="Start T",
        markeredgecolor="darkred",
        markeredgewidth=2,
    )
    ax.plot(
        [p_x[0]],
        [p_y[0]],
        [p_z[0]],
        "b^",
        markersize=15,
        label="Start P",
        markeredgecolor="darkblue",
        markeredgewidth=2,
    )
    ax.plot([t_x[-1]], [t_y[-1]], [t_z[-1]], "rx", markersize=15, label="End T", markeredgewidth=3)
    ax.plot([p_x[-1]], [p_y[-1]], [p_z[-1]], "bx", markersize=15, label="End P", markeredgewidth=3)

    time_text = ax.text2D(
        0.02,
        0.98,
        "",
        transform=ax.transAxes,
        verticalalignment="top",
        fontsize=12,
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.7),
    )

    ax.set_xlabel("X", fontsize=12, labelpad=10)
    ax.set_ylabel("Y", fontsize=12, labelpad=10)
    ax.set_zlabel("Z", fontsize=12, labelpad=10)
    ax.set_title("Pościg na Sferze", fontsize=14, fontweight="bold", pad=20)
    ax.legend(loc="upper right", fontsize=10)

    ax.set_box_aspect([1, 1, 1])

    def init():
        """Inicjalizacja animacji"""
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
        ax.view_init(elev=20, azim=frame * 360 / num_frames)

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

    file = "sphere_pursuit.mp4"
    anim.save(file, writer="ffmpeg", fps=30)
    plt.close(fig)
    print(f"Animacja zapisana do: {file}")
