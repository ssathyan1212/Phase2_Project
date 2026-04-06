from .constants import MAP, STRIDE

class Mapper:

    def map(self, attack):

        key = MAP.get(attack, None)

        if key:
            return STRIDE[key]

        return "Unknown"