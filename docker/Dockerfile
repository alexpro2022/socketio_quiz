FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DOCKER_BUILDKIT=1

WORKDIR /app

COPY requirements .

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 80

CMD ["uvicorn",  "src.web.app:app", "--host=0.0.0.0", "--port=80"]
