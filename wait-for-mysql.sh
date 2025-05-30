#!/bin/sh

echo "Waiting for MySQL to be ready..."

while ! nc -z db 3306; do
  sleep 1
done

echo "MySQL is up — starting app."

python app.py
