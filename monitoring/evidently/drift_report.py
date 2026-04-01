from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import pandas as pd
import os


def run_drift(current_path, reference_path):
    current = pd.read_csv(current_path)
    reference = pd.read_csv(reference_path)

    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference, current_data=current)

    os.makedirs("monitoring/evidently/reports", exist_ok=True)

    report.save_html("monitoring/evidently/reports/drift.html")

    print("✅ Drift report generated")