import carla
import math

def follow_vehicle(world, vehicle):
    spectator = world.get_spectator()
    transform = vehicle.get_transform()

    # Vehicle location
    location = transform.location
    rotation = transform.rotation

    # Convert yaw to radians
    yaw_rad = math.radians(rotation.yaw)

    # Place camera BEHIND the vehicle (relative to heading)
    distance = 10.0
    height = 6.0

    camera_x = location.x - distance * math.cos(yaw_rad)
    camera_y = location.y - distance * math.sin(yaw_rad)
    camera_z = location.z + height

    camera_location = carla.Location(
        x=camera_x,
        y=camera_y,
        z=camera_z
    )

    camera_rotation = carla.Rotation(
        pitch=-20.0,
        yaw=rotation.yaw,
        roll=0.0
    )

    spectator.set_transform(
        carla.Transform(camera_location, camera_rotation)
    )
