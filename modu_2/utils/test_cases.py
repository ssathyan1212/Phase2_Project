def get_test_cases():
    return [
        {"speed": 40, "location": (50,50), "expected": True},
        {"speed": 120, "location": (50,50), "expected": False},
        {"speed": 40, "location": (999,999), "expected": False},
        {"speed": 150, "location": (999,999), "expected": False},
    ]