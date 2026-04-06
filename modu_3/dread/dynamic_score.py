import random
class DynamicDREAD:
    def calculate(self, attack_type):
        # Simulating CVSS-like behavior
        if attack_type == "Spoofing":
            damage = random.randint(3,5)
            reproducibility = random.randint(3,5)
            exploitability = random.randint(3,5)
            affected = random.randint(2,5)
            discoverability = random.randint(2,4)
        elif attack_type == "Tampering":
            damage = random.randint(3,5)
            reproducibility = random.randint(2,4)
            exploitability = random.randint(2,4)
            affected = random.randint(2,5)
            discoverability = random.randint(2,4)
        elif attack_type == "Denial of Service":
            damage = random.randint(2,4)
            reproducibility = random.randint(2,5)
            exploitability = random.randint(3,5)
            affected = random.randint(2,4)
            discoverability = random.randint(2,5)
        else:
            return [1,1,1,1,1]
        return [damage, reproducibility, exploitability, affected, discoverability]
    def total(self, scores):
        return sum(scores)