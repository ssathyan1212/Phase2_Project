"""
evaluation/metrics.py
Computes classification metrics for the attack detection system.
Used for thesis Results & Discussion section.
"""

from collections import defaultdict
import math


class DetectionMetrics:
    """
    Computes per-class and macro-averaged Precision, Recall, F1-Score
    for the anomaly detector output.
    """

    ATTACK_CLASSES = ["SIGNAL_ATTACK", "MOTION_ATTACK", "DOS_ATTACK"]

    def __init__(self):
        self.true_labels = []
        self.pred_labels = []

    def add(self, true_label: str, predicted_label: str):
        self.true_labels.append(true_label)
        self.pred_labels.append(predicted_label)

    def confusion_matrix(self) -> dict:
        """Returns TP, FP, FN, TN per class."""
        matrix = {}
        for cls in self.ATTACK_CLASSES:
            tp = sum(1 for t, p in zip(self.true_labels, self.pred_labels) if t == cls and p == cls)
            fp = sum(1 for t, p in zip(self.true_labels, self.pred_labels) if t != cls and p == cls)
            fn = sum(1 for t, p in zip(self.true_labels, self.pred_labels) if t == cls and p != cls)
            tn = sum(1 for t, p in zip(self.true_labels, self.pred_labels) if t != cls and p != cls)
            matrix[cls] = {"TP": tp, "FP": fp, "FN": fn, "TN": tn}
        return matrix

    def precision(self, cls: str) -> float:
        cm = self.confusion_matrix()[cls]
        denom = cm["TP"] + cm["FP"]
        return round(cm["TP"] / denom, 4) if denom > 0 else 0.0

    def recall(self, cls: str) -> float:
        cm = self.confusion_matrix()[cls]
        denom = cm["TP"] + cm["FN"]
        return round(cm["TP"] / denom, 4) if denom > 0 else 0.0

    def f1_score(self, cls: str) -> float:
        p = self.precision(cls)
        r = self.recall(cls)
        denom = p + r
        return round(2 * p * r / denom, 4) if denom > 0 else 0.0

    def accuracy(self) -> float:
        correct = sum(1 for t, p in zip(self.true_labels, self.pred_labels) if t == p)
        return round(correct / len(self.true_labels), 4) if self.true_labels else 0.0

    def macro_avg(self) -> dict:
        precisions = [self.precision(c) for c in self.ATTACK_CLASSES]
        recalls = [self.recall(c) for c in self.ATTACK_CLASSES]
        f1s = [self.f1_score(c) for c in self.ATTACK_CLASSES]
        return {
            "macro_precision": round(sum(precisions) / len(precisions), 4),
            "macro_recall": round(sum(recalls) / len(recalls), 4),
            "macro_f1": round(sum(f1s) / len(f1s), 4),
        }

    def detection_rate(self) -> dict:
        """Per-class detection rate = TP / (TP + FN)"""
        cm = self.confusion_matrix()
        return {
            cls: round(cm[cls]["TP"] / max(cm[cls]["TP"] + cm[cls]["FN"], 1), 4)
            for cls in self.ATTACK_CLASSES
        }

    def false_positive_rate(self) -> dict:
        """Per-class FPR = FP / (FP + TN)"""
        cm = self.confusion_matrix()
        return {
            cls: round(cm[cls]["FP"] / max(cm[cls]["FP"] + cm[cls]["TN"], 1), 4)
            for cls in self.ATTACK_CLASSES
        }

    def full_report(self) -> dict:
        report = {
            "accuracy": self.accuracy(),
            "per_class": {},
            "macro_avg": self.macro_avg(),
            "detection_rate": self.detection_rate(),
            "false_positive_rate": self.false_positive_rate(),
            "confusion_matrix": self.confusion_matrix(),
        }
        for cls in self.ATTACK_CLASSES:
            report["per_class"][cls] = {
                "precision": self.precision(cls),
                "recall": self.recall(cls),
                "f1_score": self.f1_score(cls),
            }
        return report


class RiskMetrics:
    """
    Analyzes DREAD scores and composite risk levels from simulation logs.
    """

    def __init__(self, log_rows: list):
        """
        log_rows: list of dicts with keys:
            Attack, STRIDE, Score, Frequency, Final Risk
        """
        self.rows = log_rows

    def avg_dread_by_attack(self) -> dict:
        groups = defaultdict(list)
        for row in self.rows:
            groups[row["Attack"]].append(float(row["Score"]))
        return {k: round(sum(v) / len(v), 2) for k, v in groups.items()}

    def avg_composite_by_attack(self) -> dict:
        groups = defaultdict(list)
        for row in self.rows:
            groups[row["Attack"]].append(float(row["Final Risk"]))
        return {k: round(sum(v) / len(v), 2) for k, v in groups.items()}

    def risk_level_distribution(self) -> dict:
        """Count of HIGH / MEDIUM / LOW per attack"""
        from dread.risk import Risk
        risk_classifier = Risk()
        dist = defaultdict(lambda: defaultdict(int))
        for row in self.rows:
            level = risk_classifier.classify(float(row["Final Risk"]))
            dist[row["Attack"]][level] += 1
        return {k: dict(v) for k, v in dist.items()}

    def stride_frequency(self) -> dict:
        freq = defaultdict(int)
        for row in self.rows:
            freq[row["STRIDE"]] += 1
        return dict(freq)

    def dread_score_timeline(self) -> list:
        return [float(row["Score"]) for row in self.rows]

    def composite_risk_timeline(self) -> list:
        return [float(row["Final Risk"]) for row in self.rows]
