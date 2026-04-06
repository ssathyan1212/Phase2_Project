# models/mkf_ads.py

import torch
import torch.nn as nn
from models.stcam import STcAM
from models.patch_st import PatchST
from models.distillation import distillation_loss

class MKF_ADS(nn.Module):
    def __init__(self, window_size=16):
        super().__init__()
        self.student = STcAM(window_size)
        self.teacher = PatchST(window_size)

    def forward(self, x):
        student_out = self.student(x)
        with torch.no_grad():
            teacher_out = self.teacher(x)
        return student_out, teacher_out

def train_mkf_ads(dataset, epochs=20):
    model = MKF_ADS()
    optimizer = torch.optim.Adam(model.student.parameters(), lr=0.001)
    mse = nn.MSELoss()

    for epoch in range(epochs):
        total_loss = 0

        for d in dataset:
            X = torch.tensor(d["X"], dtype=torch.float32)
            y = torch.tensor(d["y"], dtype=torch.float32).unsqueeze(1)

            pred_s, pred_t = model(X)

            loss = mse(pred_s, y) + distillation_loss(pred_s, pred_t)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"[Epoch {epoch+1}] Loss: {total_loss:.4f}")

    return model
