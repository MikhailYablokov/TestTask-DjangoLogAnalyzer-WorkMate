import os
from path_parser import parse_command_line
import reports

def main():
    #Парсинг коммандной строки
    args = parse_command_line()

    # Проверка наличия необходимых аргументов
    report_name = args["report"]
    report_func = getattr(reports, f"run_{report_name}", None)

    if not callable(report_func):
        print(f"Error: Unknown report type '{report_name}'")
        return

    try:
        report_func(args["log_files"])
    except Exception as e:
        print(f"Error during report generation: {e}")

if __name__ == "__main__":
    main()
