"""
WSGI config for tasty_django project.
Replaces Node.js's app.listen(PORT, ...) — the WSGI server (gunicorn, etc.) handles this.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tasty_django.settings')
application = get_wsgi_application()
