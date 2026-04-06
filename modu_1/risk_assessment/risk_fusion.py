# risk_assessment/risk_fusion.py

def risk_fusion(anomaly_score, behavior_score, alpha=0.6):
    return alpha * anomaly_score + (1 - alpha) * behavior_score


def severity_level(risk):
    if risk >= 0.6:
        return "HIGH"
    elif risk >= 0.3:
        return "MEDIUM"
    else:
        return "LOW"
