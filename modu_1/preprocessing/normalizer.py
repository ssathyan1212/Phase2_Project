# preprocessing/normalizer.py
def min_max_normalize(series):
    min_v = min(series)
    max_v = max(series)
    if max_v - min_v == 0:
        return [0.0] * len(series)
    return [(v - min_v) / (max_v - min_v) for v in series]