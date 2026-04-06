# can_bus/can_logger.py

import csv
import os

LOG_FILE = "data/raw/can_log.csv"

def init_logger():
    os.makedirs("data/raw", exist_ok=True)

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "can_id", "signal", "value", "label"])
def log_can_frames(can_frames, mode):
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        for frame in can_frames:
            writer.writerow([
                frame["timestamp"],
                hex(frame["can_id"]),
                frame["signal"],
                frame["value"],
                mode          # ✅ attack label / mode
            ])
