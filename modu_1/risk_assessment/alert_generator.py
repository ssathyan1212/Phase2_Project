# risk_assessment/alert_generator.py

def generate_alert(severity):
    if severity == "HIGH":
        return "🚨 EMERGENCY: Immediate action required"
    elif severity == "MEDIUM":
        return "⚠️ WARNING: Monitor vehicle behavior"
    else:
        return "ℹ️ INFO: Normal operation"
