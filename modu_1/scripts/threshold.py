# scripts/threshold.py

import numpy as np
import torch
from models.stcam import STcAM

def compute_threshold(model_path, windows, actuals, k=3):
    model = STcAM(window_size=16)
    model.load_state_dict(torch.load(model_path))
    model.eval()

    errors = []

    for X, y in zip(windows, actuals):
        X_tensor = torch.tensor([X], dtype=torch.float32)
        with torch.no_grad():
            pred = model(X_tensor).item()
        errors.append(abs(pred - y))

    mean = np.mean(errors)
    std = np.std(errors)
    return mean + k * std
