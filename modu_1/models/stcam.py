# models/stcam.py
import torch
import torch.nn as nn
class STcAM(nn.Module):
    def __init__(self, window_size=16):
        super().__init__()

        # Spatial feature extractor
        self.conv1 = nn.Conv1d(
            in_channels=1,
            out_channels=8,
            kernel_size=3,
            padding=1
        )

        # Temporal feature extractor
        self.lstm = nn.LSTM(
            input_size=8,
            hidden_size=16,
            batch_first=True,
            bidirectional=True
        )

        # Attention
        self.attention = nn.Linear(32, 1)

        # Prediction head
        self.fc = nn.Linear(32, 1)

    def forward(self, x):
        # x: (batch, window)
        x = x.unsqueeze(1)               # (batch, 1, window)
        x = self.conv1(x)                # (batch, 8, window)
        x = x.permute(0, 2, 1)           # (batch, window, 8)

        lstm_out, _ = self.lstm(x)       # (batch, window, 32)

        # Attention
        weights = torch.softmax(
            self.attention(lstm_out).squeeze(-1),
            dim=1
        )
        context = torch.sum(
            lstm_out * weights.unsqueeze(-1),
            dim=1
        )

        return self.fc(context)
