import psutil
import matplotlib.pyplot as plt
import random
import math
import json
import os
import subprocess

# ---------------- CONFIG ----------------
WIDTH = 1366
HEIGHT = 768
OUTPUT_IMAGE = "/home/sarvaha/wallpaperProject/wallpaper.png"
POSITION_FILE = "/home/sarvaha/wallpaperProject/positions.json"
# ----------------------------------------


def collect_usage(limit=6, min_mb=50):
    usage = {}

    for proc in psutil.process_iter(['name', 'memory_info']):
        try:
            name = proc.info['name']
            mem = proc.info['memory_info'].rss / (1024 * 1024)
            cpu = proc.cpu_percent(interval=0.1)

            if name not in usage:
                usage[name] = {"mem": 0, "cpu": 0}

            usage[name]["mem"] += mem
            usage[name]["cpu"] += cpu

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    top = sorted(usage.items(), key=lambda x: x[1]["mem"], reverse=True)
    return [(n, d["mem"], d["cpu"]) for n, d in top if d["mem"] >= min_mb][:limit]


def overlaps(x, y, r, others):
    for ox, oy, orad in others:
        if math.hypot(x - ox, y - oy) < r + orad:
            return True
    return False


def load_positions():
    try:
        with open(POSITION_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_positions(pos):
    with open(POSITION_FILE, "w") as f:
        json.dump(pos, f)


def generate_wallpaper(data):
    apps = [d[0] for d in data]
    mems = [d[1] for d in data]
    cpus = [d[2] for d in data]

    max_mem = max(mems)
    sizes = [(m / max_mem) * 6000 + 800 for m in mems]
    radii = [math.sqrt(s / math.pi) for s in sizes]

    colors = []
    for cpu in cpus:
        if cpu > 50:
            colors.append("red")
        elif cpu > 20:
            colors.append("orange")
        else:
            colors.append("green")

    old_positions = load_positions()
    new_positions = {}
    placed = []
    x_vals, y_vals = [], []

    for app, radius in zip(apps, radii):
        if app in old_positions:
            x, y = old_positions[app]
        else:
            for _ in range(200):
                x = random.uniform(radius, 10 - radius)
                y = random.uniform(radius, 6 - radius)
                if not overlaps(x, y, radius, placed):
                    break

        placed.append((x, y, radius))
        x_vals.append(x)
        y_vals.append(y)
        new_positions[app] = [x, y]

    save_positions(new_positions)

    plt.style.use("dark_background")
    plt.figure(figsize=(WIDTH / 100, HEIGHT / 100))
    plt.axis("off")

    plt.scatter(x_vals, y_vals, s=sizes, c=colors, alpha=0.8)

    for i, app in enumerate(apps):
        plt.text(
            x_vals[i],
            y_vals[i],
            f"{app}\n{int(mems[i])} MB\n{int(cpus[i])}%",
            ha="center",
            va="center",
            fontsize=14,
            color="white",
            weight="bold"
        )

    plt.tight_layout()
    plt.savefig(OUTPUT_IMAGE, dpi=100, facecolor="black")
    plt.close()


def set_wallpaper():
    subprocess.run([
        "gsettings", "set",
        "org.gnome.desktop.background",
        "picture-uri",
        f"file://{OUTPUT_IMAGE}"
    ])


if __name__ == "__main__":
    data = collect_usage()
    if data:
        generate_wallpaper(data)
        set_wallpaper()
