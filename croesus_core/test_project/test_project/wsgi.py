import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'croesus_core.test_project.settings')

application = get_wsgi_application()
