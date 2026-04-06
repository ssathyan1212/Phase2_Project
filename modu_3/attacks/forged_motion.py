def forged_motion_attack(vehicle):
    velocity = vehicle.get_velocity()
    real_speed = velocity.x
    fake_speed = real_speed + 30
    return {
        "event": "FORGED_MOTION",
        "real_speed": real_speed,
        "fake_speed": fake_speed,
        "deviation": fake_speed - real_speed,
        "impact": "Vehicle misjudges speed → unsafe control"
    }