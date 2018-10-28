#!/usr/bin/env python
import os
import sys
from library.errorLog import get_logger

if __name__ == '__main__':
    logger = get_logger(__name__)
    logger.info('starting app')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homesite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        logger.exception("Couldn't import Django.")
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
