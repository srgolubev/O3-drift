FROM python:3.12-slim-bullseye

# Отключаем запись pyc файлов и буферизацию вывода
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Задаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем пакеты
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/

# Открываем порт 8000
EXPOSE 8000

# Команда для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
