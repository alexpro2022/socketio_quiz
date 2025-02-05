# socketio_quiz


[![Test Suite](https://github.com/alexpro2022/socketio_quiz/actions/workflows/branch_test.yml/badge.svg)](https://github.com/alexpro2022/socketio_quiz/actions/workflows/branch_test.yml)



    python -m venv venv && source venv/Scripts/activate
    python -m pip install --upgrade pip && pip install -r requirements/dev.requirements.txt


    pre-commit run --all-files


docker build -t quiz .

docker build -t quiz ./docker
docker exec -it upbeat_ramanujan bash

docker run --name quiz_cont -it -p 8000:8000 quiz

1. Запуск приложения - из корневой директории проекта выполните команду:
```bash
docker compose -f infra/local/docker-compose.yml up -d --build
```
Проект будет развернут в docker-контейнерах по адресу http://localhost  http://127.0.0.1:8000

Администрирование приложения может быть осуществлено:
  - через админ панель по адресу: http://localhost/admin
  - через Swagger доступный по адресу: http://localhost/docs

2. Остановить docker и удалить контейнеры можно командой из корневой директории проекта:
```bash
docker compose -f infra/local/docker-compose.yml down
```
Если также необходимо удалить том базы данных:
```bash
docker compose -f infra/local/docker-compose.yml down -v && docker system prune -f
```
