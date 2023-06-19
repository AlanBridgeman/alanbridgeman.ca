#from alanbridgeman_ca.settings.dev import SECRET_KEY
from .base import *
import os

ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []

# This is needed because WEBSITE_HOSTNAME (populated by Azure) is the hostname of the Azure App Service NOT the custom domain if configured
# Append is used so that you can still use the Azure App Service domain name
if 'CUSTOM_HOSTNAME' in os.environ:
    ALLOWED_HOSTS.append(os.environ['CUSTOM_HOSTNAME'])
    CSRF_TRUSTED_ORIGINS.append('https://' + os.environ['CUSTOM_HOSTNAME'])

DEBUG = False

# WhiteNoise configuration
MIDDLEWARE = [                                                                   
    'django.middleware.security.SecurityMiddleware',
# Add whitenoise middleware after the security middleware                             
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',                      
    'django.middleware.common.CommonMiddleware',                                 
    'django.middleware.csrf.CsrfViewMiddleware',                                 
    'django.contrib.auth.middleware.AuthenticationMiddleware',                   
    'django.contrib.messages.middleware.MessageMiddleware',                      
    'django.middleware.clickjacking.XFrameOptionsMiddleware',                    
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# DBHOST is only the server name, not the full URL
hostname = os.environ['DBHOST']

# Configure Postgres database; the full username for PostgreSQL flexible server is
# username (not @sever-name).
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DBNAME'],
        'HOST': hostname + ".postgres.database.azure.com",
        'USER': os.environ['DBUSER'],
        'PASSWORD': os.environ['DBPASS'] 
    }
}

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

#try:
#    from .local import *
#except ImportError:
#    pass
