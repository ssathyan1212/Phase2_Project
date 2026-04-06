import carla
import numpy as np
import cv2
class CameraView:
    def __init__(self, world, vehicle):
        self.world = world
        self.vehicle = vehicle
        self.image = None
    def attach_camera(self):
        print("Attaching camera to vehicle:", self.vehicle)
        blueprint = self.world.get_blueprint_library().find('sensor.camera.rgb')
        blueprint.set_attribute('image_size_x', '640')   
        blueprint.set_attribute('image_size_y', '480')
        blueprint.set_attribute('sensor_tick', '0.1')
        transform = carla.Transform(carla.Location(x=1.5, z=2.4))
        self.camera = self.world.try_spawn_actor(
           blueprint,
           transform,
           attach_to=self.vehicle)
        if self.camera is None:
             print("❌ Camera spawn failed")
             return
        self.camera.listen(lambda data: self.process(data))
    def process(self, image):
        array = np.frombuffer(image.raw_data, dtype=np.uint8)
        array = array.reshape((image.height, image.width, 4))
        self.image = array[:, :, :3]