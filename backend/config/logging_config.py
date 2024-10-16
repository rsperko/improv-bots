import logging

# Development configuration
DEV_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        'utils.openai_client': {  # root logger
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

# Production configuration
PROD_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/myapp.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

def setup_logging(env='dev'):
    import logging.config
    if env.lower() == 'prod':
        logging.config.dictConfig(PROD_CONFIG)
    else:
        logging.config.dictConfig(DEV_CONFIG)
