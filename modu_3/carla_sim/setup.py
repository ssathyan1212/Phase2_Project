import carla
class CarlaSetup:
    def __init__(self):
        self.client = carla.Client("localhost", 2000)
        self.client.set_timeout(20.0)
    def get_world(self):
        return self.client.get_world()