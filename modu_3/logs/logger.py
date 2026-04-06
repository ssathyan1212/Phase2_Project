import csv
import os
class Logger:
    def __init__(self):
        self.file = "logs/results.csv"
        if not os.path.exists(self.file):
            with open(self.file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Attack", "STRIDE", "Score", "Frequency", "Final Risk"
                ])
    def log(self, data):
        with open(self.file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(data)