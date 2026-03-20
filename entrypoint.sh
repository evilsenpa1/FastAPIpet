#!/bin/sh
set -e

echo "Waiting for database..."
until alembic upgrade head; do
  echo "Migration failed, retrying in 2s..."
  sleep 2
done

echo "Starting Uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port 8000