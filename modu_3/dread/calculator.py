class DREAD:
    def score(self, level):
        if level == "Spoofing":
            return [3,3,3,3,2]
        elif level == "Tampering":
            return [3,3,2,3,2]
        elif level == "Denial of Service":
            return [2,2,3,2,2]
        return [1,1,1,1,1]
    def total(self, scores):
        return sum(scores)