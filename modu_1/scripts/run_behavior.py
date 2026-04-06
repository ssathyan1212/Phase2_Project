from behavior_analysis.behavior_score import behavior_score
# Example vehicle state (from CARLA)
vehicle_state = {
    "speed": 62.0,
    "steering": 0.85
}
score = behavior_score(vehicle_state)
print("Behavior Score:", score)
