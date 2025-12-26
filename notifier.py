import subprocess
import time

# ---------------- CONFIG ----------------
MEMORY_THRESHOLD_MB = 7000          # Notify if RAM >= 2000 MB

# Cooldown logic (DISABLED FOR NOW)
COOLDOWN_SECONDS = 300
LAST_ALERT_FILE = "/tmp/wallpaper_mem_alert.time"
# ---------------------------------------


# def can_notify():
#     try:
#         with open(LAST_ALERT_FILE, "r") as f:
#             last_time = float(f.read().strip())
#             return time.time() - last_time >= COOLDOWN_SECONDS
#     except FileNotFoundError:
#         return True


def update_last_alert_time():
    with open(LAST_ALERT_FILE, "w") as f:
        f.write(str(time.time()))


def send_notification(lines):
    message = "\n\n".join(f"• {line}" for line in lines)

    subprocess.run([
        "notify-send",
        "-i", "utilities-system-monitor",
        "-u", "critical",
        "⚠ High Memory Usage",
        message
    ])



def check_high_memory(data):
    offenders = [
        f"{name} (PID {pid}) – {int(mem)} MB"
        for name, pid, mem, cpu in data
        if mem >= MEMORY_THRESHOLD_MB
    ]

    if not offenders:
        return

    send_notification(offenders)
    update_last_alert_time()
