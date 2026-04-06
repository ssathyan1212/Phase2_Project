# attacks/masquerade_attack.py

def masquerade_attack(can_frames, target_signal="speed"):
    attacked_frames = []

    for frame in can_frames:
        if frame["signal"] == target_signal:
            fake = frame.copy()
            fake["value"] = frame["value"] * 0.2
            attacked_frames.append(fake)
        else:
            attacked_frames.append(frame)

    return attacked_frames
