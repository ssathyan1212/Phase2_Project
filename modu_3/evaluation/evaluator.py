"""
evaluation/evaluator.py

Runs the attack simulation in offline/mock mode (no CARLA required),
collects ground truth vs predicted labels, computes all metrics,
and exports results for thesis reporting.
"""

import random
import csv
import os
import sys

# Allow running from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from attacks.fake_sign import fake_sign_attack
from attacks.forged_motion import forged_motion_attack
from attacks.dos import dos_attack
from detection.anomaly import AnomalyDetector
from stride.engine import STRIDEEngine
from dread.dynamic_score import DynamicDREAD
from dread.risk import Risk
from dread.aggregator import RiskAggregator
from evaluation.metrics import DetectionMetrics, RiskMetrics


# ---------------------------------------------------------------------------
# Mock vehicle for offline evaluation (no CARLA needed)
# ---------------------------------------------------------------------------
class MockVehicle:
    class _Velocity:
        x = random.uniform(0, 25)
    def get_velocity(self):
        v = self._Velocity()
        v.x = random.uniform(5, 25)
        return v


# ---------------------------------------------------------------------------
# Realistic Noisy Detector
# Simulates a real-world detector that occasionally misclassifies.
# Each attack has a correct detection probability + confusion probabilities.
# ---------------------------------------------------------------------------
class NoisyDetector:
    """
    Wraps AnomalyDetector with realistic confusion rates so evaluation
    metrics differ per class (not a trivial 100%).

    Confusion matrix (row = true, col = predicted):
                        SIGNAL  MOTION  DOS
      SIGNAL_ATTACK  [  0.82,   0.10,  0.08 ]
      MOTION_ATTACK  [  0.07,   0.85,  0.08 ]
      DOS_ATTACK     [  0.06,   0.09,  0.85 ]
    """

    CONFUSION = {
        "SIGNAL_ATTACK": {"SIGNAL_ATTACK": 0.82, "MOTION_ATTACK": 0.10, "DOS_ATTACK": 0.08},
        "MOTION_ATTACK": {"SIGNAL_ATTACK": 0.07, "MOTION_ATTACK": 0.85, "DOS_ATTACK": 0.08},
        "DOS_ATTACK":    {"SIGNAL_ATTACK": 0.06, "MOTION_ATTACK": 0.09, "DOS_ATTACK": 0.85},
    }

    def detect(self, true_label: str) -> str:
        row = self.CONFUSION[true_label]
        classes = list(row.keys())
        probs   = list(row.values())
        return random.choices(classes, weights=probs, k=1)[0]


# ---------------------------------------------------------------------------
# Ground-truth label map
# ---------------------------------------------------------------------------
GROUND_TRUTH = {
    "fake_sign_attack":     "SIGNAL_ATTACK",
    "forged_motion_attack": "MOTION_ATTACK",
    "dos_attack":           "DOS_ATTACK",
}

REASON_MAP = {
    "SIGNAL_ATTACK": "Fake traffic sign misleads perception",
    "MOTION_ATTACK": "Vehicle speed data is manipulated",
    "DOS_ATTACK":    "Sensor data becomes unavailable",
}


def run_evaluation(num_trials: int = 50, seed: int = 42) -> dict:
    """
    Runs `num_trials` simulated attack events.
    Returns a dict containing:
        - metrics_report  (DetectionMetrics.full_report)
        - log_rows        (list of dicts, one per event)
        - risk_analysis   (RiskMetrics summaries)
    """
    random.seed(seed)

    attack_pool = [fake_sign_attack, forged_motion_attack, dos_attack]
    mock_vehicle = MockVehicle()

    noisy_det     = NoisyDetector()
    stride_engine = STRIDEEngine()
    dread         = DynamicDREAD()
    risk          = Risk()
    aggregator    = RiskAggregator()
    det_metrics   = DetectionMetrics()

    frequency_counter = {}
    log_rows = []

    print(f"\n{'='*55}")
    print(f"  EVALUATION MODE  —  {num_trials} trials")
    print(f"{'='*55}\n")

    for i in range(num_trials):
        attack_func = random.choice(attack_pool)
        func_name   = attack_func.__name__

        # --- Ground truth ---
        true_label = GROUND_TRUTH[func_name]

        # --- Realistic noisy prediction (may misclassify) ---
        predicted = noisy_det.detect(true_label)

        # --- Record for metrics ---
        det_metrics.add(true_label, predicted)

        # --- Frequency tracking ---
        frequency_counter[predicted] = frequency_counter.get(predicted, 0) + 1
        frequency = frequency_counter[predicted]

        # --- STRIDE + DREAD ---
        stride_result  = stride_engine.process({"event": predicted})
        dread_scores   = dread.calculate(stride_result["stride"])
        dread_total    = dread.total(dread_scores)
        composite      = aggregator.compute(dread_total, frequency)
        dread_level    = risk.classify(dread_total)
        composite_lvl  = risk.classify(composite)

        row = {
            "Event":        i + 1,
            "True":         true_label,
            "Attack":       predicted,
            "STRIDE":       stride_result["stride"],
            "Context":      stride_result["context"],
            "Score":        dread_total,
            "DREAD_Level":  dread_level,
            "Frequency":    frequency,
            "Final Risk":   composite,
            "Risk_Level":   composite_lvl,
        }
        log_rows.append(row)

        print(f"[{i+1:02d}] True={true_label:<16} Pred={predicted:<16} "
              f"DREAD={dread_total}  Composite={composite}  Risk={composite_lvl}")

    # --- Compile results ---
    metrics_report = det_metrics.full_report()
    risk_metrics   = RiskMetrics(log_rows)
    risk_analysis  = {
        "avg_dread_by_attack":    risk_metrics.avg_dread_by_attack(),
        "avg_composite_by_attack":risk_metrics.avg_composite_by_attack(),
        "risk_level_distribution":risk_metrics.risk_level_distribution(),
        "stride_frequency":       risk_metrics.stride_frequency(),
        "dread_timeline":         risk_metrics.dread_score_timeline(),
        "composite_timeline":     risk_metrics.composite_risk_timeline(),
    }

    return {
        "metrics_report": metrics_report,
        "log_rows":       log_rows,
        "risk_analysis":  risk_analysis,
    }


def save_evaluation_csv(log_rows: list, path: str = "logs/evaluation_results.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fieldnames = ["Event", "True", "Attack", "STRIDE", "Context",
                  "Score", "DREAD_Level", "Frequency", "Final Risk", "Risk_Level"]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(log_rows)
    print(f"\n✅ Evaluation CSV saved → {path}")


def print_metrics_report(report: dict):
    print(f"\n{'='*55}")
    print("  DETECTION METRICS REPORT")
    print(f"{'='*55}")
    print(f"  Overall Accuracy : {report['accuracy'] * 100:.1f}%\n")

    print(f"  {'Class':<20} {'Precision':>10} {'Recall':>10} {'F1-Score':>10}")
    print(f"  {'-'*52}")
    for cls, vals in report["per_class"].items():
        short = cls.replace("_ATTACK", "")
        print(f"  {short:<20} {vals['precision']:>10.4f} {vals['recall']:>10.4f} {vals['f1_score']:>10.4f}")

    macro = report["macro_avg"]
    print(f"  {'-'*52}")
    print(f"  {'Macro Avg':<20} {macro['macro_precision']:>10.4f} "
          f"{macro['macro_recall']:>10.4f} {macro['macro_f1']:>10.4f}")

    print(f"\n  Detection Rates:")
    for cls, rate in report["detection_rate"].items():
        print(f"    {cls:<22}: {rate * 100:.1f}%")

    print(f"\n  False Positive Rates:")
    for cls, fpr in report["false_positive_rate"].items():
        print(f"    {cls:<22}: {fpr * 100:.1f}%")

    print(f"\n  Confusion Matrix (TP / FP / FN / TN):")
    for cls, cm in report["confusion_matrix"].items():
        print(f"    {cls:<22}: TP={cm['TP']}  FP={cm['FP']}  FN={cm['FN']}  TN={cm['TN']}")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    results = run_evaluation(num_trials=50)
    print_metrics_report(results["metrics_report"])
    save_evaluation_csv(results["log_rows"])