from config import MAX_SPEED, COMM_RANGE
def speed_plausibility(speed):
    if speed > MAX_SPEED:
        return False
    return True
def range_plausibility(distance):
    if distance > COMM_RANGE:
        return False
    return True 
def location_plausibility(location):
    x, y = location
    if x > 500 or y > 500:  # unrealistic map bounds
        return False
    return True