# behavior_analysis/speed_anomaly.py

def speed_anomaly(speed, max_speed=50):
    return 1 if speed > max_speed else 0
