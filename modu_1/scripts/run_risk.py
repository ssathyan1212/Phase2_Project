from risk_assessment.risk_fusion import risk_fusion
from risk_assessment.severity_levels import severity_level
from risk_assessment.alert_generator import generate_alert
anomaly_score = 1.0      # from Step 4
behavior_score_val = 0.9 # from Step 5
risk = risk_fusion(anomaly_score, behavior_score_val)
severity = severity_level(risk)
alert = generate_alert(severity)
print("Risk Score:", risk)
print("Severity:", severity)
print("Alert:", alert)
