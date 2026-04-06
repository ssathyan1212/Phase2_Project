import random
import carla
class FakeTrafficSignAttack:
    def __init__(self):
        self.fake_signs = []
    def inject_fake_sign(self, world, env):
        print("[ATTACK] Injecting Fake Traffic Sign...")
        # Get vehicle location
        vehicles = world.get_actors().filter('*vehicle*')
        if len(vehicles) == 0:
            return None
        vehicle = vehicles[0]
        vehicle_loc = vehicle.get_location()
        # Place sign in front of vehicle
        sign_location = vehicle_loc + carla.Location(
            x=10,
            y=random.randint(-3, 3),
            z=2
        )
        fake_sign = {
            "type": "STOP",
            "text": random.choice(["STOP", "SHOP", "ST0P"]),
            "distance": random.randint(5, 20),
            "location": sign_location
        }
        # Draw sign text in CARLA
        env.draw_text(
            sign_location,
            f"SIGN: {fake_sign['text']}",
            color=carla.Color(0, 255, 0)
        )
        self.fake_signs.append(fake_sign)
        return fake_sign