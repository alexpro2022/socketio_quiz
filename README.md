# socketio_quiz


[![Test Suite](https://github.com/alexpro2022/socketio_quiz/actions/workflows/branch_test.yml/badge.svg)](https://github.com/alexpro2022/socketio_quiz/actions/workflows/branch_test.yml)
[![CI/CD](https://github.com/alexpro2022/socketio_quiz/actions/workflows/ci_cd.yml/badge.svg)](https://github.com/alexpro2022/socketio_quiz/actions/workflows/ci_cd.yml)

Викторина для 2 игроков.<br>
Проект доступен по [185.221.162.231](http://185.221.162.231/)

<br>


## Оглавление
- [Технологии](#технологии)
- [Описание работы](#описание-работы)
- [Установка приложения](#установка-приложения)
- [Docker](#docker)
- [Виртуальное окружение](#виртуальное-окружение)
- [Удаление приложения](#удаление-приложения)
- [Автор](#автор)

<br>


## Технологии
<details><summary>Подробнее</summary><br>

[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue?logo=python)](https://www.python.org/)
[![python-socketio](https://img.shields.io/badge/-python--socketio-464646?logo=socketio)](https://python-socketio.readthedocs.io/en/latest/index.html)
[![Pydantic](https://img.shields.io/badge/pydantic-2.10-blue?logo=Pydantic)](https://docs.pydantic.dev/)
[![Uvicorn](https://img.shields.io/badge/-Uvicorn-464646?logo=uvicorn)](https://www.uvicorn.org/)
[![aiohttp](https://img.shields.io/badge/-aiohttp-464646?logo=aiohttp)](https://docs.aiohttp.org/en/stable/index.html)
[![Pytest](https://img.shields.io/badge/-Pytest-464646?logo=Pytest)](https://docs.pytest.org/en/latest/)
[![pytest-asyncio](https://img.shields.io/badge/-Pytest--asyncio-464646?logo=Pytest-asyncio)](https://pypi.org/project/pytest-asyncio/)
[![pytest-cov](https://img.shields.io/badge/-pytest--cov-464646?logo=pytest-cov)](https://pytest-cov.readthedocs.io/en/latest/)
[![Coverage](https://img.shields.io/badge/-Coverage-464646?logo=coverage)](https://coverage.readthedocs.io/en/latest/)
[![pre-commit](https://img.shields.io/badge/-pre--commit-464646?logo=pre-commit)](https://pre-commit.com/)
[![docker](https://img.shields.io/badge/-Docker-464646?logo=docker)](https://www.docker.com/)
[![GitHub_Actions](https://img.shields.io/badge/-GitHub_Actions-464646?logo=GitHub)](https://docs.github.com/en/actions)

[⬆️Оглавление](#оглавление)
<h1></h1>
</details>
<br>


## Описание работы:
  На данный момент только одна опция с реальными данными - `Персоны`.
1. Клиент запрашивает список тем.
2. Сервер отправляет список тем.
3. Клиент выбирает тему и вводит имя, сервер подключает его к залу ожидания в выбранной теме.
4. Когда клиент подключился к залу ожидания где никого нет, он ждет.
5. Когда два клиента подключились к залу ожидания, сервер объединяет их в комнату и начинает игру.
6. Когда клиент отвечает на вопрос, сервер  отправляет обратную связь - меняет вопрос и обновляет количество оставшихся вопросов, а также обоим клиентам обновляет набранные очки.
7. Когда вопросы закончились, сервер отправляет `over` и заканчивает игру.
8. Клиент показывает результаты игры (**TODO**).
9. Подготовка днных для игры (**TODO**).

[⬆️Оглавление](#оглавление)

<br>


## Установка приложения:

Клонируйте репозиторий с GitHub:
```bash
git clone https://github.com/alexpro2022/socketio_quiz.git
cd socketio_quiz
```
Все последующие команды производятся из корневой директории проекта `socketio_quiz`:

[⬆️Оглавление](#оглавление)

<br>


## Docker:
<details><summary>Запуск приложения</summary><br>

1. Создание образа:
```bash
docker build -t=quiz -f=docker/Dockerfile .
```
<br>

2. Запуск приложения - проект будет развернут по адресу http://localhost:
```bash
docker run --rm -d --name=quiz -p 80:80 quiz
```
<br>

3. Остановка приложение:
```bash
docker stop quiz
```
<br>

4. Удаление образа:
```bash
docker rmi quiz
```

[⬆️Оглавление](#оглавление)
<h1></h1>
</details>
<br>


## Виртуальное окружение:
<details><summary>Запуск тестов и приложения для разработки</summary><br>

1. Создайте и активируйте виртуальное окружение:
   * Если у вас Linux/macOS
   ```bash
    python -m venv venv && source venv/bin/activate
   ```
   * Если у вас Windows
   ```bash
    python -m venv venv && source venv/Scripts/activate
   ```
<br>

2. Установите в виртуальное окружение все необходимые зависимости из файла **requirements.txt**:
```bash
python -m pip install --upgrade pip && \
pip install -r requirements/dev.requirements.txt --no-cache-dir
```
<br>

3. Запуск тестов - после прохождения тестов в консоль будет выведен отчет `pytest` и `coverage`(**96%**).:
```bash
pytest
```

<br>

4. Запуск приложения - проект будет развернут по адресу http://localhost
```bash
python main.py
```

[⬆️Оглавление](#оглавление)
<h1></h1>
</details>
<br>


## Удаление приложения:
```bash
cd .. && rm -fr socketio_quiz
```

[⬆️Оглавление](#оглавление)

<br>


## Автор:
[Aleksei Proskuriakov](https://github.com/alexpro2022)

[⬆️В начало](#socketio_quiz)
