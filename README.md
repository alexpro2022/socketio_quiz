# socketio_quiz


[![Test Suite](https://github.com/alexpro2022/socketio_quiz/actions/workflows/branch_test.yml/badge.svg)](https://github.com/alexpro2022/socketio_quiz/actions/workflows/branch_test.yml)

Викторина для 2 игроков

<br>

## Оглавление
- [Технологии](#технологии)
- [Описание работы](#описание-работы)
- [Установка приложения](#установка-приложения)
- [Запуск тестов](#запуск-тестов)
- [Запуск приложения](#запуск-приложения)
- [Удаление приложения](#удаление-приложения)
- [Автор](#автор)

<br>


## Технологии
<details><summary>Подробнее</summary><br>

[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue?logo=python)](https://www.python.org/)
[![python-socketio](https://img.shields.io/badge/-python--socketio-464646?logo=socketio)](https://python-socketio.readthedocs.io/en/latest/index.html)
[![Pydantic](https://img.shields.io/badge/pydantic-2.10-blue?logo=Pydantic)](https://docs.pydantic.dev/)
[![aiohttp](https://img.shields.io/badge/-aiohttp-464646?logo=aiohttp)](https://docs.aiohttp.org/en/stable/index.html)
[![Uvicorn](https://img.shields.io/badge/-Uvicorn-464646?logo=uvicorn)](https://www.uvicorn.org/)
[![GitHub_Actions](https://img.shields.io/badge/-GitHub_Actions-464646?logo=GitHub)](https://docs.github.com/en/actions)
[![Pytest](https://img.shields.io/badge/-Pytest-464646?logo=Pytest)](https://docs.pytest.org/en/latest/)
[![pytest-asyncio](https://img.shields.io/badge/-Pytest--asyncio-464646?logo=Pytest-asyncio)](https://pypi.org/project/pytest-asyncio/)
[![pytest-cov](https://img.shields.io/badge/-pytest--cov-464646?logo=pytest-cov)](https://pytest-cov.readthedocs.io/en/latest/)
[![pre-commit](https://img.shields.io/badge/-pre--commit-464646?logo=pre-commit)](https://pre-commit.com/)

[⬆️Оглавление](#оглавление)

</details>

<br>


## Описание работы:

1. Клиент запрашивает список тем.
2. Сервер отправляет список тем.
3. Клиент выбирает тему и вводит имя, сервер подключает его к залу ожидания в теме.
4. Когда клиент подключился к залу ожидания где никого нет, он ждет.
5. Когда два клиента подключились к залу ожидания, сервер объединяет их в комнату и начинает игру.
6. Когда клиент отвечает на вопрос, сервер  отправляет обратную связь - меняет вопрос и обновляет количество оставшихся вопросов, а также обоим клиентам обновляет набранные очки.
7. Когда вопросы закончились, сервер отправляет `over` и клиент показывает результаты игры

[⬆️Оглавление](#оглавление)

<br>


## Установка приложения:

1. Клонируйте репозиторий с GitHub и введите данные для переменных окружения (значения даны для примера, но их можно оставить):

```bash
git clone https://github.com/alexpro2022/socketio_quiz.git
cd socketio_quiz
```
<br>

2. Создайте и активируйте виртуальное окружение:
   * Если у вас Linux/macOS
   ```bash
    python -m venv venv && source venv/bin/activate
   ```
   * Если у вас Windows
   ```bash
    python -m venv venv && source venv/Scripts/activate
   ```
<br>

3. Установите в виртуальное окружение все необходимые зависимости из файла **requirements.txt**:
```bash
python -m pip install --upgrade pip && \
pip install -r requirements/dev.requirements.txt --no-cache-dir
```

[⬆️Оглавление](#оглавление)

<br>


## Запуск тестов:
Из корневой директории проекта выполните команду:
```bash
pytest
```
После прохождения тестов в консоль будет выведен отчет pytest и coverage.

[⬆️Оглавление](#оглавление)

<br>


## Запуск приложения:
Из корневой директории проекта выполните команду:
```bash
python main.py
```
Проект будет развернут по адресу http://localhost

[⬆️Оглавление](#оглавление)

<br>

## Удаление приложения:
Из корневой директории проекта выполните команду:
```bash
cd .. && rm -fr socketio_quiz
```

[⬆️Оглавление](#оглавление)

<br>

## Автор:
[Aleksei Proskuriakov](https://github.com/alexpro2022)

[⬆️В начало](#socketio_quiz)

<!--

    python -m venv venv && source venv/Scripts/activate
    python -m pip install --upgrade pip && pip install -r requirements/dev.requirements.txt


    pre-commit run --all-files


coverage run -m pytest

pytest --cov=src

-->


# Docker

## Запуск приложения:
```bash
docker build -t=quiz -f=docker/Dockerfile .
docker run --rm -d --name=quiz -p 80:80 quiz
```
Проект будет развернут по адресу http://localhost


## Удаление приложения:
```bash
docker stop quiz
docker rmi quiz
```
