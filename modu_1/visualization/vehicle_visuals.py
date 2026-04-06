# visualization/vehicle_visuals.py

import carla

def draw_vehicle_box(world, vehicle, severity, duration=0.1):
    bbox = vehicle.bounding_box

    # Get ONLY rotation (this is required)
    rotation = vehicle.get_transform().rotation

    if severity == "HIGH":
        color = carla.Color(255, 0, 0)      # RED
    elif severity == "MEDIUM":
        color = carla.Color(255, 165, 0)    # ORANGE
    else:
        color = carla.Color(0, 255, 0)      # GREEN

    world.debug.draw_box(
        bbox,
        rotation,
        thickness=0.15,
        color=color,
        life_time=duration,
        persistent_lines=False
    )
