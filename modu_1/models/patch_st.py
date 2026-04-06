# models/patchst.py

import torch
import torch.nn as nn

class PatchST(nn.Module):
    def __init__(self, window_size=16, patch_size=4):
        super().__init__()

        self.patch_size = patch_size
        self.embed = nn.Linear(patch_size, 16)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=16,
            nhead=2,
            batch_first=True
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=1)

        self.fc = nn.Linear(16, 1)

    def forward(self, x):
        # x: (batch, window)
        patches = []

        for i in range(0, x.shape[1] - self.patch_size + 1, self.patch_size):
            patches.append(x[:, i:i+self.patch_size])

        patches = torch.stack(patches, dim=1)  # (batch, num_patches, patch)
        emb = self.embed(patches)               # (batch, num_patches, 16)

        encoded = self.encoder(emb)
        pooled = encoded.mean(dim=1)

        return self.fc(pooled)
