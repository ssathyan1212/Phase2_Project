# carla_simulator/sensor_manager.py
import math
def get_vehicle_state(vehicle):
    velocity = vehicle.get_velocity()
    speed = 3.6 * math.sqrt(
        velocity.x**2 + velocity.y**2 + velocity.z**2
    )  # km/h

    control = vehicle.get_control()

    state = {
        "speed": speed,
        "steering": control.steer,
        "throttle": control.throttle,
        "brake": control.brake
    }

    return state
