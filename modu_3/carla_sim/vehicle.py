import random
class VehicleManager:
    def __init__(self, world):
        self.world = world
    def spawn(self):
        bp = random.choice(self.world.get_blueprint_library().filter("vehicle.*"))
        spawn_point = random.choice(self.world.get_map().get_spawn_points())
        vehicle = self.world.spawn_actor(bp, spawn_point)
        return vehicle