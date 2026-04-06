# can_bus/can_signal_generator.py
import time
from can_bus.can_mapper import map_to_can
def generate_can_messages(vehicle_state):
    timestamp = time.time()
    can_frames = map_to_can(vehicle_state)

    for frame in can_frames:
        frame["timestamp"] = timestamp

    return can_frames
