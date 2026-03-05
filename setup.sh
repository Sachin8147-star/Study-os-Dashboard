#!/bin/bash
# StudyOS — Quick Setup Script
# Run this once to get started

echo "🚀 Setting up StudyOS..."

# Install Django
pip install -r requirements.txt

echo "📦 Running migrations..."
python manage.py makemigrations api
python manage.py migrate

echo "👤 Creating superuser (optional - press Ctrl+C to skip)"
python manage.py createsuperuser --noinput --username admin --email admin@studyos.local 2>/dev/null || true

echo ""
echo "✅ StudyOS is ready!"
echo ""
echo "▶  Start server with:  python manage.py runserver"
echo "🌐 Open in browser:    http://127.0.0.1:8000"
echo "🔧 Admin panel:        http://127.0.0.1:8000/admin/"
echo ""
echo "Register a new account at /register/ to get started."
