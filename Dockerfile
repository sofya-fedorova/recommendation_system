FROM python:3.10-slim-bullseye

# Устанавливаем необходимые системные пакеты
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        musl-dev \
        postgresql-client \
        libpq-dev \
        netcat \
        vim \
        curl \
        wget \
        git \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1

# Копируем файлы проекта в контейнер
WORKDIR /app
COPY ./mysite /app/mysite
COPY ./manage.py /app/
COPY ./requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Открываем порты
EXPOSE 8000

# Команда для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]