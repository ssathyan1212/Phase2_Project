import numpy as np
import torch
from models.mkf_ads import train_mkf_ads

# Load preprocessed data
dataset = np.load("data/processed/windowed_data.npy", allow_pickle=True)

print("[INFO] Training MKF-ADS model...")
model = train_mkf_ads(dataset, epochs=20)

# Save trained student model
torch.save(model.student.state_dict(), "models/mkf_ads_student.pth")
print("[SUCCESS] Model trained and saved")
