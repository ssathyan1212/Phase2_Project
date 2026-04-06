# carla_simulator/vehicle_spawner.py
import random
import carla
def spawn_vehicle(world):
    blueprint_library = world.get_blueprint_library()
    vehicle_bp = blueprint_library.filter('vehicle.tesla.model3')[0]
    spawn_points = world.get_map().get_spawn_points()
    spawn_point = random.choice(spawn_points)
    vehicle = world.spawn_actor(vehicle_bp, spawn_point)
    print("[INFO] Vehicle spawned")
    return vehicle
