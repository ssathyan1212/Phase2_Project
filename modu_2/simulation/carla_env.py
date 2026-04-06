import carla
from config import CARLA_HOST,CARLA_PORT
class CarlaEnv:
    def __init__(self):
        self.client = carla.Client(CARLA_HOST, CARLA_PORT)
        self.client.set_timeout(10.0)
        # Optional: load stable map
        try:
            self.world = self.client.load_world('Town03')
        except:
            self.world = self.client.get_world()

        self.blueprint_lib = self.world.get_blueprint_library()

    def get_spawn_points(self):
        return self.world.get_map().get_spawn_points()

    def draw_text(self, location, text, color=carla.Color(255, 0, 0), life_time=2.0):
        try:
            self.world.debug.draw_string(
                location,
                text,
                draw_shadow=True,
                color=color,
                life_time=life_time,
                persistent_lines=False
            )
        except:
            pass  # prevents crash if actor removed

    def tick(self):
        try:
            self.world.tick()
        except:
            pass