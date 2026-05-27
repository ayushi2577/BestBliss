#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Create superuser if not exists
echo "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@bestbliss.com').exists():
    User.objects.create_superuser(email='admin@bestbliss.com', password='Admin@1234', name='Admin')
    print('Superuser created')
else:
    print('Superuser already exists')
" | python manage.py shell

# Seed demo data (safe to re-run — skips existing records)
python manage.py seed_data
