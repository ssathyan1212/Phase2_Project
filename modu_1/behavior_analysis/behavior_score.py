# behavior_analysis/behavior_score.py
from behavior_analysis.lane_deviation import lane_deviation
from behavior_analysis.speed_anomaly import speed_anomaly
def behavior_score(state):
    score = 0
    score += lane_deviation(state["steering"])
    score += speed_anomaly(state["speed"])
    return min(score, 1.0)
