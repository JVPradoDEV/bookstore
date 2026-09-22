import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')
django.setup()

from django.contrib.auth.models import User

username = os.environ.get('SUPER_USER_NAME', 'admin')
email = os.environ.get('SUPER_USER_EMAIL', 'admin@example.com')
password = os.environ.get('SUPER_USER_PASSWORD', 'admin123')

if not User.objects.filter(username=username).exists():
    print(f"Criando superusuário: {username}")
    User.objects.create_superuser(username, email, password)
    print("Superusuário criado com sucesso!")
else:
    print("Superusuário já existe.")