import argparse


def parse_command_line() -> dict:
    parser = argparse.ArgumentParser(description="Django log analyzer")
    parser.add_argument("log_files", nargs="+", help="Paths to log files")
    parser.add_argument("--report", required=True, help="Report type (e.g., handlers)")
    args = parser.parse_args()

    # Преобразуем Namespace в dict
    return vars(args)


# Пример использования
if __name__ == "__main__":
    args = parse_command_line()
    print(args)
