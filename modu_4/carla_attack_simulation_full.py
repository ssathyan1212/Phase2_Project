import carla
import random
import time
import math
import csv
from collections import deque

# ==============================
# CONFIG
# ==============================
ATTACK_INTERVAL = 6
ATTACK_DURATION = 4

SAFE_THROTTLE = 0.35
SAFE_STEER = 0.0

LOG_FILE = "advanced_attack_dataset.csv"

# ==============================
# LOGGER
# ==============================
class Logger:
    def __init__(self, filename):
        self.filename = filename
        with open(self.filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                "time","speed","throttle","steer","brake",
                "imu_acc","imu_gyro","gps_x","gps_y",
                "attack","severity","detected"
            ])

    def log(self, row):
        with open(self.filename, 'a', newline='') as f:
            csv.writer(f).writerow(row)

# ==============================
# VEHICLE
# ==============================
class VehicleManager:
    def __init__(self, world):
        self.world = world
        self.vehicle = None

    def spawn(self):
        bp = random.choice(self.world.get_blueprint_library().filter('vehicle.*'))
        spawn = random.choice(self.world.get_map().get_spawn_points())
        self.vehicle = self.world.spawn_actor(bp, spawn)
        print("🚗 Vehicle Spawned")

    def get_speed(self):
        v = self.vehicle.get_velocity()
        return 3.6 * math.sqrt(v.x**2 + v.y**2 + v.z**2)

# ==============================
# SENSOR MANAGER
# ==============================
class SensorManager:
    def __init__(self, world, vehicle):
        self.world = world
        self.vehicle = vehicle

        self.imu_data = {"acc":0, "gyro":0}
        self.gps_data = {"x":0, "y":0}

        self.sensors = []

    def attach_sensors(self):
        blueprint = self.world.get_blueprint_library()

        # IMU
        imu_bp = blueprint.find('sensor.other.imu')
        imu = self.world.spawn_actor(imu_bp, carla.Transform(), attach_to=self.vehicle)
        imu.listen(self.imu_callback)
        self.sensors.append(imu)

        # GPS
        gps_bp = blueprint.find('sensor.other.gnss')
        gps = self.world.spawn_actor(gps_bp, carla.Transform(), attach_to=self.vehicle)
        gps.listen(self.gps_callback)
        self.sensors.append(gps)

    def imu_callback(self, data):
        self.imu_data["acc"] = data.accelerometer.x
        self.imu_data["gyro"] = data.gyroscope.z

    def gps_callback(self, data):
        self.gps_data["x"] = data.latitude
        self.gps_data["y"] = data.longitude

# ==============================
# ATTACK ENGINE (ADVANCED)
# ==============================
class AttackEngine:
    def __init__(self):
        self.attacks = [
            "brake","steer","throttle","zigzag",
            "stop","lane_drift","combo","sensor_spoof"
        ]
        self.severity_levels = ["low","medium","high"]

    def choose_attack(self, history):
        # Adaptive attack selection
        if history.count(True) > 3:
            return "sensor_spoof", "low"
        return random.choice(self.attacks), random.choice(self.severity_levels)

    def apply(self, control, attack, severity, tick, sensor_manager):
        factor = {"low":0.3,"medium":0.6,"high":1.0}[severity]

        if attack == "brake":
            control.brake = factor
            control.throttle = 0

        elif attack == "steer":
            control.steer = random.uniform(-1,1)*factor

        elif attack == "throttle":
            control.throttle = factor

        elif attack == "zigzag":
            control.steer = math.sin(tick*0.5)*factor

        elif attack == "stop":
            control.brake = 1.0
            control.throttle = 0

        elif attack == "lane_drift":
            control.steer = 0.3*factor

        elif attack == "combo":
            control.steer = random.uniform(-1,1)*factor
            control.brake = factor * 0.5

        elif attack == "sensor_spoof":
            sensor_manager.imu_data["acc"] *= (1 + factor)
            sensor_manager.gps_data["x"] += factor * 0.0001

        return control

# ==============================
# DETECTOR (ENHANCED)
# ==============================
class Detector:
    def __init__(self):
        self.history = deque(maxlen=15)

    def detect(self, control, sensor_data):
        detected = False

        if self.history:
            prev = self.history[-1]

            # control anomaly
            if abs(control.steer - prev["steer"]) > 0.7:
                detected = True

            # conflicting inputs
            if control.brake > 0.7 and control.throttle > 0.5:
                detected = True

            # sensor anomaly
            if abs(sensor_data["acc"] - prev["acc"]) > 5:
                detected = True

        self.history.append({
            "steer":control.steer,
            "acc":sensor_data["acc"]
        })

        return detected

# ==============================
# RECOVERY (SMART)
# ==============================
class Recovery:
    def apply(self, control):
        control.throttle = SAFE_THROTTLE
        control.steer = SAFE_STEER
        control.brake = 0
        return control

# ==============================
# VISUALIZER
# ==============================
class Visualizer:
    def __init__(self, world):
        self.world = world

    def draw(self, vehicle, text, color, y=0):
        loc = vehicle.get_location()
        loc.z += 2 + y
        self.world.debug.draw_string(loc, text, False, color, 0.1, False)

# ==============================
# MAIN SYSTEM
# ==============================
class CarlaAdvancedSystem:

    def __init__(self):
        self.client = carla.Client('localhost',2000)
        self.client.set_timeout(10.0)

        self.world = self.client.get_world()

        self.vm = VehicleManager(self.world)
        self.vm.spawn()
        self.vehicle = self.vm.vehicle

        self.sensor_manager = SensorManager(self.world, self.vehicle)
        self.sensor_manager.attach_sensors()

        self.attack_engine = AttackEngine()
        self.detector = Detector()
        self.recovery = Recovery()
        self.visual = Visualizer(self.world)
        self.logger = Logger(LOG_FILE)

        self.spectator = self.world.get_spectator()

        self.last_attack_time = time.time()
        self.attack_active = False
        self.attack_end_time = 0
        self.attack_type = None
        self.severity = None
        self.tick = 0

        self.detection_history = []

    def update_spectator(self):
        transform = self.vehicle.get_transform()
        loc = transform.location
        rot = transform.rotation

        offset = carla.Location(
            x=-8 * math.cos(math.radians(rot.yaw)),
            y=-8 * math.sin(math.radians(rot.yaw)),
            z=4
        )

        self.spectator.set_transform(
            carla.Transform(loc + offset, carla.Rotation(pitch=-15, yaw=rot.yaw))
        )

    def base_control(self):
        c = carla.VehicleControl()
        c.throttle = 0.5
        return c

    def trigger_attack(self, now):
        if now - self.last_attack_time > ATTACK_INTERVAL:
            self.attack_active = True
            self.attack_type, self.severity = self.attack_engine.choose_attack(self.detection_history)
            self.attack_end_time = now + ATTACK_DURATION
            self.last_attack_time = now
            print(f"🚨 Attack: {self.attack_type} | {self.severity}")

    def handle_attack(self, control, now):
        if self.attack_active:
            control = self.attack_engine.apply(
                control,
                self.attack_type,
                self.severity,
                self.tick,
                self.sensor_manager
            )

            if now > self.attack_end_time:
                self.attack_active = False
                print("✅ Attack Ended")

        return control

    def detect_and_recover(self, control):
        sensor_data = self.sensor_manager.imu_data

        detected = self.detector.detect(control, sensor_data)

        self.detection_history.append(detected)
        if len(self.detection_history) > 10:
            self.detection_history.pop(0)

        if detected:
            print("🧠 Attack Detected → Recovery Applied")
            control = self.recovery.apply(control)

        return control, detected

    def run(self):
        print("🚀 Advanced System Running...")

        while True:
            self.tick += 1
            now = time.time()

            control = self.base_control()

            self.trigger_attack(now)
            control = self.handle_attack(control, now)
            control, detected = self.detect_and_recover(control)

            self.vehicle.apply_control(control)
            self.update_spectator()

            speed = self.vm.get_speed()

            imu = self.sensor_manager.imu_data
            gps = self.sensor_manager.gps_data

            self.visual.draw(self.vehicle, f"Speed: {int(speed)}", carla.Color(0,255,255), 0)
            self.visual.draw(self.vehicle, f"Attack: {self.attack_type}", carla.Color(255,0,0), 1)
            self.visual.draw(self.vehicle, f"Detected: {detected}", carla.Color(0,255,0), 2)

            self.logger.log([
                time.time(),
                speed,
                control.throttle,
                control.steer,
                control.brake,
                imu["acc"],
                imu["gyro"],
                gps["x"],
                gps["y"],
                self.attack_type,
                self.severity,
                detected
            ])

            time.sleep(0.05)

# ==============================
# MAIN
# ==============================
def main():
    system = None
    try:
        system = CarlaAdvancedSystem()
        system.run()
    except KeyboardInterrupt:
        print("Stopped")
    finally:
        if system:
            if system.vehicle:
                system.vehicle.destroy()

if __name__ == "__main__":
    main()