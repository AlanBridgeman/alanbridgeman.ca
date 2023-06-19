from .base import *

import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(os.path.dirname(BASE_DIR), '.env'))

print(env('SECRET_KEY'))

# False if not in os.environ because of casting above
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

# Raises Django's ImproperlyConfigured
# exception if SECRET_KEY not in os.environ
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# Parse database connection url strings
# like psql://user:pass@127.0.0.1:8458/db
DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DBNAME'),
        'HOST': env('DBHOST'),
        'USER': env('DBUSER'),
        'PASSWORD': env('DBPASS')
    }
}

#CACHES = {
#    # Read os.environ['CACHE_URL'] and raises
#    # ImproperlyConfigured exception if not found.
#    #
#    # The cache() method is an alias for cache_url().
#    'default': env.cache(),
#
#    # read os.environ['REDIS_URL']
#    'redis': env.cache_url('REDIS_URL')
#}


# Re-route email notifications to the console/terminal
#EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Email notifications using SendGrid
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = env("SENDGRID_API_KEY")
# Toggle sandbox mode (when running in DEBUG mode)
SENDGRID_SANDBOX_MODE_IN_DEBUG=False
# echo to stdout or any other file-like object that is passed to the backend via the stream kwarg.
SENDGRID_ECHO_TO_STDOUT=True
WAGTAILADMIN_NOTIFICATION_FROM_EMAIL = 'ccd-webmaster@alanbridgeman.ca'

MAILCHIMP_API_KEY = env("MAILCHIMP_API_KEY")
MAILCHIMP_REGION = env("MAILCHIMP_REGION")
MAILCHIMP_MARKETING_AUDIENCE_ID = env("MAILCHIMP_MARKETING_AUDIENCE_ID")

try:
    from .local import *
except ImportError:
    pass

