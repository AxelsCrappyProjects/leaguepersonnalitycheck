"""
WSGI config for championpoolvalidator project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""


import os
os.environ['HTTPS'] = "on"
this_file = "/home/blrhwuo/leaguepersonnalitycheck/.venv/bin/activate_this.py"
exec(open(this_file).read(), {'__file__': this_file})

from whitenoise import WhiteNoise

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'championpoolvalidator.settings')

application = get_wsgi_application()
application = WhiteNoise(application, root="/home/blrhwuo/leaguepersonnalitycheck/staticfiles/")

