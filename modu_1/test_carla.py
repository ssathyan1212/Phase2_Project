from carla_simulator.carla_client import connect_to_carla
from carla_simulator.world_manager import setup_world
from carla_simulator.vehicle_spawner import spawn_vehicle
from carla_simulator.sensor_manager import get_vehicle_state
from carla_simulator.simple_drive import drive_vehicle
from can_bus.can_signal_generator import generate_can_messages
from can_bus.can_logger import init_logger, log_can_frames
from attacks.dos_attack import dos_attack
from attacks.fuzzy_attack import fuzzy_attack
from attacks.replay_attack import replay_attack
from attacks.suspension_attack import suspension_attack
from attacks.spoofing_attack import spoofing_attack
from attacks.masquerade_attack import masquerade_attack

ATTACK_MODE = "spoofing"  # change this

client, world = connect_to_carla()
setup_world(world)
vehicle = spawn_vehicle(world)

init_logger()

for step in range(150):
    drive_vehicle(vehicle, world, steps=1)

    state = get_vehicle_state(vehicle)
    can_frames = generate_can_messages(state)

    # 🔥 ATTACK INJECTION
    if step > 50:
        if ATTACK_MODE == "dos":
            can_frames = dos_attack(can_frames)
        elif ATTACK_MODE == "fuzzy":
            can_frames = fuzzy_attack(can_frames)
        elif ATTACK_MODE == "replay":
            can_frames = replay_attack(can_frames)
        elif ATTACK_MODE == "suspension":
            can_frames = suspension_attack(can_frames)
        elif ATTACK_MODE == "spoofing":
            can_frames = spoofing_attack(can_frames)
        elif ATTACK_MODE == "masquerade":
            can_frames = masquerade_attack(can_frames)

    log_can_frames(can_frames)

print("[INFO] Attack simulation completed")
