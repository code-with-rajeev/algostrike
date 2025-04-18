"""
Note: This manage_backend.py handles core backend logic:
API's, database operations, and background tasks (Celery, Redis, etc.).

No templates or static frontend assets are served here.
"""

"""Django's command-line utility for administrative tasks."""
import os
import sys

# Root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Module Path
BACKEND_PATH = os.path.join(ROOT_DIR,'backend_app')
KOTAKNEO_PATH = os.path.join(ROOT_DIR,'kotak_neo')
# append module path
sys.path.append(BACKEND_PATH)
sys.path.append(KOTAKNEO_PATH)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_app.settings')
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