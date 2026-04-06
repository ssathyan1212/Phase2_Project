# carla_simulator/world_manager.py

def setup_world(world):
    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 0.05  # 20 FPS
    world.apply_settings(settings)

    print("[INFO] World set to synchronous mode")
