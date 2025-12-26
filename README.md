# 🖥️ System Process Monitor Wallpaper

A Linux desktop wallpaper system monitor that visualizes CPU and memory usage of running processes directly on your wallpaper. It features a modern neural-network–style background and provides real-time alerts for high memory usage.

This project automatically collects system statistics, renders them as clean horizontal bars on a generative background, sets the image as your GNOME wallpaper, and notifies you if RAM usage spikes—all without user intervention.

---

## ✨ Features

* **📊 Live Process Monitoring:** Displays top processes ranked by memory usage, including PID, Memory (MB), and CPU (%).
* **🎨 Dynamic Wallpaper:** Generates a dark, minimal UI with a neural-network-style animated background.
* **🔔 High Memory Alerts:** Sends desktop notifications when specific processes exceed your configured RAM limit.
* **⏱️ Fully Automated:** Designed to run via `cron` to update your wallpaper every minute silently.
* **Smart Truncation:** Automatically shortens long process names to keep the visual clean.

---

## 🛠️ Tech Stack

* **Python 3**
* **[matplotlib](https://matplotlib.org/):** Rendering the wallpaper and graphs.
* **[psutil](https://github.com/giampaolo/psutil):** Collecting CPU & memory statistics.
* **GNOME gsettings:** Setting the desktop background (Linux/GNOME).
* **notify-send:** Sending desktop notifications.
* **cron:** Scheduling and automation.

---

## 📂 Project Structure

```text
wallpaperProject/
├── main.py              # Entry point (wallpaper generation + automation)
├── monitor.py           # Collects CPU & memory usage of processes
├── background.py        # Draws neural-network style background
├── notifier.py          # High memory notification logic
├── wallpaper.png        # Generated wallpaper image
├── requirements.txt     # Python dependencies
└── cron.log             # Cron execution logs

```

---

## ⚙️ Configuration

You can customize the behavior by editing constants in `main.py` and `notifier.py`.

### Wallpaper Settings

```python
WIDTH = 1366
HEIGHT = 768
OUTPUT_IMAGE = "/home/youruser/wallpaperProject/wallpaper.png"

```

*> **Note:** Ensure `OUTPUT_IMAGE` is an absolute path.*

### Process Filtering

```python
MIN_MEM_MB = 50      # Ignore processes using less than this memory
LIMIT = 6            # Number of processes to display

```

### Notification Threshold

```python
MEMORY_THRESHOLD_MB = 7000  # Trigger alert if RAM usage exceeds this

```

---

## 📦 Installation

### 1️⃣ Clone the repository

```bash
git clone [https://github.com/yourusername/system-process-wallpaper.git](https://github.com/yourusername/system-process-wallpaper.git)
cd system-process-wallpaper

```

### 2️⃣ Create a virtual environment (Recommended)

```bash
python3 -m venv wallpaper-env
source wallpaper-env/bin/activate

```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt

```

### 4️⃣ Install system tools

Ensure you have the required notification libraries installed:

```bash
sudo apt install python3-notify2 libnotify-bin

```

---

## ▶️ Usage

### Manual Run

You can test the project immediately by running:

```bash
python3 main.py

```

**This will:**

1. Generate `wallpaper.png`.
2. Set it as your current GNOME wallpaper.
3. Send a notification if memory usage is above the threshold.

---

## ⏱️ Automating with Cron

To update the wallpaper automatically (e.g., every minute), use a cron job.

**1. Open your crontab:**

```bash
crontab -e

```

**2. Add the following line:**
*Replace `/home/youruser/` with your actual home directory path.*

```bash
* * * * * /home/youruser/wallpaperProject/wallpaper-env/bin/python /home/youruser/wallpaperProject/main.py >> /home/youruser/wallpaperProject/cron.log 2>&1

```

**3. Save and Exit.**
The wallpaper will now update automatically every minute.

---

## 📝 Logs & Troubleshooting

If the wallpaper stops updating or notifications fail, check the logs:

```bash
cat cron.log

```

**Common Issues:**

* **Path Errors:** Ensure all paths in `main.py` and `crontab` are **absolute** (e.g., `/home/john/project/` instead of `./project/`).
* **Display Environment:** Cron runs without a display environment. If `gsettings` fails, you may need to export `DBUS_SESSION_BUS_ADDRESS` in your script.

---

## 🧠 How It Works

1. **`monitor.py`**: Scans the system using `psutil` to find the most resource-intensive processes.
2. **`background.py`**: Generates a procedural, neural-network-inspired graphic using `matplotlib`.
3. **`main.py`**: Combines the data and the background, saves the image, and commands GNOME to update the desktop background.
4. **`notifier.py`**: Checks if any specific process is hogging RAM and fires a system notification if necessary.

---

## 🚀 Future Improvements

* [ ] CPU usage specific alerts.
* [ ] Animated transitions between updates.
* [ ] Clickable process details (requires desktop widget integration).
* [ ] Multi-monitor support.
* [ ] Better Wayland compatibility.

---

## 📜 License

This project is open-source and free to use for learning and personal projects.
