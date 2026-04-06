import matplotlib.pyplot as plt
import numpy as np

class Metrics:

    def __init__(self):
        self.tp = 0
        self.fp = 0
        self.fn = 0
        self.tn = 0
        self.history = []  # for graph

    def update(self, prediction, actual):

        if prediction and actual:
            self.tp += 1
        elif prediction and not actual:
            self.fp += 1
        elif not prediction and actual:
            self.fn += 1
        else:
            self.tn += 1

        # store accuracy per step
        acc = (self.tp + self.tn) / max(1,(self.tp+self.tn+self.fp+self.fn))
        self.history.append(acc)

    def compute(self):

        accuracy = (self.tp + self.tn) / max(1,(self.tp+self.tn+self.fp+self.fn))
        precision = self.tp / max(1,(self.tp+self.fp))
        recall = self.tp / max(1,(self.tp+self.fn))
        f1 = 2 * precision * recall / max(1,(precision+recall))

        return accuracy, precision, recall, f1

    def confusion_matrix(self):
        return np.array([
            [self.tp, self.fp],
            [self.fn, self.tn]
        ])