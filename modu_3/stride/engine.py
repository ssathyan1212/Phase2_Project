from .identifier import Identifier
from .mapper import Mapper
from .context import Context
class STRIDEEngine:
    def __init__(self):
        self.id = Identifier()
        self.map = Mapper()
        self.ctx = Context()
    def process(self, data):
        attack = self.id.identify(data)
        stride = self.map.map(attack)
        context = self.ctx.get(attack)
        return {
            "attack": attack,
            "stride": stride,
            "context": context
        }