import os

class Config(object):
    """Base configuration class."""
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_very_secret_key')

    # Celery settings
    CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Default broker (e.g., Redis)
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # Default backend
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'UTC'
    CELERY_ENABLE_UTC = True

    # Allowed tasks and their queues
    # Format: {task_name: queue_name} 
    ALLOWED_TASKS = {
        'runModule01': 'module01',
        'runModule02': 'module02',
        # Add more task needed
    }
    # Other settings (e.g., database or logging)

    # Database settings

    # Logging settings
    LOGGER_DEBUG = False
    LOGGER_IDENTIFIER = "my_celery_app"
    LOGGER_MAX_BYTE = 10485760
    LOGGER_BACKUP_COUNT = 10

class DevelopmentConfig(Config):
    """Development environment configuration."""
    # Celery settings
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1' 

    # Logging settings
    LOGGER_DEBUG = True
    LOGGER_IDENTIFIER = "dev_log"
    LOGGER_MAX_BYTE = 10485760
    LOGGER_BACKUP_COUNT = 5

class ProductionConfig(Config):
    """Production environment configuration."""
    # Celery settings
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'

    # Logging settings
    LOGGER_DEBUG = False
    LOGGER_IDENTIFIER = "production_log"
    LOGGER_MAX_BYTE = 10485760
    LOGGER_BACKUP_COUNT = 10


# Load config based on environment (e.g., APP_ENV=development)
env = os.environ.get('APP_ENV', 'development').lower()
config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

config = config_dict.get(env, DevelopmentConfig)()