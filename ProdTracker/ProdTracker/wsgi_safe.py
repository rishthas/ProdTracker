"""
WSGI config for ProdTracker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""
activate_this = 'C:/AIMS_PRD_TRACKER/ProdTrackerEnv/Scripts/activate_this.py'
exec(open(activate_this).read(),dict(__file__=activate_this))

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('C:/AIMS_PRD_TRACKER/ProdTrackerEnv/Lib/site-packages')
site.addsitedir('C:/Users/saniy/AppData/Local/Programs/Python/Python37')


# Add the app's directory to the PYTHONPATH
sys.path.append('C:/AIMS_PRD_TRACKER/ProdTracker/ProdTracker')
sys.path.append('C:/AIMS_PRD_TRACKER/ProdTracker/ProdTracker/ProdTracker')

os.environ['DJANGO_SETTINGS_MODULE'] = 'ProdTracker.settings'
os.environ['PYTHONHOME'] = 'C:/AIMS_PRD_TRACKER/ProdTrackerEnv'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ProdTracker.settings")

from django.core.wsgi import get_wsgi_application



application = get_wsgi_application()
