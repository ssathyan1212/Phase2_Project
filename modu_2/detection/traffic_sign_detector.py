import carla
class TrafficSignDetector:
    def detect(self, sign, env):
       base_loc = sign["location"]
       loc1 = base_loc + carla.Location(z=0.5)
       loc2 = base_loc + carla.Location(z=1)
       if sign["text"] != "STOP":
        env.draw_text(loc2, "FAKE SIGN ❌", carla.Color(255,0,0))
        return False
       else:
        env.draw_text(loc2, "REAL SIGN ✅", carla.Color(0,255,0))
        return True