Описание
---
Это CLI-приложение анализирует логи Django-приложения и генерирует отчёты, выводимые в консоль. На данный момент реализован отчёт о состоянии ручек API с разбиением по уровням логирования.

Пример запуска:
---
Для генерации отчёта о состоянии ручек API, можно передать пути к логам и указать тип отчёта с аргументом --report:

`python3 main.py logs/app1.log logs/app2.log logs/app3.log --report handlers`

Формат отчёта:
---
Программа обрабатывает несколько файлов логов и генерирует отчёт, который включает количество запросов для каждой ручки по каждому из уровней логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL).

Пример вывода:

``` 
Total requests: 1000

HANDLER               	DEBUG  	        INFO   	WARNING	        ERROR  	        CRITICAL  
/admin/dashboard/     	20     		72     	19     		14     		18  	 
/api/v1/auth/login/   	23     		78     	14     		15     		18  	 
/api/v1/orders/       	26     		77     	12     		19     		22  	 
/api/v1/payments/     	26     		69     	14     		18     		15  	 
/api/v1/products/     	23     		70     	11     		18     		18  	 
/api/v1/shipping/     	60     		128    	26     		32     		25  	 
                        178    		494    	96     		116    		116

```

Структура приложения:
---
Программа состоит из нескольких файлов, каждый из которых отвечает за свою часть работы:

 - main.py — главный файл, который отвечает за парсинг командной строки и запуск генерации отчётов.

 - path_parser.py — модуль для парсинга аргументов командной строки.

 - log_parser.py — модуль для анализа и обработки логов, извлекает уровни логов и обработчики.

 - reports/handlers.py — модуль для формирования отчёта о состоянии ручек API.

Технические требования:
---
- Приложение должно корректно обрабатывать несколько файлов логов.

- Приложение должно проверять наличие файлов и корректность переданного имени отчёта.

- Приложение должно генерировать отчёт в консоль и сохранять его в текстовый файл.

- Программа должна обрабатывать логи с размером до нескольких гигабайт.

- Программа использует только стандартную библиотеку Python для CLI и вывода отчётов.

- Код покрыт тестами с использованием pytest и аннотациями типов.

- Архитектура и расширяемость

Отчёты:
---
На данный момент реализован только один отчёт (как и просилось в тест.задании) — о состоянии ручек API. Архитектура приложения позволяет легко добавлять новые отчёты. Для этого достаточно создать новый модуль с логикой формирования отчёта и добавить его в основной скрипт.


Дополнительные отчёты:
- Чтобы добавить новый отчёт, необходимо создать функцию, которая будет заниматься его формированием. Все отчёты должны быть реализованы в виде функций, которые принимают список логов и возвращают строку с отчётом.


Для добавления нового отчёта нужно:
---

- Создать новый файл в папке reports, например, reports/new_report.py.

- Реализовать функцию для формирования отчёта в виде функции, принимающей список логов и возвращающей строку с результатом.

- Добавить функцию в основной скрипт для обработки командной строки, как это сделано для отчёта handlers.

Пример структуры нового отчёта:
---
```python
# reports/new_report.py

from typing import Dict

def generate_new_report(data: Dict) -> str:
    # Логика формирования отчёта
    return "New report content"

def run_new_report(log_files: list[str]) -> None:
    data = {}
    for log_file in log_files:
        # Обработка логов
        pass

    report = generate_new_report(data)
    print(report)
```

Примеры тестов:
---
Программа покрыта тестами с использованием библиотеки pytest. Тесты включают проверку корректности обработки логов, а также генерации отчётов.

Пример теста для проверки корректности обработки данных:
```python
# test_log_parser.py

from log_parser import extract_log_level_and_handler

def test_extract_log_level_and_handler():
    log_line = "INFO django.request /api/v1/auth/login/"
    result = extract_log_level_and_handler(log_line)
    assert result == ("INFO", "/api/v1/auth/login/")
```