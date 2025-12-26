# background.py
import numpy as np
import random


def draw_neural_background(
    ax,
    width_units,
    height_units,
    nodes=120,
    alpha=0.05
):
    """
    Draws a subtle neural-network–like background.
    Designed to be non-distracting.
    """

    np.random.seed()

    xs = np.random.uniform(0, width_units, nodes)
    ys = np.random.uniform(0, height_units, nodes)

    # Connections
    for i in range(nodes):
        for _ in range(random.randint(1, 3)):
            j = random.randint(0, nodes - 1)
            ax.plot(
                [xs[i], xs[j]],
                [ys[i], ys[j]],
                linewidth=0.6,
                color="#22d3ee",
                alpha=alpha
            )

    # Nodes
    ax.scatter(
        xs,
        ys,
        s=4,
        color="#22d3ee",
        alpha=alpha + 0.01
    )
