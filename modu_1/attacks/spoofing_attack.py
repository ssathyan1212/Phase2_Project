# attacks/spoofing_attack.py

def spoofing_attack(can_frames, target_signal="steering"):
    attacked_frames = []

    for frame in can_frames:
        fake = frame.copy()
        if frame["signal"] == target_signal:
            fake["value"] = 0.9  # extreme steering
        attacked_frames.append(fake)

    return attacked_frames
