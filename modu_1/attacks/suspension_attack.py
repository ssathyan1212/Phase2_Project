# attacks/suspension_attack.py

def suspension_attack(can_frames, drop_rate=0.5):
    kept = []

    for frame in can_frames:
        if hash(frame["signal"]) % 10 > drop_rate * 10:
            kept.append(frame)

    return kept
