# Використовуємо офіційний образ Python як базовий
FROM python:3.11-slim

# Встановлення системних залежностей
RUN apt-get update && \
    apt-get install -y \
    ffmpeg \
    libgl1 \
    libsm6 \
    libxext6 --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*
# Встановлюємо робочу директорію в контейнері
WORKDIR /usr/src/app

# Копіюємо файл вимог та встановлюємо залежності
# Це робиться на окремому кроці, щоб кешувати встановлення залежностей
# якщо зміни в коді програми не торкаються requirements.txt
COPY requirements.txt ./
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код програми в контейнер
COPY . .

# Визначаємо порт, на якому працюватиме додаток (Flask зазвичай використовує 5000)
EXPOSE 5000

# Визначаємо команду для запуску додатку
# Примітка: для промислового використання варто використовувати WSGI-сервер
# наприклад, Gunicorn або uWSGI, а не вбудований dev-сервер Flask.
# Для прикладу тут використовується вбудований сервер.
# Замініть 'app.py' на назву вашого основного файлу додатку,
# а 'app' на назву вашого Flask-об'єкта, якщо вони інші.
# Встановлюємо змінні середовища для запуску Flask
ENV FLASK_APP=app_srvc.webapp
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["python", "-m", "flask", "run"]

# Альтернативний CMD для Gunicorn (більш підходящий для production):
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
# де 'app:app' - це файл:об'єкт Flask