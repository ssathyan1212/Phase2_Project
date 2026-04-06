from simulation.carla_env import CarlaEnv
from simulation.vehicle_setup import VehicleManager
from attacks.fake_traffic_sign import FakeTrafficSignAttack
from attacks.forged_motion import ForgedMotionAttack
from detection.traffic_sign_detector import TrafficSignDetector
from detection.motion_detector import MotionDetector
from utils.metrics import Metrics
from utils.test_cases import get_test_cases
from utils.logger import log
from utils.plot_results import plot_metrics, plot_confusion_matrix, plot_accuracy_trend
import carla
import time
def main():
    env = CarlaEnv()
    world = env.world
    vehicle = None
    camera = None
    try:
        # ===============================
        # 🔧 INITIALIZATION
        # ===============================
        vehicle_manager = VehicleManager(world, env.blueprint_lib)
        spawn_points = env.get_spawn_points()

        vehicle = vehicle_manager.spawn_vehicle(spawn_points)

        # 🎥 Attach camera
        camera = vehicle_manager.attach_camera(vehicle)

        spectator = world.get_spectator()

        # Modules
        sign_attack = FakeTrafficSignAttack()
        motion_attack = ForgedMotionAttack()
        sign_detector = TrafficSignDetector()
        motion_detector = MotionDetector()
        metrics = Metrics()

        print("\n🚀 Simulation Started...\n")

        # ===============================
        # 🔁 MAIN LOOP
        # ===============================
        for step in range(20):

            print(f"\n--- Step {step} ---")

            # 🎥 Follow vehicle (TOP VIEW)
            transform = vehicle.get_transform()
            spectator.set_transform(
                carla.Transform(
                    transform.location + carla.Location(z=20),
                    carla.Rotation(pitch=-90)
                )
            )

            # ===============================
            # 🚦 TRAFFIC SIGN ATTACK
            # ===============================
            fake_sign = sign_attack.inject_fake_sign(world, env)

            if fake_sign is None:
                continue

            result_sign = sign_detector.detect(fake_sign, env)

            # ===============================
            # 🚗 MOTION ATTACK
            # ===============================
            motion_data = motion_attack.inject_data(vehicle)

            result_motion = motion_detector.detect(
                motion_data, vehicle, env
            )

            # Ground truth (actual condition)
            actual_motion = (
                motion_data["speed"] < 60 and
                motion_data["location"][0] < 500
            )

            # ===============================
            # 📊 METRICS UPDATE
            # ===============================
            metrics.update(result_motion, actual_motion)

            # ===============================
            # 📝 LOGGING
            # ===============================
            log(
                f"Step {step} | Sign: {result_sign} | Motion: {result_motion}"
            )

            env.tick()
            time.sleep(1.5)

        # ===============================
        # 📊 FINAL RESULTS
        # ===============================
        acc, prec, rec, f1 = metrics.compute()

        print("\n==============================")
        print("📊 FINAL EVALUATION RESULTS")
        print("==============================")
        print(f"Accuracy  : {round(acc, 3)}")
        print(f"Precision : {round(prec, 3)}")
        print(f"Recall    : {round(rec, 3)}")
        print(f"F1 Score  : {round(f1, 3)}")

        # ===============================
        # 📊 GRAPH GENERATION
        # ===============================
        print("\n📈 Generating Graphs...\n")

        cm = metrics.confusion_matrix()

        plot_metrics(acc, prec, rec, f1)
        plot_confusion_matrix(cm)
        plot_accuracy_trend(metrics.history)

        print("✅ Graphs saved in output/ folder")

        # ===============================
        # 🧪 TEST CASES
        # ===============================
        print("\n🧪 Running Test Cases...\n")

        test_cases = get_test_cases()

        for i, test in enumerate(test_cases):

            print(f"Test Case {i+1}")

            result = motion_detector.detect(test, vehicle, env)

            print(f"Expected: {test['expected']} | Predicted: {result}")

            if result == test["expected"]:
                print("✅ PASS\n")
            else:
                print("❌ FAIL\n")

    except KeyboardInterrupt:
        print("\n⛔ Interrupted by user")

    finally:
        # ===============================
        # 🧹 CLEANUP
        # ===============================
        print("\n🧹 Cleaning up actors...")

        try:
            if camera is not None:
                camera.stop()
                time.sleep(0.5)
                camera.destroy()
        except:
            pass

        try:
            if vehicle is not None:
                vehicle.destroy()
        except:
            pass

        print("✅ Cleanup complete")


if __name__ == "__main__":
    main()