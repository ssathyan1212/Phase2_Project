class Context:

    def get(self, attack):

        if attack == "SIGNAL_ATTACK":
            return "Camera / Perception"

        elif attack == "MOTION_ATTACK":
            return "ECU / Control"

        elif attack == "DOS_ATTACK":
            return "Sensor Layer"

        return "Unknown"