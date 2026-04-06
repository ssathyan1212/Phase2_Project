import cv2
class AttackVisualizer:
    def draw(self, frame, attack_type):
        if frame is None:
            return frame
        if attack_type == "SIGNAL_ATTACK":
            cv2.putText(frame, "FAKE TRAFFIC SIGN",
                        (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 3)
        elif attack_type == "MOTION_ATTACK":
            cv2.putText(frame, "FORGED SPEED",
                        (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 0, 0), 3)
        elif attack_type == "DOS_ATTACK":
            cv2.putText(frame, "SENSOR FREEZE",
                        (50, 150), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 255), 3)
        return frame