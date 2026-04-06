# evaluation/attack_evaluation.py

from evaluation.metrics import precision, recall, f1

def evaluate(tp, fp, fn):
    p = precision(tp, fp)
    r = recall(tp, fn)
    return f1(p, r)
