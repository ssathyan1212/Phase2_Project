from carla_simulator.carla_client import connect_to_carla
from carla_simulator.world_manager import setup_world
from carla_simulator.vehicle_spawner import spawn_vehicle
from carla_simulator.sensor_manager import get_vehicle_state

from can_bus.can_signal_generator import generate_can_messages
from can_bus.can_logger import init_logger, log_can_frames

from attacks.dos_attack import dos_attack
from attacks.fuzzy_attack import fuzzy_attack
from attacks.replay_attack import replay_attack
from attacks.spoofing_attack import spoofing_attack
from attacks.suspension_attack import suspension_attack
from attacks.masquerade_attack import masquerade_attack


import time



def run(mode="normal"):
    print(f"[INFO] Running system in {mode.upper()} mode")

    client, world = connect_to_carla()
    setup_world(world)
    vehicle = spawn_vehicle(world)

    # ✅ Initialize CSV logger
    init_logger()

    for _ in range(200):
        world.tick()

        # 1️⃣ Get physical vehicle state
        state = get_vehicle_state(vehicle)

        # 2️⃣ Convert to CAN frames
        can_frames = generate_can_messages(state)
        if mode == "dos":
            can_frames = dos_attack(can_frames)
        elif mode == "fuzzy":
            can_frames = fuzzy_attack(can_frames)
        elif mode == "replay":
            can_frames = replay_attack(can_frames)
        elif mode == "spoofing":
            can_frames = spoofing_attack(can_frames)
        elif mode == "suspension":
            can_frames = suspension_attack(can_frames)
        elif mode == "masquerade":
            can_frames = masquerade_attack(can_frames)
        # 3️⃣ Log CAN frames
        log_can_frames(can_frames,mode)

        time.sleep(0.05)

    print("[INFO] Simulation completed")


if __name__ == "__main__":
    run("normal")
