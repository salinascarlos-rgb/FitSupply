#!/usr/bin/env bash
# Este script se ejecuta automáticamente en Render después de cada deploy

echo "🔹 Ejecutando migraciones..."
python manage.py migrate --noinput

echo "🔹 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "✅ Migraciones y staticfiles completados correctamente."
