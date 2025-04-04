import pytest
from ..path_parser import parse_command_line


def test_parse_command_line(monkeypatch):
    # Тестируем парсинг аргументов командной строки
    test_args = ["script.py", "log1.log", "log2.log", "--report", "handlers"]
    monkeypatch.setattr("sys.argv", test_args)

    args = parse_command_line()
    assert args["log_files"] == ["log1.log", "log2.log"]
    assert args["report"] == "handlers"

    # Тестируем обязательность --report
    with pytest.raises(SystemExit):
        test_args = ["script.py", "log1.log"]
        monkeypatch.setattr("sys.argv", test_args)
        parse_command_line()