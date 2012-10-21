import os
from global_settings import PROJECT_PATH

# Uncomment to put the application in non-debug mode. This is useful
# for testing error handling and messages.
# DEBUG = False
# TEMPLATE_DEBUG = DEBUG

# Override this to match the application endpoint
# FORCE_SCRIPT_NAME = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_PATH, '{{ project_name }}.db')
    }
}

# Non-restricted email port for development, run in a terminal:
# python -m smtpd -n -c DebuggingServer localhost:1025
EMAIL_PORT = 1025
EMAIL_SUBJECT_PREFIX = '[{{ project_name }} Local] '

# This is used as a "seed" for various hashing algorithms. This must be set to
# a very long random string (40+ characters)
SECRET_KEY = '{{ secret_key }}'
