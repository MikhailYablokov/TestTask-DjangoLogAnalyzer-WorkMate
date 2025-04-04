import argparse
import os
from typing import List
from log_parser import parse_logs
from reports import generate_handlers_report

def main():
    parser = argparse.ArgumentParser(description="Django log analyzer")
    parser.add_argument("log_files", nargs="+", help="Paths to log files")
    parser.add_argument("--report", required=True, help="Report type (e.g., handlers)")
    args = parser.parse_args()

    # Проверка существования файлов
    for log_file in args.log_files:
        if not os.path.exists(log_file):
            print(f"Error: File {log_file} does not exist")
            return

    # Проверка типа отчета
    # Если я правильно понял, то в теории есть несколько видов отчетов,
    # если же --report это просто название для файла то это нужно убрать).
    if args.report != "handlers":
        print(f"Error: Unknown report type '{args.report}'. Supported: 'handlers'")
        return

    # Парсинг логов
    data = {}
    for log_file in args.log_files:
        parse_logs(log_file, data)

    report = generate_handlers_report(data)
    # Генерация отчета
    print(report)
    with open(f"reports/{args.report}.txt", "w") as report_file:
        report_file.write(report)

if __name__ == "__main__":
    main()