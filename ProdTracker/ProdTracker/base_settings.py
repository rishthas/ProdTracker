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


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fc__^u$ubiv7s6b)rb84lp8cwix2sl=700t3$cm*^%965l(dss'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'product',
    'rest_framework',
    'rest_framework_datatables',
    'accounts',
    'menu_generator',

    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ProdTracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ProdTracker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aimserp',
        'USER': 'aims',
        'PASSWORD': 'aims#2021',
        'HOST': 'localhost',
        'PORT': 3307
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'


MEDIA_URL = '/media/'
MEDIA_ROOT =  BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    "DATE_INPUT_FORMATS": ["%d-%m-%Y"],
    'DATETIME_FORMAT': "%d-%b-%Y %H:%M:%S",
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_datatables.renderers.DatatablesRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_datatables.filters.DatatablesFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework_datatables.pagination.DatatablesPageNumberPagination',
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,
}

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

ADMIN_MENU = [
    
    {
        "name": _("Admin"),
        "icon_class": 'menu-icon fa fa-fw fa fas fa-fax',
        "url": "#",
        "ref":"admin",
        'access_level': 'all',
        "in_menu" : True,
        'description': _("Adminstration"),
        "has_sub" : True,
        "validators": [("accounts.menu_validators.has_menu_access","admin")],
        "submenu": [
            {
                "name": _("Role Management"),
                "icon_class": 'menu-icon fa fa-fw fa fa-cubes',
                "url": "roles",
                "ref":"role_management",
                'access_level': 'all',
                "in_menu" : True,
                'description': _("Role Management"),
                "has_sub" : False,
                "access_type": [
                    {
                        "type": "add",
                        "desc": _("Add")
                    },
                    {
                        "type": "modify",
                        "desc": _("Modify")
                    },
                    {
                        "type": "delete",
                        "desc": _("Delete")
                    },
                ],
                "validators": [("accounts.menu_validators.has_menu_access","role_management")],
                
            },
            {
                "name":_("User Management"),
                "url": "users",
                "ref":"user_management",
                'access_level': 'all',
                "in_menu" : True,
                'description': _("User Management"),
                "has_sub" : False,
                "access_type": [
                    {
                        "type": "add",
                        "desc": _("Add")
                    },
                    {
                        "type": "modify",
                        "desc": _("Modify")
                    },
                    {
                        "type": "delete",
                        "desc": _("Delete")
                    },
                ],
                "validators": [("accounts.menu_validators.has_menu_access","user_management")],


            },
        ],
    },
    {
        "name": "Product",
        "icon_class": 'menu-icon fa fa-fw fas fa-history',
        "url": "#",
        "ref":"product",
        'access_level': 'all',
        "in_menu" : True,
        'description': _("Product Management"),
        "has_sub" : True,

        "validators": [("accounts.menu_validators.has_menu_access","product")],
        "submenu":[
            
            {
                "name": 'Purchase',
                "url": "purchase",
                "icon_class" : "menu-bullet menu-bullet-dot",
                "ref":"prd_purchase",
                'access_level': 'all',
                "in_menu" : True,
                'description': _("Purchase Product"),
                "has_sub" : False,
               "access_type": [
                    {"type": "access",
                    "desc": _("Has Access")}
                ],

                "validators": [("accounts.menu_validators.has_menu_access","prd_purchase")],
            },
            {
                "name": 'Transfer',
                "url": "transfer",
                "icon_class" : "menu-bullet menu-bullet-dot",
                "ref":"prd_transfer",
                'access_level': 'all',
                "in_menu" : True,
                'description': _("Purchase Transfer"),
                "has_sub" : False,
               "access_type": [
                    {"type": "access",
                    "desc": _("Has Access")}
                ],

                "validators": [("accounts.menu_validators.has_menu_access","prd_transfer")],
            },
            {
                "name": 'Link Invoice',
                "url": "invoice",
                "icon_class" : "menu-bullet menu-bullet-dot",
                "ref":"link_invoice",
                'access_level': 'all',
                "in_menu" : True,
                'description': _("Link Invoice"),
                "has_sub" : False,
               "access_type": [
                    {"type": "access",
                    "desc": _("Has Access")}
                ],

                "validators": [("accounts.menu_validators.has_menu_access","link_invoice")],
            },
            {
                "name": 'Take Stock',
                "url": "stock",
                "icon_class" : "menu-bullet menu-bullet-dot",
                "ref":"take_stock",
                'access_level': 'all',
                "in_menu" : True,
                'description': _("Take Stock"),
                "has_sub" : False,
               "access_type": [
                    {"type": "access",
                    "desc": _("Has Access")}
                ],

                "validators": [("accounts.menu_validators.has_menu_access","take_stock")],
            },
            {
                "name": 'Credit Note',
                "url": "credit_note",
                "icon_class" : "menu-bullet menu-bullet-dot",
                "ref":"credit_note",
                'access_level': 'all',
                "in_menu" : True,
                'description': _("Credit Note"),
                "has_sub" : False,
               "access_type": [
                    {"type": "access",
                    "desc": _("Has Access")}
                ],

                "validators": [("accounts.menu_validators.has_menu_access","credit_note")],
            },
        ]
    },
    {
        "name": "Prameters",
        "icon_class": 'menu-icon fa fa-fw fas fa-history',
        "url": "#",
        "ref":"parameter",
        'access_level': 'all',
        "in_menu" : True,
        'description': _("Prameters"),
        "has_sub" : True,
        "validators": [("accounts.menu_validators.has_menu_access","parameter")],
        "submenu":[
            {
                "name": 'Branches',
                "url": "branch",
                "icon_class" : "menu-bullet menu-bullet-dot",
                "ref":"branches",
                'access_level': 'all',
                "in_menu" : True,
                'description': _("Branches"),
                "has_sub" : False,
                "access_type": [
                    {
                        "type": "add",
                        "desc": _("Add")
                    },
                    {
                        "type": "modify",
                        "desc": _("Modify")
                    },
                    {
                        "type": "delete",
                        "desc": _("Delete")
                    },
                ],

                "validators": [("accounts.menu_validators.has_menu_access","branches")],
            },
            {
                "name": 'Vendor',
                "url": "vendor",
                "icon_class" : "menu-bullet menu-bullet-dot",
                "ref":"vendor",
                'access_level': 'all',
                "in_menu" : True,
                'description': _("Vendor"),
                "has_sub" : False,
                "access_type": [
                    {
                        "type": "add",
                        "desc": _("Add")
                    },
                    {
                        "type": "modify",
                        "desc": _("Modify")
                    },
                    {
                        "type": "delete",
                        "desc": _("Delete")
                    },
                ],

                "validators": [("accounts.menu_validators.has_menu_access","vendor")],
            },
            {
                "name": 'Models',
                "url": "model",
                "icon_class" : "menu-bullet menu-bullet-dot",
                "ref":"model",
                'access_level': 'all',
                "in_menu" : True,
                'description': _("Models"),
                "has_sub" : False,
                "access_type": [
                    {
                        "type": "add",
                        "desc": _("Add")
                    },
                    {
                        "type": "modify",
                        "desc": _("Modify")
                    },
                    {
                        "type": "delete",
                        "desc": _("Delete")
                    },
                ],

                "validators": [("accounts.menu_validators.has_menu_access","model")],
            },
            
            

        ]
    },
    {
        "name": "Reports",
        "icon_class": 'menu-icon fa fa-fw fas fa-history',
        "url": "#",
        "ref":"reports",
        'access_level': 'all',
        "in_menu" : True,
        'description': _("Reports"),
        "has_sub" : True,

        "validators": [("accounts.menu_validators.has_menu_access","reports")],
        "submenu":[
            {
                "name": 'Product Report',
                "url": "report",
                "icon_class" : "menu-bullet menu-bullet-dot",
                "ref":"prd_report",
                'access_level': 'all',
                "in_menu" : True,
                'description': _("Purchase Product"),
                "has_sub" : False,
               "access_type": [
                    {"type": "access",
                    "desc": _("Has Access")}
                ],

                "validators": [("accounts.menu_validators.has_menu_access","prd_report")],
            },
            {
                "name": 'Stock Report',
                "url": "stock-report",
                "icon_class" : "menu-bullet menu-bullet-dot",
                "ref":"stock_rpt",
                'access_level': 'all',
                "in_menu" : True,
                'description': _("Stock Report"),
                "has_sub" : False,
               "access_type": [
                    {"type": "access",
                    "desc": _("Has Access")}
                ],

                "validators": [("accounts.menu_validators.has_menu_access","stock_rpt")],
            },
            {
                "name": 'Summary Report',
                "url": "summ-report",
                "icon_class" : "menu-bullet menu-bullet-dot",
                "ref":"summ_report",
                'access_level': 'all',
                "in_menu" : True,
                'description': _("Summary Report"),
                "has_sub" : False,
               "access_type": [
                    {"type": "access",
                    "desc": _("Has Access")}
                ],

                "validators": [("accounts.menu_validators.has_menu_access","summ_report")],
            },
        ]
    },

    

  

]