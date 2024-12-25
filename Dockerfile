# Шаг 1: Используем официальный образ Python
FROM python:3.12-slim

# Шаг 2: Устанавливаем рабочий каталог в контейнере
WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir poetry==1.6.1

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# Шаг 5: Копируем весь проект в контейнер
COPY . .

# Шаг 6: Открываем порт, на котором Flask будет слушать
EXPOSE 5000

# Шаг 7: Запускаем приложение Flask
CMD ["python", "run.py"]
