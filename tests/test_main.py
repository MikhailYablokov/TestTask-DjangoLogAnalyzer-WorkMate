import pytest
import sys
from main import main

def test_main(monkeypatch, capsys):
    # Подмена аргументов командной строки
    test_args = ["script.py", "logs/app1.log", "--report", "handlers"]
    monkeypatch.setattr(sys, "argv", test_args)

    # Подмена парсинга аргументов
    monkeypatch.setattr("main.parse_command_line", lambda: {
        "log_files": ["logs/app1.log"],
        "report": "handlers"
    })

    # Подмена функции в reports
    import reports
    monkeypatch.setattr(reports, "run_handlers", lambda logs: print("Report generated"))

    main()
    captured = capsys.readouterr()
    assert "Report generated" in captured.out

    # Проверка неизвестного типа отчета
    monkeypatch.setattr(sys, "argv", ["script.py", "logs/app1.log", "--report", "unknown"])
    monkeypatch.setattr("main.parse_command_line", lambda: {
        "log_files": ["logs/app1.log"],
        "report": "unknown"
    })

    main()
    captured = capsys.readouterr()
    assert "Error: Unknown report type 'unknown'" in captured.out
