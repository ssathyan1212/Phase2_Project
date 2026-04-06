class AnomalyDetector:
    def detect(self, data):
        if data["event"] == "FAKE_SIGN":
            return "SIGNAL_ATTACK"
        elif data["event"] == "FORGED_MOTION":
            return "MOTION_ATTACK"
        elif data["event"] == "SENSOR_FREEZE":
            return "DOS_ATTACK"
        return "NORMAL"