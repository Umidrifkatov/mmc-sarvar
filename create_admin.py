# create_admin.py


import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = "admin"
email = "admin@example.com"
password = "adminpass"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("Суперпользователь создан.")
else:
    print("Суперпользователь уже существует.")