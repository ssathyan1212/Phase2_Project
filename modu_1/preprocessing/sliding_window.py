# preprocessing/sliding_window.py
def create_sliding_windows(series, window_size=16):
    X, y = [], []
    for i in range(len(series) - window_size):
        X.append(series[i:i + window_size])
        y.append(series[i + window_size])
    return X, y
