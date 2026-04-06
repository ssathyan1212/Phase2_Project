import random
import carla
class VehicleManager:
    def __init__(self, world, blueprint_lib):
        self.world = world
        self.blueprint_lib = blueprint_lib
        self.vehicles = []
    def spawn_vehicle(self, spawn_points):
        vehicle_bp = random.choice(self.blueprint_lib.filter('vehicle.*'))
        spawn_point = random.choice(spawn_points)
        vehicle = self.world.spawn_actor(vehicle_bp, spawn_point)
        vehicle.set_autopilot(True)
        self.vehicles.append(vehicle)
        print("✅ Vehicle spawned and moving")
        return vehicle
    def attach_camera(self, vehicle):
        camera_bp = self.blueprint_lib.find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x', '800')
        camera_bp.set_attribute('image_size_y', '600')
        camera_bp.set_attribute('fov', '110')
        # FRONT CAMERA
        transform = carla.Transform(
            carla.Location(x=1.5, z=2.4),
            carla.Rotation(pitch=0)
        )
        camera = self.world.spawn_actor(
            camera_bp,
            transform,
            attach_to=vehicle
        )
        # ✅ process image INSIDE method
        def process_image(image):
            pass
        camera.listen(lambda image: process_image(image))
        print("📷 Front camera attached (driver view)")
        return camera