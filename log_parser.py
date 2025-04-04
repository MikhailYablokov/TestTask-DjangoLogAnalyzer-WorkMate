from typing import Dict
import re

def parse_logs(file_path: str, data: Dict[str, Dict[str, int]]) -> None:
    log_pattern = re.compile(r"(DEBUG|INFO|WARNING|ERROR|CRITICAL) django.request.*?(?:/[^/\s][^\s]*)")
    with open(file_path, "r") as f:
        for line in f:
            match = log_pattern.search(line)
            if match:
                level = match.group(1)
                # Извлекаем ручку из всей строки
                path_pattern = re.compile(r"/[^/\s][^\s]*")
                path_match = path_pattern.search(line)
                if path_match:
                    handler = path_match.group(0)
                    if handler not in data:
                        data[handler] = {"DEBUG": 0, "INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}
                    data[handler][level] += 1