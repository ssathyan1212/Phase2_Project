# scripts/preprocess.py
import csv
import os
import numpy as np
from preprocessing.read_algorithm import read_extract
from preprocessing.normalizer import min_max_normalize
from preprocessing.sliding_window import create_sliding_windows
RAW_FILE = "data/raw/can_log.csv"
OUT_DIR = "data/processed"
OUT_FILE = "data/processed/windowed_data.npy"
def load_csv(path):
    rows = []
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows
def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    print("[INFO] Loading CAN CSV...")
    rows = load_csv(RAW_FILE)

    print("[INFO] Extracting signals...")
    signals = read_extract(rows)

    dataset = []

    print("[INFO] Creating windows...")
    for key, series in signals.items():
        if len(series) < 20:
            continue  # skip very short signals

        norm = min_max_normalize(series)
        X, y = create_sliding_windows(norm, window_size=16)

        if len(X) == 0:
            continue

        dataset.append({
            "key": key,
            "X": X,
            "y": y
        })

    np.save(OUT_FILE, dataset)
    print(f"[SUCCESS] Preprocessing completed → {OUT_FILE}")


if __name__ == "__main__":
    main()
