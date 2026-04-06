# visualization/emergency_action.py

import carla

def emergency_brake(vehicle):
    control = carla.VehicleControl(
        throttle=0.0,
        brake=1.0,
        steer=0.0
    )
    vehicle.apply_control(control)
