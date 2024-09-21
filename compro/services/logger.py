from django.conf import settings
import logging, os
import logging.config

# Path ke file log
LOG_DIR = f'/var/log/{settings.APP_NAME}'
LOG_FILE = os.path.join(LOG_DIR, 'x.log')

# Konfigurasi logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        f'{settings.APP_NAME}': {  # Ganti f'{settings.APP_NAME}' dengan nama aplikasi kamu
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Setup logging
logging.config.dictConfig(LOGGING)
logger = logging.getLogger(f'{settings.APP_NAME}')