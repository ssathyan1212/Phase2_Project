# models/anomaly_detector.py
import numpy as np
class AnomalyDetector:
    def __init__(self, k=3):
        self.k = k
        self.threshold = None
    def fit(self, errors):
        mean = np.mean(errors)
        std = np.std(errors)
        self.threshold = mean + self.k * std
    def predict(self, error):
        return error > self.threshold 