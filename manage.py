"""
Note: This manage.py handles HTTP requests and serve the frontend (HTML templates, static files, etc)
"""

"""Django's command-line utility for administrative tasks."""
import os
import sys

# Root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Module Path
PATH = os.path.join(ROOT_DIR, "backend_app")

# Added some packages
sys.path.append(PATH)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
