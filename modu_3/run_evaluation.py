"""
run_evaluation.py
=================
Master script — run this from the MODU_3 project root:

    python run_evaluation.py

What it does:
  1. Runs 50-trial offline simulation (no CARLA needed)
  2. Computes detection metrics (Precision, Recall, F1, Accuracy)
  3. Generates 8 thesis-quality matplotlib figures → evaluation/figures/
  4. Saves evaluation CSV → logs/evaluation_results.csv
"""

import sys
import os

# Make sure project root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from evaluation.evaluator import run_evaluation, print_metrics_report, save_evaluation_csv
from evaluation.report_generator import generate_all_figures


def main():
    print("\n" + "█" * 55)
    print("  AV CYBERSECURITY — THESIS EVALUATION PIPELINE")
    print("█" * 55)

    # ── Step 1: Run evaluation ──────────────────────────────────────────────
    results = run_evaluation(num_trials=50, seed=42)

    # ── Step 2: Print metrics to console ───────────────────────────────────
    print_metrics_report(results["metrics_report"])

    # ── Step 3: Print risk analysis summary ────────────────────────────────
    ra = results["risk_analysis"]
    print("  RISK ANALYSIS SUMMARY")
    print(f"  {'='*50}")
    print("  Average DREAD Score by Attack:")
    for k, v in ra["avg_dread_by_attack"].items():
        print(f"    {k:<22}: {v}")
    print("\n  Average Composite Risk by Attack:")
    for k, v in ra["avg_composite_by_attack"].items():
        print(f"    {k:<22}: {v}")
    print("\n  STRIDE Frequency:")
    for k, v in ra["stride_frequency"].items():
        print(f"    {k:<25}: {v} events")
    print(f"  {'='*50}\n")

    # ── Step 4: Save CSV ───────────────────────────────────────────────────
    save_evaluation_csv(results["log_rows"])

    # ── Step 5: Generate figures ───────────────────────────────────────────
    generate_all_figures(results["metrics_report"], results["risk_analysis"])

    print("█" * 55)
    print("  EVALUATION COMPLETE")
    print("  Figures : evaluation/figures/")
    print("  CSV     : logs/evaluation_results.csv")
    print("█" * 55 + "\n")


if __name__ == "__main__":
    main()