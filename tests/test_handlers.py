from pathlib import Path

import pytest
import os
from ..reports.handlers import calculate_totals, format_report, generate_handlers_report, run_handlers


@pytest.fixture
def sample_data():
    # Пример данных логов, используется в нескольких тестах
    return {
        "/api/users": {"DEBUG": 5, "INFO": 3, "ERROR": 1},
        "/api/posts": {"INFO": 2, "WARNING": 4}
    }


def test_calculate_totals():
    # Тестирует суммирование логов по уровням (DEBUG, INFO, ...)
    data = {
        "/api/users": {"DEBUG": 5, "INFO": 3},
        "/api/posts": {"INFO": 2, "ERROR": 1}
    }
    result = calculate_totals(data)
    expected = {
        "DEBUG": 5,
        "INFO": 5,
        "WARNING": 0,
        "ERROR": 1,
        "CRITICAL": 0
    }
    assert result == expected


def test_format_report(sample_data):
    # Проверяет, что текст отчёта содержит нужные элементы (пути, суммы, уровни)
    totals = calculate_totals(sample_data)
    report = format_report(sample_data, totals, 15)
    assert "Total requests: 15" in report
    assert "/api/posts" in report
    assert "/api/users" in report
    assert str(totals["DEBUG"]) in report


def test_generate_handlers_report(sample_data):
    # Проверяет корректность итогового отчёта для "handlers"
    report = generate_handlers_report(sample_data)
    assert "Total requests: 15" in report
    assert "HANDLER" in report
    assert "DEBUG" in report


def test_run_handlers(tmp_path):
    # Создаёт временный лог-файл
    # Проверяет FileNotFoundError при несуществующем файле
    # Проверяет успешную генерацию отчёта по существующему лог-файлу
    log_file = tmp_path / "test.log"
    log_file.write_text(
        "DEBUG django.request /api/users\n"
        "INFO django.request /api/users\n"
    )

    output_file = Path("logs/handlers.txt")
    assert output_file.exists()

    with pytest.raises(FileNotFoundError):
        run_handlers([str(tmp_path / "nonexistent.log")])

    run_handlers([str(log_file)])
    assert output_file.exists()
    content = output_file.read_text()
    assert "Total requests: 2" in content
    assert "/api/users" in content