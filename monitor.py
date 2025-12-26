# monitor.py
import psutil


def collect_usage(limit=6, min_mb=50):
    usage = {}

    for proc in psutil.process_iter(['name', 'memory_info']):
        try:
            name = proc.info['name'] or "unknown"
            mem = proc.info['memory_info'].rss / (1024 * 1024)
            cpu = proc.cpu_percent(interval=0.1)

            if name not in usage:
                usage[name] = {"mem": 0, "cpu": 0}

            usage[name]["mem"] += mem
            usage[name]["cpu"] += cpu

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    top = sorted(
        usage.items(),
        key=lambda x: x[1]["mem"],
        reverse=True
    )

    return [
        (name, data["mem"], data["cpu"])
        for name, data in top
        if data["mem"] >= min_mb
    ][:limit]

