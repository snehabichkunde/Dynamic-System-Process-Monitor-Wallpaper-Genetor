#!/usr/bin/env python3

import matplotlib.pyplot as plt
import subprocess
from datetime import datetime
from notifier import check_high_memory

from monitor import collect_usage
from background import draw_neural_background

# ---------------- CONFIG ----------------
WIDTH = 1366
HEIGHT = 768
OUTPUT_IMAGE = "/home/sarvaha/wallpaperProject/wallpaper.png"

MIN_MEM_MB = 50
LIMIT = 6

NAME_COL_UNITS = 32
BAR_MAX_UNITS = 100
STATS_PADDING = 6
# ----------------------------------------


def truncate_to_fit(ax, text, max_x, y, fontsize):
    renderer = ax.figure.canvas.get_renderer()
    max_px = ax.transData.transform((max_x, y))[0]

    while True:
        temp = ax.text(0, y, text, fontsize=fontsize, family="monospace")
        bbox = temp.get_window_extent(renderer=renderer)
        temp.remove()

        if bbox.x1 <= max_px or len(text) <= 1:
            break

        text = text[:-2] + "…"

    return text


def generate_wallpaper(data):
    apps = [d[0] for d in data]
    pids = [d[1] for d in data]
    mems = [d[2] for d in data]
    cpus = [d[3] for d in data]

    max_mem = max(mems)
    mem_norm = [(m / max_mem) * BAR_MAX_UNITS for m in mems]

    plt.style.use("dark_background")
    fig = plt.figure(figsize=(WIDTH / 100, HEIGHT / 100))

    # ---- Background ----
    bg_ax = fig.add_axes([0, 0, 1, 1])
    bg_ax.set_facecolor("#0b0e14")
    bg_ax.axis("off")

    draw_neural_background(
        bg_ax,
        NAME_COL_UNITS + BAR_MAX_UNITS + 60,
        len(data) + 6
    )

    # ---- Center Panel ----
    panel_width = 0.6
    panel_height = 0.55
    panel_x = (1 - panel_width) / 2
    panel_y = (1 - panel_height) / 2

    # ---- Title Bar ----
    title_height = 0.12
    title_ax = fig.add_axes([
        panel_x,
        panel_y + panel_height - title_height,
        panel_width,
        title_height
    ])
    title_ax.set_facecolor("#020617")
    title_ax.axis("off")

    title_ax.text(
        0.02, 0.5,
        "SYSTEM PROCESS MONITOR",
        va="center",
        ha="left",
        fontsize=15,
        color="#22d3ee",
        family="monospace",
        weight="bold"
    )

    title_ax.text(
        0.98, 0.5,
        datetime.now().strftime("%H:%M:%S"),
        va="center",
        ha="right",
        fontsize=13,
        color="#94a3b8",
        family="monospace"
    )

    # ---- Data Panel ----
    panel_ax = fig.add_axes([
        panel_x,
        panel_y,
        panel_width,
        panel_height - title_height
    ])
    panel_ax.set_facecolor("#111827")
    panel_ax.axis("off")

    y_positions = list(range(len(apps)))[::-1]
    bar_start_x = NAME_COL_UNITS

    colors = []
    for cpu in cpus:
        intensity = min(cpu / 100, 1.0)
        colors.append((0.1, 0.75 + intensity * 0.25, 0.9))

    panel_ax.barh(
        y_positions,
        mem_norm,
        left=bar_start_x,
        height=0.55,
        color=colors,
        alpha=0.9
    )

    panel_ax.axvline(bar_start_x, color="#1f2933", linewidth=1)

    for i, app in enumerate(apps):
        label = f"[{pids[i]}] {app}"

        safe_label = truncate_to_fit(
            panel_ax,
            label,
            bar_start_x - 1.5,
            y_positions[i],
            fontsize=14
        )

        panel_ax.text(
            bar_start_x - 1.5,
            y_positions[i],
            safe_label,
            va="center",
            ha="right",
            fontsize=14,
            color="#e5e7eb",
            family="monospace",
            weight="bold"
        )

        panel_ax.text(
            bar_start_x + mem_norm[i] + STATS_PADDING,
            y_positions[i],
            f"{int(mems[i])} MB | {int(cpus[i])}%",
            va="center",
            ha="left",
            fontsize=12,
            color="#9ca3af",
            family="monospace"
        )

    panel_ax.set_xlim(
        0,
        NAME_COL_UNITS + BAR_MAX_UNITS + STATS_PADDING + 20
    )
    panel_ax.set_ylim(-1, len(apps))

    plt.savefig(OUTPUT_IMAGE, dpi=100, facecolor="#0b0e14")
    plt.close()

def set_wallpaper():
    subprocess.run([
        "gsettings", "set",
        "org.gnome.desktop.background",
        "picture-uri",
        f"file://{OUTPUT_IMAGE}"
    ])


if __name__ == "__main__":
    data = collect_usage(limit=LIMIT, min_mb=MIN_MEM_MB)
    if data:
        generate_wallpaper(data)
        set_wallpaper()
    check_high_memory(data)
