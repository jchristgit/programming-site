#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # Check whether we're running `collectstatic` or `check --deploy`
    if any(cmd in sys.argv for cmd in ('collectstatic', '--deploy')):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings.prod")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings.debug")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
