# Use an official Python runtime as a parent image
FROM python:3.9

# Установите рабочую директорию в контейнере
WORKDIR /app

# Скопируйте файл зависимостей в рабочую директорию
COPY requirements.txt .

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Add the current directory files (on your machine) to the container
COPY . .

# Expose the port server is running on
EXPOSE 8000

# Start the server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "olim.wsgi:application"]