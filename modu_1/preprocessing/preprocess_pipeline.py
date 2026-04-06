# preprocessing/preprocess_pipeline.py
import csv
from preprocessing.read_algorithm import read_extract
from preprocessing.sliding_window import create_sliding_windows
from preprocessing.normalizer import min_max_normalize
def load_can_csv(path="data/raw/can_log.csv"):
    rows = []
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows
def preprocess(window_size=16):
    rows = load_can_csv()
    extracted = read_extract(rows)
    dataset = []
    for (can_id, signal), values in extracted.items():
        if len(values) < window_size + 1:
            continue
        normalized = min_max_normalize(values)
        X, y = create_sliding_windows(normalized, window_size)
        dataset.append({
            "can_id": can_id,
            "signal": signal,
            "X": X,
            "y": y
        })
    return dataset
