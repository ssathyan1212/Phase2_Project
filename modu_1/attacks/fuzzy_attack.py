# attacks/fuzzy_attack.py

import random

def fuzzy_attack(can_frames):
    attacked_frames = []

    for frame in can_frames:
        fake = frame.copy()
        fake["can_id"] = random.randint(0x000, 0x7FF)
        fake["value"] = random.uniform(-1.0, 1.0)
        attacked_frames.append(fake)

    return attacked_frames
