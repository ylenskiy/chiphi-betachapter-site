import os, sys
from os.path import dirname,realpath

sys.path.append("/home/termchair/www")
sys.path.append("/home/termchair/www/chiphi-betachapter-site")

os.environ['DJANGO_SETTINGS_MODULE'] = 'chiphi-betachapter-site.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
