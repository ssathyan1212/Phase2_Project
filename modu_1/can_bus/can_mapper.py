# can_bus/can_mapper.py

CAN_ID_MAP = {
    "speed": 0x100,
    "steering": 0x101,
    "throttle": 0x102,
    "brake": 0x103
}
def map_to_can(vehicle_state):
    can_messages = []
    for signal, value in vehicle_state.items():
        if signal in CAN_ID_MAP:
            can_messages.append({
                "can_id": CAN_ID_MAP[signal],
                "signal": signal,
                "value": round(value, 3)
            })

    return can_messages
