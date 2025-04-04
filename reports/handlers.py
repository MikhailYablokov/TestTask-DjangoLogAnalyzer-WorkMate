#reports/handlers.py
import os
from typing import Dict

from log_parser import parse_logs

# Папка с нашим скриптом
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# Папка для отчётов на уровень выше
REPORTS_DIR = os.path.join(os.path.dirname(PROJECT_ROOT), "logs")

# Уровни логов
LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

def calculate_totals(data: Dict[str, Dict[str, int]]) -> Dict[str, int]:
    """
    Считаем, сколько всего логов каждого уровня получилось по всем ручкам.
    """
    totals = {level: 0 for level in LEVELS}
    for counts in data.values():
        for level in LEVELS:
            totals[level] += counts.get(level, 0)  # Если уровня нет, считаем 0
    return totals

def format_report(data: Dict[str, Dict[str, int]], totals: Dict[str, int], total_requests: int) -> str:
    """
    Собираем красивый текстовый отчёт: шапка, строки с ручками, итоговая строка.
    Всё выравниваем, чтобы было аккуратно в консоли.
    """
    lines = []
    lines.append(f"Total requests: {total_requests}\n")  # Пишем общее число запросов
    # Шапка с названиями уровней
    lines.append(f"{'HANDLER':<26} " + " ".join(f"{level:<14}" for level in LEVELS))

    # Проходим по ручкам в алфавитном порядке
    for handler in sorted(data.keys()):
        row = f"{handler:<27}" + "".join(f"{data[handler].get(level, 0):<15}" for level in LEVELS)
        lines.append(row)

    # Итоговая строка с суммами по уровням
    total_row = f"{'':<27}" + "".join(f"{totals[level]:<15}" for level in LEVELS)
    lines.append(total_row)

    return "\n".join(lines)

def generate_handlers_report(data: Dict[str, Dict[str, int]]) -> str:
    """
    Главная функция для отчёта handlers: считает общее число запросов,
    вызывает подсчёт сумм и форматирует результат.
    """
    total_requests = sum(sum(counts.values()) for counts in data.values())  # Суммируем все логи
    totals = calculate_totals(data)
    return format_report(data, totals, total_requests)

def run_handlers(log_files: list[str]) -> None:
    """
    Запускаем обработку логов и генерацию отчёта:
    - Проверяем, что файлы есть
    - Парсим их
    - Пишем отчёт в файл и в консоль
    """
    data: Dict[str, Dict[str, int]] = {}

    # Обрабатываем каждый файл по очереди
    for log_file in log_files:
        if not os.path.exists(log_file):
            raise FileNotFoundError(f"File {log_file} does not exist")
        parse_logs(log_file, data)

    report = generate_handlers_report(data)

    # Создаём папку для отчётов, если её нет
    os.makedirs(REPORTS_DIR, exist_ok=True)
    output_path = os.path.join(REPORTS_DIR, "handlers.txt")
    with open(output_path, "w") as f:
        f.write(report)

    print(f"Report saved to {output_path}")
    print(report)