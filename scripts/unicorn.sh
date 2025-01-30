#!/bin/sh

# применяем миграции
alembic -c ./app/alembic.ini upgrade head

# запускаем uvicorn
uvicorn app:app --app-dir ./app --host 0.0.0.0 --workers 1 --port 8000 --reload
