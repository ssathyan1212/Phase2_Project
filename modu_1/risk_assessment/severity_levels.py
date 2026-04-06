def severity_level(risk):
    if risk >= 0.6:
        return "HIGH"
    elif risk >= 0.3:
        return "MEDIUM"
    else:
        return "LOW"
