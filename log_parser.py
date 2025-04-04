#log_parser
import re
from typing import Dict

LOG_PATTERN = re.compile(r"(DEBUG|INFO|WARNING|ERROR|CRITICAL) django.request.*?(?:/[^/\s][^\s]*)")
PATH_PATTERN = re.compile(r"/[^/\s][^\s]*")

def extract_log_level_and_handler(line: str) -> tuple[str, str] | None:
    match = LOG_PATTERN.search(line)
    if not match:
        return None

    level = match.group(1)
    path_match = PATH_PATTERN.search(line)
    if not path_match:
        return None

    handler = path_match.group(0)
    return level, handler

def parse_logs(file_path: str, data: Dict[str, Dict[str, int]]) -> None:
    with open(file_path, "r") as f:
        for line in f:
            result = extract_log_level_and_handler(line)
            if result:
                level, handler = result
                if handler not in data:
                    data[handler] = {lvl: 0 for lvl in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]}
                data[handler][level] += 1
