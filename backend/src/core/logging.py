import logging
import logging.config

from .constants import LOGS_PATH


def setup_logging() -> None:
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        
        'formatters': {
            'base_format': {
                'format': '{levelname} {asctime} {message}',
                'style': '{',
            }
        },
        
        'handlers': {
            'file_app': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': str(LOGS_PATH / 'app.log'),
                'formatter': 'base_format',
            },
            'file_error': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': str(LOGS_PATH / 'errors.log'),
                'formatter': 'base_format',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'base_format',
            }
        },
        
        'loggers': {
            'app': {
                'handlers': ['file_error', 'console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'app.api': {
                'handlers': ['file_app'],
                'level': 'INFO',
                'propagate': True
            },
            'app.core': {
                'handlers': ['file_app'],
                'level': 'INFO',
                'propagate': True
            },
            'app.models': {
                'handlers': ['file_app'],
                'level': 'INFO',
                'propagate': True
            },
            'app.repositories': {
                'handlers': ['file_app'],
                'level': 'INFO',
                'propagate': True
            },
            'app.schemas': {
                'handlers': ['file_app'],
                'level': 'INFO',
                'propagate': True
            },
            'app.services': {
                'handlers': ['file_app'],
                'level': 'INFO',
                'propagate': True
            },
            'app.utils': {
                'handlers': ['file_app'],
                'level': 'INFO',
                'propagate': True
            },
        }
    }
    
    logging.config.dictConfig(config)
    

def get_logger(name: str | None) -> logging.Logger:
    if name is None:
        return logging.getLogger('app')
    
    if not name.startswith('app.'):
        name = 'app.' + name
        
    return logging.getLogger(name)