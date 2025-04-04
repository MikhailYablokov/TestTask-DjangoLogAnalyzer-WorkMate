import os
from typing import Dict
from log_parser import parse_logs

def generate_handlers_report(data: Dict[str, Dict[str, int]]) -> str:
    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    total_requests = sum(sum(counts.values()) for counts in data.values())

    report = []
    report.append(f"Total requests: {total_requests}\n")
    report.append(f"{'HANDLER':<26} {'DEBUG':<14} {'INFO':<14} {'WARNING':<14} {'ERROR':<14} {'CRITICAL':<14}")

    totals = {level: 0 for level in levels}
    for handler in sorted(data.keys()):
        counts = data[handler]
        row = f"{handler:<27}"
        for level in levels:
            count = counts.get(level, 0)
            row += f"{count:<15}"
            totals[level] += count
        report.append(row)

    total_row = f"{'':<27}"
    for level in levels:
        total_row += f"{totals[level]:<15}"
    report.append(total_row)

    return "\n".join(report)


def run_handlers(log_files: list[str]):
    data = {}

    for log_file in log_files:
        if not os.path.exists(log_file):
            raise FileNotFoundError(f"File {log_file} does not exist")
        parse_logs(log_file, data)

    report = generate_handlers_report(data)
    os.makedirs("reports", exist_ok=True)
    with open("handlers.txt", "w") as f:
        f.write(report)

    print("Report saved to reports/handlers.txt")
