import pytest
import sys
import os

# Добавляем корневую директорию в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from log_parser import parse_logs

def test_parse_logs_extended(tmp_path):
    # Создаем тестовый файл логов с разными случаями
    log_file = tmp_path / "test.log"
    log_file.write_text(
        # Успешные запросы с INFO и DEBUG
        "2025-03-27 12:36:45,000 INFO django.request: GET /api/v1/checkout/ 201 OK [192.168.1.62]\n"
        "2025-03-27 12:36:46,000 DEBUG django.request: GET /api/v1/checkout/ 200 OK [192.168.1.63]\n"
        # Ошибки с ERROR и CRITICAL
        "2025-03-27 12:33:05,000 ERROR django.request: Internal Server Error: /api/v1/users/ [192.168.1.39] - PermissionDenied\n"
        "2025-03-27 12:33:06,000 CRITICAL django.request: Internal Server Error: /api/v1/users/ [192.168.1.40] - Crash\n"
        # WARNING с ручкой
        "2025-03-27 12:34:00,000 WARNING django.request: GET /api/v1/orders/ 400 Bad Request [192.168.1.50]\n"
        # Строка без ручки (должна игнорироваться)
        "2025-03-27 12:35:00,000 WARNING django.security: PermissionDenied: User does not have permission\n"
        # Строка с другой ручкой и несколькими уровнями
        "2025-03-27 12:37:00,000 INFO django.request: GET /api/v1/orders/ 204 OK [192.168.1.51]\n"
        "2025-03-27 12:37:01,000 ERROR django.request: Internal Server Error: /api/v1/orders/ [192.168.1.52] - Timeout\n"
        # Строка без django.request (должна игнорироваться)
        "2025-03-27 12:38:00,000 DEBUG django.db.backends: (0.2) SELECT * FROM 'users' WHERE id = 1;\n"
    )

    # Выполняем парсинг
    data = {}
    parse_logs(str(log_file), data)

    # Ожидаемый результат
    expected = {
        "/api/v1/checkout/": {
            "DEBUG": 1,  # Один DEBUG-запрос
            "INFO": 1,   # Один INFO-запрос
            "WARNING": 0,
            "ERROR": 0,
            "CRITICAL": 0
        },
        "/api/v1/users/": {
            "DEBUG": 0,
            "INFO": 0,
            "WARNING": 0,
            "ERROR": 1,   # Один ERROR
            "CRITICAL": 1 # Один CRITICAL
        },
        "/api/v1/orders/": {
            "DEBUG": 0,
            "INFO": 1,    # Один INFO
            "WARNING": 1, # Один WARNING
            "ERROR": 1,   # Один ERROR
            "CRITICAL": 0
        }
    }

    # Проверяем результат
    assert data == expected, f"Expected {expected}, but got {data}"

def test_parse_logs_empty_file(tmp_path):
    # Тест для пустого файла
    log_file = tmp_path / "empty.log"
    log_file.write_text("")
    data = {}
    parse_logs(str(log_file), data)
    assert data == {}, "Empty file should result in empty data"

def test_parse_logs_no_handlers(tmp_path):
    # Тест для файла без ручек
    log_file = tmp_path / "no_handlers.log"
    log_file.write_text(
        "2025-03-27 12:00:00,000 INFO django.security: Some security event\n"
        "2025-03-27 12:01:00,000 DEBUG django.db.backends: (0.1) SELECT * FROM 'table';\n"
    )
    data = {}
    parse_logs(str(log_file), data)
    assert data == {}, "File without handlers should result in empty data"