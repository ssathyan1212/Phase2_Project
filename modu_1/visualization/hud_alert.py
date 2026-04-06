# visualization/hud_alert.py

import carla

def show_alert(world, vehicle, text, color, duration=0.1):
    location = vehicle.get_location()
    location.z += 2.5  # above vehicle

    world.debug.draw_string(
        location,
        text,
        draw_shadow=True,
        color=color,
        life_time=duration,
        persistent_lines=False
    )
