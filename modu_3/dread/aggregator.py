class RiskAggregator:
    def compute(self, dread_score, frequency):
        # Weighted risk formula
        # This adds complexity for your review
        risk = (dread_score * 0.7) + (frequency * 0.3)
        return round(risk, 2)