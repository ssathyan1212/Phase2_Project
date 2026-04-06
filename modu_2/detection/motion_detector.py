import carla
from detection.plausibility import *

class MotionDetector:

    def detect(self, data, vehicle, env):

        score = 0

        base_loc = vehicle.get_location()

        # 👉 Offsets to avoid overlap
        loc1 = base_loc + carla.Location(z=2)
        loc2 = base_loc + carla.Location(z=2.5)
        loc3 = base_loc + carla.Location(z=3)

        # ===============================
        # 🚗 SPEED CHECK
        # ===============================
        speed_ok = speed_plausibility(data["speed"])

        if speed_ok:
            score += 1
            env.draw_text(loc1, f"SPEED OK ({data['speed']})", carla.Color(0,255,0))
        else:
            env.draw_text(loc1, f"SPEED ❌ ({data['speed']})", carla.Color(255,0,0))

        # ===============================
        # 📍 LOCATION CHECK
        # ===============================
        loc_ok = location_plausibility(data["location"])

        if loc_ok:
            score += 1
            env.draw_text(loc2, "LOCATION OK", carla.Color(0,255,0))
        else:
            env.draw_text(loc2, "LOCATION ❌", carla.Color(255,0,0))

        # ===============================
        # 🎯 FINAL RESULT
        # ===============================
        if score == 2:
            env.draw_text(loc3, "MOTION NORMAL ✅", carla.Color(0,255,0))
            return True
        else:
            env.draw_text(loc3, "MOTION ATTACK ⚠️", carla.Color(255,0,0))
            return False