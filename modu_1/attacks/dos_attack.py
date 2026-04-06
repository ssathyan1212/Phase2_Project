# attacks/dos_attack.py

def dos_attack(can_frames, intensity=5):
    attacked_frames = []

    for frame in can_frames:
        for _ in range(intensity):
            fake = frame.copy()
            fake["can_id"] = 0x001  # very high priority
            attacked_frames.append(fake)

    return attacked_frames
