# carla_simulator/simple_drive.py

import carla
import time

def drive_vehicle(vehicle, world, steps=200):
    for _ in range(steps):
        control = carla.VehicleControl(
            throttle=0.5,
            steer=0.0
        )
        vehicle.apply_control(control)
        world.tick()
        time.sleep(0.05)

    print("[INFO] Vehicle driving completed")
