import numpy as np
from numpy.typing import NDArray


def spherical_to_cartesian(r: float, theta: float, phi: float) -> NDArray[np.float32]:
    x = r * np.cos(theta) * np.cos(phi)
    y = r * np.cos(theta) * np.sin(phi)
    z = r * np.sin(theta)
    return np.array([x, y, z], dtype=np.float32)
