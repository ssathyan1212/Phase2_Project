from carla_simulator.carla_client import connect_to_carla
from carla_simulator.world_manager import setup_world
from carla_simulator.vehicle_spawner import spawn_vehicle
from carla_simulator.sensor_manager import get_vehicle_state
from carla_simulator.simple_drive import drive_vehicle
from carla_simulator.camera_manager import follow_vehicle
from behavior_analysis.behavior_score import behavior_score
from risk_assessment.risk_fusion import risk_fusion
from risk_assessment.severity_levels import severity_level
from risk_assessment.alert_generator import generate_alert
from visualization.hud_alert import show_alert
from visualization.vehicle_visuals import draw_vehicle_box
from visualization.emergency_action import emergency_brake
import carla
#==============================
#🔥 EXPERIMENT MODE
#==============================
MODE = "dos"      # "normal", "spoofing", "dos"
print(f"\n[INFO]Starting experiment in {MODE.upper()} mode\n")
# ==============================
# CARLA SETUP
# ==============================
client, world = connect_to_carla()
setup_world(world)
vehicle = spawn_vehicle(world)
# Force camera to vehicle immediately
follow_vehicle(world, vehicle)
world.tick()
# ==============================
# RESULT LOGGING
# ==============================
results = {
    "mode": MODE,
    "attack_detected": False,
    "final_risk": "LOW"
}
# ==============================
# MAIN SIMULATION LOOP
# ==============================
for step in range(200):
    drive_vehicle(vehicle, world, steps=1)
    follow_vehicle(world, vehicle)

    # Debug movement (optional)
    print("Vehicle location:", vehicle.get_location())

    # Get vehicle state
    state = get_vehicle_state(vehicle)
    b_score = behavior_score(state)

    # ==============================
    # ATTACK SIMULATION
    # ==============================
    if MODE == "normal":
        anomaly_score = 0.0

    elif MODE == "dos":
        anomaly_score = 1.0 if step > 120 else 0.0

    elif MODE == "spoofing":
        anomaly_score = 1.0 if step > 80 else 0.0

    # ==============================
    # RISK CALCULATION
    # ==============================
    risk = risk_fusion(anomaly_score, b_score)

    # ==============================
    # ATTACK-AWARE SEVERITY
    # ==============================
    if MODE == "normal":
        severity = "LOW"

    elif MODE == "dos":
        severity = "MEDIUM" if anomaly_score > 0 else "LOW"

    elif MODE == "spoofing":
        severity = "HIGH" if anomaly_score > 0 else "LOW"

    alert = generate_alert(severity)

    # Debug log
    print(f"[DEBUG] Step={step}, Mode={MODE}, Anomaly={anomaly_score}, "
          f"Behavior={b_score:.2f}, Risk={risk:.2f}, Severity={severity}")

    # Update results
    if severity in ["MEDIUM", "HIGH"]:
        results["attack_detected"] = True
        results["final_risk"] = severity

    # ==============================
    # 🎯 VISUAL OUTPUTS
    # ==============================
    draw_vehicle_box(world, vehicle, severity)

    color = (
        carla.Color(255, 0, 0) if severity == "HIGH" else
        carla.Color(255, 165, 0) if severity == "MEDIUM" else
        carla.Color(0, 255, 0)
    )
    show_alert(world, vehicle, f"{alert} | RISK: {severity}", color)
    # Emergency response ONLY for spoofing
    if severity == "HIGH":
        emergency_brake(vehicle)
# ==============================
# FINAL SUMMARY
# ==============================
print("\n==============================")
print("EXPERIMENT SUMMARY")
print("==============================")
print("Mode:", results["mode"])
print("Attack detected:", results["attack_detected"])
print("Final risk level:", results["final_risk"])
print("==============================\n")
print("[INFO] Visual demo completed")
