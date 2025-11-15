#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "PostgreSQL is ready!"

# Run migrations
echo "Running migrations..."
python temizxali/manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python temizxali/manage.py collectstatic --noinput

# Execute the command passed to the container
exec "$@"

