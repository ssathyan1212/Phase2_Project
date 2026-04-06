# attacks/replay_attack.py

REPLAY_BUFFER = []

def replay_attack(can_frames, buffer_size=50):
    global REPLAY_BUFFER

    REPLAY_BUFFER.extend(can_frames)
    REPLAY_BUFFER = REPLAY_BUFFER[-buffer_size:]

    if len(REPLAY_BUFFER) > 10:
        return REPLAY_BUFFER[:len(can_frames)]

    return can_frames
