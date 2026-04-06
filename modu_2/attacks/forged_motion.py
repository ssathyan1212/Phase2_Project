import random

class ForgedMotionAttack:

    def inject_data(self, vehicle):

        # 50% normal, 50% attack
        if random.random() < 0.5:
            print("[NORMAL] Sending normal motion data")

            return {
                "speed": random.randint(20, 50),
                "location": (random.randint(0, 100), random.randint(0, 100)),
                "acceleration": random.randint(1, 5)
            }

        else:
            print("[ATTACK] Injecting forged motion data")

            return {
                "speed": random.randint(100, 200),
                "location": (999, 999),
                "acceleration": random.randint(20, 50)
            }