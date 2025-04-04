import pytest
from ..log_parser import extract_log_level_and_handler, parse_logs


def test_extract_log_level_and_handler():
    # Проверяет извлечение уровня лога и пути из строки
    # Также проверяет обработку невалидных строк
    line = "DEBUG django.request /api/users some text"
    result = extract_log_level_and_handler(line)
    assert result == ("DEBUG", "/api/users")

    invalid_line = "DEBUG some.random.text"
    assert extract_log_level_and_handler(invalid_line) is None

    no_path = "INFO django.request some text"
    assert extract_log_level_and_handler(no_path) is None


def test_parse_logs(tmp_path):
    # Проверяет корректность парсинга лог-файла и наполнение структуры data
    # Убеждается, что невалидные строки игнорируются
    log_file = tmp_path / "test.log"
    log_file.write_text(
        "DEBUG django.request /api/users\n"
        "INFO django.request /api/users\n"
        "ERROR django.request /api/posts\n"
        "RANDOM text\n"
    )

    data = {}
    parse_logs(str(log_file), data)

    assert "/api/users" in data
    assert data["/api/users"]["DEBUG"] == 1
    assert data["/api/users"]["INFO"] == 1
    assert data["/api/posts"]["ERROR"] == 1
    assert "RANDOM" not in data