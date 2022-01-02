"""
Django settings for ProdTracker project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from django.utils.translation import ugettext_lazy as _
from .base_settings import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': BASE_DIR / 'db.sqlite3',
   }
}

# STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = [
   BASE_DIR / "static",
   
]

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'aimserp',
#         'USER': 'aims',
#         'PASSWORD': 'aims#2021',
#         'HOST': 'localhost',
#         'PORT': 3307
#     }
# }

