class Risk:
    def classify(self, score):
        # ✅ Adjusted for COMPOSITE scale (~8 to 16)
        if score >= 13:
            return "HIGH"
        elif score >= 10:
            return "MEDIUM"
        return "LOW"