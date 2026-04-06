# scripts/run_detection.py
import torch
import time
from models.stcam import STcAM
from scripts.realtime_window import SlidingWindow
from behavior_analysis.behavior_score import behavior_score
from risk_assessment.risk_fusion import risk_fusion, severity_level
from risk_assessment.alert_generator import generate_alert
# Load trained model
model = STcAM(window_size=16)
model.load_state_dict(torch.load("models/mkf_ads_student.pth"))
model.eval()
print("[INFO] MKF-ADS model loaded")

# Sliding window for SPEED signal
window = SlidingWindow(size=16)

# Example threshold (set after computing)
THRESHOLD = 0.15   # temporary, will be learned

def simulate_realtime(speed, steering):
    window.add(speed)

    if not window.is_ready():
        return

    X = torch.tensor([window.get()], dtype=torch.float32)

    with torch.no_grad():
        pred = model(X).item()

    anomaly_score = abs(pred - speed)

    # Physical behavior
    state = {
        "speed": speed,
        "steering": steering
    }
    b_score = behavior_score(state)

    # Risk fusion
    risk = risk_fusion(anomaly_score, b_score)
    severity = severity_level(risk)
    alert = generate_alert(severity)

    print(f"[SCORE] Anomaly={anomaly_score:.3f}, Behavior={b_score:.2f}, Risk={risk:.2f}")
    print(alert)


# -------------------------------
# Simulated realtime loop
# -------------------------------
if __name__ == "__main__":
    print("[INFO] Running real-time detection")

    # Example values (replace with CARLA state)
    for t in range(50):
        speed = 30 + (t * 0.1)     # normal
        steering = 0.05

        if t > 30:
            speed = 45            # attack-like deviation

        simulate_realtime(speed, steering)
        time.sleep(0.2)
