from celery import Celery
from app.config import config


def initialize_celery() -> Celery:
    """
    Initialize celery configuration.
    """

    app = Celery(
        'celery_app',
        broker=config.CELERY_BROKER_URL,
        backend=config.CELERY_RESULT_BACKEND
    )
    print("Initializing celery app.")
    print(f"Broker: {config.CELERY_BROKER_URL}")
    print(f"Backend: {config.CELERY_RESULT_BACKEND}")

    app.conf.update(
        accept_content=config.CELERY_ACCEPT_CONTENT,
        task_serializer=config.CELERY_TASK_SERIALIZER,
        result_serializer=config.CELERY_RESULT_SERIALIZER,
        timezone=config.CELERY_TIMEZONE,
        enable_utc=config.CELERY_ENABLE_UTC,
    )

    return app
