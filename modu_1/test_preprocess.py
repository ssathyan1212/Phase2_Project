import os
import pandas as pd
import numpy as np

RAW_PATH = "data/raw/can_log.csv"
PROCESSED_DIR = "data/processed"

WINDOW_SIZE = 16   # sliding window length
STEP_SIZE = 4      # overlap

def load_raw_data():
    if not os.path.exists(RAW_PATH):
        raise FileNotFoundError("Raw CAN log not found")

    df = pd.read_csv(RAW_PATH)
    return df

def pivot_can_data(df):
    """
    Convert CAN rows into time-aligned feature vectors:
    [speed, steering, throttle, brake]
    """
    pivot = df.pivot_table(
        index="timestamp",
        columns="signal",
        values="value"
    ).fillna(0.0)

    return pivot[["speed", "steering", "throttle", "brake"]]

def sliding_window(data, window, step):
    X = []
    for i in range(0, len(data) - window, step):
        X.append(data[i:i + window])
    return np.array(X)

def main():
    print("[INFO] Loading raw CAN data")
    df = load_raw_data()

    print("[INFO] Converting CAN rows to feature vectors")
    features = pivot_can_data(df)

    print("[INFO] Applying sliding window")
    X = sliding_window(features.values, WINDOW_SIZE, STEP_SIZE)

    os.makedirs(PROCESSED_DIR, exist_ok=True)

    np.save(os.path.join(PROCESSED_DIR, "X.npy"), X)

    print(f"[INFO] Preprocessing completed")
    print(f"[INFO] Shape of X: {X.shape}")
    print(f"[INFO] Saved to {PROCESSED_DIR}/X.npy")

if __name__ == "__main__":
    main()
