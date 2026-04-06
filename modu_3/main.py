from attacks.fake_sign import fake_sign_attack
from attacks.forged_motion import forged_motion_attack
from attacks.dos import dos_attack
from detection.anomaly import AnomalyDetector
from stride.engine import STRIDEEngine
from dread.dynamic_score import DynamicDREAD
from dread.risk import Risk
from dread.aggregator import RiskAggregator
from logs.logger import Logger
# ✅ CARLA imports
from carla_sim.setup import CarlaSetup
from carla_sim.vehicle import VehicleManager
import random
from visualization.camera_view import CameraView
from visualization.attack_visualizer import AttackVisualizer
import cv2
import time
def main():
    print("\n===== INITIALIZING SYSTEM =====")
    # ✅ 1. Setup CARLA
    setup = CarlaSetup()
    world = setup.get_world()
    vm = VehicleManager(world)
    vehicle = vm.spawn()
    print("Vehicle spawned successfully\n")
    time.sleep(2) 
    camera = CameraView(world, vehicle)
    camera.attach_camera()
    visualizer = AttackVisualizer()
    # ✅ 2. Initialize modules
    detector = AnomalyDetector()
    stride_engine = STRIDEEngine()
    dread = DynamicDREAD()
    risk = Risk()
    aggregator = RiskAggregator()
    logger = Logger()
    # ✅ 3. Attack list
    attacks = [
        fake_sign_attack,
        forged_motion_attack,
        dos_attack
    ]
    frequency_counter = {}
    print("===== RUNNING SIMULATION =====\n")
    # ✅ Reason mapping (defined once)
    reason_map = {
        "SIGNAL_ATTACK": "Fake traffic sign misleads perception",
        "MOTION_ATTACK": "Vehicle speed data is manipulated",
        "DOS_ATTACK": "Sensor data becomes unavailable"
    }
    # ✅ 4. Simulation loop
    for i in range(5):
        attack_func = random.choice(attacks)
        print(f"\n[DEBUG] Running attack: {attack_func.__name__}")
        # ✅ Handle forged_motion separately
        if attack_func.__name__ == "forged_motion_attack":
            attack_data = attack_func(vehicle)
        else:
            attack_data = attack_func()
        # ✅ Detection
        anomaly = detector.detect(attack_data)     
        camera = CameraView(world, vehicle)
        camera.attach_camera()
        visualizer = AttackVisualizer()
        # ✅ Frequency tracking
        frequency_counter[anomaly] = frequency_counter.get(anomaly, 0) + 1
        frequency = frequency_counter[anomaly]
        # ✅ STRIDE processing
        stride_result = stride_engine.process({"event": anomaly})
        # ✅ DREAD scoring
        dread_scores = dread.calculate(stride_result["stride"])
        dread_total = dread.total(dread_scores)

        # ✅ DREAD level classification
        dread_level = risk.classify(dread_total)

        # ✅ Composite risk
        composite = aggregator.compute(dread_total, frequency)

        # ✅ Composite risk level
        composite_level = risk.classify(composite)

        # ✅ Output (clean + correct)
        print("\n===== EVENT RESULT =====")
        print(f"Event No        : {i+1}")
        print(f"Attack Type     : {anomaly}")
        print(f"STRIDE Category : {stride_result['stride']}")
        print(f"Context         : {stride_result['context']}")
        print(f"Reason          : {reason_map.get(anomaly, 'Unknown')}")
        print(f"DREAD Score     : {dread_total}")
        print(f"DREAD Level     : {dread_level}")
        print(f"Frequency       : {frequency}")
        print(f"Composite Risk  : {composite}")
        print(f"Final Risk      : {composite_level}")
        print("========================")

        # ✅ Logging
        logger.log([
            anomaly,
            stride_result["stride"],
            dread_total,
            frequency,
            composite
        ])

    print("\n===== SIMULATION COMPLETED =====\n")


if __name__ == "__main__":
    main()