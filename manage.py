#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IllustShop.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

# 用於部署於Render平台，於build階段建立superuser
def Add_Superuser():
    try:
        from django.contrib.auth.models import User
        from dotenv import load_dotenv
        username = os.getenv("SUPERUSER_USERNAME")
        email = os.getenv("SUPERUSER_USEREMAIL")
        password = os.getenv("SUPERUSER_USERPASSWORD")
        # 檢查是否已存在該使用者
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            print("Superuser created successfully.")
        else:
            print("Superuser already exists.")

    except:
        raise

if __name__ == '__main__':
    main()
